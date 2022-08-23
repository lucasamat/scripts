//Set - Global Variables - Start
localStorage.setItem("selected_items", JSON.stringify([]))
// localStorage.setItem("add_new_functionality","TRUE")
//Set - Global Variables - End

// Add parts - Start A055S000P01-9646
function partsModelListKeyHyperLink(value, row) {
	var materialRecordId = row.MATERIAL_RECORD_ID
	var offerings_value = row.pop_val
	return '<a href="#" id=' + offerings_value + ' onclick="addPart(this,\'' + materialRecordId + '\')">' + value + '</a>'
}


function addPart(ele, materialRecordId) {
	localStorage.setItem("add_new_functionality", "TRUE");
	var actionType = "ADD_PART"
	var relatedListID = "SYOBJR-00029"
	if (localStorage.getItem("currentSubTab") == "Spare Parts") {
		actionType = "ADD_SPARE_PART"
		relatedListID = "SYOBJR-00005"
	}
	if (localStorage.getItem("currentSubTab") == "New Parts") {
		new_part = 1
	}
	else {
		new_part = 0
	}
	if (localStorage.getItem("currentSubTab") == "Inclusions") {
		inclusion = 1
	}
	else {
		inclusion = 0
	}

	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': actionType,
			'NodeType': 'PARTS MODEL',
			'Values': [materialRecordId],
			'new_part': new_part,
			'inclusion': inclusion
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList(relatedListID, 'div_CTR_related_list');
		});
	} catch (e) {
		console.log(e);
	}
}


function mark_primary_contact(ele) {
	var Values = $(ele).closest('tr').find('td:nth-child(3) > a > abbr').attr('id');
	var get_currentnode = node.nodeId

	cpq.server.executeScript("CQRPLACTCT", {
		'ActionType': 'MARK_PRIMARY', 'Values': Values
	}, function (dataset) {
		[CurrentRecordId, RecName] = ['SYOBJR-98871', 'div_CTR_Revisions'];
		loadRelatedList(CurrentRecordId, RecName);
	});

	localStorage.setItem("add_new_functionality", "TRUE");

}

function addPartsList(ele) {
	localStorage.setItem("add_new_functionality", "TRUE");
	reload_parts_val();
	var selectedOfferings = [];
	//selectedOfferings = JSON.parse(localStorage.getItem("selected_items"));
	var selectAll = false;
	var actionType = "ADD_PART"
	var relatedListID = "SYOBJR-00029"
	if (localStorage.getItem("currentSubTab") == "Spare Parts") {
		actionType = "ADD_SPARE_PART"
		relatedListID = "SYOBJR-00005"
	}
	$('#parts-addnew-model').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedOfferings.push(sel_val);
		}
	});
	var A_Keys = [];
	var A_Values = [];
	$('#parts-addnew-model  .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#parts-addnew-model .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
				search_value = A_Values.length
				//console.log(search_value)
				if (search_value > 0 && selectAll == true) {
					selectAll = false;
				}
			};
		}
	});
	if (localStorage.getItem("currentSubTab") == "New Parts") {
		new_part = 1
	}
	else {
		new_part = 0
	}
	if (localStorage.getItem("currentSubTab") == "Inclusions") {
		inclusion = 1
	}
	else {
		inclusion = 0
	}
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': actionType,
			'NodeType': 'PARTS MODEL',
			'Values': selectedOfferings,
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values,
			'new_part': new_part,
			'inclusion': inclusion
		}, function () {
			//$("#MM_ALL_REFRESH").click();
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList(relatedListID, 'div_CTR_related_list');
		});
	} catch (e) {
		console.log(e);
	}
}
//Add parts - End A055S000P01-9646

// Add Offerings - Start
function offeringsModelListKeyHyperLink(value, row) {
	var materialRecordId = row.MATERIAL_RECORD_ID
	var offerings_value = row.pop_val
	return '<a href="#" id=' + offerings_value + ' onclick="addOffering(this,\'' + materialRecordId + '\')">' + value + '</a>'
}
function replaceAccountKeyHyperLink(value, row) {
	var accountRecordId = row.ACCOUNT_PARTNER_FUNCTION_ID
	var account_value = row.pop_val
	return '<a href="#" id=' + account_value + ' onclick="replaceContact(this,\'' + accountRecordId + '\')">' + value + '</a>'
}
function validateInput(id) {
	var value = Number($('#' + id).val());
	if (value < 0 || !Number.isInteger(value)) {
		$('#alertMessage').text('Should be a positive Integer');
		$('#' + id + '_save').attr('disabled', 'true');
	}
	else {
		$('#alertMessage').text('');
		$('#' + id + '_save').removeAttr('disabled');
	}
}
function replaceContact(ele, accountRecordId) {
	localStorage.setItem("add_new_functionality", "TRUE");
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'REPLACE_ACCOUNT',
			'NodeType': 'ACCOUNT MODEL',
			'ReplaceContact': localStorage.getItem('replacingAccount'),
			'Values': [accountRecordId]
		}, function () {
			localStorage.removeItem('replacingAccount');
			$('#cont_viewModalSection').css('display', 'none');
			$('#COMMON_TABS ul li.active').click();
		});
	} catch (e) {
		console.log(e);
	}
}
function addOffering(ele, materialRecordId) {
	localStorage.setItem("add_new_functionality", "TRUE")
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_OFFERING',
			'NodeType': 'OFFERINGS MODEL',
			'Values': [materialRecordId]
		}, function () {
			//$("#MM_ALL_REFRESH").click();
			$('#cont_viewModalSection').css('display', 'none');
			CommonLeftView();
			$('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			$('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
		});
	} catch (e) {
		console.log(e);
	}
}

function addOfferings(ele) {
	localStorage.setItem("add_new_functionality", "TRUE")
	reload_offering_val()
	var selectedOfferings = [];
	//selectedOfferings = JSON.parse(localStorage.getItem("selected_items"));
	var selectAll = false;
	$('#offerings-addnew-model').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedOfferings.push(sel_val);
		}
	});
	var A_Keys = [];
	var A_Values = [];
	$('#offerings-addnew-model  .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#offerings-addnew-model .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_OFFERING',
			'NodeType': 'OFFERINGS MODEL',
			'Values': selectedOfferings,
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function () {
			//$("#MM_ALL_REFRESH").click();
			$('#cont_viewModalSection').css('display', 'none');
			CommonLeftView();
			$('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			$('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
		});
	} catch (e) {
		console.log(e);
	}
}
function modelOfferingsPaginationFunc(showResultCount, recordEnd, tableId) {


	first_record_id = localStorage.getItem("keyData");
	first_record_feild = $('#attributesContainer .Detail input').first().attr('id');
	localStorage.setItem("first_record_id", first_record_id);
	localStorage.setItem("first_record_feild", first_record_feild);
	var A_Keys = [];
	var A_Values = [];
	var type="";
	var ele_id = "offerings-addnew-model"
	if (tableId == "ADDNEW__SYOBJR_00029_SYOBJ_1177034" || tableId == "ADDNEW__SYOBJR_00005_SYOBJ_00272") {
		ele_id = "parts-addnew-model"
	}
	else if (tableId == "ADDNEW__SYOBJR_00038_SYOBJ_00919") {
		ele_id = "fablocation_addnew"
	}
	else if(tableId == "ADDNEW__SYOBJR_98798_SYOBJ_00910"){
		ele_id = "replace-account"
		first_record_id = localStorage.getItem('replacingAccount');
		type="REPLACE"
	}
	$('#' + ele_id + ' .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#' + ele_id + ' .' + x).val();
			if (xyz == undefined) {
				xyz = ""
			}
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	//localStorage.setItem('cont_table_id', tableId)
	try {
		cpq.server.executeScript("SYUADNWPOP", {
			'TABLEID': tableId,
			'OPER': 'NO',
			'RECORDID': first_record_id,
			'RECORDFEILD': first_record_feild,
			'NEWVALUE': '',
			'LOOKUPOBJ': '',
			'LOOKUPAPI': '',
			'Offset_Skip_Count': recordEnd,
			'Fetch_Count': showResultCount,
			'A_Keys': A_Keys,
			'A_Values': A_Values,
			'TOOL_TYPE':type,
			'SUBTAB':$('#COMMON_TABS ul li.active').text().trim()
		}, function (data) {
			date_field = data[3];
			var assoc = data[1];
			var api_name = data[2];
			data5 = data[5];
			data6 = data[6];
			tableId = localStorage.getItem('cont_table_id')
			try {
				$('#' + ele_id).bootstrapTable('load', date_field);
			} catch (err) {
				setTimeout(function () {
					$('#' + ele_id).bootstrapTable('load', date_field);
				}, 5000);
			} finally {
				if(ele_id == "replace-account"){
					$('#replace-account > tbody > tr').each(function(){
						var element = $(this).find('td:nth-child(5)');
						var text = $(element).text();
						$(element).attr('title',text);
						
					});
				}
			 }
			$('#add-parts').css('display', 'block');
			// $('#add-'+ele_id+'-model-footer').html(data6)
			$('#pagination_' + ele_id).html(data6)
			eval(data5);
		});
	} catch (e) {
		console.log(e);
	}
}

function ShowResultCountFunc(ele, footerId, action, table) {
	var recordsStartAndEnd = $("div#" + footerId + " #RecordsStartAndEnd").text();
	var recordEnd = recordsStartAndEnd.split(' ')[0];
	if (action == 'addOfferings' || action == 'addParts') {
		modelOfferingsPaginationFunc(showResultCount = parseInt(ele.value), recordEnd = parseInt(recordEnd), tableId = table)
	}
	else if (action == 'addEquipment') {
		modelEquipmentPaginationFunc(showResultCount = parseInt(ele.value), recordEnd = parseInt(recordEnd), tableId = table);
	}
	else if (action == 'addFab') {
		reload_fab_val();
		modelFabPaginationFunc(showResultCount = parseInt(ele.value), recordEnd = parseInt(recordEnd), tableId = table);
	}
	else if (action == 'addCoveredObj') {
		modelCovObjPaginationFunc(showResultCount = parseInt(ele.value), recordEnd = parseInt(recordEnd), tableId = table);
	}
}

function GetNextResultFunc(footerId, action, table) {
	var showResultCount = $("div#" + footerId + " #ShowResultCount option:selected").text();
	var recordsStartAndEnd = $("div#" + footerId + " #RecordsStartAndEnd").text();
	var recordEnd = recordsStartAndEnd.split(' ')[2];
	if (action == 'addOfferings' || action == 'addParts') {
		modelOfferingsPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd), tableId = table);
	}
	else if (action == 'addEquipment') {
		modelEquipmentPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd) + 1, tableId = table);
	}
	else if (action == 'addFab') {
		reload_fab_val();
		modelFabPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd), tableId = table);
	} else if (action == 'addCoveredObj') {
		modelCovObjPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd) + 1, tableId = table);
	}
}

function GetPreviuosResultFunc(footerId, action, table) {
	var showResultCount = $("div#" + footerId + " #ShowResultCount option:selected").text();
	var recordsStartAndEnd = $("div#" + footerId + " #RecordsStartAndEnd").text();
	var recordEnd = parseInt(recordsStartAndEnd.split(' ')[0]) - parseInt(showResultCount);
	if (action == 'addOfferings' || action == 'addParts') {
		modelOfferingsPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd) > 0 ? parseInt(recordEnd) : 1, tableId = table);
	}
	else if (action == 'addEquipment') {
		modelEquipmentPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd) > 0 ? parseInt(recordEnd) : 1, tableId = table);
	}
	else if (action == 'addFab') {
		reload_fab_val();
		modelFabPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd) > 0 ? parseInt(recordEnd) : 1, tableId = table);
	} else if (action == 'addCoveredObj') {
		modelCovObjPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd) > 0 ? parseInt(recordEnd) : 1, tableId = table);
	}
}

function GetFirstResultFunc(footerId, action, table) {
	var showResultCount = $("div#" + footerId + " #ShowResultCount option:selected").text();
	if (action == 'addOfferings' || action == 'addParts') {
		modelOfferingsPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = 1, tableId = table);
	}
	else if (action == 'addEquipment') {
		modelEquipmentPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = 1, tableId = table);
	}
	else if (action == 'addFab') {
		reload_fab_val();
		modelFabPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = 1, tableId = table);
	} else if (action == 'addCoveredObj') {
		modelCovObjPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = 1, tableId = table);
	}
}

function GetLastResultFunc(footerId, action, table) {
	var showResultCount = $("div#" + footerId + " #ShowResultCount option:selected").text();
	var totalRecordsCount = $("div#" + footerId + " #TotalRecordsCount").text();
	var recordEnd = 0;
	var remainingCount = parseInt(totalRecordsCount) % parseInt(showResultCount)
	if (remainingCount == 0) {
		recordEnd = parseInt(totalRecordsCount) - parseInt(showResultCount);
	} else {
		recordEnd = parseInt(totalRecordsCount) - parseInt(remainingCount);
	}
	if (action == 'addOfferings' || action == 'addParts') {
		modelOfferingsPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd), tableId = table);
	}
	else if (action == 'addEquipment') {
		modelEquipmentPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd) + 1, tableId = table);
	}
	else if (action == 'addFab') {
		reload_fab_val();
		modelFabPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd) + 1, tableId = table);
	} else if (action == 'addCoveredObj') {
		modelCovObjPaginationFunc(showResultCount = parseInt(showResultCount), recordEnd = parseInt(recordEnd) + 1, tableId = table);
	}
}
// Add Offerings - End

// Add Equipment - Start
function modelEquipmentPaginationFunc(showResultCount, recordEnd, tableId) {

	first_record_id = localStorage.getItem("keyData");
	first_record_feild = $('#attributesContainer .Detail input').first().attr('id');
	localStorage.setItem("first_record_id", first_record_id);
	localStorage.setItem("first_record_feild", first_record_feild);
	var replace_action = ""
	if (tableId == "ADDNEW__SYOBJR_98797_SYOBJ_00937") {
		ele_id = "equipments_addnew"
		footer_id = "equipments_footer"
	}
	else if (tableId == "ADDNEW__SYOBJR_98871_SYOBJ_002649") {
		ele_id = "contact_replace_addnew_model"
		footer_id = "contact_replace_addnew_model_footer"
	}
	else if (tableId == "ADDNEW__SYOBJR_00643_SYOBJ_0026410") {
		ele_id = "contact_manager_addnew_model"
		footer_id = "contact_replace_addnew_model_footer"
		replace_action = localStorage.getItem("rep_btn")
	}
	else if (tableId == "ADDNEW__SYOBJR_98880_SYOBJ_1177045") {
		ele_id = "add_credits_add_new"
		footer_id = "add_credits_addnew_footer"
	}
	else if (tableId == "ADDNEW__SYOBJR_98859_SYOBJ_00975") {
		ele_id = "Include_add_on_addnew"
		footer_id = "Include_add_on_addnew_footer"
	}
	else if (tableId == "ADDNEW__SYOBJR_00033_SYOBJ_1177088") {
		ele_id = "fts_equipments_addnew"
		footer_id = "sending_equipments_footer"
	}
	else {
		ele_id = "involved_parties_equipment_addnew"
		footer_id = "involved_parties_equipment_addnew_footer"
	}
	var A_Keys = [];
	var A_Values = [];
	$('#' + ele_id + ' .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#' + ele_id + ' > thead > tr > th > div.fht-cell > div > .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("SYUADNWPOP", {
			'TABLEID': tableId,
			'OPER': 'NO',
			'RECORDID': first_record_id,
			'RECORDFEILD': first_record_feild,
			'NEWVALUE': '',
			'LOOKUPOBJ': '',
			'LOOKUPAPI': '',
			'Offset_Skip_Count': recordEnd,
			'Fetch_Count': showResultCount,
			'A_Keys': A_Keys,
			'A_Values': A_Values,
			'ACTION': replace_action,
			'TOOL_TYPE': localStorage.getItem('TOOL_TYPE')
		}, function (data) {
			date_field = data[3];
			var assoc = data[1];
			var api_name = data[2];
			data5 = data[5];
			data6 = data[6];
			tableId = localStorage.getItem('cont_table_id')
			var edit_index = $("#add_credits_add_new").find("[data-field='ZAFNOTE']").index() + 1;
			var green_book = $("#add_credits_add_new").find("[data-field='ZAFGBOOK']").index() + 1;
			var zaftype_index = $("#add_credits_add_new").find("[data-field='ZAFTYPE']").index() + 1;
			var zuonr_index = $("#add_credits_add_new").find("[data-field='ZUONR']").index() + 1;
			var gjahr_index = $("#add_credits_add_new").find("[data-field='GJAHR']").index() + 1;
			var gaf_expirydate_index = $("#add_credits_add_new").find("[data-field='ZAFEXPIRY_DATE']").index() + 1;
			var belnr_index = $("#add_credits_add_new").find("[data-field='BELNR']").index() + 1;
			var unapplied_index = $("#add_credits_add_new").find("[data-field='UNBL_INGL_CURR']").index() + 1;
			var creditapplied_index = $("#add_credits_add_new").find("[data-field='CREDIT_APPLIED']").index() + 1;
			try {
				$('#' + ele_id).bootstrapTable('load', date_field);
			} catch (err) {
				setTimeout(function () {
					$('#' + ele_id).bootstrapTable('load', date_field);
				}, 5000);
			} finally {
				$('#add_credits_add_new > tbody > tr').each(function () {
					var html_text = $(this).find('td:nth-child(' + edit_index + ')').text();
					$(this).find('td:nth-child(' + edit_index + ')').html(html_text);
					var html_text = $(this).find('td:nth-child(' + green_book + ')').text();
					$(this).find('td:nth-child(' + green_book + ')').html(html_text);
					var html_text = $(this).find('td:nth-child(' + zaftype_index + ')').text();
					$(this).find('td:nth-child(' + zaftype_index + ')').html(html_text);
					var html_text = $(this).find('td:nth-child(' + zuonr_index + ')').text();
					$(this).find('td:nth-child(' + zuonr_index + ')').html(html_text);
					var html_text = $(this).find('td:nth-child(' + gjahr_index + ')').text();
					$(this).find('td:nth-child(' + gjahr_index + ')').html(html_text);
					var html_text = $(this).find('td:nth-child(' + gaf_expirydate_index + ')').text();
					$(this).find('td:nth-child(' + gaf_expirydate_index + ')').html(html_text);
					var html_text = $(this).find('td:nth-child(' + belnr_index + ')').text();
					$(this).find('td:nth-child(' + belnr_index + ')').html(html_text);
					var html_text = $(this).find('td:nth-child(' + unapplied_index + ')').text();
					$(this).find('td:nth-child(' + unapplied_index + ')').html(html_text);
					var html_text = $(this).find('td:nth-child(' + creditapplied_index + ')').text();
					$(this).find('td:nth-child(' + creditapplied_index + ')').html(html_text);
						})
				}
			$('#' + footer_id).html(data6)
			eval(data5);
			$('.custom').attr('onchange', 'credit_button_enable()');
		});
	} catch (e) {
		console.log(e);
	}
}
// Add Equipments - End

// Add Covered Objects - START
function modelCovObjPaginationFunc(showResultCount, recordEnd, tableId) {

	first_record_id = localStorage.getItem("keyData");
	first_record_feild = $('#attributesContainer .Detail input').first().attr('id');
	localStorage.setItem("first_record_id", first_record_id);
	localStorage.setItem("first_record_feild", first_record_feild);
	var A_Keys = [];
	var A_Values = [];
	$('#Coveredobjectsaddnew  .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#Coveredobjectsaddnew .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("SYUADNWPOP", {
			'TABLEID': tableId,
			'OPER': 'NO',
			'RECORDID': first_record_id,
			'RECORDFEILD': first_record_feild,
			'NEWVALUE': '',
			'LOOKUPOBJ': '',
			'LOOKUPAPI': '',
			'Offset_Skip_Count': recordEnd,
			'Fetch_Count': showResultCount,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function (data) {
			date_field = data[3];
			var assoc = data[1];
			var api_name = data[2];
			data5 = data[5];
			data6 = data[6];
			tableId = localStorage.getItem('cont_table_id')
			try {
				$('#Coveredobjectsaddnew').bootstrapTable('load', date_field);
			} catch (err) {
				setTimeout(function () {
					$('#Coveredobjectsaddnew').bootstrapTable('load', date_field);
				}, 5000);
			} finally { }
			$('#Coveredobjectsaddnew_footer').html(data6)
			eval(data5);
		});
	} catch (e) {
		console.log(e);
	}
}
// Add Covered Objects - END
function modelFabPaginationFunc(showResultCount, recordEnd, tableId) {

	first_record_id = localStorage.getItem("keyData");
	first_record_feild = $('#attributesContainer .Detail input').first().attr('id');
	localStorage.setItem("first_record_id", first_record_id);
	localStorage.setItem("first_record_feild", first_record_feild);
	var selected_fab_list = []
	selected_fab_list = JSON.parse(localStorage.getItem("selected_items"));
	var A_Keys = [];
	var A_Values = [];
	var ele_id = '';
	var footer = '';
	if (tableId == "ADDNEW__SYOBJR_98857_SYOBJ_01033") {
		ele_id = "source_fablocation_addnew"
	}
	else if (tableId == "ADDNEW__SYOBJR_00038_SYOBJ_00919") {
		ele_id = "fablocation_addnew"
	}
	else if (tableId == "ADDNEW__SYOBJR_00032_SYOBJ_1177087") {
		ele_id = "add_fablocation_fts"
	}
	else if (tableId == "ADDNEW__SYOBJR_98882_SYOBJ_1177093") {
		ele_id = "nso_addnew"
	}
	else if (tableId == "ADDNEW__SYOBJR_98789_SYOBJ_00919") {
		ele_id = "fablocation_addnew"
		footer = "fablocation_footer"
	}
	else {
		ele_id = "source_fablocation_addnew"
	}
	if (footer == '') {
		footer = ele_id + '_footer'
	}
	try {
		$('#' + ele_id + '  .filter-control').each(function () {
			values = this.firstElementChild.className;
			if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
				x = values.split(' ')[1];
				y = x.split("-").slice(-1)[0];
				xyz = $('#' + ele_id + ' .' + x).val();
				if ($.inArray(y, A_Keys) === -1) {
					A_Keys.push(y);
					A_Values.push(xyz)
				};
			}
		});
	}
	catch (e) {
		console.log(e);
	}
	try {
		cpq.server.executeScript("SYUADNWPOP", {
			'TABLEID': tableId,
			'OPER': 'NO',
			'RECORDID': first_record_id,
			'RECORDFEILD': first_record_feild,
			'NEWVALUE': '',
			'LOOKUPOBJ': '',
			'LOOKUPAPI': '',
			'Offset_Skip_Count': recordEnd,
			'Fetch_Count': showResultCount,
			'selected_fab_list': selected_fab_list,
			'A_Keys': A_Keys,
			'A_Values': A_Values

		}, function (data) {
			date_field = data[3];
			var assoc = data[1];
			var api_name = data[2];
			data5 = data[5];
			data6 = data[6];
			tableId = localStorage.getItem('cont_table_id')
			try {
				$('#' + ele_id).bootstrapTable('load', date_field);
			} catch (err) {
				setTimeout(function () {
					$('#' + ele_id).bootstrapTable('load', date_field);
				}, 5000);
			} finally { }
			$('#' + ele_id + '_footer').html(data6)
			eval(data5);
		});
	} catch (e) {
		console.log(e);
	}
}
function addEquipments(ele) {
	localStorage.setItem("add_new_functionality", "TRUE")
	var selectedEquipments = [];
	var selectAll = false;
	$('#equipments_addnew').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedEquipments.push(sel_val);
		}
	});
	var A_Keys = [];
	var A_Values = [];
	$('#equipments_addnew .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#equipments_addnew .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
				//search_value = A_Values.length
				//console.log(search_value)
				//if (search_value > 0 && selectAll == true){
				//selectAll = false;
				//}
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_EQUIPMENTS',
			'NodeType': 'FAB MODEL',
			'Values': selectedEquipments,
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values,
			'TOOL_TYPE': localStorage.getItem('TOOL_TYPE')
		}, function () {
			localStorage.removeItem('TOOL_TYPE');
			$('#cont_viewModalSection').css('display', 'none');
			localStorage.setItem("AddEquipment", "yes")
			CommonLeftView();
		});
	} catch (e) {
		console.log(e);
	}
}
function addUnmappedEquipments(ele) {
	localStorage.setItem("add_new_functionality", "TRUE")
	var selectedEquipments = [];
	var selectAll = false;
	$('#unmapped_equipments_addnew').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedEquipments.push(sel_val);
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_UNMAPPED_EQUIPMENTS',
			'NodeType': 'FAB MODEL',
			'Values': selectedEquipments,
			'AllValues': selectAll
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			localStorage.setItem("AddEquipment", "yes")
			CommonLeftView();
		});
	} catch (e) {
		console.log(e);
	}
}

function add_nsos(ele) {
	localStorage.setItem("add_new_functionality", "TRUE")
	var selectedEquipments = [];
	var selectAll = false;
	$('#nso_addnew').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedEquipments.push(sel_val);
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_NSO',
			'NodeType': 'FAB MODEL',
			'Values': selectedEquipments,
			'AllValues': selectAll
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			localStorage.setItem("AddEquipment", "yes")
			loadRelatedList("SYOBJR-98882", "div_CTR_nso_catalogs");
			$('div#COMMON_TABS').find("li a:contains('Add-on Products')").parent().css("display", "none");
			$('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "block");
			$('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
			$('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
			$('div#COMMON_TABS').find("li a:contains('NSO Catalog')").parent().css("display", "block");
		});
	} catch (e) {
		console.log(e);
	}
}
//function for Tool Relocation add equipment starts...(ADD EQUIPMENT BUTTON)
function addtoolrelocationequipment(ele) {
	localStorage.setItem("add_new_functionality", "TRUE")
	reload_tool_equipmeents()
	var selectedEquipments = [];
	var selectAll = false;
	$('#involved_parties_equipment_addnew').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedEquipments.push(sel_val);
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_TOOL_RELOCATION_EQUIPMENTS',
			'NodeType': 'TOOL RELOCATION MODEL',
			'Values': selectedEquipments,
			'AllValues': selectAll
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList("SYOBJR-98858", "div_CTR_Involved_Parties_Equipments")
			localStorage.setItem("AddToolRelocationEquipment", "yes")
			//CommonLeftView();

		});
	} catch (e) {
		console.log(e);
	}
}

function addtoolrelocation(ele, equipment_id) {
	localStorage.setItem("add_new_functionality", "TRUE")
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_TOOL_RELOCATION_EQUIPMENTS',
			'NodeType': 'TOOL RELOCATION MODEL',
			'Values': [equipment_id],
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList("SYOBJR-98858", "div_CTR_Involved_Parties_Equipments")
			localStorage.setItem("AddToolRelocationEquipment", "yes")
			//CommonLeftView();

		});
	} catch (e) {
		console.log(e);
	}
}
//function for Tool Relocation add equipment ends...(ADD EQUIPMENT BUTTON)
function bulkUploadData(ele) {
	document.getElementById('VIEW_DIV_ID').innerHTML = '';
	try {
		cpq.server.executeScript("CQSPBLKUPL", {
			"ACTION": "BULKUPLOADDATA"
		}, function (dataset) {
			document.getElementById('VIEW_DIV_ID').innerHTML = dataset[0];

		});
	} catch (e) {
		console.log(e);
	}
}

// Bulk Add Spare Parts - Start
function showSparePartsBulkAddModal(ele) {
	$('#partnumbers').val('')
	document.getElementById('VIEW_DIV_ID').innerHTML = '';
	try {
		cpq.server.executeScript("CQSPBLKUPL", {
		}, function (dataset) {
			document.getElementById('VIEW_DIV_ID').innerHTML = dataset[0];
			//CommonLeftView();
		});
	} catch (e) {
		console.log(e);
	}
}
function bulkAddSpareParts() {

	$('#spare-parts-bulk-add-save-btn').prop('disabled', true);
	//var content = $('div#VIEW_DIV_ID #spare-parts-bulk-add-ctnr').val();
	var content = $('div#edit_decrip .txtarea-bulkadd').val();
	$('#cont_viewModalSection').css('display', 'none');
	var ActionType = "ADD_SPARE_PARTS"
	var relatedListID = "SYOBJR-00029"
	if (localStorage.getItem('currentSubTab') == "Spare Parts" && TreeSuperParentParam == "Product Offerings") {
		ActionType = "ADD_PARTS"
		relatedListID = "SYOBJR-00005"
	}
	if (localStorage.getItem("currentSubTab") == "New Parts") {
		new_part = 1
	}
	else {
		new_part = 0
	}
	if (localStorage.getItem("currentSubTab") == "Inclusions") {
		inclusion = 1
	}
	else {
		inclusion = 0
	}
	if (content != '') {
		try {
			localStorage.setItem("showProgressBar", 1);
			$("div#progress-bar-model-text").text("ADDING SPARE PARTS");
			showProgressBar();
			cpq.server.executeScript("CQCRUDOPTN", {
				'Opertion': 'ADD',
				'ActionType': ActionType,
				'NodeType': 'OFFERINGS MODEL',
				'Values': [content],
				'new_part': new_part,
				'inclusion': inclusion
			}, function () {
				localStorage.setItem("showProgressBar", 0);
				$("#dynamic").css("width", "100%").attr("aria-valuenow", 100).text("100% Complete");
				//$('#cont_viewModalSection').css('display', 'none');
				localStorage.setItem("add_new_functionality", "TRUE");
				loadRelatedList(relatedListID, 'div_CTR_related_list');
				$('#progress_bar_modal').modal('hide');
			});
		} catch (e) {
			console.log(e);
		}
	}
}
// Bulk Add Spare Parts - End

// Value Driver functions
function fablocationListKeyHyperLink(value, row) {
	var equipmentRecordId = row.EQUIPMENT_RECORD_ID
	var equipment_value = row.pop_val
	return '<a href="#" id=' + equipment_value + ' onclick="addequipments(this,\'' + equipmentRecordId + '\')">' + value + '</a>'
}
function UnmappedListKeyHyperLink(value, row) {
	var equipmentRecordId = row.EQUIPMENT_RECORD_ID
	var equipment_value = row.pop_val
	return '<a href="#" id=' + equipment_value + ' onclick="addUnmappedEquipment(this,\'' + equipmentRecordId + '\')">' + value + '</a>'
}
function toolrelocationKeyHyperLink(value, row) {
	var equipmentRecordId = row.EQUIPMENT_RECORD_ID
	var equipment_value = row.pop_val
	return '<a href="#" id=' + equipment_value + ' onclick="addtoolrelocation(this,\'' + equipmentRecordId + '\')">' + value + '</a>'
}

function add_on_prdListKeyHyperLink(value, row) {
	var equipmentRecordId = row.PO_COMP_RECORD_ID
	var equipment_value = row.pop_val
	return '<a href="#" id=' + equipment_value + ' onclick="addon_product(this,\'' + equipmentRecordId + '\')">' + value + '</a>'
}
function creditListKeyHyperLink(value, row) {
	var equipmentRecordId = row.CREDITVOUCHER_RECORD_ID
	var equipment_value = row.pop_val
	return '<a href="#" id=' + equipment_value + ' title=\'' + value + '\' onclick="addCredit(this,\'' + equipmentRecordId + '\')">' + value + '</a>'
}
function addUnmappedEquipment(ele, equipmentRecordId) {
	localStorage.setItem("add_new_functionality", "TRUE")
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_UNMAPPED_EQUIPMENTS',
			'NodeType': 'FAB MODEL',
			'Values': [equipmentRecordId]
		}, function () {
			//$("#MM_ALL_REFRESH").click();			
			$('#cont_viewModalSection').css('display', 'none');
			localStorage.setItem("AddEquipment", "yes")
			CommonLeftView();
		});
	} catch (e) {
		console.log(e);
		$('#progress_bar_modal').modal('hide');
	}
}

function addnso(ele, equipmentRecordId) {
	localStorage.setItem("add_new_functionality", "TRUE")
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_NSO',
			'NodeType': 'FAB MODEL',
			'Values': [equipmentRecordId]
		}, function () {
			//$("#MM_ALL_REFRESH").click();			
			$('#cont_viewModalSection').css('display', 'none');
			localStorage.setItem("AddEquipment", "yes")
			// CommonLeftView();
			loadRelatedList("SYOBJR-98882", "div_CTR_nso_catalogs");
			$('div#COMMON_TABS').find("li a:contains('Add-on Products')").parent().css("display", "none");
			$('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "block");
			$('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
			$('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
			$('div#COMMON_TABS').find("li a:contains('NSO Catalog')").parent().css("display", "block");
		});
	} catch (e) {
		console.log(e);
		$('#progress_bar_modal').modal('hide');
	}
}

function addequipments(ele, equipmentRecordId) {
	localStorage.setItem("add_new_functionality", "TRUE")
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_EQUIPMENTS',
			'NodeType': 'FAB MODEL',
			'Values': [equipmentRecordId],
			'TOOL_TYPE': localStorage.getItem("TOOL_TYPE")
		}, function () {
			//$("#MM_ALL_REFRESH").click();			
			localStorage.removeItem('TOOL_TYPE');
			$('#cont_viewModalSection').css('display', 'none');
			localStorage.setItem("AddEquipment", "yes")
			CommonLeftView();
		});
	} catch (e) {
		console.log(e);
		$('#progress_bar_modal').modal('hide');
	}
}
function MAfablocationKeyHyperLink(value, row) {
	var fabRecordId = row.FAB_LOCATION_RECORD_ID
	var fab_value = row.pop_val
	return '<a href="#" id=' + fab_value + ' onclick="addfab(this,\'' + fabRecordId + '\')">' + value + '</a>'
}

function sourcefablocationKeyHyperLink(value, row) {
	var fabRecordId = row.FAB_LOCATION_RECORD_ID
	var fab_value = row.pop_val
	return '<a href="#" id=' + fab_value + ' onclick="addsourcefab(this,\'' + fabRecordId + '\')">' + value + '</a>'
}
function nsoKeyHyperLink(value, row) {
	var fabRecordId = row.PRICEBOOK_ENTRIES_RECORD_ID
	var fab_value = row.pop_val
	return '<a href="#" id=' + fab_value + ' onclick="addnso(this,\'' + fabRecordId + '\')">' + value + '</a>'
}

function addfab(ele, fabRecordId) {
	localStorage.setItem("add_new_functionality", "TRUE")
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_FAB',
			'NodeType': 'FAB MODEL',
			'Values': [fabRecordId]
		}, function () {
			//$("#MM_ALL_REFRESH").click();
			$('#cont_viewModalSection').css('display', 'none');
			//localStorage.setItem("AddFab", "yes")
			localStorage.setItem("left_tree_refresh", "yes");
			$('div#COMMON_TABS').find("li a:contains('Fab Locations')").parent().click();
			CommonLeftView();
			$('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			$('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
		});
	} catch (e) {
		console.log(e);
	}
}
function addCredit(ele, creditRecId) {
	localStorage.setItem("add_new_functionality", "TRUE")
	addon_id = localStorage.getItem("TreeParamRecordId");
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_CREDIT',
			'NodeType': 'FAB MODEL',
			'Values': [creditRecId],
			'ADDON_PRD_ID': addon_id
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList("SYOBJR-98880", "div_CTR_related_list");
			$('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			$('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
		});
	} catch (e) {
		console.log(e);
	}
}
function addCredits(ele) {
	localStorage.setItem("add_new_functionality", "TRUE")
	reload_credit_val();
	var selectedaddons = [];
	var applied_credits = [];
	var credit_amounts = [];
	selectedaddons = JSON.parse(localStorage.getItem("selected_items"));
	addon_id = localStorage.getItem("TreeParamRecordId");
	var selectAll = false;
	var A_Keys = [];
	var A_Values = [];
	$('#add_credits_add_new').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		else {
			var sel_val = $(this).closest('tr').find('td:nth-child(2)').text();
			var edit_index = $("#add_credits_add_new").find("[data-field='CREDIT_APPLIED']").index() + 1;
			var applied_credit = $(this).closest('tr').find('td:nth-child(' + edit_index + ') > input').val();
			edit_index = $("#add_credits_add_new").find("[data-field='WRBTR']").index() + 1;
			var credit_amount = $(this).closest('tr').find('td:nth-child(' + edit_index + ')').text();
			if (sel_val != '') {
				selectedaddons.push(sel_val);
			}
			applied_credits.push(applied_credit)
			credit_amounts.push(credit_amount)
		}
	});
	selectedaddons = removeDuplicates(selectedaddons)
	selectedaddons = selectedaddons.filter(function (el) { return el != ''; });
	$('#add_credits_add_new  .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#add_credits_add_new .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	edit_index = $("#add_credits_add_new").find("[data-field='ZAFNOTE']").index() + 1;
	var credit_note = $('#add_credits_add_new tr:last-child td:nth-child(' + edit_index + ')').text();
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_CREDIT',
			'NodeType': 'FAB MODEL',
			'Values': selectedaddons,
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values,
			'ADDON_PRD_ID': addon_id,
			'APPLIED_CREDITS': applied_credits,
			'CREDIT_AMOUNTS': credit_amounts,
			'CREDIT_NOTE': credit_note
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList("SYOBJR-98880", "div_CTR_related_list");

			$('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			$('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
		});

	} catch (e) {
		console.log(e);
	}
}
function addon_product(ele, addon_RecordId) {
	localStorage.setItem("add_new_functionality", "TRUE")
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_ON_PRODUCTS',
			'NodeType': 'FAB MODEL',
			'Values': [addon_RecordId]
		}, function () {
			//$("#MM_ALL_REFRESH").click();
			$('#cont_viewModalSection').css('display', 'none');
			CommonLeftView();
			$('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			$('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
		});
	} catch (e) {
		console.log(e);
	}
}
function addon_products(ele) {
	localStorage.setItem("add_new_functionality", "TRUE")
	reload_add_on_val();
	var selectedaddons = [];
	selectedaddons = JSON.parse(localStorage.getItem("selected_items"));
	var selectAll = false;
	var A_Keys = [];
	var A_Values = [];
	$('#Include_add_on_addnew').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedaddons.push(sel_val);
		}
	});
	$('#Include_add_on_addnew  .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#Include_add_on_addnew .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_ON_PRODUCTS',
			'NodeType': 'FAB MODEL',
			'Values': selectedaddons,
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function () {
			//$("#MM_ALL_REFRESH").click();
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList("SYOBJR-98859", "div_CTR_Add_On_Products")

			$('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			$('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			CommonLeftView();
		});

	} catch (e) {
		console.log(e);
	}
}
function addfabs(ele) {
	localStorage.setItem("add_new_functionality", "TRUE")
	reload_fab_val();
	var selectedFabs = [];
	selectedFabs = JSON.parse(localStorage.getItem("selected_items"));
	var selectAll = false;
	var A_Keys = [];
	var A_Values = [];
	$('#fablocation_addnew').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedFabs.push(sel_val);
		}
	});
	$('#fablocation_addnew  .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#fablocation_addnew .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_FAB',
			'NodeType': 'FAB MODEL',
			'Values': selectedFabs,
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function () {
			//$("#MM_ALL_REFRESH").click();
			$('#cont_viewModalSection').css('display', 'none');
			// localStorage.setItem("AddFab", "yes")
			localStorage.setItem("left_tree_refresh", "yes")
			CommonLeftView();
			$('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			$('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			loadRelatedList("SYOBJR-98789", "div_CTR_related_list")
		});

	} catch (e) {
		console.log(e);
	}
}
function addcontacts(ele) {
	localStorage.setItem("add_new_functionality", "TRUE")
	reload_contact_val();
	var selectedContacts = [];
	selectedContacts = JSON.parse(localStorage.getItem("selected_items"));
	var selectAll = false;
	var A_Keys = [];
	var A_Values = [];
	$('#contact_replace_addnew_model').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedContacts.push(sel_val);
		}
	});
	$('#contact_replace_addnew_model.filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#contact_replace_addnew_model.' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQRPLACTCT", {
			'ActionType': 'ADD_CONTACT',
			'Values': selectedContacts,
			'AllValues': selectAll,
		}, function () {
			//$("#MM_ALL_REFRESH").click();
			$('#cont_viewModalSection').css('display', 'none');
			// localStorage.setItem("AddContact", "yes")
			localStorage.setItem("left_tree_refresh", "yes")
			CommonLeftView();
			$('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			$('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			loadRelatedList("SYOBJR-98871", "div_CTR_related_list")
		});

	} catch (e) {
		console.log(e);
	}
}

function addsourcefabs(ele) {
	localStorage.setItem("add_new_functionality", "TRUE")
	reload_source_fab_val();
	var selectedFabs = [];
	selectedFabs = JSON.parse(localStorage.getItem("selected_items"));
	var selectAll = false;
	$('#fablocation_addnew').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedFabs.push(sel_val);
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_SOURCE_FAB',
			'NodeType': 'FAB MODEL',
			'Values': selectedFabs,
			'AllValues': selectAll
		}, function () {
			//$("#MM_ALL_REFRESH").click();
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList("SYOBJR-98857", "div_CTR_Source_Fab_Locations");
			chainsteps_breadcrumb(localStorage.getItem('currentSubTab'));
			tool_breadcrumb();
			// CommonLeftView();
			$('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			$('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
		});

	} catch (e) {
		console.log(e);
	}
}

function addsourcefab(ele, sourcefab_id) {
	localStorage.setItem("add_new_functionality", "TRUE")
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_SOURCE_FAB',
			'NodeType': 'FAB MODEL',
			'Values': [sourcefab_id],
		}, function () {
			//$("#MM_ALL_REFRESH").click();
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList("SYOBJR-98857", "div_CTR_Source_Fab_Locations");
			chainsteps_breadcrumb(localStorage.getItem('currentSubTab'));
			chainsteps_breadcrumb($('#COMMON_TABS > ul > li.active').text());
			// CommonLeftView();
			$('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
			$('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
				silent: true
			}]);
		});

	} catch (e) {
		console.log(e);
	}
}


function addcoveredobj(ele, CoveredRecordId) {
	localStorage.setItem("add_new_functionality", "TRUE")
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_COVERED_OBJ',
			'NodeType': 'COVERED OBJ MODEL',
			'Values': [CoveredRecordId]
		}, function () {
			//$("#MM_ALL_REFRESH").click();
			$('#cont_viewModalSection').css('display', 'none');
			localStorage.setItem("COVERED_OBJ_SAVING", "yes");
			localStorage.setItem("left_tree_refresh", "yes");
			subTabDetails(localStorage.getItem('currentSubTab'), 'Related', localStorage.getItem('CurrentObject'), node.id);
			CommonLeftView();
		});
	} catch (e) {
		console.log(e);
	}
}

function CovObjKeyHyperLink(value, row) {
	if (TreeParam == "Add-On Products"){
		var CoveredRecordId = row.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID
	}
	else{
		var CoveredRecordId = row.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID
	}
	
	var covered_obj_value = row.pop_val
	return '<a href="#" id=' + covered_obj_value + ' onclick="addcoveredobj(this,\'' + CoveredRecordId + '\')">' + value + '</a>'
}


function showProgressBar(intervalTime = 2100) {
	var show = localStorage.getItem("showProgressBar");
	$('#pageloader').css('cssText', 'top: 61.5px; left: 582.004px; display:none !important;');
	$('.overlay').css('display', 'none !important');
	$('#progress_bar_modal .modal-dialog').css('cssText', 'width:550px !important');

	if (show == 1) {
		show = 0;
		var width = 10;
		var id = setInterval(frame, intervalTime);
		$('#pageloader').css('cssText', 'top: 61.5px; left: 582.004px; display:none !important;');
		$('.overlay').css('display', 'none !important');
		$("#dynamic").css("width", "0%").attr("aria-valuenow", 0).text("0% Complete");
		$('#progress_bar_modal').modal('show');
		function frame() {

			if (width >= 100) {
				clearInterval(id);
				show = 1;
			} else {
				$('#pageloader').css('cssText', 'top: 61.5px; left: 582.004px; display:none !important;');
				$('.overlay').css('display', 'none !important');
				$("#dynamic").css("width", width + "%").attr("aria-valuenow", width).text(width + "% Complete");

				width = width + 10;
			}
		}
	}
}
function realProgressBar(value) {
	var show = localStorage.getItem("realProgressBar");
	$('#pageloader').css('cssText', 'top: 61.5px; left: 582.004px; display:none !important;');
	$('.overlay').css('display', 'none !important');
	$('#progress_bar_sscm_popup .modal-dialog').css('cssText', 'width:550px !important');

	if (show == 1) {
		show = 0;
		var width = 10;
		var id = setInterval(frame, value);
		$('#pageloader').css('cssText', 'top: 61.5px; left: 582.004px; display:none !important;');
		$('.overlay').css('display', 'none !important');
		$("#progress_sscm_dynamic").css("width", "0%").attr("aria-valuenow", 0).text("0% Complete");
		$('#progress_bar_sscm_popup').modal('show');
		function frame() {

			if (width >= 100) {
				clearInterval(id);
				show = 1;
			} else {
				$('#pageloader').css('cssText', 'top: 61.5px; left: 582.004px; display:none !important;');
				$('.overlay').css('display', 'none !important');
				$("#progress_sscm_dynamic").css("width", width + "%").attr("aria-valuenow", width).text(width + "% Complete");

				width = width + 10;
			}
		}
	}
}
function addcoveredobjs(ele) {
	localStorage.setItem("add_new_functionality", "TRUE")
	var selectedobjs = [];
	var selectAll = false;
	$('#Coveredobjectsaddnew').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if ($(this).attr('name') == 'btSelectItem' && sel_val != '') {
			selectedobjs.push(sel_val);
		}
	});
	var A_Keys = [];
	var A_Values = [];
	$('#Coveredobjectsaddnew  .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#Coveredobjectsaddnew .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {

		localStorage.setItem("showProgressBar", 1);
		$("div#progress-bar-model-text").text("ADDING COVERED OBJECTS");
		var totalRecordsCount = $("div#pagination_Coveredobjectsaddnew #TotalRecordsCount").text();
		var intervalCount = 1000;
		if (parseInt(totalRecordsCount) > 350) {
			intervalCount = parseInt(parseInt(totalRecordsCount) / 350) * intervalCount;
		}
		showProgressBar(intervalCount);
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'ADD',
			'ActionType': 'ADD_COVERED_OBJ',
			'NodeType': 'COVERED OBJ MODEL',
			'Values': selectedobjs,
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values,
			'tools_from_ui': 'Yes'
		}, function () {
			//$("#MM_ALL_REFRESH").click();		
			localStorage.setItem("showProgressBar", 0);
			$("#dynamic").css("width", "100%").attr("aria-valuenow", 100).text("100% Complete");
			$('#cont_viewModalSection').css('display', 'none');
			localStorage.setItem("left_tree_refresh", "yes")
			localStorage.setItem("restrict_covered_obj_grid", 'yes');
			CommonLeftView();
			localStorage.setItem("COVERED_OBJ_SAVING", "yes")
			$('#progress_bar_modal').modal('hide');
			if (AllTreeParam['TreeParam'] == "Sending Equipment") {
				SendingEquipmentTreeTable()
			} else {
				CoveredObjTreeTable();
			}


		});
	} catch (e) {
		console.log(e);
		$('#progress_bar_modal').modal('hide');
	}
}
// function reload_add_on_product() {
//     localStorage.setItem("selected_items", '');
//     if (localStorage.getItem("selected_items").length == 0) {
//         var selected_items = [];
//     } else {
//         var selected_items = JSON.parse(localStorage.getItem("selected_items"))
//     }
//     var arr = $('#SYOBJR_98859_E7F67BDD_48A4_499A_B1AB_C4FDB2031D6E').find('[type="checkbox"]:checked').map(function () {
//         sel_val = $(this).closest('tr').find('td:nth-child(3)').text()
//         if (jQuery.inArray(sel_val, selected_items) == -1) {
//             selected_items.push(sel_val);
//         }
//     });
//     var unchecked_prd = []
//     var arr = $('#SYOBJR_98859_E7F67BDD_48A4_499A_B1AB_C4FDB2031D6E').find('[type="checkbox"]:not(:checked)').map(function () {
//         unchecked_prd.push($(this).closest('tr').find('td:nth-child(3)').text());
//     });
//     let difference = selected_items.filter(x => !unchecked_prd.includes(x));
//     localStorage.setItem("selected_items", JSON.stringify(difference))
// }
function reload_tool_equipmeents() {
	localStorage.setItem("selected_items", '');
	if (localStorage.getItem("selected_items").length == 0) {
		var selected_items = [];
	} else {
		var selected_items = JSON.parse(localStorage.getItem("selected_items"))
	}
	var arr = $('#involved_parties_equipment_addnew').find('[type="checkbox"]:checked').map(function () {
		sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (jQuery.inArray(sel_val, selected_items) == -1) {
			selected_items.push(sel_val);
		}
	});
	var unchecked_fab = []
	var arr = $('#involved_parties_equipment_addnew').find('[type="checkbox"]:not(:checked)').map(function () {
		unchecked_fab.push($(this).closest('tr').find('td:nth-child(2)').text());
	});
	let difference = selected_items.filter(x => !unchecked_fab.includes(x));
	localStorage.setItem("selected_items", JSON.stringify(difference))
}

// Billing Matrix - START
/*function openBillingMatrixDateChangeModal(ele){
	var billingDate = ele;
	$('div#billing_matrix_viewModal input#BILLING_DATE').val(billingDate); 
	$('#spare-parts-bulk-save-btn').css('display','none');
	$('#spare-parts-bulk-cancel-btn').css('display','none');
	$('div#billing_matrix_viewModal input#BILLING_DATE_ORIGINAL').val(billingDate); 
	$('#billing_matrix_viewModal').modal('show'); 
	$('#billingmatrix_save').css('display','none');
	$('#billingmatrix_cancel').css('display','none');
	
}*/

function billing_matrix_date_change() {

	var modified_date = $('div#billing_matrix_viewModal input#BILLING_DATE').val();
	var billing_date = $('div#billing_matrix_viewModal input#BILLING_DATE_ORIGINAL').val();
	var service_id = AllTreeParam['TreeParam']
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'UPDATE',
			'ActionType': 'UPDATE_BILLING_MATRIX_ITEMS_DATE',
			'NodeType': 'BILLING MATRIX MODEL',
			'Values': [{ 'modified_date': modified_date, 'billing_date': billing_date, 'service_id':service_id }]
		}, function () {
			$('#billing_matrix_viewModal').modal('hide');
			$('div#COMMON_TABS').find('li.active').trigger('click');
		});
	} catch (e) {
		console.log(e);
	}

}

function onclick_datepicker_billing_matrix(id) {
	var billing_date = $("#" + id).val();
	var billing_start_date = $(".segment_part_number_text_child").text();
	var billing_end_date = $(".segment_part_text_child").text();
	if (billing_date) {		
		var current_date = new Date(billing_start_date);
		var last_date = new Date(billing_end_date)
		var startDate = new Date(current_date.getFullYear(), current_date.getMonth(), 1);
		var endDate = last_date
		$("#" + id).datepicker({
			autoclose: true,
			startDate: startDate,
			endDate: endDate
		});
		$("#" + id).datepicker('show');
	}
}
// Billing Matrix - END
function reload_fab_val() {
	localStorage.setItem("selected_items", '');
	if (localStorage.getItem("selected_items").length == 0) {
		var selected_items = [];
	} else {
		var selected_items = JSON.parse(localStorage.getItem("selected_items"))
	}
	var arr = $('#source_fablocation_addnew').find('[type="checkbox"]:checked').map(function () {
		sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (jQuery.inArray(sel_val, selected_items) == -1) {
			selected_items.push(sel_val);
		}
	});
	var unchecked_fab = []
	var arr = $('#source_fablocation_addnew').find('[type="checkbox"]:not(:checked)').map(function () {
		unchecked_fab.push($(this).closest('tr').find('td:nth-child(2)').text());
	});
	let difference = selected_items.filter(x => !unchecked_fab.includes(x));
	localStorage.setItem("selected_items", JSON.stringify(difference))
}

function reload_contact_val() {
	localStorage.setItem("selected_items", '');
	if (localStorage.getItem("selected_items").length == 0) {
		var selected_items = [];
	} else {
		var selected_items = JSON.parse(localStorage.getItem("selected_items"))
	}
	var arr = $('#source_contact_replace_addnew_model').find('[type="checkbox"]:checked').map(function () {
		sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (jQuery.inArray(sel_val, selected_items) == -1) {
			selected_items.push(sel_val);
		}
	});
	var unchecked_contact = []
	var arr = $('#source_contact_replace_addnew_model').find('[type="checkbox"]:not(:checked)').map(function () {
		unchecked_contact.push($(this).closest('tr').find('td:nth-child(2)').text());
	});
	let difference = selected_items.filter(x => !unchecked_contact.includes(x));
	localStorage.setItem("selected_items", JSON.stringify(difference))
}
function reload_offering_val() {
	localStorage.setItem("selected_items", '');
	if (localStorage.getItem("selected_items").length == 0) {
		var selected_items = [];
	} else {
		var selected_items = JSON.parse(localStorage.getItem("selected_items"))
	}
	var arr = $('#offerings-addnew-model').find('[type="checkbox"]:checked').map(function () {
		sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (jQuery.inArray(sel_val, selected_items) == -1) {
			selected_items.push(sel_val);
		}
	});
	var unchecked_fab = []
	var arr = $('#offerings-addnew-model').find('[type="checkbox"]:not(:checked)').map(function () {
		unchecked_fab.push($(this).closest('tr').find('td:nth-child(2)').text());
	});
	let difference = selected_items.filter(x => !unchecked_fab.includes(x));
	localStorage.setItem("selected_items", JSON.stringify(difference))
}

function reload_parts_val() {
	localStorage.setItem("selected_items", '');
	if (localStorage.getItem("selected_items").length == 0) {
		var selected_items = [];
	} else {
		var selected_items = JSON.parse(localStorage.getItem("selected_items"))
	}
	var arr = $('#parts-addnew-model').find('[type="checkbox"]:checked').map(function () {
		sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (jQuery.inArray(sel_val, selected_items) == -1) {
			selected_items.push(sel_val);
		}
	});
	var unchecked_fab = []
	var arr = $('#parts-addnew-model').find('[type="checkbox"]:not(:checked)').map(function () {
		unchecked_fab.push($(this).closest('tr').find('td:nth-child(2)').text());
	});
	let difference = selected_items.filter(x => !unchecked_fab.includes(x));
	localStorage.setItem("selected_items", JSON.stringify(difference))
}
function reload_source_fab_val() {
	localStorage.setItem("selected_items", '');
	if (localStorage.getItem("selected_items").length == 0) {
		var selected_items = [];
	} else {
		var selected_items = JSON.parse(localStorage.getItem("selected_items"))
	}
	var arr = $('#source_fablocation_addnew').find('[type="checkbox"]:checked').map(function () {
		sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (jQuery.inArray(sel_val, selected_items) == -1) {
			selected_items.push(sel_val);
		}
	});
	var unchecked_fab = []
	var arr = $('#source_fablocation_addnew').find('[type="checkbox"]:not(:checked)').map(function () {
		unchecked_fab.push($(this).closest('tr').find('td:nth-child(2)').text());
	});
	let difference = selected_items.filter(x => !unchecked_fab.includes(x));
	localStorage.setItem("selected_items", JSON.stringify(difference))
}
function reload_credit_val() {
	localStorage.setItem("selected_items", '');
	if (localStorage.getItem("selected_items").length == 0) {
		var selected_items = [];
	} else {
		var selected_items = JSON.parse(localStorage.getItem("selected_items"))
	}
	var arr = $('#add_credits_add_new').find('[type="checkbox"]:checked').map(function () {
		sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (jQuery.inArray(sel_val, selected_items) == -1) {
			selected_items.push(sel_val);
		}
	});
	var unchecked_fab = []
	var arr = $('#add_credits_add_new').find('[type="checkbox"]:not(:checked)').map(function () {
		unchecked_fab.push($(this).closest('tr').find('td:nth-child(2)').text());
	});
	let difference = selected_items.filter(x => !unchecked_fab.includes(x));
	localStorage.setItem("selected_items", JSON.stringify(difference))
}
function reload_add_on_val() {
	localStorage.setItem("selected_items", '');
	if (localStorage.getItem("selected_items").length == 0) {
		var selected_items = [];
	} else {
		var selected_items = JSON.parse(localStorage.getItem("selected_items"))
	}
	var arr = $('#Include_add_on_addnew').find('[type="checkbox"]:checked').map(function () {
		sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (jQuery.inArray(sel_val, selected_items) == -1) {
			selected_items.push(sel_val);
		}
	});
	var unchecked_fab = []
	var arr = $('#Include_add_on_addnew').find('[type="checkbox"]:not(:checked)').map(function () {
		unchecked_fab.push($(this).closest('tr').find('td:nth-child(2)').text());
	});
	let difference = selected_items.filter(x => !unchecked_fab.includes(x));
	localStorage.setItem("selected_items", JSON.stringify(difference))
}
// Equipments Saave Functionality starts
function reload_equipments() {
	if (localStorage.getItem("selected_equipments").length == 0) {
		var selected_equipments = [];
	}
	else {
		var selected_equipments = JSON.parse(localStorage.getItem("selected_equipments"))
	}
	$('table#equipments_addnew tbody.equipments_id tr').each(function (index) {
		var classname = $(this).attr('class');

		if (classname == 'selected') {
			var get_Id = $(this).children('td:nth-child(2)').text();
			get_Idlist.push($(this).children('td:nth-child(2)').text());
		}

		if (jQuery.inArray(get_Idlist, selected_equipments) == -1) {
			selected_equipments.push(get_Idlist);
		}
	});
	var unchecked_equipments1 = []
	$('table#equipments_addnew tbody.equipments_id tr').each(function (index) {
		var classname = $(this).attr('class');

		if (classname != 'selected') {
			var unchecked_equipments = $(this).children('td:nth-child(2)').text();
			unchecked_equipments1.push($(this).children('td:nth-child(2)').text());
		}
	});
	let difference = selected_equipments.filter(x => !unchecked_equipments1.includes(x));
	localStorage.setItem("selected_equipments", JSON.stringify(difference))
}

function save_equipments() {
	reload_equipments();
	var selected_equipments = [];
	var get_Idlist = [];
	selected_equipments = JSON.parse(localStorage.getItem("selected_equipments"));
	var mode = localStorage.getItem("Profile_ACTION");
	var [currentprofileId, currentprofilename, Primary_Data] = [$("input#SYSEFL_QT_00001").val(), $("input#SYSEFL_QT_00004").val(), $("input#SYSEFL_QT_00001").val()];
	localStorage.setItem("prfid", currentprofileId)
	localStorage.setItem("Primary_Dataapp", Primary_Data)
	localStorage.setItem("prfname", currentprofilename)
	localStorage.setItem("Profile_MEMEBR", "VIEW")
	$('table#equipments_addnew tbody.equipments_id tr').each(function (index) {
		var classname = $(this).attr('class');

		if (classname == 'selected') {
			var get_Id = $(this).children('td:nth-child(2)').text();
			get_Idlist.push($(this).children('td:nth-child(2)').text());
		}
	});
	localStorage.setItem("SELECTED_EQUIPMENTS", JSON.stringify(get_Idlist))
	var currentid = localStorage.getItem("CurrentNodeId");

	try {
		cpq.server.executeScript("CQEQUPSAVE", { 'CURRREC': currentprofileId, 'SELECTROW': JSON.parse(localStorage.getItem("SELECTED_EQUIPMENTS")), 'Primary_Data': Primary_Data, 'currentprofilename': currentprofilename }, function () {

			$('.BTN_MA_ALL_REFRESH').click();


		});

		$("#PROFILE_BANNER_RECORD_ID abbr").text(Primary_Data);
		$("#PROFILE_BANNER_RECORD_ID abbr").attr('title', Primary_Data);
		$('#Profilestreeview').treeview('selectNode', [parseInt(currentid), { silent: true }]);
		[CurrentRecordId, RecName] = ['SYOBJR-98797', 'div_CTR_Equipments'];
		loadRelatedList(CurrentRecordId, RecName);

	}
	catch (e) {
		console.log(e);
	}
}
localStorage.setItem("selected_equipments", JSON.stringify([]));
// Equipments save functionality ends 





function calculate_QItems(ele) {
	try {
		QIDriver_popup();
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'CALCULATE',
			'NodeType': 'QUOTE ITEM CALCULATION'
		}, function (dataset) {

		});
	} catch (e) {
		console.log(e);
	}
}

// Entitlements Notification Display
function display_notification() {
	try {
		cpq.server.executeScript("CQENTLMENT", {
			'ACTION': 'NOTIFY',
		}, function (data) {

			$('#TREE_div').prepend(data);

		});
	} catch (e) {
		console.log(e);
	}
}


// Items Covered Object - Price Benchmark - Column toggle - Start
// function price_benchmark_column_toggle(ele){
//     var tableId = $(ele).closest('table').attr('id');
//     var columns = ['PRICE_BENCHMARK_TYPE','TOOL_CONFIGURATION','ANNUAL_BENCHMARK_BOOKING_PRICE','CONTRACT_ID','CONTRACT_VALID_FROM','CONTRACT_VALID_TO','BENCHMARKING_THRESHOLD'];
//     var btnClasses = document.getElementById("price-benchmark-column-toggle").className;
//     if (btnClasses.includes('glyphicon-minus-sign')){     
//         //$(ele).removeClass("glyphicon-minus").addClass("glyphicon-plus");   
//         $.each(columns, function(index, column) {
//             $('#'+tableId).bootstrapTable('hideColumn', column);
//         });
//         $('#price-benchmark-column-toggle').removeClass("glyphicon-minus-sign").addClass("glyphicon-plus-sign");
//         if ($("#pricing_picklist_select :selected").attr('value') == 'Pricing' && AllTreeParam['TreeParam'] == 'Quote Items'){
//             $('#price-benchmark-column-toggle').closest('th').attr('rowspan',3);
//         }
//         $('#price-benchmark-column-toggle').closest('th').attr('colspan',1);
//         $('div#div_CTR_Assemblies table tbody tr td:nth-last-child(1)').css('cssText', 'border-left:1px solid #dcdcdc !important');
//     }
//     else{        
//         //$(ele).removeClass("glyphicon-plus").addClass("glyphicon-minus");
//         $.each(columns, function(index, column) {
//             $('#'+tableId).bootstrapTable('showColumn', column);
//         });
//         $('#price-benchmark-column-toggle').removeClass("glyphicon-plus-sign").addClass("glyphicon-minus-sign");
//         $('#price-benchmark-column-toggle').closest('th').attr('colspan',7);
//         $('div#div_CTR_Assemblies table tbody tr td:nth-last-child(7)').css('cssText', 'border-left:1px solid #dcdcdc !important');
//     }
// }
function quote_items_column_toggle(ele) {
	var tableId = $(ele).closest('table').attr('id');
	var rec_id = $(ele).attr('id');
	var btnClasses = document.getElementById(rec_id).className;
	var grouping_dict = {}
	var temp_flag = ""
	var grouping_list = ['contractual_info_column_toggle', 'object_info_column_toggle', 'warranty_info_column_toggle', 'cat_info_column_toggle', 'price_info_column_toggle']
	var index = grouping_list.indexOf(rec_id);
	if (index > -1) {
		grouping_list.splice(index, 1);
	};
	grouping_list.forEach(function (ele) {
		var btnclasses_temp = document.getElementById(ele).className
		if (btnclasses_temp.includes('glyphicon-plus-sign')) {
			temp_flag = "plus"
			grouping_dict[ele] = temp_flag
		}

	});
	if (rec_id == 'object_info_column_toggle') {
		var columns = ['GOT_CODE', 'ASSEMBLY_ID', 'EQNODE', 'PROCES', 'PM_ID', 'MNTEVT_LEVEL', 'KIT_NAME', 'KIT_NUMBER', 'KPU'];
	}
	else if (rec_id == 'contractual_info_column_toggle') {
		var columns = ['QUANTITY', 'GREENBOOK', 'FABLOCATION_ID', 'CNTYER', 'STADTE', 'ENDDTE', 'TENVGC', 'TNTVGC', 'TNTMGC', 'BILTYP'];
	}
	else if (rec_id == 'warranty_info_column_toggle') {
		var columns = ['SPSPCT', 'WTYSTE', 'WTYEND', 'WTYDAY']
	}
	else if (rec_id == 'cat_info_column_toggle') {
		var columns = ['UIMVCI', 'UIMVPI', 'CAVVCI', 'CAVVPI', 'ATGKEY', 'ATGKEC', 'ATGKEP', 'NWPTOC', 'NWPTOP', 'AMNCCI']
	}
	else if (rec_id == 'price_info_column_toggle') {
		var columns = ['TRGPRC', 'SLSPRC', 'BDVPRC', 'CELPRC', 'TGADJP', 'YOYPCT', 'USRPRC', 'BCHPGC', 'BCHDPT']
	}

	if (btnClasses.includes('glyphicon-minus-sign')) {
		$.each(columns, function (index, column) {
			get_index = $("#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F ").find("th[data-field='" + column + "']").index() + 1 + 8
			$("#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F th[data-field='" + column + "']").hide()
			$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F td:nth-child(' + get_index + ')').hide();
			//$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F td:nth-child('+get_index+')').css('cssText', 'border-left:0px solid #dcdcdc !important');

		});
		$("#" + rec_id).removeClass("glyphicon-minus-sign").addClass("glyphicon-plus-sign");
		$("#" + rec_id).closest('th').attr('colspan', 1);
	}
	else {
		$.each(columns, function (index, column) {
			get_index = $("#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F ").find("th[data-field='" + column + "']").index() + 1 + 8
			$("#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F th[data-field='" + column + "']").show()
			$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F td:nth-child(' + get_index + ')').show();
			//$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F td:nth-child('+get_index+')').css('cssText', 'border-left:1px solid #dcdcdc !important');
		});
		$("#" + rec_id).removeClass("glyphicon-plus-sign").addClass("glyphicon-minus-sign");
		$("#" + rec_id).closest('th').attr('colspan', columns.length + 1);
	}
	//$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F tbody tr td:nth-child(8)').css('cssText', 'border-left:1px solid #dcdcdc !important');
	// assigning class for adjacent groups
	if (Object.keys(grouping_dict).length != 0) {
		for (const [key, value] of Object.entries(grouping_dict)) {
			$("#" + key).removeClass("glyphicon-minus-sign").addClass("glyphicon-plus-sign");
			$("#" + key).closest('th').attr('colspan', 1);

		}
	}
	// if(temp_flag == 'plus'){
	// 	$("#"+near_group).removeClass("glyphicon-minus-sign").addClass("glyphicon-plus-sign");
	// 	$("#"+near_group).closest('th').attr('colspan',1);
	// }


}
// Items Covered Object - Price Benchmark - Column toggle - End
// Items Covered Object - Entitlement Category - Column toggle starts
//A055S000P01-4401 Pricing view
function entitlement_category_toggle(ele) {
	var tableId = $(ele).closest('table').attr('id');
	var arr_id = [];
	var header2_id_arr = []
	var rec_id = $(ele).attr('id');
	var data_value = $(ele).attr('data-field');
	var btnClasses = document.getElementById(rec_id).className;
	//header1
	if (rec_id == 'entitlement-header-category-toggle') {
		subclass = ".entitlement_category_header"
		//hiding header2
		$("#" + tableId + ' .ent_header2').each(function () {
			header2_id_arr.push($(this).attr("data-field"));
		});
	}
	//header2
	else if (rec_id == 'entitlement-category-toggle') {
		subclass = ".entitlement_category_" + data_value
	}


	//getting col name dynamically
	$("#" + tableId + ' ' + subclass).each(function () {
		arr_id.push($(this).attr("data-field"));
	});
	for (var i = 0; i < arr_id.length; i++) {

		if (arr_id[i] === undefined) {
			arr_id.splice(i, 1);
			i--;
		}
	}
	//console.log(arr_id)
	if (arr_id.length != 0) {
		localStorage.setItem('hided_column_ent', arr_id)
	}

	//hiding columns
	if (btnClasses.includes('glyphicon-minus-sign')) {

		//$(ele).removeClass("glyphicon-minus").addClass("glyphicon-plus");   
		$.each(arr_id, function (index, column) {
			$('#' + tableId).bootstrapTable('hideColumn', column);
		});
		//hiding header2 
		if (rec_id == 'entitlement-header-category-toggle') {
			$.each(header2_id_arr, function (index, column) {
				$("#" + tableId + " th[data-field='" + column + "']").hide()
			});

		}
		if (rec_id == 'entitlement-category-toggle') {

			$('.ent_header1').attr('colspan', arr_id.length + 1);
		}
		$('#' + rec_id).removeClass("glyphicon-minus-sign").addClass("glyphicon-plus-sign");
		$('#' + rec_id).closest('th').attr('colspan', 1);
		$('#' + rec_id).closest('th').attr('rowspan', arr_id.length);
		$('div#div_CTR_Assemblies table tbody tr td:nth-last-child(1)').css('cssText', 'border-left:1px solid #dcdcdc !important');
	}
	else {
		//$(ele).removeClass("glyphicon-plus").addClass("glyphicon-minus");
		if (arr_id.length == 0) {
			arr_id = localStorage.getItem('hided_column_ent').split(',')
		}
		$.each(arr_id, function (index, column) {
			$('#' + tableId).bootstrapTable('showColumn', column);
		});
		//showing header2
		if (rec_id == 'entitlement-header-category-toggle') {
			$.each(header2_id_arr, function (index, column) {
				$("#" + tableId + " th[data-field='" + column + "']").show()
			});

		}
		$('#' + rec_id).removeClass("glyphicon-plus-sign").addClass("glyphicon-minus-sign");
		$('#' + rec_id).closest('th').attr('colspan', arr_id.length);
		$('div#div_CTR_Assemblies table tbody tr td:nth-last-child(7)').css('cssText', 'border-left:1px solid #dcdcdc !important');
	}
}
// Items Covered Object - Entitlement Category - Column toggle - End
// Items Covered Object - grouping for cost,price,line summary - Column toggle - Start
function line_item_column_toggle(ele) {
	var tableId = $(ele).closest('table').attr('id');
	var rec_id = $(ele).attr('id');
	var columns = []
	if (rec_id == 'cost-column-toggle') {
		columns = ['TOTAL_COST_WOSEEDSTOCK', 'TOTAL_COST_WSEEDSTOCK'];
	}
	else if (rec_id == 'price-column-toggle') {
		columns = ['MODEL_PRICE', 'TARGET_PRICE', 'CEILING_PRICE', 'SALES_DISCOUNT_PRICE', 'NET_PRICE'];
	}
	else if (rec_id == 'linesummary-column-toggle') {
		columns = ['DISCOUNT', 'SRVTAXCLA_DESCRIPTION', 'TAX_PERCENTAGE', 'NET_VALUE'];
	}

	var btnClasses = document.getElementById(rec_id).className;
	if (btnClasses.includes('glyphicon-minus-sign')) {
		//$(ele).removeClass("glyphicon-minus").addClass("glyphicon-plus");   
		$.each(columns, function (index, column) {
			$('#' + tableId).bootstrapTable('hideColumn', column);
		});
		$('#' + rec_id).removeClass("glyphicon-minus-sign").addClass("glyphicon-plus-sign");
		if ($("#pricing_picklist_select :selected").attr('value') == 'Pricing' && AllTreeParam['TreeParam'] == 'Quote Items') {
			$('#' + rec_id).closest('th').attr('rowspan', 3);
		}
		$('#' + rec_id).closest('th').attr('colspan', 1);
		// $('div#div_CTR_Assemblies table tbody tr td:nth-last-child(1)').css('cssText', 'border-left:1px solid #dcdcdc !important');
	}
	else {
		//$(ele).removeClass("glyphicon-plus").addClass("glyphicon-minus");
		$.each(columns, function (index, column) {
			$('#' + tableId).bootstrapTable('showColumn', column);
		});
		$('#' + rec_id).removeClass("glyphicon-plus-sign").addClass("glyphicon-minus-sign");
		$('#' + rec_id).closest('th').attr('colspan', columns.length);
		// $('div#div_CTR_Assemblies table tbody tr td:nth-last-child(7)').css('cssText', 'border-left:1px solid #dcdcdc !important');
	}
}
// Items Covered Object - Items Covered Object - grouping for cost,price,line summary - Column toggle - Column toggle - End
//setInterval(showpricingbenchmarknotify, 10)

function showpricingbenchmarknotify() {

	cpq.server.executeScript("CQCRUDOPTN", {
		'Opertion': 'GET',
		'ActionType': 'SHOW_PRICING_BENCHMARKING_NOTIFICATION',
		'NodeType': 'QUOTE LEVEL NOTIFICATION'
	}, function (data) {
		approval_txn_noty = data[2]
		if (approval_txn_noty) {
			$(".emp_notifiy").css('display', 'block');
			$("#PageAlert ").css('display', 'block');
			$("#alertnotify").html(approval_txn_noty);
			$(".alert-warning").css('display', 'block');
		}

	});




}
//commented code(Approvals node functionality in Quotes explorer) - start
//SUBMIT FOR APPROVAL AND APPROVE BUTTON ONCLICK
// function quote_approval(ele){
//     var status = "";
//     if(ele == 'APPROVE'){
//         status = "APPROVED"
//     }else if(ele == "SUBMIT"){
//         status = "SUBMIT FOR APPROVAL"
//     }
//     try {
//         cpq.server.executeScript("CQCRUDOPTN", {
//             'TriggerFrom': status,
//             'Opertion':'UPDATE',
//             'ActionType': 'UPDATE_APPROVAL_STATUS',
//             'NodeType': 'QUOTE APPROVAL MODEL',
//         }, function () {
//             //$("#MM_ALL_REFRESH").click();		
//             $('#SUBMIT').css('display','none');
//             $('#APPROVE').css('display','none');
//         });
//         quote_status_update();
//     } catch (e) {
//         console.log(e);
//     }
// }
//commented code(Approvals node functionality in Quotes explorer) - end
function quote_status_update() {
	setTimeout(function () {
		cpq.server.executeScript("SYALLTABOP", {
			'Primary_Data': quotenumber,
			'Primary_Data_rec': '',
			'TabNAME': 'Quotes',
			'ACTION': 'VIEW',
			'RELATED': ''
		}, function (dataset) {
			$("#BTN_MA_ALL_REFRESH").click();
		});
	}, 10);
}

function generateLineItems(ele) {
	localStorage.setItem("left_tree_refresh", "yes")
	localStorage.setItem("add_new_functionality", "TRUE")
	//localStorage.setItem("entitlement_save_flag",'False')
	cpq.server.executeScript("CQCRUDOPTN", {
		'Opertion': 'ADD',
		'ActionType': 'INSERT_LINE_ITEMS',
		'NodeType': 'QUOTE ITEMS MODEL'
	}, function (data) {
		//$("#BTN_MA_ALL_REFRESH").click();
		$("[id='qtn_save'] span").click();
		//CommonLeftView();
		var button_disp = localStorage.getItem("get_button_price");
		CurrentNodeId = node.nodeId
		Subbaner('Offerings', CurrentNodeId, 'SYOBJR-00009', 'SAQITM');
		$("#step1").removeClass("disabled").addClass("complete");
		$("#step1 .bar_number").css("display", "none");
		$("#step1 .bar_tick_img").css("display", "block");
		$("#step2").removeClass("disabled").addClass("active");
		//if (button_disp == "show_button"){$('#CALCULATE_QItems').css('display','block');}
		//localStorage.setItem("get_button_price", "");

		//$('#itemhide_generate').css('display','none');

	});
	if (ProductId == '273' || ProductId == '2240') {
		try {
			//entitlement_save_flag = localStorage.getItem("entitlement_save_flag");
			var button_disp = localStorage.getItem("get_button_price");
			//console.log('button_disp---1426--',button_disp)
			cpq.server.executeScript("CQCRUDOPTN", {
				'Opertion': 'GET',
				'ActionType': 'SHOW_PRICING_BENCHMARKING_NOTIFICATION',
				'NodeType': 'QUOTE LEVEL NOTIFICATION',

			}, function (data) {

				if (data != "") {

					if (data[0] != "" || data[1] != "" || data[2] != "") {
						$(".emp_notifiy").css('display', 'block');
						$("#PageAlert ").css('display', 'block');
						$("#alertnotify").html(data);
					}
					else {
						$(".emp_notifiy").css('display', 'none');
						$("#PageAlert ").css('display', 'none');
					}
				}
				else {
					$(".emp_notifiy").css('display', 'none');
					$("#PageAlert ").css('display', 'none');
				}

			});
		}
		catch { console.log('===error price bench mark notification') }
	}

}

// Entitlement View part 
function EntitlementView(CurrentRecordId, ObjName, subTabName, v1) {
	TreeParam = AllTreeParam['TreeParam']
	AllTreeParam = maintreeparamfunction(parseInt(CurrentNodeId), 0);
	AllTreeParams = JSON.stringify(AllTreeParam);
	if (subTabName == 'Equipment Entitlements' || (subTabName == 'Entitlements' && (TreeTopSuperParentParam == 'Product Offerings' || TreeTopSuperParentParam == 'Comprehensive Services' || TreeTopSuperParentParam == 'Complementary Services') && TreeParam != 'Add-On Products')) {
		CurrentRecordId = localStorage.getItem("CurrentRecordId")
	}
	//var CurrentRecordId = localStorage.getItem("CurrentRecordId");
	var EquipmentId = localStorage.getItem("EquipmentIdValue")
	var AssemblyId = localStorage.getItem("AssemblyIdValue")
	$('.CommonTreeDetail').css('display', 'block');
	localStorage.setItem('EntCurrentId', CurrentRecordId)
	getprevdatadict = localStorage.getItem("prventdict");
	if (subTabName == 'Equipment Entitlements' && (TreeSuperTopParentParam == 'Product Offerings' || TreeTopSuperParentParam == 'Add-On Products')) {
		v1 = ""
		if (CurrentTab == "Quote" || CurrentTab == "Quotes") {
			ObjName = 'SAQTSE';
		}
		else {
			ObjName = 'CTCTSE';
		}
	}
	if (TreeParentParam == "Quote Items") {
		CurrentRecordId = TreeParam.split(" -")[0]
	}
	edit_configuration_flag = localStorage.getItem("edit_configuration_flag")
	if (edit_configuration_flag == "TRUE") {
		RECORD_ID = localStorage.getItem("configurating_service")
		localStorage.setItem("edit_configuration_flag", "")
		localStorage.setItem("configurating_service", "")
	}
	else {
		RECORD_ID = CurrentRecordId
	}
	cpq.server.executeScript("CQENTLVIEW", { 'RECORD_ID': RECORD_ID, 'ObjectName': ObjName, 'alltreeparam': AllTreeParams, 'action': 'VIEW', 'DetailList': v1, 'SubtabName': subTabName, 'EquipmentId': EquipmentId, 'AssemblyId': AssemblyId, 'getprevdatadict': getprevdatadict, 'edit_configuration_flag': edit_configuration_flag }, function (dataset) {
		var [datas, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17, data18, data19, data20, data21, data22, data23, data24, data25, data26, data27, data28, data29, data30, data31, data32, data33, data34, data35, data36, data37, data38, data39] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[6], dataset[7], dataset[8], dataset[9], dataset[10], dataset[11], dataset[12], dataset[13], dataset[14], dataset[15], dataset[16], dataset[17], dataset[18], dataset[19], dataset[20], dataset[21], dataset[22], dataset[23], dataset[24], dataset[25], dataset[26], dataset[27], dataset[28], dataset[29], dataset[30], dataset[31], dataset[32], dataset[33], dataset[34], dataset[35], dataset[36], dataset[37], dataset[38], dataset[39]];
		localStorage.setItem('Lookupobjd', data5)
		if (document.getElementById("TREE_div")) {
			document.getElementById("TREE_div").innerHTML = datas;

			$("#div_CTR_related_list").css("display", "none");
			$("#TREE_div").css('display', 'block');

			// Enabling Add On Products in Entitlements subtab
			if (subTabName == 'Entitlements' && TreeParentParam == "Comprehensive Services") {
				$('div#COMMON_TABS').find("li a:contains('Add On Products')").parent().css("display", "block");
				$('#PageAlert').show();
			}
			document.getElementById('TREE_div').innerHTML = data7
			$('#TREE_div').prepend(datas);
			$('#Headerbnr').css('display', 'block');
			localStorage.setItem('EDITENT_SEC', '');
			localStorage.setItem("prvdatadict", JSON.stringify(data8));
			var columns = ['CALCULATION FACTOR', 'ENTITLEMENT PRICE IMPACT', 'ENTITLEMENT COST IMPACT'];

			$.each(data8, function (k, v) {
				pre_rec_id = undefined
				$.each(v, function (index2, value2) {
					ctid = 'sec_' + index2


					$('#' + index2).bootstrapTable({
						data: value2
					});
					//hiding column in entitlement view part starts....
					$.each(columns, function (index, column) {
						//$('#'+ index2).bootstrapTable('hideColumn', column);
						$('#' + index2 + " th[data-field='" + column + "']").hide();
						$("#" + index2 + " td:nth-last-child(1)").hide();
						$("#" + index2 + " td:nth-last-child(2)").hide();
						$("#" + index2 + " td:nth-last-child(3)").hide();

					});
					//hiding column in entitlement view part ends....

					//Hide the section , if the section does not nave attributes to show code starts....
					if (TabName != "Contracts") {
						if (data38.includes(ctid)) {

							$('#' + ctid).css('display', 'none');
							$('#' + index2).css('display', 'none');
						}
					}
					//Hide the section , if the section does not nave attributes to show code ends...
					if (value2 == '') {

						$('#' + index2).html('<div class="noRecDisp">No Records to Display</div>');
					}

					if (typeof (pre_rec_id) == 'undefined' || index2 != pre_rec_id) {
						$("#" + index2 + "  tbody tr").addClass('hovergreyent');
						$("#" + index2 + "  tbody tr td:nth-child(2)").css('text-align', 'left');
						$("#" + index2 + "  tbody tr td:nth-child(2)").each(function () { var ent_desc = $(this).text(); $(this).html(ent_desc); });
						$("#" + index2 + "  tbody tr td:nth-child(3)").each(function () { var ent_val = $(this).text(); $(this).html(ent_val); });
						$("#" + index2 + "  tbody tr td:nth-child(4)").each(function () { var data_typrval = $(this).text(); $(this).html(data_typrval); });
						$("#" + index2 + "  tbody tr td:nth-child(1)").each(function () { var ent_val_im = $(this).text(); $(this).html(ent_val_im); });
						$("#" + index2 + "  tbody tr td:nth-child(6)").each(function () { var factcurr = $(this).text(); $(this).html(factcurr); });
						$("#" + index2 + "  tbody tr td:nth-child(5)").each(function () { var ent_val_cf = $(this).text(); $(this).html(ent_val_cf); });
						$("#" + index2 + "  tbody tr td:nth-child(7)").each(function () { var ent_val_imp = $(this).text(); $(this).html(ent_val_imp); });
						$("#" + index2 + "  tbody tr td:nth-child(8)").each(function () { var ent_val_primp = $(this).text(); $(this).html(ent_val_primp); });
						$("#" + index2 + "  tbody tr td:nth-child(9)").each(function () { var ent_val_primp = $(this).text(); $(this).html(ent_val_primp); });
					}
					pre_rec_id = index2
					if (data15 === undefined || data15 == null) { data15 = "" }
					if (data16 === undefined || data16 == null) { data16 = "" }
					if (data17 === undefined || data17 == null) { data17 = "" }
					if (data18 === undefined || data18 == null) { data18 = "" }
					if (data19 === undefined || data19 == null) { data19 = "" }
					if (data20 === undefined || data20 == null) { data20 = "" }
					if (data21 === undefined || data21 == null) { data21 = "" }
					if (data23 === undefined || data23 == null) { data23 = "" }
					if (data24 === undefined || data24 == null) { data24 = "" }
					if (data22 === undefined || data22 == null) { data22 = "" }
					if (data26 === undefined || data26 == null) { data22 = "" }
					if (data27 === undefined || data27 == null) { data27 = "" }
					if (data28 === undefined || data28 == null) { data28 = "" }
					if (data29 === undefined || data29 == null) { data29 = "" }
					if (data30 === undefined || data30 == null) { data30 = "" }
					if (data31 === undefined || data31 == null) { data31 = "" }
					if (data32 === undefined || data32 == null) { data32 = "" }
					if (data33 === undefined || data33 == null) { data33 = "" }
					if (data34 === undefined || data34 == null) { data34 = "" }
					if (data35 === undefined || data35 == null) { data35 = "" }
					if (data36 === undefined || data36 == null) { data36 = "" }



				});

			});
			//A055S000P01-9499 hide entitlement attribute starts 
			/*var itementilementlevel1 = '#AGS_'+TreeParam+'_PQB_QTITST'
			var itementilementlevel2 = '#AGS_'+TreeParentParam+'_PQB_QTITST'
			var itementilementlevel3 = '#AGS_'+TreeSuperParentParam+'_PQB_QTITST'

			$(itementilementlevel1).closest('tr').css('display','none');
			$(itementilementlevel2).closest('tr').css('display','none');
			$(itementilementlevel3).closest('tr').css('display','none');*/
			//A055S000P01-9499 hide entitlement attribute ends
			// Checkbox construction starts ..
			if (data39 != "" && data39 != undefined) {
				arr_list = data39

				for (const [key, value] of Object.entries(arr_list)) {
					//console.log(key, value);
					if (value != "") {
						defaultText = value
					}
					else {
						defaultText = 'Select Below'
					}
					$("#" + key).CreateMultiCheckBox({ width: '230px', defaultText: defaultText, height: '250px', attr_id: key });
					$('#' + key).closest('td').attr('title', defaultText);
				};

			}
			// Checkbox construction ends ..
			//sections hide if ano
			data38.forEach(function (ele) {
				try {

					$('#sec_' + ele).css('display', 'none');
					$('#sc_' + ele).css('display', 'none');
					$('#' + ele).css('display', 'none');
					//$('#'+ele).selected();
				}
				catch {
					console.log("error")
				}
			});
			$.each(data11, function (index, value) {
				$("#" + value).closest('tr').css('display', 'none');
			});
			if (data13 != '' && data13 != null) {
				$.each(data13, function (index, value) {
					$('#' + value).css('color', '#0060B1');
				});
			}

			try {
				//console.log('2602--2795-----',eval(data9))
				eval(data9);
				eval(data37)
				if (subTabName != 'Assembly Entitlements') {
					if ($('#approve_status').text() == "APPROVALS") {
						eval(data9);
					}
					var getdataprevent = eval(data10)

				}
			} catch { console.log('error---') }
			//}
			//A055S000P01-8873 hide entitlement attribute 
			if (subTabName == 'Entitlements' && AllTreeParam['TreeParentLevel1'] == 'Z0091' && (AllTreeParam['TreeParam'] == 'PDC' || AllTreeParam['TreeParam'] == 'MPS')) {
				$('#AGS_Z0091_NET_PRMALB').closest('tr').css('display', 'none');
			}

			// FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
			popover()
			if (CurrentTab == "Quotes") {
				//var getopptype = $( "#QSTN_SYSEFL_QT_00723 option:selected" ).text();
				var getopptype = localStorage.getItem("getopptype");
			}
			else if (CurrentTab == "Contracts") {
				var getopptype = $("#QSTN_SYSEFL_QT_016912 option:selected").text();
			}



			if (getopptype == "ZTBC - TOOL BASED") {
				$('.CC119201-572D-41BB-8C53-5C063EEAAD4F').css('display', 'none');
				//$(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display','none');


			}
			//if (getopptype == "ZWK1 - SPARES")
			if (getopptype == "ZWK1") {
				$('.F5414216-018E-47EB-9778-53F0FD95D273').css('display', 'none');
				$(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display', 'block');
			}

		}
		onFieldChanges();
	});
}
//Quote Items Tool Idling Edit A055S000P01-10455
function isNumberKey(value, ele) {
	try {
		//console.log(value['key']);
		//var ent_base_target = ele.id
		var regex = /^[-+]?\d*.$/;
		// if (ent_base_target.includes('_KPI_SDUTBP')){
		// 	var regex = /^[-+]?\d*.$/;

		// }
		// else if(ent_base_target.includes('_KPI_SDUTTP')){
		// 	var regex = /^[-+]?\d*.$/;

		// }
		// else{
		// 	var regex = /^[-+]?\d*$/;
		// }
		//if (ele.id == 'AGS_Z0091_KPI_SDUTBP' || ele.id =='AGS_Z0091_KPI_SDUTTP'){
		//	var regex = /^[-+]?\d*.$/;
		//}
		//else{
		//	var regex = /^[-+]?\d*$/;
		//}

		if (regex.test(value['key'])) {
			if (value['key'] == '.') {

			}
			//console.log("true");
			return true;
		} else {
			//console.log("false");
			return false;
		}
	}
	catch {
		return true
	}
}


function QuoteItemsIdlingEdit() {
	option = $("#AGS_Z0091_KPI_PRPFGT").val();
	cpq.server.executeScript("CQQTEITEMS", {
		'SUBTAB': "Summary",
		'ACTION': "EDIT",
	}, function (dataset) {
		$('.quote_sec').html(dataset);
		$('html').css('cssText', 'overflow-y:hidden !important');
		$("#ctr_drop").css("display", "none");

	});
}
//Quote Items Tool Idling Save A055S000P01-10455
function QuoteItemsIdlingSave() {
	//option = $("#AGS_Z0091_KPI_PRPFGT").val();
	var values = {};
	$("select option:selected").each(function () {
		values[this.id] = this.text;
		//values.join(',');
	});
	IdleNoticeException = $("#Idle_Notice_Exception").val();
	if (IdleNoticeException != "") {
		values["Idle_Notice_Exception"] = IdleNoticeException;
	}
	IdleDurationException = $("#Idle_Duration_Exception").val();
	if (IdleDurationException != "") {
		values["Idle_Duration_Exception"] = IdleDurationException;
	}
	IdlingExceptionNotes = $("#Idling_Exception_Notes").val();
	if (IdleDurationException != "") {
		values["Idling_Exception_Notes"] = IdlingExceptionNotes;
	}
	//console.log("VALUES--->",values);
	QuoteItemsView();
	cpq.server.executeScript("CQQTEITEMS", {
		'SUBTAB': "Summary",
		'ACTION': "SAVE",
		'VALUES': values
	}, function (dataset) {

		//$('.quote_sec').html(dataset);
		$("#toast-title").remove();
		$("#toast_title").remove();
		$("#toast-container").remove();

	});
	$("#cust_fields_div").css("display", "block");
	$(".quote_summary_new").css("display", "none");
	$(".alert").css("display", "none");
	cpq.server.executeScript("CQQTEITEMS", {
		'SUBTAB': "Summary",
		'ACTION': "VIEW"
	}, function (dataset) {

		$('.quote_sec').html(dataset[0]);



		$("#toast-title").remove();
		$("#toast-container").remove();
		$("#toast_title").remove();
		$("#ctr_drop").css("display", "inline-block");
		$('#total_sales_price').html(dataset[1]);
		$('input#discount').val(dataset[2]);
		$('#total_excluding_amount').html(dataset[3]);
		$('#tax_vat').html(dataset[4]);
		$('#net_price').html(dataset[5]);
		$('#TOTAL_NET_VALUE').html(dataset[6]);
		$('#total_credit_amount').html(dataset[7]);
		$('#total_discount_amount').html(dataset[8]);
	});
	cpq.server.executeScript("CQQTEITEMS", {
		'SUBTAB': "Summary",
		'ACTION': "VIEW"
	}, function (dataset) {

		$('.quote_sec').html(dataset[0]);



		$("#toast-title").remove();
		$("#toast-container").remove();
		$("#toast_title").remove();
		$("#ctr_drop").css("display", "inline-block");
		$('#total_sales_price').html(dataset[1]);
		$('input#discount').val(dataset[2]);
		$('#total_excluding_amount').html(dataset[3]);
		$('#tax_vat').html(dataset[4]);
		$('#net_price').html(dataset[5]);
		$('#TOTAL_NET_VALUE').html(dataset[6]);
		$('#total_credit_amount').html(dataset[7]);
		$('#total_discount_amount').html(dataset[8]);
	});



}
function QuoteItemsNoticeOnChange() {
	IdleNotice = $("#Idle_Notice").val();
	if (IdleNotice.includes("30")) {
		$('tr:has(td:contains("Idle Notice Exception"))').remove();
	}
	//IdleDuration = $("#Idle_Duration").val();
	//IdlingException = $("#Idling_Exception").val();
	cpq.server.executeScript("CQQTEITEMS", {
		'SUBTAB': "Summary",
		'ACTION': "NOTICE ONCHANGE",
		'IDLENOTICE': IdleNotice
	}, function (dataset) {
		if ($("#notice_onchange").length == 0) {
			$('table#63FE9099-59CD-4CF2-BC6D-DD85CB96395B').find("[data-index='" + $('#Idle_Notice').closest('td').closest('tr').attr('data-index') + "']").after(dataset);
			$('html').css('cssText', 'overflow-y:hidden !important');
			//$("#dropdown").css("display","none");
		}

	});
}
function QuoteItemsDurationOnChange() {
	//IdleNotice = $("#Idle_Notice").val();
	IdleDuration = $("#Idle_Duration").val();
	if (IdleDuration.includes("28")) {
		$('tr:has(td:contains("Idle Duration Exception"))').remove();
	}
	//IdlingException = $("#Idling_Exception").val();
	cpq.server.executeScript("CQQTEITEMS", {
		'SUBTAB': "Summary",
		'ACTION': "DURATION ONCHANGE",
		'IDLEDURATION': IdleDuration
	}, function (dataset) {
		if ($("#duration_onchange").length == 0) {
			$('table#63FE9099-59CD-4CF2-BC6D-DD85CB96395B').find("[data-index='" + $('#Idle_Duration').closest('td').closest('tr').attr('data-index') + "']").after(dataset);
			$('html').css('cssText', 'overflow-y:hidden !important');
			//$("#dropdown").css("display","none");
		}
	});
}
function QuoteItemsExceptionOnChange() {
	//IdleNotice = $("#Idle_Notice").val();
	//IdleDuration = $("#Idle_Duration").val();
	IdlingException = $("#Idling_Exception").val();
	if (IdlingException.includes("No")) {
		$('tr:has(td:contains("Idling Exception Notes"))').remove();
	}
	cpq.server.executeScript("CQQTEITEMS", {
		'SUBTAB': "Summary",
		'ACTION': "EXCEPTION ONCHANGE",
		'IDLINGEXCEPTION': IdlingException
	}, function (dataset) {
		if ($("#exception_onchange").length == 0) {
			$('table#63FE9099-59CD-4CF2-BC6D-DD85CB96395B').find("[data-index='" + $('#Idling_Exception').closest('td').closest('tr').attr('data-index') + "']").after(dataset);
			$('html').css('cssText', 'overflow-y:hidden !important');
			//$("#dropdown").css("display","none");
		}
	});
}
function QuoteItemsColdOnChange() {
	//IdleNotice = $("#Idle_Notice").val();
	Cold = $("#Cold_Idle_Allowed").val();
	if (Cold.includes("No")) {
		$('tr:has(td:contains("Cold Idle Fee"))').remove();
	}
	//IdlingException = $("#Idling_Exception").val();
	cpq.server.executeScript("CQQTEITEMS", {
		'SUBTAB': "Summary",
		'ACTION': "COLD ONCHANGE",
		'COLD': Cold
	}, function (dataset) {
		if ($("cold_onchange").length == 0) {
			$('table#63FE9099-59CD-4CF2-BC6D-DD85CB96395B').find("[data-index='" + $('#Cold_Idle_Allowed').closest('td').closest('tr').attr('data-index') + "']").after(dataset);
			$('html').css('cssText', 'overflow-y:hidden !important');
			//$("#dropdown").css("display","none");
		}
	});
}
function QuoteItemsHotOnChange() {
	//IdleNotice = $("#Idle_Notice").val();
	Hot = $("#WarmHotIdleAllowed").val();
	if (Hot.includes("No")) {
		$('tr:has(td:contains("Warm / Hot Idle Fee"))').remove();
	}
	//IdlingException = $("#Idling_Exception").val();
	cpq.server.executeScript("CQQTEITEMS", {
		'SUBTAB': "Summary",
		'ACTION': "HOT ONCHANGE",
		'HOT': Hot
	}, function (dataset) {
		if ($("hot_onchange").length == 0) {
			$('table#63FE9099-59CD-4CF2-BC6D-DD85CB96395B').find("[data-index='" + $('#WarmHotIdleAllowed').closest('td').closest('tr').attr('data-index') + "']").after(dataset);
			$('html').css('cssText', 'overflow-y:hidden !important');
			//$("#dropdown").css("display","none");
		}
	});
}
function QuoteItemsView() {
	cpq.server.executeScript("CQQTEITEMS", {
		'SUBTAB': "Summary",
		'ACTION': "VIEW"
	}, function (dataset) {

		$('.quote_sec').html(dataset[0]);



		$("#toast-title").remove();
		$("#toast-container").remove();
		$("#toast_title").remove();
		$("#ctr_drop").css("display", "inline-block");
		$('#total_sales_price').html(dataset[1]);
		$('input#discount').val(dataset[2]);
		$('#total_excluding_amount').html(dataset[3]);
		$('#tax_vat').html(dataset[4]);
		$('#net_price').html(dataset[5]);
		$('#TOTAL_NET_VALUE').html(dataset[6]);
		$('#total_credit_amount').html(dataset[7]);
		$('#total_discount_amount').html(dataset[8]);
	});
}

function cbcEDIT(ele) {
	var sec = $(ele).attr('id');
	var secdynamic = 'clean_booking_checklist_' + sec
	localStorage.setItem('secdynamic', secdynamic)
	$('#ctr_drop').css('display', 'none');
	$("div#ctr_drop.cbc_ctr_drop").css('display', 'none');
	$('#cbc_savecancel').css('display', 'block');
	$(ele).closest('#ctr_drop').closest('.dyn_main_head').closest('#container').addClass('g4 pad-10 brdr except_sec');
	$('table#' + secdynamic + '').after('<div class="g4 collapse in except_sec removeHorLine iconhvr sec_edit_sty" id="cbc_savecancel"><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="cbcCancel(this)">CANCEL</button><button id="cbc_save_id" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="cbcSAVE(this)">SAVE</button></div>');
	$('#' + secdynamic + ' > tbody > tr').each(function () {
		$(this).find('td:nth-child(3) > input').css('z-index', 1);
		$(this).find('td:nth-child(4) > input').css('z-index', 1);
		$(this).find('td:nth-child(3) > input').removeAttr('disabled');
		$(this).find('td:nth-child(4) > input').removeAttr('disabled');
		$(this).find('td:nth-child(5) > textarea').removeAttr('disabled');
		$(this).find('td:nth-child(3)').css('background', 'lightyellow');
		$(this).find('td:nth-child(4)').css('background', 'lightyellow');
		$(this).find('td:nth-child(5)').css('background', 'lightyellow');
		$('table#' + secdynamic + ' tbody tr td:nth-child(5) .related_popup_css').css('background', 'lightyellow');
	});
}

function cbcCancel() {

	keyDataVal = localStorage.getItem('keyDataVal')
	quote_id = $(".segment_part_number_text").text()
	cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'CBC_VIEW', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal, 'AllTreeParam': AllTreeParam }, function (data0) {
		if (data0 != '') {
			$('.CommonTreeDetail').css('display', 'none');
			$('.container_banner_inner_sec').css("display", "none")
			$('#TREE_div').html(data0);
			$('#cbc_savecancel').css('display', 'none');
			$("#TREE_div").closest('.Related').css("display", "block");
			$('[data-toggle="popover"]').popover();
		}
	});

}
function cbcSAVE(ele) {
	secdynamic = localStorage.getItem('secdynamic')

	// To remove cloapse while sectional edit - Start
	//$(ele).closest('#ctr_drop').closest('.dyn_main_head').removeAttr('data-toggle');
	//$(ele).closest('#ctr_drop').closest('.dyn_main_head').removeAttr('data-target');
	// To remove cloapse while sectional edit - End
	localStorage.setItem('AddNew', 'false')
	var values = [];
	$('#' + secdynamic + ' > tbody > tr').each(function (index) {
		var obj = {};
		var CHECKLIST_ID = $(this).find('td:nth-child(1) > input').val();
		if (CHECKLIST_ID != '') {
			obj.CHECKLIST_ID = CHECKLIST_ID;
			obj.SERVICE_CONTRACT = $(this).find('td:nth-child(3) > input[type=checkbox]').is(":checked");
			obj.SPECIALIST_REVIEW = $(this).find('td:nth-child(4) > input[type=checkbox]').is(":checked");
			obj.COMMENT = $(this).find('td:nth-child(5) > textarea').val();
			values.push(obj);
		}
	});
	try {
		keyDataVal = localStorage.getItem('keyDataVal')
		quote_id = $(".segment_part_number_text").text()
		cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'CBC_EDIT', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal, 'VALUES': values }, function (data0) {
			cbcCancel();

		});
		primary_banner();

	}
	catch (e) {
		console.log(e);
	}
}

function cbc_popup_trigger() {
	keyDataVal = localStorage.getItem('keyDataVal')
	quote_id = $(".segment_part_number_text").text()
	que = $('.segment_revision_sale_id_text').text();
	cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'CBC_COUNT', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal }, function (data0) {

		if (data0 == '0' && que != 'CBC-CBC COMPLETED') {
			$('#trigger_cbc_btn').click();
		}
	});
}


function cbcpop_save(ele) {
	keyDataVal = localStorage.getItem('keyDataVal')
	quote_id = $(".segment_part_number_text").text()
	cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'CBC_SAVE', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal }, function (data0) {
		$('.segment_revision_sale_id_text').text('CBC-CBC COMPLETED');
		QuoteStatus();
		//dynamic_status();
		$('#Newrevision1').css('display', 'none')
		cbcCancel();
	});
	primary_banner();
}

function CreateSow(ele) {
	var quote_id = $('.segment_part_number_text').text();
    var rev_no = $('.segment_part_text').text();
	localStorage.setItem(quote_id+"_"+rev_no+"_create_sow_flag", 'True');
	$('#Newrevision1').css('display', 'none')
	$('#Completesowbtn').css('display', 'block')
	quote_id = $(".segment_part_number_text").text()
	quote_rev_id = $(".segment_part_text").text()

	cpq.server.executeScript("CQSTSVADTN", { 'QUOTE_ID': quote_id, 'REVISION_ID': quote_rev_id, 'STATUS': 'CREATE_SOW' }, function (dataset) {
		//primary_banner();
		dynamic_status();
	});
	cpq.server.executeScript("QTPOSTACRM", { 'QUOTE_ID': quote_id, 'REVISION_ID': quote_rev_id, 'Fun_type': 'CPQ_TO_CLM' }, function (dataset) {

	});
	$('#Completesowbtn').css('display', 'block')
}
function CompleteSow(ele) {
	var quote_id = $('.segment_part_number_text').text();
    var rev_no = $('.segment_part_text').text();
	localStorage.removeItem(quote_id+"_"+rev_no+"_create_sow_flag");
	quote_id = $(".segment_part_number_text").text();
	quote_rev_id = $(".segment_part_text").text()
	cpq.server.executeScript("CQSTSVADTN", { 'QUOTE_ID': quote_id, 'REVISION_ID': quote_rev_id, 'STATUS': 'SOW_ACCEPT' }, function (dataset) {
		//
	});
	localStorage.setItem('sow_status', "completed");
	dynamic_status();
	$('#Completesowbtn').css('display', 'block');
	$("#step1").removeClass("disabled active").addClass("complete");
	$("#step1 .bar_number").css("display", "none");
	$("#step1 .bar_tick_img").css("display", "block");
	$("#step2").removeClass("disabled active").addClass("complete");
	$("#step2 .bar_number").css("display", "none");
	$("#step2 .bar_tick_img").css("display", "block");
	$("#step3").removeClass("disabled active").addClass("complete");
	$("#step3 .bar_number").css("display", "none");
	$("#step3 .bar_tick_img").css("display", "block");
	$("#step4").removeClass("disabled active").addClass("complete");
	$("#step4 .bar_number").css("display", "none");
	$("#step4 .bar_tick_img").css("display", "block");
	//$("#step5").removeClass("disabled active").addClass("complete");
	//$("#step5 .bar_number").css("display","none");
	//$("#step5 .bar_tick_img").css("display","block");
	//$("#step6").removeClass("disabled").addClass("active");
	$("#step5").removeClass("disabled active").addClass("complete");
	$("#step5 .bar_number").css("display", "none");
	$("#step5 .bar_tick_img").css("display", "block");
	$("#step6").removeClass("disabled").addClass("active");
	$('div#seginnerbnr').children('button').css('display', 'none');
	$("#export-spare-parts-data-as-excel").show();
	$('div[id^=dyn] div#ctr_drop').css('display', 'none');
	if (TreeParam != "Quote Documents") {
		$("div#ctr_drop").css('display', 'none');
	}
	$("div#ctr_drop.cbc_ctr_drop").css('display', 'block');
	$('#recall_for_edit').hide();
	$('.segment_table').find('li').find('a:contains("EDIT")').remove();
	$('.segment_table').find('li').find('a:contains("DELETE")').remove();
	$('#Generate_Documents').show();
	$("#refreshdoc").show();
	$('.secondary_highlight_panel').find('button#Generate_Documents').css('display', 'block');
	$('#ADDNEW__SYOBJR_98869_SYOBJ_1176895').css('display', 'block');
	var act_tab = $('#COMMON_TABS ul li.active').text().trim();
	$('#upload_attachment').css('display', 'block');
	primary_banner();
	$('#Completesowbtn').css('display', 'none')
}


//CODE FOR REPLACE CONTACT IN CONTACTS TAB START AND ALSO CODE FOR REPLACE CONTRACT MANAGER IN SALES TEAM NODE.
function contactreplaceKeyHyperLink(value, row) {
	var equipmentRecordId = row.CONTACT_RECORD_ID
	var equipment_value = row.pop_val
	return '<a href="#" id=' + equipment_value + ' onclick="addcontactreplacement(this,\'' + equipment_value + '\')">' + value + '</a>'
}

function addcontactreplacement(ele, contactreplace_RecordId) {
	var cont_rec_id = localStorage.getItem("acct_rpl")
	if (TreeParam == "Sales Team") {
		try {
			cpq.server.executeScript("CQRPLACTCT", {
				'repalce_values': contactreplace_RecordId,
				'cont_rec_id': cont_rec_id,
				'table_name': "SAQDLT",
				'ActionType': "CONTRACT_MANAGER_REPLACE"
			}, function () {
				$('#cont_viewModalSection').css('display', 'none');
				loadRelatedList('SYOBJR-00643', 'div_CTR_related_list');
			});
		} catch (e) {
			console.log(e);
		}
	}
	else {
		try {
			cpq.server.executeScript("CQRPLACTCT", {
				'repalce_values': contactreplace_RecordId,
				'cont_rec_id': cont_rec_id,
				'table_name': "SACONT"
			}, function () {
				$('#cont_viewModalSection').css('display', 'none');
				loadRelatedList('SYOBJR-98871', RecName);
			});
		} catch (e) {
			console.log(e);
		}
	}
}

function dynamic_status(ele) {
	console.log(ele);
	$('.container_banner_inner_sec').css("display", "none");
	$("#cbcpopup").hide();
	$("#cbcpopup").css('display', 'none');
	var active_tab_set = $('ul#carttabs_head li.active a span').text().trim();
	que = $('.segment_revision_sale_id_text').text();
	var editbtn_disp = localStorage.getItem("dispRecall");
	que_expired = $(".quote_revision_expiration_text abbr input").val();
	if (que != "APPROVED") {
		localStorage.setItem('sow_status', 'not_completed')
	}
	if (que_expired == 'True') {
		$('div[id^=dyn] div#ctr_drop').css('display', 'none');
		$("div#ctr_drop").css('display', 'none');
		$("div#ctr_drop.cbc_ctr_drop").css('display', 'none');
	}
	CurrentTab = $("ul#carttabs_head li.active a span").text();
	var act_tab = $('#COMMON_TABS ul li.active').text().trim();
	if (localStorage.getItem('sow_status') == "completed") {
		//console.log("sow completed");
		CompleteSow();
	}
	else {

		if(que=="CFG-CONFIGURING"){
			quote_item_insert = "yes"
		}
		else{
			quote_item_insert = "no"
		}
		prog_bar = $(ele).text().trim();
		cpq.server.executeScript("CQSTSVADTN", { 'CurrentTab': CurrentTab, 'quote_item_insert': quote_item_insert, 'Text': prog_bar }, function (datasetres) {
			try {
				if (localStorage.getItem('edit_config') == "Yes") {
					var dataset = "CONFIGURE"
				}
				else {
					var dataset = datasetres[0];
				}
			}
			catch {
				var dataset = datasetres[0];
			}


			if (datasetres[1] != '') {
				$('.notificatsection').css('display','block');
					$('.cpq_notification_div').css('display','block');
					$('.cpq_cust_notify').css('display','block');
					$('.alert-warning').css('display','block');
					$('.cpq_cust_notify').html(datasetres[1]);
			}
			if (dataset != '') {
				//if (dataset[0] != ''){
				if (que == 'REJECTED' && editbtn_disp == 'True') {
					$('#recall_for_edit').show();
					$('div#seginnerbnr').children('button').css('display', 'none');
					$("#export-spare-parts-data-as-excel").show();
					$('div[id^=dyn] div#ctr_drop').css('display', 'none');
					$('.segment_table').find('li').find('a:contains("EDIT")').remove();
					$('.segment_table').find('li').find('a:contains("DELETE")').remove();
				}
				else if (que == 'WAITING FOR APPROVAL' || que == 'CONVERTED TO CONTRACT') {
					$('div#seginnerbnr').children('button').css('display', 'none');
					$("#export-spare-parts-data-as-excel").show();
					$('div[id^=dyn] div#ctr_drop').css('display', 'none');
					$('#recall_for_edit').hide();
					$('.segment_table').find('li').find('a:contains("EDIT")').remove();
					$('.segment_table').find('li').find('a:contains("DELETE")').remove();
				}
				else if (dataset == 'IN-COMPLETE') {
					//console.log('button hidden in quote items---',dataset[2])
					$('#CALCULATE_QItems').css('display', 'none');
					localStorage.setItem("get_button_price", "hide_button");
					$("#step1").removeClass("disabled").addClass("active");
				}
				else if (dataset == 'CONFIGURE') {
					localStorage.setItem("get_button_price", "show_button");
					$('#CALCULATE_QItems').css('display', 'block');
					//$("#step1").removeClass("disabled active").addClass("complete");
					//$("#step1 .bar_number").css("display","none");
					//$("#step1 .bar_tick_img").css("display","block");
					//$("#step2").removeClass("disabled").addClass("active");
					if(datasetres[1].includes('MISSING ATTRIBUTES FROM IBASE') && prog_bar == "COMPLETE STAGE"){
						$(".cpq_notification_div .cpq_cust_warning.alert-warning").css("display","block").parent().css("display","block").parent().prev().children("div").removeClass("collapsed");
						$("#notify").addClass("in");
						$("#notify").css("height","auto");
					}	
					$("#step1").removeClass("disabled").addClass("active");
					$("#step2").addClass("disabled").removeClass("active");
					//$("#step2").removeClass("disabled").removeClass("complete").addClass("disabled");
					//$("#step3").removeClass("disabled").removeClass("active").addClass("disabled");
					primary_banner();

				}
				else if (dataset == 'PRICING REVIEW') {
					localStorage.setItem("get_button_price", "show_button");
					$('#CALCULATE_QItems').css('display', 'block');
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					//$("#step2").removeClass("disabled active").addClass("complete");
					//$("#step2 .bar_number").css("display","none");
					//$("#step2 .bar_tick_img").css("display","block");
					//$("#step3").removeClass("disabled").addClass("active");		
					$("#step2").removeClass("disabled").addClass("active");
					primary_banner();
				}
				else if (dataset == 'PRICING') {
					localStorage.setItem("get_button_price", "show_button");
					$('#CALCULATE_QItems').css('display', 'block');
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					//$("#step3").removeClass("disabled active").addClass("complete");
					//$("#step3 .bar_number").css("display", "none");
					//$("#step3 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled").addClass("active");
					primary_banner();
				}
				else if (dataset == 'APPROVAL PENDING') {
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled").addClass("active");
					$("#export-spare-parts-data-as-excel").show();
				}
				else if (dataset == 'APPROVALS') {
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled").addClass("active");
					primary_banner();
					$("#export-spare-parts-data-as-excel").show();
				}
				else if (dataset == 'APR-APPROVALS') {
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled active").addClass("complete");
					$("#step4 .bar_number").css("display", "none");
					$("#step4 .bar_tick_img").css("display", "block");
					$("#step5").removeClass("disabled").addClass("active");
					if (TreeParam != "Revisions"){
						$('div#seginnerbnr').children('button').css('display', 'none');
						$('div.dyn_main_head > label > div > div#ctr_drop').css('display', 'none');
					}		
					primary_banner();
					$("#export-spare-parts-data-as-excel").show();
				}
				else if (dataset == 'QUOTE DOCUMENTS') {
					var getcreatesow = localStorage.getItem(quote_id+"_"+rev_no+"_create_sow_flag");
					var getquotetype = $('.segment_revision_trans_type_text').text()
					var getpoes = $(".segment_revision_poes_text > abbr > input").val()
					if (getcreatesow == "True" || getquotetype =="A-QUOTE" || getpoes =="True" || que =="APR-SUBMITTED TO CUSTOMER" || que =="OPD-CUSTOMER REJECTED" || que == "OPD-PREPARING QUOTE DOCUMENTS") {
					$('#Newrevision1').css('display','none')}
					else{$('#Newrevision1').css('display','block')}
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled active").addClass("complete");
					$("#step4 .bar_number").css("display", "none");
					$("#step4 .bar_tick_img").css("display", "block");
					//$("#step5").removeClass("disabled active").addClass("complete");
					//$("#step5 .bar_number").css("display","none");
					//$("#step5 .bar_tick_img").css("display","block");
					//$("#step6").removeClass("disabled").addClass("active");
					//$("#step5").removeClass("disabled active").addClass("complete");
					$("#step5").removeClass("disabled").addClass("active");
					$('div#seginnerbnr').children('button').css('display', 'none');
					$("#export-spare-parts-data-as-excel").show();
					$('div[id^=dyn] div#ctr_drop').css('display', 'none');
					if (TreeParam != "Quote Documents") {
						$("div#ctr_drop").css('display', 'none');
						$(".btn-group").css('display','none');
					}
					$("div#ctr_drop.cbc_ctr_drop").css('display', 'block');
					$('#recall_for_edit').hide();
					$('.segment_table').find('li').find('a:contains("EDIT")').remove();
					$('.segment_table').find('li').find('a:contains("DELETE")').remove();
					$('#Generate_Documents').show();
					$("#refreshdoc").show();
					$('.secondary_highlight_panel').find('button#Generate_Documents').css('display', 'block');
					$('#ADDNEW__SYOBJR_98869_SYOBJ_1176895').css('display', 'block');
					var act_tab = $('#COMMON_TABS ul li.active').text().trim();
					$('#upload_attachment').css('display', 'block');
					primary_banner();
				}
				else if (dataset == 'GENERATE SOW') {
					var getcreatesow = localStorage.getItem(quote_id+"_"+rev_no+"_create_sow_flag");
					var getquotetype = $('.segment_revision_trans_type_text').text()
					var getpoes = $(".segment_revision_poes_text > abbr > input").val()
					if (getcreatesow == "True" || getquotetype =="A-QUOTE" || getpoes =="True") {
					$('#Newrevision1').css('display','none')}
					else{$('#Newrevision1').css('display','block')}
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled active").addClass("complete");
					$("#step4 .bar_number").css("display", "none");
					$("#step4 .bar_tick_img").css("display", "block");
					//$("#step5").removeClass("disabled active").addClass("complete");
					//$("#step5 .bar_number").css("display","none");
					//$("#step5 .bar_tick_img").css("display","block");
					//$("#step6").removeClass("disabled").addClass("active");
					$("#step5").removeClass("disabled active").addClass("complete");
					$("#step5 .bar_number").css("display", "none");
					$("#step5 .bar_tick_img").css("display", "block");
					$("#step6").removeClass("disabled").addClass("active");
					$('div#seginnerbnr').children('button').css('display', 'none');
					$("#export-spare-parts-data-as-excel").show();
					// $('div[id^=dyn] div#ctr_drop').css('display', 'none');
					if (TreeParam != "Quote Documents" && TreeParam != "Quote Information") {
						$("div#ctr_drop").css('display', 'none');
					}
					$("div#ctr_drop.cbc_ctr_drop").css('display', 'block');
					$('#recall_for_edit').hide();
					$('.segment_table').find('li').find('a:contains("EDIT")').remove();
					$('.segment_table').find('li').find('a:contains("DELETE")').remove();
					$('#Generate_Documents').show();
					$("#refreshdoc").show();
					$('.secondary_highlight_panel').find('button#Generate_Documents').css('display', 'block');
					$('#ADDNEW__SYOBJR_98869_SYOBJ_1176895').css('display', 'block');
					var act_tab = $('#COMMON_TABS ul li.active').text().trim();
					$('#upload_attachment').css('display', 'block');
					primary_banner();
				}
				else if (dataset == 'LEGAL SOW') {
					var getcreatesow = localStorage.getItem(quote_id+"_"+rev_no+"_create_sow_flag");
					var getquotetype = $('.segment_revision_trans_type_text').text()
					var getpoes = $(".segment_revision_poes_text > abbr > input").val()
					if (getcreatesow == "True" || getquotetype =="A-QUOTE" || getpoes =="True") {
					$('#Newrevision1').css('display','none')
					}
					else{$('#Newrevision1').css('display','block')}
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled active").addClass("complete");
					$("#step4 .bar_number").css("display", "none");
					$("#step4 .bar_tick_img").css("display", "block");
					//$("#step5").removeClass("disabled active").addClass("complete");
					//$("#step5 .bar_number").css("display","none");
					//$("#step5 .bar_tick_img").css("display","block");
					//$("#step6").removeClass("disabled").addClass("active");
					$("#step5").removeClass("disabled active").addClass("complete");
					$("#step5 .bar_number").css("display", "none");
					$("#step5 .bar_tick_img").css("display", "block");
					$("#step6").removeClass("disabled").addClass("active");
					$('div#seginnerbnr').children('button').css('display', 'none');
					$('div[id^=dyn] div#ctr_drop').css('display', 'none');
					if (TreeParam != "Quote Documents") {
						$("div#ctr_drop").css('display', 'none');
					}
					$("div#ctr_drop.cbc_ctr_drop").css('display', 'block');
					$('#recall_for_edit').hide();
					$('.segment_table').find('li').find('a:contains("EDIT")').remove();
					$('.segment_table').find('li').find('a:contains("DELETE")').remove();
					$('#Generate_Documents').show();
					$("#refreshdoc").show();
					$('.secondary_highlight_panel').find('button#Generate_Documents').css('display', 'block');
					$('#ADDNEW__SYOBJR_98869_SYOBJ_1176895').css('display', 'block');
					$("#export-spare-parts-data-as-excel").show();
					var act_tab = $('#COMMON_TABS ul li.active').text().trim();
					$('#upload_attachment').css('display', 'block');
					primary_banner();
				}
				else if (dataset == 'LEGAL SOW ACCEPT') {
					var getcreatesow = localStorage.getItem(quote_id+"_"+rev_no+"_create_sow_flag");
					var getquotetype = $('.segment_revision_trans_type_text').text()
					var getpoes = $(".segment_revision_poes_text > abbr > input").val()
					if (getcreatesow == "True" || getquotetype =="A-QUOTE" || getpoes =="True") {
					$('#Newrevision1').css('display','none')
					}
					else{$('#Newrevision1').css('display','block')}
					$('#Newrevision1').hide();//Bug #323
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled active").addClass("complete");
					$("#step4 .bar_number").css("display", "none");
					$("#step4 .bar_tick_img").css("display", "block");
					$("#step5").removeClass("disabled active").addClass("complete");
					$("#step5 .bar_number").css("display", "none");
					$("#step5 .bar_tick_img").css("display", "block");
					//$("#step6").removeClass("disabled").addClass("active");
					$("#step6").removeClass("disabled active").addClass("complete");
					$("#step6 .bar_number").css("display", "none");
					$("#step6 .bar_tick_img").css("display", "block");
					$("#step7").removeClass("disabled").addClass("active");
					$('div#seginnerbnr').children('button').css('display', 'none');
					$("#export-spare-parts-data-as-excel").show();
					$('div[id^=dyn] div#ctr_drop').css('display', 'none');
					if (TreeParam != "Quote Documents") {
						$("div#ctr_drop").css('display', 'none');
					}
					$("div#ctr_drop.cbc_ctr_drop").css('display', 'block');
					$('#recall_for_edit').hide();
					$('.segment_table').find('li').find('a:contains("EDIT")').remove();
					$('.segment_table').find('li').find('a:contains("DELETE")').remove();
					$('#Generate_Documents').show();
					$("#refreshdoc").show();
					$('.secondary_highlight_panel').find('button#Generate_Documents').css('display', 'block');
					$('#ADDNEW__SYOBJR_98869_SYOBJ_1176895').css('display', 'block');
					var act_tab = $('#COMMON_TABS ul li.active').text().trim();
					$('#upload_attachment').css('display', 'block');
					$("#export-spare-parts-data-as-excel").show();
					primary_banner();
				}
				else if (dataset == 'COMPLETESOW') {
					$('#Newrevision1').hide();
					$('#Completesowbtn').css('display', 'block');
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled active").addClass("complete");
					$("#step4 .bar_number").css("display", "none");
					$("#step4 .bar_tick_img").css("display", "block");
					//$("#step5").removeClass("disabled active").addClass("complete");
					//$("#step5 .bar_number").css("display","none");
					//$("#step5 .bar_tick_img").css("display","block");
					//$("#step6").removeClass("disabled").addClass("active");
					$("#step5").removeClass("disabled active").addClass("complete");
					$("#step5 .bar_number").css("display", "none");
					$("#step5 .bar_tick_img").css("display", "block");
					$("#step6").removeClass("disabled").addClass("active");
					$('div#seginnerbnr').children('button').css('display', 'none');
					$('div[id^=dyn] div#ctr_drop').css('display', 'none');
					if (TreeParam != "Quote Documents") {
						$("div#ctr_drop").css('display', 'none');
					}
					$("div#ctr_drop.cbc_ctr_drop").css('display', 'block');
					$('#recall_for_edit').hide();
					$('.segment_table').find('li').find('a:contains("EDIT")').remove();
					$('.segment_table').find('li').find('a:contains("DELETE")').remove();
					$('#Generate_Documents').show();
					$("#refreshdoc").show();
					$('.secondary_highlight_panel').find('button#Generate_Documents').css('display', 'block');
					$('#ADDNEW__SYOBJR_98869_SYOBJ_1176895').css('display', 'block');
					var act_tab = $('#COMMON_TABS ul li.active').text().trim();
					$('#upload_attachment').css('display', 'block');
					$("#export-spare-parts-data-as-excel").show();
					primary_banner();
					var act_tab = $('#COMMON_TABS ul li.active').text().trim();
					if (act_tab == "Spare Parts") {
						$("div#ctr_drop").css('display', 'block');
					}

				}
				else if (dataset == 'CLEAN BOOKING CHECKLIST') {
					$('#Newrevision1').css('display','none');
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled active").addClass("complete");
					$("#step4 .bar_number").css("display", "none");
					$("#step4 .bar_tick_img").css("display", "block");
					$("#step5").removeClass("disabled active").addClass("complete");
					$("#step5 .bar_number").css("display", "none");
					$("#step5 .bar_tick_img").css("display", "block");
					$("#step5").removeClass("disabled active").addClass("complete");
					$("#step6 .bar_number").css("display", "none");
					$("#step6 .bar_tick_img").css("display", "block");
					$("#step6").removeClass("disabled").addClass("complete");
					$("#step7").removeClass("disabled").addClass("active");
					if (TreeParam != "Revisions"){
						$('.secondary_highlight_panel').find('button').css('display', 'none');
						$('div.dyn_main_head > label > div > div#ctr_drop').css('display', 'none');
					}
					primary_banner();
					$("#export-spare-parts-data-as-excel").show();
				}
				else if (dataset == 'CBC-COMPLETED') {
					$('#Newrevision1').css('display','none')
					$('#Newrevision1').css('display','none')
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled active").addClass("complete");
					$("#step4 .bar_number").css("display", "none");
					$("#step4 .bar_tick_img").css("display", "block");
					$("#step5").removeClass("disabled active").addClass("complete");
					$("#step5 .bar_number").css("display", "none");
					$("#step5 .bar_tick_img").css("display", "block");
					$("#step5").removeClass("disabled active").addClass("complete");
					$("#step6 .bar_number").css("display", "none");
					$("#step6 .bar_tick_img").css("display", "block");
					$("#step6").removeClass("disabled").addClass("complete");
					$("#step7 .bar_number").css("display", "none");
					$("#step7 .bar_tick_img").css("display", "block");
					$("#step7").removeClass("disabled").addClass("complete");
					$("#step8").removeClass("disabled").addClass("active");
					primary_banner();
					var act_tab = $('#COMMON_TABS ul li.active').text().trim();
					if (act_tab == "Spare Parts") {
						$("div#ctr_drop").css('display', 'block');
					}
					if(TreeParam!="Revisions"){
						$('.secondary_highlight_panel').find('button').css('display', 'none');
						$('div.dyn_main_head > label > div > div#ctr_drop').css('display', 'none');
					}
					$("#export-spare-parts-data-as-excel").show();
				}
				else if (dataset == 'APR-APPROVED') {
					$("#export-spare-parts-data-as-excel").show();
					var getcreatesow = localStorage.getItem(quote_id+"_"+rev_no+"_create_sow_flag");
					var getquotetype = $('.segment_revision_trans_type_text').text()
					var getpoes = $(".segment_revision_poes_text > abbr > input").val()
					if (getcreatesow == "True" || getquotetype =="A-QUOTE" || getpoes =="True") {
					$('#Newrevision1').css('display','none')}
					else{$('#Newrevision1').css('display','block')}
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled active").addClass("complete");
					$("#step4 .bar_number").css("display", "none");
					$("#step4 .bar_tick_img").css("display", "block");
					$("#step5").removeClass("disabled").addClass("active");
					primary_banner();

				}
				else if (dataset == 'BOOKEDCONTRACT') {
					$('#Newrevision1').css('display','none')
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled active").addClass("complete");
					$("#step4 .bar_number").css("display", "none");
					$("#step4 .bar_tick_img").css("display", "block");
					$("#step5").removeClass("disabled active").addClass("complete");
					$("#step5 .bar_number").css("display", "none");
					$("#step5 .bar_tick_img").css("display", "block");
					$("#step6").removeClass("disabled active").addClass("complete");
					$("#step6 .bar_number").css("display", "none");
					$("#step6 .bar_tick_img").css("display", "block");
					$("#step7").removeClass("disabled active").addClass("complete");
					$("#step7 .bar_number").css("display", "none");
					$("#step7 .bar_tick_img").css("display", "block");
					$("#step8").removeClass("disabled active").addClass("complete");
					$("#step8 .bar_number").css("display", "none");
					$("#step8 .bar_tick_img").css("display", "block");
					primary_banner();
					$('.secondary_highlight_panel').find('button').css('display', 'none');
					$('div.dyn_main_head > label > div > div#ctr_drop').css('display', 'none');
					$("#export-spare-parts-data-as-excel").show();

				}
				else if (dataset == 'BOOKED') {
					var getcreatesow = localStorage.getItem(quote_id+"_"+rev_no+"_create_sow_flag");
					var getquotetype = $('.segment_revision_trans_type_text').text()
					var getpoes = $(".segment_revision_poes_text > abbr > input").val()
					$('#Newrevision1').css('display','none')
					$('#Newrevision1').css('display','none');
					$("#step1").removeClass("disabled active").addClass("complete");
					$("#step1 .bar_number").css("display", "none");
					$("#step1 .bar_tick_img").css("display", "block");
					$("#step2").removeClass("disabled active").addClass("complete");
					$("#step2 .bar_number").css("display", "none");
					$("#step2 .bar_tick_img").css("display", "block");
					$("#step3").removeClass("disabled active").addClass("complete");
					$("#step3 .bar_number").css("display", "none");
					$("#step3 .bar_tick_img").css("display", "block");
					$("#step4").removeClass("disabled active").addClass("complete");
					$("#step4 .bar_number").css("display", "none");
					$("#step4 .bar_tick_img").css("display", "block");
					$("#step5").removeClass("disabled active").addClass("complete");
					$("#step5 .bar_number").css("display", "none");
					$("#step5 .bar_tick_img").css("display", "block");
					$("#step6").removeClass("disabled active").addClass("complete");
					$("#step6 .bar_number").css("display", "none");
					$("#step6 .bar_tick_img").css("display", "block");
					$("#step7").removeClass("disabled active").addClass("complete");
					$("#step7 .bar_number").css("display", "none");
					$("#step7 .bar_tick_img").css("display", "block");
					$("#step8").removeClass("disabled active").addClass("complete");
					$("#step8 .bar_number").css("display", "none");
					$("#step8 .bar_tick_img").css("display", "block");
					primary_banner();
					$('.secondary_highlight_panel').find('button').css('display', 'none');
					$('div.dyn_main_head > label > div > div#ctr_drop').css('display', 'none');
					$("#export-spare-parts-data-as-excel").show();
				}
				var act_tab = $('#COMMON_TABS ul li.active').text().trim();
				if (act_tab == "Document Generator") {
					$('#Generate_Documents').show();
					$('.secondary_highlight_panel').find('button#Generate_Documents').css('display', 'block');
				}
				else {
					$('#Generate_Documents').hide();
					$('.secondary_highlight_panel').find('button#Generate_Documents').css('display', 'none');
					if (dataset == 'APPROVALS') {
						if (act_tab == "Attachments") {
							$('.secondary_highlight_panel').find('button#upload_attachment').css('display', 'none');
						}
						if (act_tab == "Legal SoW") {
							$('div[id^=dyn] div#ctr_drop').css('display', 'none');
							$("#cbcpopup").hide();
							$("#cbcpopup").css('display', 'none');
						}

					}
				}
				if (datasetres[3] == 'True'){
					console.log("reloading")
					window.location.reload();
				}
			}
			//Commented the script call to restrict the sscm call multiple times by clicking complete stage button...
			//cpq.server.executeScript("CQTRSSCMPR", {			
			//}, function (dataset) {			

			//});
		});
	}
}

//CODE FOR REPLACE CONTACT IN CONTACTS TAB END

//Code only for cbc dynamic call instead of dynamic status bar function
function QuoteStatus() {
	$('.container_banner_inner_sec').css("display", "none");
	var active_tab_set = $('ul#carttabs_head li.active a span').text().trim();
	que = $('.segment_revision_sale_id_text').text();
	var editbtn_disp = localStorage.getItem("dispRecall");
	if (active_tab_set == 'Quotes') {
		setTimeout(function () {
			if (que == 'CBC-CBC COMPLETED') {
				$('#Newrevision1').css('display', 'none');
				$("#step1").removeClass("disabled active").addClass("complete");
				$("#step1 .bar_number").css("display", "none");
				$("#step1 .bar_tick_img").css("display", "block");
				$("#step2").removeClass("disabled active").addClass("complete");
				$("#step2 .bar_number").css("display", "none");
				$("#step2 .bar_tick_img").css("display", "block");
				$("#step3").removeClass("disabled active").addClass("complete");
				$("#step3 .bar_number").css("display", "none");
				$("#step3 .bar_tick_img").css("display", "block");
				$("#step4").removeClass("disabled active").addClass("complete");
				$("#step4 .bar_number").css("display", "none");
				$("#step4 .bar_tick_img").css("display", "block");
				$("#step5").removeClass("disabled active").addClass("complete");
				$("#step5 .bar_number").css("display", "none");
				$("#step5 .bar_tick_img").css("display", "block");
				$("#step6").removeClass("disabled active").addClass("complete");
				$("#step6 .bar_number").css("display", "none");
				$("#step6 .bar_tick_img").css("display", "block");
				//$("#step7").removeClass("disabled active").addClass("complete");
				$("#step7").removeClass("disabled").addClass("active");
				//$("#step7 .bar_number").css("display","none");
				//$("#step7 .bar_tick_img").css("display","block");
				//$("#step8").removeClass("disabled active").addClass("complete");
				//$("#step8 .bar_number").css("display","none");
				//$("#step8 .bar_tick_img").css("display","block");

			}
		}, 800);
	}
}


function total_credit(ele) {
	$("#trigger_tc_btn").click()
}
function attachfile() {
	try {
		cpq.server.executeScript("CQGNRTDOCS", {
			'ATTACH': "YES"
		}, function (dataset) {
			document.getElementById("VIEW_DIV_ID").innerHTML = dataset;
		});
	} catch (e) {
		console.log(e);
	}
}
function Saveattachfile() {
	if (TreeParam == "Quote Documents") {
		var doc = localStorage.getItem('file_name');
		localStorage.removeItem('file_name');
	}
	else {
		var doc = document.getElementById("my_file").files[0].name;
	}
	try {
		cpq.server.executeScript("CQGNRTDOCS", {
			'SAVE': "YES",
			'DOCUMENT_NAME': doc
		}, function (dataset) {
			if (dataset != "") {
				document.getElementById("VIEW_DIV_ID").innerHTML = dataset;
			}
			else {
				loadRelatedList('SYOBJR-98879', 'div_CTR_Attachments')
			}
		});
	} catch (e) {
		console.log(e);
	}
}
function OnChangeAttachFile() {
	//doc = document.getElementById("my_file").files[0].name;
	$(".upload_icon_file").change(function () {
		var i = document.getElementById("my_file").files[0].name;
		$("#input_file").val(i);
	});
}

function ItemsEdit() {
	var editline = "";
	cpq.server.executeScript("CQQTEITEMS", {'SUBTAB':'Items','ACTION':'Edit'}, function (dataset) {
	editline = dataset;
	var table_id = "SYOBJR_98872_66040985_5AE9_4DDC_BF34_8F50F1B1AA33"
	var fields = ["ESTVAL_INGL_CURR","NET_VALUE_INGL_CURR"];
	localStorage.setItem("InlineEdit","YES");
	if(localStorage.getItem('currentSubTab')=="Items" && TreeParam == "Quote Items"){
		table_id = "SYOBJR_98872_66040985_5AE9_4DDC_BF34_8F50F1B1AA33"
	}
	localStorage.setItem("table_id_RL_edit", table_id);
	var edit_index=[];
	fields.forEach(field => edit_index.push($("#" + table_id).find("[data-field=" + field + "]").index() + 1));
	localStorage.setItem("edit_index", edit_index);
	var reco_id = [];
	if (document.getElementById("RL_EDIT_DIV_ID")) {
		localStorage.setItem("saqico_title", fields);
		count = 1;
		reco_id = []
		$("#" + table_id + " > tbody > tr").each(function () {
			tr_number = $(this).closest('[data-index]').data('index');
			if(editline.includes(count.toString())){
				count = count + 1;
				reco_id.push($(this).find("td:nth-child(3)").text().trim());
				edit_index.forEach(function(index){
					$("#" + table_id + " tr[data-index='"+tr_number+"']").find("td:nth-child("+index+")").attr("contenteditable", "true");
					$("#" + table_id + " tr[data-index='"+tr_number+"']").find("td:nth-child("+index+")").addClass("light_yellow");
					if($("#" + table_id).find("td:nth-child("+index+") > input").attr('type')=="checkbox"){
						val = $(this).find("td:nth-child("+index+") > input").removeAttr('disabled');
					}
					else{
						val = $(this).find("td:nth-child("+index+")").text();
						$(this).find("td:nth-child("+index+") > a").remove();
						$(this).find("td:nth-child("+index+"))").text(val);	
					}
				});				
			}
			else{
				count = count + 1;
			}
		});
		localStorage.setItem('multiedit_save_date',reco_id);
		$("#seginnerbnr").find("button").map(function () { $(this).css('display', 'none'); });
		var buttonlen = $("#seginnerbnr").find("button#saveButton");
		if (buttonlen.length == 0) {
			$("#seginnerbnr").append('<button class="btnconfig" type="button" value="Save" onclick="ItemsMultiEdit()" id="saveButton">SAVE</button><button class="btnconfig" type="button" value="Cancel" id="cancelButton">CANCEL</button>');
			$('#cancelButton').attr('onclick',$('#COMMON_TABS ul li.active').attr('onclick'));
		} else {
			$("#cancelButton").css("display", "block");
			$("#saveButton").css("display", "block");
		}
	}
		});

}

function SplitEdit() {
	CurrentTab = $("ul#carttabs_head li.active a span").text();
	try {
		cpq.server.executeScript("CQSPLITQTE", { 'CurrentTab': CurrentTab }, function (dataset) {
			document.getElementById("VIEW_DIV_ID").innerHTML = dataset;
		});
		subTabDetails('Items', 'Related', 'SAQRIT', 'SYOBJR-00010');
	} catch (e) {
		console.log(e);
	}
}

// Download Spare Parts - Start
function exportSparePartsDataAsExcel(ele) {
	var tableArrayObj = $("#div_CTR_related_list").find(".fixed-table-body").find("table");
	if (tableArrayObj) {
		var relatedListAttributeName = (tableArrayObj[0].id).split("_").slice(0, 2).join("-");
		try {
			cpq.server.executeScript("CQTDUPDDWD", { 'RelatedListAttributeName': relatedListAttributeName, 'ActionType': 'Download' }, function (dataset) {
				requirejs(["xlsx", "FileSaver"], function (XLSX) {

					var createXLSLFormatObj = [];

					/* XLS Head Columns */
					var xlsHeader = dataset[0];

					/* XLS Rows Data */
					var xlsRows = dataset[1];

					createXLSLFormatObj.push(xlsHeader);
					createXLSLFormatObj.push(...xlsRows);
					/* $.each(xlsRows, function(index, value) {
						var innerRowData = [];					
						$.each(value, function(ind, val) {
							innerRowData.push(val);
						});
						createXLSLFormatObj.push(value);
					}); */

					var workBookObj = XLSX.utils.book_new();
					const currentDate = new Date();

					workBookObj.Props = {
						Title: "Applied Materials",
						Subject: "Spare Parts",
						Author: "BHC",
						CreatedDate: currentDate.toISOString().split('T')[0]
					};

					workBookObj.SheetNames.push("Spare Parts");
					var workSheetObj = XLSX.utils.aoa_to_sheet(createXLSLFormatObj);

					// Set column width based on column string length - START
					let objectMaxLength = []

					createXLSLFormatObj.map(arr => {
						Object.keys(arr).map(key => {
							let value = arr[key] === null ? '' : arr[key]

							if (typeof value === 'number') {
								return objectMaxLength[key] = 10
							}

							objectMaxLength[key] = objectMaxLength[key] >= value.length ? objectMaxLength[key] : value.length
						})
					})

					let worksheetCols = objectMaxLength.map(width => {
						return {
							width
						}
					})

					workSheetObj["!cols"] = worksheetCols;
					// Set column width based on column string length - End
					workBookObj.Sheets["Spare Parts"] = workSheetObj;

					var wbout = XLSX.write(workBookObj, { bookType: 'xlsx', type: 'binary' });
					function s2ab(s) {
						var buf = new ArrayBuffer(s.length);
						var view = new Uint8Array(buf);
						for (var i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xFF;
						return buf;

					}
					var quoteId = $(".segment_part_number_text").text();
					saveAs(new Blob([s2ab(wbout)], { type: "application/octet-stream" }), 'AppliedMaterialsSpareParts-' + quoteId + '.xlsx');

				})
			});
		} catch (e) {
			console.log(e);
		}

	}

	/* $('#'+ele.id).bootstrapTable('refreshOptions',{
	exportDataType: 'all'
	});
	var tableArrayObj = $("#div_CTR_related_list").find(".fixed-table-body").find("table");
	if (tableArrayObj) {
		//console.log("======================");
		var quoteId = $(".segment_part_number_text").text();
		var $table = $('#'+tableArrayObj[0].id);
		$table.tableExport({
			type: 'excel',
			escape: false,
			exportDataType: 'all',
			refreshOptions: { exportDataType: 'all'},
			exportOptions: {
			ignoreColumn: [0], // Ignore index arrays for some columns
			fileName: "AMATSpareParts-"+quoteId,
			},
		});
	} */
}
// Download Spare Parts - End

// Upload Spare Parts From Excel - Start
var process_wb = (function () {
	var to_json = function to_json(workbook, XLSX) {
		var result = {};
		workbook.SheetNames.forEach(function (sheetName) {
			var roa = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName], { header: 1, defval: null });
			if (roa.length) result[sheetName] = roa;
		});
		//return JSON.stringify(result, 2, 2);
		return result;
	};

	return function process_wb(wb, XLSX) {
		var output = to_json(wb, XLSX);
		//console.log("data ==> ", output);		
		var tableArrayObj = $("#div_CTR_related_list").find(".fixed-table-body").find("table");
		cpq.server.executeScript("CQTDUPDDWD", { 'RelatedListAttributeName': 'SYOBJR-00005', 'ActionType': 'Upload', 'UploadData': output }, function (dataset) {
		loadRelatedList('SYOBJR-00005', "div_CTR_related_list");
		$('.notify_info_top_cls').html(dataset[1]);
		$('.notify_info_top_cls').show();
			});
	};
})();

var do_file = (function () {
	return function do_file(files, XLSX) {
		var f = files[0];
		var reader = new FileReader();
		reader.onload = function (e) {
			var data = e.target.result;
			data = new Uint8Array(data);
			process_wb(XLSX.read(data, { type: 'array' }), XLSX);
		};
		reader.readAsArrayBuffer(f);
	};
})();

function bulkUploadSave() {
	requirejs(["xlsx", "FileSaver"], function (XLSX) {
		var xlf = document.getElementById('file-input');
		if (xlf) {
			do_file(xlf.files, XLSX)
		}
	});
}
// Upload Spare Parts From Excel - Start

function credit_button_enable() {
	check_box_status = $('.custom').is(':checked');
	if (check_box_status == true) {
		$("#edit_credits_button").show();
	}
	else {
		$("#edit_credits_button").hide();
	}
}
//SAQICO EDIT GRID
function annualized_editable() {
	var edit_mode = $("#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F input").hasClass("light_yellow");
	if (edit_mode == false) {
		var btnFlag = false;
		$('#annualizedSaveButton').css('display', 'none');
		$('#annualizedcancelButton').css('display', 'none');
		var get_pick_annualitems = $("#anual_grid_picklist").val();

		if (get_pick_annualitems == 'Contract Information') {
			edit_list = [];// Should be in the order in the grid
		}
		else if (get_pick_annualitems == 'Object Information') {
			edit_list = []
		}
		else if (get_pick_annualitems == 'Pricing Review - Manual Information') {
			$('#ann_edit').css('display', 'none');
			lines = []
			$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F > tbody > tr').each(function () {

				lines.push($(this).find('td:nth-child(4)').text())
			})

			cpq.server.executeScript("CQANULEDIT", { 'ACTION': 'CAT4_ENTITLMENT', 'values': lines }, function (dataset) {
				var converted_data = dataset.replace(/'/g, '"');
				var obj_dataset = JSON.parse(converted_data);
				for (k in obj_dataset) {
					console.log(k + ' is ' + obj_dataset[k])
					$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F tbody tr').each(function() {
						if (k == $(this).find("td:nth-child(4) abbr").html()){
							va = obj_dataset[k]
							for (index = 0; index < va.length; index++) {
								var index_1 = $("#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F  > thead > tr:nth-child(1)").find("[data-field='" + va[index] + "']").index() + 1;
								var edit_ele = $(this).find("td:nth-child(" + index_1 + ")");
								var field_val = $(edit_ele).text();
								$(edit_ele).html('<input type="text" class="light_yellow" value = "' + field_val + '" onchange="annualized_fields_onchange(this)">');
								$(edit_ele).addClass('light_yellow');
							}
						}
					})
					
					
					
				}
				var a = obj_dataset;
				for (var key in a){
					if(a[key].length>0){
						btnFlag = true;
						break;
					}
				}
				if(btnFlag){
					$("#seginnerbnr").append("<button class='btnconfig' onclick='annualizedCancel();' type='button' value='Cancel' id='annualizedcancelButton'>CANCEL</button><button class='btnconfig' type='button' value='Save' onclick='annualizedSave()' id='annualizedSaveButton'>SAVE</button>");
				}
			});
			//$('#annualizedSaveButton').css('display', 'none'); 
			//$('#annualizedcancelButton').css('display', 'none');
			//$('.btnconfig').css('display', 'none');
			
			
		}
		else if (get_pick_annualitems == 'Pricing - Summary Information') {
			$('#ann_edit').css('display', 'none');
			lines_summary = []
			$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F > tbody > tr').each(function () {

				lines_summary.push($(this).find('td:nth-child(4)').text())
			})

			cpq.server.executeScript("CQANULEDIT", { 'ACTION': 'PRICING_SUMMARY', 'values': lines_summary }, function (dataset) {

				var converted_data = dataset.replace(/'/g, '"');
				var obj_dataset = JSON.parse(converted_data);
				for (k in obj_dataset) {
					console.log(k + ' is ' + obj_dataset[k])
					$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F tbody tr').each(function() {
						if (k == $(this).find("td:nth-child(4) abbr").html()){
							va = obj_dataset[k]
							//btnFlag = (va.length > 0 && btnFlag == false) ? true : btnFlag
							for (index = 0; index < va.length; index++) {
								var index_1 = $("#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F  > thead > tr:nth-child(1)").find("[data-field='" + va[index] + "']").index() + 1;
								var edit_ele = $(this).find("td:nth-child(" + index_1 + ")");
								var field_val = $(edit_ele).text();
								$(edit_ele).html('<input type="text" class="light_yellow" value = "' + field_val + '" onchange="annualized_fields_onchange(this)">');
								$(edit_ele).addClass('light_yellow');
							}
						}
					})					
				}
				var a = obj_dataset;
				for (var key in a){
					if(a[key].length>0){
						btnFlag = true;
						break;
					}
				}
				if(btnFlag){
					$("#seginnerbnr").append("<button class='btnconfig' onclick='annualizedCancel();' type='button' value='Cancel' id='annualizedcancelButton'>CANCEL</button><button class='btnconfig' type='button' value='Save' onclick='annualizedSave()' id='annualizedSaveButton'>SAVE</button>");
				}
			});
			//if (btnFlag) {
			//	$('#annualizedSaveButton').css('display', 'none');
			//	$('#annualizedcancelButton').css('display', 'none');
			//	$('.btnconfig').css('display', 'none');
			//	$("#seginnerbnr").append("<button class='btnconfig' onclick='annualizedCancel();' type='button' value='Cancel' id='annualizedcancelButton'>CANCEL</button><button class='btnconfig' type='button' value='Save' onclick='annualizedSave()' id='annualizedSaveButton'>SAVE</button>");
			//}
		}
	}
}


function annualized_fields_onchange(ele) {
	var values = []
	
	var index_val = $(ele).parent().index();
	var input_value = $(ele).val().replace(/,/g, '').split(' ')[0];
	var input_value_final = input_value.replace("%", "")
	var lineid = $(ele).closest('tr').find('td:nth-child(4) abbr').attr('id');
	var apiname = $(ele).closest('table').find("thead > tr > th:nth-child(" + ((index_val) + 1) + ")").attr('data-field');

	if (localStorage.getItem('Annualized_Values') != '' && localStorage.getItem('Annualized_Values') != null && localStorage.getItem('Annualized_Values') != undefined) {
		var existing_array_string = localStorage.getItem('Annualized_Values');
		var existing_array = JSON.parse(existing_array_string)
		for(i=0; i < existing_array.length; i++){
			if (existing_array_string.includes(lineid)){
			if ((Object.keys(existing_array[i])) == lineid) {
				existing_array[i][lineid][apiname] = input_value_final;
				break;
			}}
			else {
				var updated_values = {}
				updated_values[lineid] = {};
				updated_values[lineid][apiname] = input_value_final;
				existing_array.push(updated_values)
				break;
			}
		}
	
		/*existing_array.forEach(element => {
			if (existing_array_string.includes(lineid)){
			if ((Object.keys(element)) == lineid) {
				element[lineid][apiname] = input_value;
			}
		}
			else {
				var updated_values = {}
				updated_values[lineid] = {};
				updated_values[lineid][apiname] = input_value;
				existing_array.push(updated_values)
			}
		})*/
		//existing_array.push(values);
		localStorage.setItem('Annualized_Values', JSON.stringify(existing_array));
	}
	else {
		var updated_values = {}
		updated_values[lineid] = {};
		updated_values[lineid][apiname] = input_value_final;
		values.push(updated_values);
		//annualitem_array.push(values);
		localStorage.setItem('Annualized_Values', JSON.stringify(values));
	}
}



function annualizedSave() {
	var Records = localStorage.getItem('Annualized_Values');
	cpq.server.executeScript("CQUPPRWLFD", { 'Records': Records }, function (data0) {
		localStorage.setItem('Annualized_Values', '');
		annualizedCancel();
		subTabDetails('Annualized Items', 'Related', 'SAQITM', 'SYOBJR-00010');
	});

}



function annualizedCancel() {
	$('#annualizedSaveButton').css('display', 'none');
	$('#annualizedcancelButton').css('display', 'none');
	loadRelatedList('SYOBJR-00009', "div_CTR_related_list");
	subTabDetails('Annualized Items', 'Related', 'SAQITM', 'SYOBJR-00010');
}


//Added the below functions for sending fab , sending equipment , receiving fab and receiving equipment add new popups ...

function addSendingFabFtsLink(value, row) {
	var fabRecordId = row.FAB_LOCATION_RECORD_ID
	var fab_value = row.pop_val
	return '<a href="#" id=' + fab_value + ' onclick="singleAddSendingFab(this,\'' + fabRecordId + '\')">' + value + '</a>'
}

function singleAddSendingFab(ele, fabRecordId) {
	subtab_name = $('#COMMON_TABS ul li.active').text().trim();
	localStorage.setItem("add_new_functionality", "TRUE")
	var A_Keys = [];
	var A_Values = [];
	$('#add_fablocation_fts .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#add_fablocation_fts .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOFTS", {
			'subtab_name': subtab_name,
			'NodeType': 'ADD SENDING FAB',
			'Values': [fabRecordId],
			'AllValues': false,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList('SYOBJR-00032', 'div_CTR_Sending_Fab_Locations');
		});
	} catch (e) {
		console.log(e);
	}
}

function add_sending_fab_fts(ele) {
	subtab_name = $('#COMMON_TABS ul li.active').text().trim();
	localStorage.setItem("add_new_functionality", "TRUE")
	var selectedSendingFab = [];
	var selectAll = false;
	$('#add_fablocation_fts').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedSendingFab.push(sel_val);
		}
	});
	var A_Keys = [];
	var A_Values = [];
	$('#add_fablocation_fts .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#add_fablocation_fts .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOFTS", {
			'subtab_name': subtab_name,
			'NodeType': 'ADD SENDING FAB',
			'Values': selectedSendingFab,
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList('SYOBJR-00032', 'div_CTR_related_list');
			//eval(subtab_name)
			//CommonLeftView();
		});
	} catch (e) {
		console.log(e);
	}
}



function add_sending_equipment(ele) {
	subtab_name = $('#COMMON_TABS ul li.active').text().trim();
	localStorage.setItem("add_new_functionality", "TRUE")
	var selectedSendingEquipment = [];
	var selectAll = false;
	$('#fts_equipments_addnew').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedSendingEquipment.push(sel_val);
		}
	});
	var A_Keys = [];
	var A_Values = [];
	$('#fts_equipments_addnew .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#fts_equipments_addnew .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOFTS", {
			'subtab_name': subtab_name,
			'NodeType': 'ADD SENDING EQUIPMENT',
			'Values': selectedSendingEquipment,
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList('SYOBJR-00033', 'div_CTR_related_list');
			//eval(subtab_name)
			//CommonLeftView();
		});
	} catch (e) {
		console.log(e);
	}
}

function add_receving_fab(ele) {
	subtab_name = $('#COMMON_TABS ul li.active').text().trim();
	localStorage.setItem("add_new_functionality", "TRUE")
	var selectedReceivingFab = [];
	var selectAll = false;
	$('#fablocation_addnew').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedReceivingFab.push(sel_val);
		}
	});
	var A_Keys = [];
	var A_Values = [];
	$('#fablocation_addnew .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#fablocation_addnew .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOFTS", {
			'subtab_name': subtab_name,
			'NodeType': 'ADD RECEIVING FAB',
			'Values': selectedReceivingFab,
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			// loadRelatedList('SYOBJR-00038','div_CTR_related_list');
			//eval(subtab_name)
			CommonLeftView();
		});
	} catch (e) {
		console.log(e);
	}
}

function add_receving_equipment(ele) {
	subtab_name = $('#COMMON_TABS ul li.active').text().trim();
	localStorage.setItem("add_new_functionality", "TRUE")
	var selectedReceivingEquipment = [];
	var selectAll = false;
	$('#add_receiving_equipment').find('[type="checkbox"]:checked').map(function () {
		if ($(this).attr('name') == 'btSelectAll') {
			selectAll = true;
		}
		var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
		if (sel_val != '') {
			selectedReceivingEquipment.push(sel_val);
		}
	});
	var A_Keys = [];
	var A_Values = [];
	$('#add_receiving_equipment .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#add_receiving_equipment .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOFTS", {
			'subtab_name': subtab_name,
			'NodeType': 'ADD RECEIVING EQUIPMENT',
			'Values': selectedReceivingEquipment,
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			CommonLeftView()
		});
	} catch (e) {
		console.log(e);
	}
}

function addSendingEquipFtsLink(value, row) {
	var fabRecordId = row.EQUIPMENT_RECORD_ID
	var fab_value = row.pop_val
	return '<a href="#" id=' + fab_value + ' onclick="singleAddSendingEquipment(this,\'' + fabRecordId + '\')">' + value + '</a>'
}

function singleAddSendingEquipment(ele, selectedSendingEquipment) {
	subtab_name = $('#COMMON_TABS ul li.active').text().trim();
	localStorage.setItem("add_new_functionality", "TRUE")
	var selectAll = false;
	var A_Keys = [];
	var A_Values = [];
	$('#fts_equipments_addnew .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#fts_equipments_addnew .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOFTS", {
			'subtab_name': subtab_name,
			'NodeType': 'ADD SENDING EQUIPMENT',
			'Values': [selectedSendingEquipment],
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			loadRelatedList('SYOBJR-00033', 'div_CTR_Sending_Equipment');
		});
	} catch (e) {
		console.log(e);
	}
}

function addReceivingFabFtsLink(value, row) {
	var fabRecordId = row.FAB_LOCATION_RECORD_ID
	var fab_value = row.pop_val
	return '<a href="#" id=' + fab_value + ' onclick="singleAddReceivingFab(this,\'' + fabRecordId + '\')">' + value + '</a>'
}

function singleAddReceivingFab(ele, selectedReceivingFab) {
	subtab_name = $('#COMMON_TABS ul li.active').text().trim();
	localStorage.setItem("add_new_functionality", "TRUE")
	var selectAll = false;
	var A_Keys = [];
	var A_Values = [];
	$('#add_receiving_fab .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#add_receiving_fab .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOFTS", {
			'subtab_name': subtab_name,
			'NodeType': 'ADD RECEIVING FAB',
			'Values': [selectedReceivingFab],
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			// loadRelatedList('SYOBJR-00038','div_CTR_Fab_Locations');
			CommonLeftView();
		});
	} catch (e) {
		console.log(e);
	}
}

function addReceivingEquipFtsLink(value, row) {
	var equipmentRecordId = row.QUOTE_REV_SENDING_ACC_FAB_EQUIPMENT_RECORD_ID
	var equipmentValue = row.pop_val
	return '<a href="#" id=' + equipmentValue + ' onclick="singleAddReceivingEquipment(this,\'' + equipmentRecordId + '\')">' + value + '</a>'
}

function singleAddReceivingEquipment(ele, selectedReceivingEquipment) {
	subtab_name = $('#COMMON_TABS ul li.active').text().trim();
	localStorage.setItem("add_new_functionality", "TRUE")
	var selectAll = false;
	var A_Keys = [];
	var A_Values = [];
	$('#add_receiving_equipment .filter-control').each(function () {
		values = this.firstElementChild.className;
		if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
			x = values.split(' ')[1];
			y = x.split("-").slice(-1)[0];
			xyz = $('#add_receiving_equipment .' + x).val();
			if ($.inArray(y, A_Keys) === -1) {
				A_Keys.push(y);
				A_Values.push(xyz)
			};
		}
	});
	try {
		cpq.server.executeScript("CQCRUDOFTS", {
			'subtab_name': subtab_name,
			'NodeType': 'ADD RECEIVING EQUIPMENT',
			'Values': [selectedReceivingEquipment],
			'AllValues': selectAll,
			'A_Keys': A_Keys,
			'A_Values': A_Values
		}, function () {
			$('#cont_viewModalSection').css('display', 'none');
			CommonLeftView()
		});
	} catch (e) {
		console.log(e);
	}
}

// function edit_configuration(ele){
// 	var table_id = $(ele).closest('table').attr('id');
// 	node_text = $(ele).closest('tr').find('td:nth-child(5)').text();
// 	$('ul.list-group li.list-group-item.node-commontreeview').each(function (index) {
// 		var nodeText = $(this).text();
// 		if(nodeText == "Product Offerings" ){
// 			x = $(this).attr('data-nodeid');
// 		}
// 		});
// 	node = $('#commontreeview').treeview('getNode', parseInt(x));

// 	var childrenNodes = _getChildren(node);
// 	localStorage.setItem("edit_config",'Yes')
// 	try {
// 		cpq.server.executeScript("CQSTATUSBR", {
// 			'edit_config' : 'True'
// 		}, function () {
// 			console.log("edit config")
// 		});
// 	} catch (e) {
// 		console.log(e);
// 	}
// 	try{
// 			cpq.server.executeScript("CQCRUDOPTN", {
// 			           'Opertion': 'GET',
// 						'ActionType': 'SHOW_PRICING_BENCHMARKING_NOTIFICATION',
// 						'NodeType': 'QUOTE LEVEL NOTIFICATION'
// 					},function (data) {
// 				if (data != ""){

// 				 if (data[0] != "" || data[1] != "" ){

// 				   $(".emp_notifiy").css('display','block');
// 				   $("#PageAlert ").css('display','block');
// 				$("#alertnotify").html(data);
// 				 }
// 				}

// 			});
// 		}
// 		catch{console.log('===error edit config notification')}
// 	$(childrenNodes).each(function (ele) {
// 		j = $('#lefttreepan #commontreeview').treeview('getNode', [ this.nodeId, { silent: true } ]);
// 		n_text = j.text
// 		i = j.nodeId
// 		CurrentNodeId = i
// 		node = $('#commontreeview').treeview('getNode', parseInt(CurrentNodeId));
// 		var childrenNodes = _getChildren(node);
// 		$(childrenNodes).each(function (ele) {
// 			j1 = $('#lefttreepan #commontreeview').treeview('getNode', [ this.nodeId, { silent: true } ]);
// 			n_text = j1.text
// 			if (n_text.includes(node_text)){
// 				ii = j1.nodeId
// 				CommonRightView(ii)

// 				// $('ul.list-group li.list-group-item.node-commontreeview').each(function (index) {
// 				// 	var nodeText = $(this).text();
// 				// 	if(nodeText == node_text ){


// 				// 		$(this).trigger('click');
// 				// 	}
// 				// 	});

// 				setTimeout(function () {
// 					if (AllTreeParam['TreeParentLevel2'] == 'Comprehensive Services' || AllTreeParam['TreeParentLevel2'] == 'Complementary Products') {
// 						$('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "block");
// 						$('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
// 						$('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
// 						$('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "block");
// 						$('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
// 						$('div#COMMON_TABS').find("li a:contains('Equipment')").parent().removeClass('active');
// 						$('div#COMMON_TABS').find("li a:contains('Events')").parent().removeClass('active');
// 						$('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().addClass('active');
// 						localStorage.setItem("edit_configuration_flag","TRUE")
// 						localStorage.setItem("configurating_service",node_text)
// 						$(".Quotes"+node_text+"Entitlements").click();
// 					}
// 				}, 3000);
// 				console.log("coming inside Z0091")
// 			}
// 			// CommonRightView(ii)
// 		});
// 	});
// }

function complete_stage(ele) {
	try {
		cpq.server.executeScript("CQCMPSTGER", {
			'complete_stage': 'True'
		}, function (dataset) {
			console.log("complete Stage error")
		});
	} catch (e) {
		console.log(e);
	}
	
	try {
		cpq.server.executeScript("CQCRUDOPTN", {
			'Opertion': 'GET',
			'ActionType': 'SHOW_PRICING_BENCHMARKING_NOTIFICATION',
			'NodeType': 'QUOTE LEVEL NOTIFICATION'
		}, function (data) {
			if (data != "") {

				if (data[0] != "" || data[1] != "") {

					$(".emp_notifiy").css('display', 'block');
					$("#PageAlert ").css('display', 'block');
					$("#alertnotify").html(data);
				}
			}

		});
	}
	catch { console.log('===error edit config notification') }
	localStorage.setItem('edit_config', 'No')
	dynamic_status(ele)
	$("#PageAlert").css('display', 'none')
	localStorage.setItem("ApprovalCompleteStage","yes");
	que = $('.segment_revision_sale_id_text').text();
	CurrentTab = $("ul#carttabs_head li.active a span").text();
	var act_tab = $('#COMMON_TABS ul li.active').text().trim();
	var current_trigger_tab = localStorage.getItem('currentSubTabtriggerpopup')
	if (act_tab == 'Clean Booking Checklist' && CurrentTab == 'Quotes'&& que != 'CBC-CBC COMPLETED' && current_trigger_tab =='Clean Booking Checklist' ){
		cbc_popup_trigger();
	}
}



function annualgrid_show(){
	$(".display_gird").css("display", "block");
	var tableId = "SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F"
	$('#'+tableId).wrapAll('<div class="benchmarkdiv"></div>');
	$('.JCLRgrips').remove();
	var get_pick_annualitems = $("#anual_grid_picklist").val();
	if (get_pick_annualitems == 'Contract Information') {
	var restrictedColumns = ['QUOTE_ITEM_COVERED_OBJECT_RECORD_ID','ATGKEC','ATGKEP','NWPTOC','NWPTOP','CONSCP','CONSPI','NONCCI','NONCPI','AIUICI','AIUIPI','SBTCST','SBTPRC','AMNCCI','AMNPPI','FCWISS','ITCTAS','ITTPMF','TRGPRC','SLSPRC','BDVPRC','CELPRC','TGADJP','YOYPCT','USRPRC','CNTPRC'];

	}
	else if (get_pick_annualitems == 'Pricing Review - Manual Information') {
	var restrictedColumns = ['QUOTE_ITEM_COVERED_OBJECT_RECORD_ID','SPQTEV','SPSPCT','BILTYP','INWRTY','SVSPCT','WTYSTE',
	'WTYEND','WTYDAY','TNTVGC','TENVGC','TAXVGC','TGADJP','YOYPCT','USRPRC','CNTPRC'];

	}
	else if (get_pick_annualitems == 'Pricing - Summary Information') {
	var restrictedColumns = ['QUOTE_ITEM_COVERED_OBJECT_RECORD_ID','SPQTEV','SPSPCT','SVSPCT','WTYSTE','WTYEND','WTYDAY',
	'INWRTY','BILTYP','TNTVGC','TENVGC','TAXVGC','ATGKEC','ATGKEP','NWPTOC','NWPTOP','CONSCP','CONSPI','NONCCI','NONCPI','AIUICI','AIUIPI','SBTCST','SBTPRC','AMNCCI','AMNPPI','FCWISS','TOLCFG'];

	}
	restrictedColumns.forEach(function(column){
	var edit_index = $("#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F  > thead > tr:nth-child(1)").find("[data-field='"+column+"']").index() + 1;
	//var edit_index = $('#'+tableId+' thead tr th').find("[data-field='"+column+"']").index() + 1;
	$("#"+tableId+" tbody tr td:nth-child("+edit_index+")").hide();
	$("#"+tableId+" thead tr th:nth-child("+edit_index+")").hide();
	});
}



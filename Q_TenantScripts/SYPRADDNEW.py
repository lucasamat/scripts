# =========================================================================================================================
#   __script_name : SYPRADDNEW.PY
#   __script_description : This script is used to load Add New Mode in Profile Information Section in Profiles Tab (In System Admin )
#   __primary_author__ : JOE EBENEZER
#   __create_date : 31/08/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ===========================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
Webcom = Webcom  # pylint: disable=E0602
Trace = Trace  # pylint: disable=E0602
User = User  # pylint: disable=E0602
Product = Product  # pylint: disable=E0602
ScriptExecutor = ScriptExecutor  # pylint: disable=E0602
AttributeAccess = AttributeAccess  # pylint: disable=E0602
Session = Session  # pylint: disable=E0602
ApiResponseFactory = ApiResponseFactory  # pylint: disable=E0602
# pylint: disable = no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order
import SYCNGEGUID as CPQID
from SYDATABASE import SQL

Sql = SQL()

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()

def RolesTree_Basic_info_ADD_NEW():
	try:
		current_prod = Product.Name
	except:
		current_prod = ""

	if str(current_prod) == "SYSTEM ADMIN" and str(current_prod) != "":

		Related_Tab = "Role"
		Product.Attributes.GetByName("MA_MTR_ACTIVE_TAB").AssignValue("Role")
		TestProduct.ChangeTab(Related_Tab)

		sec_str = ""
		auto_field = ""
		TableName = "SYROMA"
		date_field = []

		sec_str += '<div id="alert_msg" class="row  alert-danger pad-10 mrg-bt-10 collapse in brdr" style="display: none;"><div class="row"><label class="pad_top10"><img src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg" alt="Error"> You will not able to save until all required fields are populated!</label></div></div>'

		section_edit_obj = Sql.GetFirst(
			"SELECT top 10 * FROM SYSECT WITH (NOLOCK) WHERE PRIMARY_OBJECT_NAME='"
			+ str(TableName)
			+ "'  ORDER BY abs(DISPLAY_ORDER)"
		)
		if section_edit_obj is not None and str(section_edit_obj) != "":
			SECTION_EDIT = str(section_edit_obj.RECORD_ID)

		SYSECT = (
			"SELECT top 10* FROM SYSECT WITH (NOLOCK) WHERE PRIMARY_OBJECT_NAME='"
			+ str(TableName)
			+ "' ORDER BY abs(DISPLAY_ORDER)"
		)
		SYSECT_obj = Sql.GetList(SYSECT)

		for sec in SYSECT_obj:
			sec_rec_id = str(sec.RECORD_ID)
			a = "g4 " + str(sec_rec_id)
			if SECTION_EDIT != "":
				if str(sec.RECORD_ID) != str(SECTION_EDIT):
					MODE = "SEC_VIEW"
				else:
					MODE = "EDIT"

			SYSEFL_OBJ = (
				"SELECT top 100 a.SOURCE_DATA,q.FIELD_LABEL as FIELD_LABEL , a.FIELD_LABEL as FIELD_LABEL,a.RECORD_ID,a.API_NAME,a.DATA_TYPE,a.PERMISSION,a.FORMULA_LOGIC,a.FORMULA_DATA_TYPE,a.LOOKUP_API_NAME,a.LOOKUP_OBJECT FROM  SYOBJD a WITH (NOLOCK) INNER JOIN SYSEFL q WITH (NOLOCK) ON a.API_NAME = q.API_NAME WHERE q.API_NAME='"
				+ str(TableName)
				+ "' AND q.SECTION_RECORD_ID='"
				+ str(sec.RECORD_ID)
				+ "' AND a.OBJECT_NAME='"
				+ str(TableName)
				+ "' order by abs(q.DISPLAY_ORDER) "
			)
			data_obj = Sql.GetList(SYSEFL_OBJ)

			sec_str += '<div id="container" class="width100 ' + str(a) + '" >'

			sec_str += (
				'<div class="g4 dyn_main_head master_manufac glyphicon pointer glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)"  data-toggle="collapse" data-target="#colls'
				+ str(sec_rec_id)
				+ '"><label class="onlytext"><div>'
				+ str(sec.SECTION_NAME)
				+ "</div></label></div>"
			)

			sec_str += '<div id="colls' + str(sec_rec_id) + '" class="col-md-12 collapse in" aria-expanded="true">'
			sec_str += '<table id="SYPRFL" class="ma_width_marg">'
			sec_str += auto_field

			if data_obj is not None:
				for val in data_obj:
					disable = "disabled"
					current_obj_api_name = val.API_NAME.strip()
					current_obj_field_lable = val.FIELD_LABEL.strip()
					readonly_val = val.PERMISSION.strip()
					data_type = val.DATA_TYPE.strip()
					datepicker = "onclick_datepicker('" + current_obj_api_name + "')"
					add_style = ""
					edit_warn_icon = ""
					formula_permission = ""
					formula_obj_permission = ""
					left_float = ""
					datepicker_onchange = "onchangedatepicker('" + current_obj_api_name + "')"

					if readonly_val.upper() != "READ ONLY" and data_type != "AUTO NUMBER":
						edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
					else:
						edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'

					if readonly_val == "READ ONLY":
						if formula_obj_permission == "true" and formula_permission != "READ ONLY":
							edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
							if MODE == "EDIT":
								disable = ""
						else:
							edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
							disable = "disabled"
					elif MODE == "EDIT":
						if data_type != "AUTO NUMBER":
							edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
							disable = ""
						else:
							edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
							disable = "disabled"

					sec_str += (
						'<tr class="iconhvr borbot1" id="'
						+ str(current_obj_api_name)
						+ '" style=" '
						+ str(add_style)
						+ '"><td class="width350"><label class="padd_marbot">'
						+ str(current_obj_field_lable)
						+ '</label></td><td class="Width40"><a class="color_align_width" href="#" data-placement="top" data-toggle="popover" data-content="'
						+ str(current_obj_field_lable)
						+ '" ><i class="fa fa-info-circle flt_lt"></i>'
					)

					if readonly_val.upper() != "READ ONLY" and data_type != "AUTO NUMBER":
						sec_str += '<span class="req-field mrg3fltltmt7" >*</span></a></td>'
					else:
						sec_str += "</a></td>"

					if data_type == "AUTO NUMBER":

						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="" class="form-control related_popup_css" disabled></td>'
						)
						auto_field = (
							'<tr style="display: none;" class="iconhvr borbot1" style=" '
							+ str(add_style)
							+ '"><td class="width350"><label class="padd_marbot">'
							+ str(current_obj_field_lable)
							+ '</label></td><td class="width40"><a class="color_align_width" href="#" data-placement="top" data-toggle="popover" data-content="'
							+ str(current_obj_field_lable)
							+ '" ><i class="fa fa-info-circle flt_lt"></i><td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="" class="form-control related_popup_css" disabled></td><tr>'
						)

					elif data_type == "LONG TEXT AREA":
						sec_str += (
							'<td><textarea class="form-control related_popup_css txtArea col_width75" id="'
							+ str(current_obj_api_name)
							+ '" rows="1" cols="100" value='
							"></textarea></td>"
						)

					elif data_type == "DATE" and MODE == "EDIT":
						date_field.append(current_obj_api_name)
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" value="" type="text"  onclick="'
							+ str(datepicker)
							+ '" onchange="'
							+ str(datepicker_onchange)
							+ '" class="form-control datePickerField wid_mar_float_l_bor" ></td>'
						)

					elif data_type == "NUMBER":
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="number" value="" class="form-control related_popup_css" style="'
							+ str(add_style)
							+ '" '
							+ disable
							+ "></td>"
						)

					elif data_type == "FORMULA":
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="" class="form-control related_popup_css" style="'
							+ str(add_style)
							+ '" disabled ></td>'
						)

					else:
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="" class="form-control related_popup_css" style="'
							+ str(left_float)
							+ ' " '
							+ disable
							+ ">"
							+ str(edit_warn_icon)
							+ "</td>"
						)
					sec_str += (
						'<td class="fltrtbrdbt0"><div class="col-md-12 editiconright"><a href="#" class="editclick">'
						+ str(edit_pencil_icon)
						+ "</a></div></td>"
					)

					sec_str += "</tr>"
			sec_str += "</table>"
			sec_str += "</div></div>"

		return sec_str, date_field


def Role_users_addnew(record_id):
	sec_str = ""
	auto_field = ""
	TableName = "SYROUS"
	date_field = []
	sec_str += '<div id="alert_msg" class="row  alert-danger pad-10 mrg-bt-10 collapse in brdr" style="display: none;"><div class="row"><label class="pad_top10"><img src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/stopicon1.svg" alt="Error"> You will not able to save until all required fields are populated!</label></div></div>'

	section_edit_obj = Sql.GetFirst(
		"SELECT top 10 * FROM SYSECT WITH (NOLOCK) WHERE PRIMARY_OBJECT_NAME='"
		+ str(TableName)
		+ "'  ORDER BY abs(DISPLAY_ORDER)"
	)
	if section_edit_obj is not None and str(section_edit_obj) != "":
		SECTION_EDIT = str(section_edit_obj.RECORD_ID)

	SYSECT = (
		"SELECT top 10* FROM SYSECT WITH (NOLOCK) WHERE PRIMARY_OBJECT_NAME='"
		+ str(TableName)
		+ "' ORDER BY abs(DISPLAY_ORDER)"
	)
	SYSECT_obj = Sql.GetList(SYSECT)

	for sec in SYSECT_obj:
		sec_rec_id = str(sec.RECORD_ID)
		a = "g4 " + str(sec_rec_id)
		if SECTION_EDIT != "":
			if str(sec.RECORD_ID) != str(SECTION_EDIT):
				MODE = "SEC_VIEW"
			else:
				MODE = "EDIT"

		SYSEFL_OBJ = (
			"SELECT top 100 a.SOURCE_DATA,q.FIELD_LABEL as FIELD_LABEL , a.FIELD_LABEL as FIELD_LABEL,a.RECORD_ID,a.API_NAME,a.DATA_TYPE,a.PERMISSION,a.FORMULA_LOGIC,a.FORMULA_DATA_TYPE,a.LOOKUP_API_NAME,a.LOOKUP_OBJECT FROM  SYOBJD a WITH (NOLOCK) INNER JOIN SYSEFL q WITH (NOLOCK) ON a.API_NAME = q.API_NAME WHERE q.API_NAME='"
			+ str(TableName)
			+ "' AND q.SECTION_RECORD_ID='"
			+ str(sec.RECORD_ID)
			+ "' AND a.OBJECT_NAME='"
			+ str(TableName)
			+ "' order by abs(q.DISPLAY_ORDER) "
		)
		data_obj = Sql.GetList(SYSEFL_OBJ)

		sec_str += '<div id="container" class="width100 ' + str(a) + '" >'

		sec_str += (
			'<div class="g4 dyn_main_head master_manufac glyphicon pointer glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)"  data-toggle="collapse" data-target="#colls'
			+ str(sec_rec_id)
			+ '"><label class="onlytext"><div>'
			+ str(sec.SECTION_NAME)
			+ "</div></label></div>"
		)

		sec_str += '<div id="colls' + str(sec_rec_id) + '" class="col-md-12 collapse in" aria-expanded="true">'
		sec_str += '<table id="SYROUS" class="ma_width_marg">'
		sec_str += auto_field

		if data_obj is not None:
			for val in data_obj:
				disable = "disabled"
				current_obj_api_name = val.API_NAME.strip()
				current_obj_field_lable = val.FIELD_LABEL.strip()
				readonly_val = val.PERMISSION.strip()
				data_type = val.DATA_TYPE.strip()
				datepicker = "onclick_datepicker('" + current_obj_api_name + "')"
				add_style = ""
				edit_warn_icon = ""
				formula_permission = ""
				formula_obj_permission = ""
				left_float = ""
				datepicker_onchange = "onchangedatepicker('" + current_obj_api_name + "')"

				if readonly_val.upper() != "READ ONLY" and data_type != "AUTO NUMBER":
					edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
				else:
					edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'

				if readonly_val == "READ ONLY":
					if formula_obj_permission == "true" and formula_permission != "READ ONLY":
						edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
						if MODE == "EDIT":
							disable = ""
					else:
						edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
						disable = "disabled"
				elif MODE == "EDIT":
					if data_type != "AUTO NUMBER":
						edit_pencil_icon = '<i class="fa fa-pencil" aria-hidden="true"></i>'
						disable = ""
					else:
						edit_pencil_icon = '<i class="fa fa-lock" aria-hidden="true"></i>'
						disable = "disabled"
				if (
					current_obj_api_name == "ROLE_RECORD_ID"
					or current_obj_api_name == "ROLE_USER_RECORD_ID"
					or current_obj_api_name == "USER_RECORD_ID"
				):
					add_style = "display:none;"
				else:
					add_style = ""
				sec_str += (
					'<tr class="iconhvr borbot1" id="'
					+ str(current_obj_api_name)
					+ '" style=" '
					+ str(add_style)
					+ '"><td class="width350"><label class="padd_marbot">'
					+ str(current_obj_field_lable)
					+ '</label></td><td class="Width40"><a class="color_align_width" href="#" data-placement="top" data-toggle="popover" data-content="'
					+ str(current_obj_field_lable)
					+ '" ><i class="fa fa-info-circle flt_lt"></i>'
				)

				if readonly_val.upper() != "READ ONLY" and data_type != "AUTO NUMBER":
					sec_str += '<span class="req-field mrg3fltltmt7" >*</span></a></td>'
				else:
					sec_str += "</a></td>"

				if data_type == "AUTO NUMBER":
					add_style = "display:none;"
					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" type="text" value="" class="form-control related_popup_css" disabled></td>'
					)
					auto_field = (
						'<tr style="display: none;" class="iconhvr borbot1" style=" '
						+ str(add_style)
						+ '"><td class="width350"><label class="padd_marbot">'
						+ str(current_obj_field_lable)
						+ '</label></td><td class="width40"><a class="color_align_width" href="#" data-placement="top" data-toggle="popover" data-content="'
						+ str(current_obj_field_lable)
						+ '" ><i class="fa fa-info-circle flt_lt"></i><td><input id="'
						+ str(current_obj_api_name)
						+ '" type="text" value="" class="form-control related_popup_css" disabled></td><tr>'
					)

				elif data_type == "LONG TEXT AREA":
					sec_str += (
						'<td><textarea class="form-control related_popup_css txtArea col_width75" id="'
						+ str(current_obj_api_name)
						+ '" rows="1" cols="100" value='
						"></textarea></td>"
					)
				elif data_type == "LOOKUP":
					if current_obj_api_name == "ROLE_RECORD_ID":
						current_obj_value = record_id
					else:
						current_obj_value = ""
					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" type="text" value="'
						+ str(current_obj_value)
						+ '" class="form-control related_popup_css" disabled="">'
					)

				elif data_type == "DATE" and MODE == "EDIT":
					date_field.append(current_obj_api_name)
					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" value="" type="text"  onclick="'
						+ str(datepicker)
						+ '" onchange="'
						+ str(datepicker_onchange)
						+ '" class="form-control datePickerField wid_mar_float_l_bor" ></td>'
					)

				elif data_type == "NUMBER":
					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" type="number" value="" class="form-control related_popup_css" style="'
						+ str(add_style)
						+ '" '
						+ disable
						+ "></td>"
					)

				elif data_type == "FORMULA":
					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" type="text" value="" class="form-control related_popup_css" style="'
						+ str(add_style)
						+ '" disabled ></td>'
					)
					if current_obj_api_name == "ROLE_ID" and TableName == "SYROUS":
						formula_logic = Sql.GetFirst(
							"SELECT ROLE_ID FROM SYROMA WHERE ROLE_RECORD_ID ='" + str(record_id) + "'"
						)
						current_obj_value = formula_logic.ROLE_ID

					elif current_obj_api_name == "ROLE_NAME" and TableName == "SYROUS":
						formula_logic = Sql.GetFirst(
							"SELECT ROLE_NAME FROM SYROMA WHERE ROLE_RECORD_ID ='" + str(record_id) + "'"
						)
						current_obj_value = formula_logic.ROLE_NAME
					else:
						current_obj_value = ""
					if readonly_val == "READ ONLY":
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ str(current_obj_value)
							+ '" class="form-control related_popup_css" disabled="">'
						)
					else:
						sec_str += (
							'<td><input id="'
							+ str(current_obj_api_name)
							+ '" type="text" value="'
							+ str(current_obj_value)
							+ '" class="form-control related_popup_css fltltlightyello">'
						)
						sec_str += (
							'<input class="popup flt_lt" id="'
							+ str(current_obj_api_name)
							+ '" data-target="#cont_viewModalSection" onclick="cont_lookup_popup_new(this)" type="image" src="../mt/default/images/customer_lookup.gif"></td>'
						)

				else:
					sec_str += (
						'<td><input id="'
						+ str(current_obj_api_name)
						+ '" type="text" value="" class="form-control related_popup_css" style="'
						+ str(left_float)
						+ ' " '
						+ disable
						+ ">"
						+ str(edit_warn_icon)
						+ "</td>"
					)
				sec_str += (
					'<td class="fltrtbrdbt0"><div class="col-md-12 editiconright"><a href="#" class="editclick">'
					+ str(edit_pencil_icon)
					+ "</a></div></td>"
				)

				sec_str += "</tr>"
		sec_str += "</table>"
		sec_str += "</div></div>"
	return sec_str, date_field


if Product.Attributes.GetByName("BTN_ROLE_BACK_TO_LIST"):
	Product.Attributes.GetByName("BTN_ROLE_BACK_TO_LIST").Allowed = True
	Product.Attributes.GetByName("BTN_ROLE_BACK_TO_LIST").HintFormula = "CANCEL"
if Product.Attributes.GetByName("BTN_ROLES_ADDNEW_SAVE"):
	Product.Attributes.GetByName("BTN_ROLES_ADDNEW_SAVE").Allowed = True
if hasattr(Param, "ACTION"):
	ACTION = Param.ACTION
else:
	ACTION = ""
record_id = ""
if hasattr(Param, "RECORD_ID"):
	RECORD_ID = Param.RECORD_ID
	rec_list = RECORD_ID.split("-")
	Trace.Write(str(RECORD_ID) + "RECORD_ID" + str(rec_list))
	record_id = CPQID.KeyCPQId.GetKEYId(str(rec_list[0]), str(rec_list[1]))
else:
	RECORD_ID = ""
if ACTION == "ROLE ADDNEW":
	ApiResponse = ApiResponseFactory.JsonResponse(RolesTree_Basic_info_ADD_NEW())
else:
	ApiResponse = ApiResponseFactory.JsonResponse(Role_users_addnew(record_id))
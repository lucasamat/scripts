# =========================================================================================================================================
#   __script_name : SYPVTBEDPO.PY
#   __script_description :  THIS SCRIPT IS USED TO EDIT PIVOT TABLE DATA IN A POPUP.
#   __primary_author__ : LEO JOSEPH
#   __create_date :
# ==========================================================================================================================================
import SYTABACTIN as Table
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
Sql = SQL()

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
CurrentTabName = TestProduct.CurrentTab


def PivotTableAttredit(TABLEID, ATTR_ID, PRICEAGREEMENT_ID, SEGMENT_DESC, Display_save_val):
	sec_str = ""
	Value_code = ""
	Product.SetGlobal("disp_val", str(Display_save_val))
	sec_str = (
		'<div class="modal-content"><div class="modal-body" id="pivot_table_popup">'
	)
	sec_str += (
		'<div id="PIVOT_TABLE_EDIT"><div class="row modulebnr brdr ma_mar_btm"> MATERIAL ATTRIBUTE : EDIT <button type="button" class="close flt_rt" data-dismiss="modal">X</button></div><div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr"><button type="button" class="btnconfig" data-dismiss="modal">CANCEL</button><button type="button" id='
		+ str(ATTR_ID)
		+ ' class="btnconfig " onclick="pivottablemat_attr_update(this)" data-dismiss="modal">SAVE</button></div></div><div class="col-md-12"   id="alert_msg_outer" ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert24" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div><div  id="Alert24" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"   id="alert_msg" style="display:none" ><label ><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/stopicon1.svg" alt="Error">  </label></div></div></div><div id="container" class="g4 pad-10 brdr except_sec">'
	)

	sec_str += '<table class="ma_width_marg"><tbody>'
	sec_str += (
		'<tr class="iconhvr borbot1"><td class="width350"><label class="fltltpadlt">SAP Part Number</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="SAP Part Number" class="color_align_width"><i class="fa fa-info-circle flt_lt"></i></a></td><td><input type="text" id="segement_part_no" value ="'
		+ str(PRICEAGREEMENT_ID)
		+ '" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td></tr>'
	)
	sec_str += (
		'<tr class="iconhvr borbot1"><td class="width350"><label class="fltltpadlt">SAP Description</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="SAP Description" class="color_align_width"><i class="fa fa-info-circle flt_lt"></i></a></td><td><input type="text" value ="'
		+ str(SEGMENT_DESC)
		+ '" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td></tr>'
	)

	sec_str += '<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr>'
	sec_str += (
		'<tr class="iconhvr borbot1"><td class="width350"><label class="fltltpadlt">Value Code</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Value Code" class="color_align_width"><i class="fa fa-info-circle flt_lt"></i></a></td><td><input id="VALUE_CODE" type="text" value ="'
		+ str(Value_code)
		+ '" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td></tr>'
	)
	sec_str += "</tbody></table></div></div></div></div>"
	return sec_str


def PivotTableAttrView(TABLEID, ATTR_ID, PRICEAGREEMENT_ID, SEGMENT_DESC, Display_save_val):
	sec_str = ""
	Product.SetGlobal("disp_val", str(Display_save_val))
	sec_str = (
		'<div class="modal-content"><div class="modal-body" id="pivot_table_popup">'
	)
	sec_str += '<div id="PIVOT_TABLE_EDIT"><div class="row modulebnr brdr ma_mar_btm"> MATERIAL ATTRIBUTE : VIEW <button type="button" class="close flt_rt" data-dismiss="modal">X</button></div><div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr"> <button type="button" class="btnconfig" data-dismiss="modal">CANCEL</button><button type="button" onclick="pivottable_attr_edit(this)" class="btnconfig">EDIT</button></div></div>'
	
	sec_str += '<div class="col-md-12"   id="alert_msg_outer" ><div class="row modulesecbnr brdr" data-toggle="collapse" data-target="#Alert25" aria-expanded="true" >NOTIFICATIONS<i class="pull-right fa fa-chevron-down "></i><i class="pull-right fa fa-chevron-up"></i></div>'
	
	sec_str += '<div  id="Alert25" class="col-md-12  alert-notification  brdr collapse in" ><div  class="col-md-12 alert-danger"   id="alert_msg"  style="display: none;"><label ><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/stopicon1.svg" alt="Error">  </label></div></div></div><div id="container" class="g4 pad-10 brdr except_sec">'

	sec_str += '<table class="ma_width_marg"><tbody>'
	sec_str += (
		'<tr class="iconhvr borbot1"><td class="width350"><label class="fltltpadlt">SAP Part Number</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="SAP Part Number" class="color_align_width"><i class="fa fa-info-circle flt_lt"></i></a></td><td><input type="text" id="segement_part_no" value ="'
		+ str(PRICEAGREEMENT_ID)
		+ '" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td></tr>'
	)
	sec_str += (
		'<tr class="iconhvr borbot1"><td class="width350"><label class="fltltpadlt">SAP Description</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="SAP Description" class="color_align_width"><i class="fa fa-info-circle flt_lt"></i></a></td><td><input type="text" id="segement_part_desc" value ="'
		+ str(SEGMENT_DESC)
		+ '" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-lock" aria-hidden="true"></i></a></div></td></tr>'
	)
	sec_str += '<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr>'
	sec_str += "</tbody></table></div></div></div></div>"
	return sec_str



def PivotTableSetedit(TABLEID, ATTR_ID, SEGMENT_DESC, Display_save_val):
	sec_str = ""
	sec_str = (
		'<div class="modal-content"><div class="modal-body" id="pivot_table_popup">'
	)
	sec_str += (
		'<div id="PIVOT_TABLE_EDIT"><div class="row modulebnr brdr ma_mar_btm"> PIVOT TABLE : EDIT <button type="button" class="close flt_rt" data-dismiss="modal">X</button></div><div class="col-md-12"><div class="row pad-10 bg-lt-wt brdr"><button type="button" class="btnconfig" data-dismiss="modal">CANCEL</button><button type="button" id='
		+ str(ATTR_ID)
		+ ' class="btnconfig " onclick="pivottablemat_attr_update(this)" data-dismiss="modal">SAVE</button></div></div><div id="container" class="g4 pad-10 brdr except_sec">'
	)

	sec_str += '<table class="ma_width_marg"><tbody>'
	sec_str += (
		'<tr class="iconhvr borbot1"><td class="width350"><label class="fltltpadlt">Set Name</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Set Name" class="color_align_width"><i class="fa fa-info-circle flt_lt"></i></a></td><td><input type="text" id="Set_Name" value ="'
		+ str(ATTR_ID)
		+ '" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr>'
	)

	sec_str += (
		'<tr class="iconhvr borbot1"><td class="width350"><label class="fltltpadlt">Set Type</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Set type" class="color_align_width"><i class="fa fa-info-circle flt_lt"></i></a></td><td><input type="text" id="Set_Type" value ="'
		+ str(ATTR_ID)
		+ '" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr>'
	)

	sec_str += (
		'<tr class="iconhvr borbot1"><td class="width350"><label class="fltltpadlt">SAP Part Number</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="SAP Part Number" class="color_align_width"><i class="fa fa-info-circle flt_lt"></i></a></td><td><input type="text" id="SAP_Part_Number" value ="'
		+ str(ATTR_ID)
		+ '" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr>'
	)

	sec_str += (
		'<tr class="iconhvr borbot1"><td class="width350"><label class="fltltpadlt">SAP Description</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Set Item Rank" class="color_align_width"><i class="fa fa-info-circle flt_lt"></i></a></td><td><input type="text" id="Set_Item_Rank" value ="'
		+ str(ATTR_ID)
		+ '" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr>'
	)

	# sec_str += '<tr class="iconhvr"><td ><label>Set Quantity</label></td><td ><a href="#" data-placement="top" data-toggle="popover" data-content="Set Quantity"><i class="fa fa-info-circle"></i></a></td><td><input type="text" id="Set_Quantity" value ="'+str(ATTR_ID)+'" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr>'

	sec_str += (
		'<tr class="iconhvr borbot1"><td class="width350"><label class="fltltpadlt">Attribute Name</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Attribute Name" class="color_align_width"><i class="fa fa-info-circle flt_lt"></i></a></td><td><input type="text" id="Attribute_Name" value ="'
		+ str(ATTR_ID)
		+ '" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr>'
	)

	sec_str += (
		'<tr class="iconhvr borbot1"><td class="width350"><label class="fltltpadlt">Value</label></td><td class="width40"><a href="#" data-placement="top" data-toggle="popover" data-content="Value" class="color_align_width"><i class="fa fa-info-circle flt_lt"></i></a></td><td><input type="text" id="Value" value ="'
		+ str(ATTR_ID)
		+ '" class="form-control related_popup_css flt_lt" disabled=""></td><td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr>'
	)

	sec_str += '<td class="float_r_bor_bot"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td></tr>'
	sec_str += "</tbody></table></div></div></div></div>"
	return sec_str


OPER = Param.OPER

if OPER == "EDIT":
	TABLEID = Param.TABLEID
	ATTR_ID = Param.ATTR_ID
	PRICEAGREEMENT_ID = Param.PRICEAGREEMENT_ID

	Display_save_val = ""
	SEGMENT_DESC = Param.SEGMENT_DESC
	ApiResponse = ApiResponseFactory.JsonResponse(
		PivotTableAttredit(TABLEID, ATTR_ID, PRICEAGREEMENT_ID, SEGMENT_DESC, Display_save_val)
	)

elif OPER == "VIEW":
	TABLEID = Param.TABLEID
	ATTR_ID = Param.ATTR_ID
	PRICEAGREEMENT_ID = Param.PRICEAGREEMENT_ID
	Display_save_val = ""
	SEGMENT_DESC = Param.SEGMENT_DESC
	ApiResponse = ApiResponseFactory.JsonResponse(
		PivotTableAttrView(TABLEID, ATTR_ID, PRICEAGREEMENT_ID, SEGMENT_DESC, Display_save_val)
	)
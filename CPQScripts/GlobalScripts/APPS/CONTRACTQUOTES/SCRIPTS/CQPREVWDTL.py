# =========================================================================================================================================
#   __script_name : CQPREVWDTL.PY
#   __script_description : THIS SCRIPT IS USED TO  TRIGGER POPUP WHILE SAVING THE DRIVERS, PRICE,ENTITLEMENTS 
#   __primary_author__ : WASIM ABDUL 
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from asyncio.windows_events import NULL
from curses.ascii import NUL
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import datetime
from datetime import datetime
Sql = SQL()
import SYCNGEGUID as CPQID
import CQVLDRIFLW
import CQCPQC4CWB
import CQREVSTSCH

# import CMGTRULRAC as CMRUL
try:
	userId = str(User.Id)
	userName = str(User.UserName)
	TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
	CurrentTabName = TestProduct.CurrentTab
except:
	userId = str(User.Id)
	userName = str(User.UserName)
	TestProduct = "Sales"
	CurrentTabName = "Quote"


def popups(params):
	sec_str = ""
	sec_str += """<div class="drop-boxe" style="display: none;">
				<div class="col-md-3 pl-0 rolling_popup">
				<div class="col-md-2 p-0">
					<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/info_icon.svg" class="img-responsive center-block">
					
				</div>
				<div class="col-md-10 p-0">
					<h3>"""+str(params)+""" Roll Down <button type="button"
					class="close"
					aria-label="Close" onclick="close_popup()"> 
				<span aria-hidden="true">×</span> 
			</button> </h3>
				<p>The <q>"""+str(params)+"""</q> settings are being applied to the Equipment in this quote. You will be notified by email when this background job completes.</p>
				</div>
				</div>
				</div>"""  
	return sec_str


# commented the code(Approvals node functionality in Quotes explorer) -start
# def submitapproval():
#     sec_str = ""
#     sec_str += """<div class="drop-boxess" style="display: none;">
#                 <div class="col-md-3 pl-0 rolling_popup">
#                 <div class="col-md-2 p-0">
#                     <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/info_icon.svg" class="img-responsive center-block">
#                 </div>
#                 <div class="col-md-10 p-0">
#                     <h3>Approval Request Submitted <button type="button"
#                     class="close" data-dismiss="modal" 
#                     aria-label="Close" onclick="close_popup()"> 
#                 <span aria-hidden="true">×</span> 
#             </button></h3>
#                 <p>The Quote has been successfully Submitted for Approval.The responsible approvers will notified by email notification.</p>
#                 </div>
#                 </div>
#                 </div>"""  
#     return sec_str
# commented the code(Approvals node functionality in Quotes explorer) -end

def constructopportunity(Qt_rec_id, Quote, MODE):    
	VAR1 = ""
	sec_str = ""
	add_style = ""
	API_NAME_LIST = []
	PModel = "disabled"
	sec_rec_id = "B0B5E48B-DC63-4B1A-95AC-695973D3AA06"
	Oppp_SECT = Sql.GetList(
		"SELECT TOP 1000 RECORD_ID,SECTION_NAME FROM SYSECT WHERE PRIMARY_OBJECT_NAME = 'SAOPQT' ORDER BY DISPLAY_ORDER"
	)
	for sect in Oppp_SECT:
		sec_str += '<div id="container" class="wdth100 margtop10 g4 ' + str(sect.RECORD_ID) + '">'
		sec_str += (
			'<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_'
			+ str(sect.RECORD_ID)
			+ '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>'
			+ str(sect.SECTION_NAME)
			+ "</div></label></div>"
		)

		Oppp_SEFL = Sql.GetList(
			"SELECT TOP 1000 FIELD_LABEL, API_FIELD_NAME,API_NAME FROM SYSEFL WHERE SECTION_RECORD_ID = '" + str(sect.RECORD_ID) + "' ORDER BY DISPLAY_ORDER"
		)
		for sefl in Oppp_SEFL:
			sec_str += '<div id="sec_' + str(sect.RECORD_ID) + '" class= "sec_' + str(sect.RECORD_ID) + ' collapse in">'
			sec_str += "<div style='height:30px;border-left: 0;border-right: 0;border-bottom:1px solid  #dcdcdc;' data-bind='attr: {'id':'mat'+stdAttrCode(),'class': isWholeRow() ? 'g4  except_sec removeHorLine iconhvr' : 'g1 except_sec removeHorLine iconhvr' }' id='mat1578' class='g4  except_sec removeHorLine iconhvr'>"
			sec_str += (
				"<div class='col-md-5'>	<abbr data-bind='attr:{'title':label}' title='"
				+ str(sefl.FIELD_LABEL)
				+ "'> <label class='col-md-11 pull-left' style='padding: 5px 5px;margin: 0;' data-bind='html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), 'pull-left': hint() }'>"
				+ str(sefl.FIELD_LABEL)
				+ "</label> </abbr> <a href='#' title='"+str(sefl.FIELD_LABEL)+"' data-placement='auto top' data-toggle='popover' data-trigger='focus' data-content='"+str(sefl.FIELD_LABEL)+"' class='col-md-1 bgcccwth10' style='text-align:right;padding: 7px 5px;color:green;' data-original-title=''><i title='"+str(sefl.FIELD_LABEL)+"' class='fa fa-info-circle fltlt'></i></a> </div>"
			)
			sefl_api = sefl.API_FIELD_NAME
			object_name = sefl.API_NAME
			syobjd_obj = Sql.GetFirst("SELECT DATA_TYPE FROM SYOBJD WHERE API_NAME = '{}' and OBJECT_NAME ='{}'".format(sefl_api,object_name))
			data_type = syobjd_obj.DATA_TYPE
			col_name = Sql.GetFirst("SELECT * FROM SAOPQT WHERE QUOTE_RECORD_ID = '" + str(Quote) + "'")
			if col_name:
				if sefl_api == "CpqTableEntryModifiedBy":
					current_obj_value = col_name.CpqTableEntryModifiedBy
					current_user = Sql.GetFirst(
						"SELECT USERNAME FROM USERS WHERE ID = " + str(current_obj_value) + ""
					).USERNAME
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' value = '"
						+ str(current_user)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					)
				elif data_type =="CHECKBOX":
					act_status = (eval("col_name." + str(sefl_api)))
					#Trace.Write("act_status---->"+str(act_status))
					if act_status == True  or act_status == 1:
						sec_str += (
							'<div class="col-md-3 padtop5 padleft10"><input id="'
							+ str(sefl_api)
							+ '" type="CHECKBOX" value="'
							+ str(act_status)
							+ '" class="custom" '
							+ 'disabled checked><span class="lbl"></span></div>'
						)

					else:
						sec_str += (
							'<div class="col-md-3 padtop5 padleft10"><input id="'
							+ str(sefl_api)
							+ '" type="CHECKBOX" value="'
							+ str(act_status)
							+ '" class="custom" '
							+ 'disabled ><span class="lbl"></span></div>'
						)
				else:
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' value = '"
						+ str(eval("col_name." + str(sefl_api)))
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='"
						+ str(eval("col_name." + str(sefl_api)))
						+ "' tabindex='' disabled=''> </div>"
					)
			else:

				sec_str += "<div class='col-md-3 pad-0'> <input type='text' value = '' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
			sec_str += "<div class='col-md-3' style='display:none;'> <span class='' data-bind='attr:{'id': $data.name()}' id=''>  </div>"
			sec_str += "<div class='col-md-1' style='float: right;'> <div class='col-md-12 editiconright'><a href='#' onclick='editclick_row(this)' class='editclick'>	<i class='fa fa-lock' aria-hidden='true'></i></a></div></div>"
			sec_str += "</div>"

			sec_str += "</div>"
		sec_str += "</div>"
	sec_str += '<table class="wth100mrg8"><tbody>'
	#Trace.Write("111111" + str(Qt_rec_id))

	sec_str += "</tbody></table></div>"
	sec_str += "</div>"
	#Trace.Write(str(sec_str))
	return sec_str
# def get_value_from_obj(record_obj, column):
#     return getattr(record_obj, column, "")

def constructquoteinformation(Qt_rec_id, Quote, MODE):    
	anchor_tag_id_value = ""
	VAR1 = ""
	sec_str = ""
	quote_id=""
	add_style = ""
	API_NAME_LIST = []
	PModel = "disabled"
	editclick = "QuoteinformationEDIT(this)"
	edit_action = ""
	#sec_rec_id = "B0B5E48B-DC63-4B1A-95AC-695973D3AA06"
	if ACTION == "CONTRACT_INFO":
		primary_objname = "CTCNRT"
	else:
		primary_objname = "SAQTRV"

	Oppp_SECT = Sql.GetList(
		"SELECT TOP 1000 RECORD_ID,SECTION_NAME FROM SYSECT WHERE SECTION_DESC = '' AND PRIMARY_OBJECT_NAME = '{primary_objname}'  and RECORD_ID not in ('AED0A92A-8644-46AE-ACF0-90D6E331E506') ORDER BY DISPLAY_ORDER".format(primary_objname = primary_objname)
	)
	for sect in Oppp_SECT:
		sec_str += '<div id="container" class="wdth100 margtop10 ' + str(sect.RECORD_ID) + '">'
		# if (str(sect.SECTION_NAME) == "CONTRACT BOOKING INFORMATION" or str(sect.SECTION_NAME) == "AUDIT INFORMATION" ):
		#     sec_str += (
		#         '<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down mt-10px" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_'
		#         + str(sect.RECORD_ID)
		#         + '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>'
		#         + str(sect.SECTION_NAME)
		#         + "</div></label></div>"
		#     )
		
		# else:
		sec_html_btn = Sql.GetFirst("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE ACTION_NAME = 'EDIT' AND SECTION_RECORD_ID = '"+str(sect.RECORD_ID)+"'")
		if sec_html_btn is not None:
			edit_action = str(sec_html_btn.HTML_CONTENT).format(rec_id = str(sect.RECORD_ID), edit_click = str(editclick))
		else:
			edit_action = ''
		sec_str += (
			'''<div onclick="dyn_main_sec_collapse_arrow(this)" 
			data-bind="attr: {'data-toggle':'collapse','data-target':'.col'+stdAttrCode(), 
			'id':'dyn'+stdAttrCode(),'class': isWholeRow() ? 'g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer' : 'g1 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer'}" 
				data-target=".sec_'''+str(sect.RECORD_ID)+'''"  id="dyn1577"  data-toggle="collapse"  class="g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer"> 
			<label data-bind="html: hint" class="onlytext"><div>'''+ str(edit_action) + str(sect.SECTION_NAME)+'''</div></label> </div>'''
		)
		


		Oppp_SEFL = Sql.GetList(
			"SELECT TOP 1000 SYSEFL.FIELD_LABEL, SYSEFL.API_FIELD_NAME,SYSEFL.RECORD_ID,SYSEFL.DISPLAY_ORDER,SYOBJD.DATA_TYPE,SYOBJD.FORMULA_DATA_TYPE,SYOBJD.CURRENCY_INDEX FROM SYSEFL JOIN SYOBJD ON SYOBJD.API_NAME = SYSEFL.API_FIELD_NAME AND SYOBJD.OBJECT_NAME = SYSEFL.API_NAME WHERE SECTION_RECORD_ID = '" + str(sect.RECORD_ID) + "' ORDER BY DISPLAY_ORDER"
		)
		for sefl in Oppp_SEFL:
			sec_str += '<div id="sec_' + str(sect.RECORD_ID) + '" class=  "sec_' + str(sect.RECORD_ID) + ' collapse in "> '
			sec_str += "<div style='height:30px;border-left: 0;border-right: 0;border-bottom:1px solid  #dcdcdc;' data-bind='attr: {'id':'mat'+stdAttrCode(),'class': isWholeRow() ? 'g4  except_sec removeHorLine iconhvr' : 'g1 except_sec removeHorLine iconhvr' }' id='mat1578' class='g4  except_sec removeHorLine iconhvr'>"
			sec_str += (
				"<div class='col-md-5'>	<abbr data-bind='attr:{'title':label}' title='"
				+ str(sefl.FIELD_LABEL)
				+ "'> <label class='col-md-11 pull-left' style='padding: 5px 5px;margin: 0;' data-bind='html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), 'pull-left': hint() }'>"
				+ str(sefl.FIELD_LABEL)
				+ "</label> </abbr> <a href='#' title='' data-placement='auto top' data-toggle='popover' data-trigger='focus' data-content='"+str(sefl.FIELD_LABEL)+"' class='col-md-1 bgcccwth10' style='text-align:right;padding: 7px 5px;color:green;' data-original-title=''><i title='"+str(sefl.FIELD_LABEL)+"' class='fa fa-info-circle fltlt'></i></a> </div>"
			)
			sefl_api = sefl.API_FIELD_NAME
			objd_datatype = sefl.DATA_TYPE
			objd_formulatype = sefl.FORMULA_DATA_TYPE
			curr_index = sefl.CURRENCY_INDEX
			#sefl_api = sefl_api.encode('ascii', 'ignore').decode('ascii')
			if ACTION == "CONTRACT_INFO": 
				col_name = Sql.GetFirst("SELECT * from CTCNRT (NOLOCK) WHERE CONTRACT_RECORD_ID = '{contract_record_id}' ".format(contract_record_id= str(contract_record_id) ))
				
			else:
				col_name = Sql.GetFirst("SELECT * FROM SAQTRV WHERE QUOTE_RECORD_ID = '" + str(Quote) + "' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) + "' ") 
			if col_name:
				if objd_datatype =="CURRENCY" or objd_formulatype == "CURRENCY":
					#Trace.Write('@@@SEFL_API** --> '+str(sefl_api))
					curr_symbol = ""
					current_obj_value = eval("col_name." + sefl_api)
					decimal_val = 3
					try:
						curr_symbol_obj = Sql.GetFirst("select SYMBOL,CURRENCY,isnull(DISPLAY_DECIMAL_PLACES,3) AS DISPLAY_DECIMAL_PLACES  from PRCURR WITH (NOLOCK) where CURRENCY_RECORD_ID = (select top 1 " + curr_index + " from "+ str(primary_objname)+ " where QUOTE_RECORD_ID = '"+ str(Quote)+ "' AND QTEREV_RECORD_ID = '"+ str(quote_revision_record_id)+ "'  ) ")
						if curr_symbol_obj is not None:
							if curr_symbol_obj != "":
								curr_symbol = curr_symbol_obj.CURRENCY
								decimal_val = curr_symbol_obj.DISPLAY_DECIMAL_PLACES  # modified for A043S001P01-9963					
						if current_obj_value != "" and decimal_val != "":
							formatting_string = "{0:." + str(decimal_val) + "f}"
							current_obj_value = formatting_string.format(float(current_obj_value))
						if current_obj_value is not None:
							if current_obj_value != "":
								current_obj_value = str(current_obj_value) + " " + str(curr_symbol)
					except:
						Trace.Write('Unable to bind Currency price')
					
					try:
						sec_str += (
								"<div class='col-md-3 pad-0'> <input type='text' id ='"+sefl_api+"' title = '"+ current_obj_value+"' value = '"
								+ current_obj_value
								+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
						)
					except Exception:
						sec_str += (
							"<div class='col-md-3 pad-0'> <input type='text' id ='"+str(sefl_api)+"' title = '"+  str(current_obj_value)+"' value = '"
							+ str(current_obj_value)
							+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
						)	

				elif sefl_api == "CpqTableEntryModifiedBy":
					current_obj_value = col_name.CpqTableEntryModifiedBy	
					current_user = Sql.GetFirst(
						"SELECT USERNAME FROM USERS WHERE ID = " + str(current_obj_value) + ""
					).USERNAME
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' title = '"+ str(current_user)+"' value = '"
						+ str(current_user)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					)
				elif sefl_api == "MASTER_TABLE_QUOTE_RECORD_ID":
					cpq_key_id = CPQID.KeyCPQId.GetCPQId("SAQTMT", str(eval("col_name." + str(sefl_api))))
					sec_str += (
						"<div class='col-md-3 pad-0'> <input id= 'key_field_id' type='text' title = '"+ str(cpq_key_id)+"' value = '"
						+ str(cpq_key_id)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					)
				elif sefl_api == "QUOTE_REVISION_RECORD_ID":
					cpq_key_id = CPQID.KeyCPQId.GetCPQId("SAQTRV", str(eval("col_name." + str(sefl_api))))
					sec_str += (
						"<div class='col-md-3 pad-0'> <input id= 'key_field_id' type='text' title = '"+ str(cpq_key_id)+"' value = '"
						+ str(cpq_key_id)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					)
				## Contract Key field
				elif sefl_api == "CONTRACT_RECORD_ID":
					cpq_key_id = CPQID.KeyCPQId.GetCPQId("CTCNRT", str(eval("col_name." + str(sefl_api))))
					sec_str += (
						"<div class='col-md-3 pad-0'> <input id= 'key_field_id' type='text' title = '"+ str(cpq_key_id)+"' value = '"
						+ str(cpq_key_id)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					)
				# To get the hyperlink for source contract id field in Quote information node - start
				elif sefl_api == "SOURCE_CONTRACT_ID":
					if str(eval("col_name." + str(sefl_api))):
					#parent_rec_id = get_value_from_obj(record_obj, column_name)
						contract_obj = Sql.GetFirst("SELECT CONTRACT_RECORD_ID FROM CTCNRT (NOLOCK) WHERE CONTRACT_ID = '"+str(eval("col_name." + str(sefl_api)))+"'")
						if contract_obj:
							parent_rec_id = contract_obj.CONTRACT_RECORD_ID
							anchor_tag_id_value = parent_rec_id + '|Contracts'
						sec_str += (
							"<div class='col-md-1 col-xs-2 col-sm-1 pad-0 pt-5px pb-5px'><a id='"+str(anchor_tag_id_value)+"' onclick='Move_to_parent_obj(this)' class='curptr''>"+str(eval("col_name." + str(sefl_api)))+"</a></div>"
						)
					else:
						sec_str += (
							"<div class='col-md-3 pad-0'> <input type='text' title = '"+ str(sefl_api)+"' value = '"
							+ str(eval("col_name." + str(sefl_api)))
							+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
						)  
				# To get the hyperlink for source contract id field in Quote information node - end              
				##to get date from datetime for CONTRACT_VALID_FROM and CONTRACT_VALID_TO strts
				elif sefl_api in ("CONTRACT_VALID_FROM","CONTRACT_VALID_TO","QUOTE_EXPIRE_DATE","QUOTE_CREATED_DATE","REV_APPROVE_DATE","REV_CREATE_DATE","REV_EXPIRE_DATE","EXCHANGE_RATE_DATE"):
					#Trace.Write("date---->"+str(eval("col_name." + str(sefl_api))))
					try:
						datetime_value = datetime.strptime(str(eval("col_name." + str(sefl_api))), '%m/%d/%Y %I:%M:%S %p').strftime('%m/%d/%Y')
					except:
						datetime_value  = str(eval("col_name." + str(sefl_api)))
					
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' title = '"+ str(datetime_value)+"' value = '"
						+ str(datetime_value)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='"+ str(sefl_api)+"' title='' tabindex='' disabled=''> </div>"
					)
				##to get date from datetime for CONTRACT_VALID_FROM and CONTRACT_VALID_TO ends
				elif sefl_api in ("CPQTABLEENTRYDATEADDED","CpqTableEntryDateModified"):
					try:
						datetime_value = datetime.strptime(str(eval("col_name." + str(sefl_api))), '%m/%d/%Y %I:%M:%S %p').strftime('%m/%d/%Y %I:%M:%S %p')
					except:
						datetime_value  = str(eval("col_name." + str(sefl_api)))
					
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' title = '"+ str(datetime_value)+"' value = '"
						+ str(datetime_value)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					)
				elif sefl_api=="POES":
					#if str((eval("col_name." + str(sefl_api)))).upper() == "TRUE" or (eval("col_name." + str(sefl_api))) == "1":
					#Trace.Write("313")
					act_status = (eval("col_name." + str(sefl_api)))
					sec_str += (
						'<td><input id="'
						+ str(sefl_api)
						+ '" type="CHECKBOX" value="'
						+ str(act_status)
						#+ (eval("col_name." + str(sefl_api)))
						+ '" class="custom" '
						+ 'disable checked><span class="lbl"></span></td>'
					)			
				elif sefl_api=="ACTIVE":
					act_status = (eval("col_name." + str(sefl_api)))
					sec_str += (
						'<div class="col-md-3 padtop5 padleft10"><input id="'
						+ str(sefl_api)
						+ '" type="CHECKBOX" value="'
						+ str(act_status)
						+ '" class="custom" '
						+ 'disabled checked><span class="lbl"></span></div>'
					)
				elif sefl_api in ["INTERNAL_NOTES","CUSTOMER_NOTES"]:
					#Trace.Write('At line 289-->err'+str(sefl_api))
					sec_str += (
						"<div class='col-md-3 pad-0'> <textarea type='text' id ='"+str(sefl_api)+"' title = '"+  str(eval("col_name." + str(sefl_api)))+"' value = '"
						+ str(eval("col_name." + str(sefl_api)))
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control txtArea remove_yellow bor-left bor-right' style='height: 28px;border-top: 0 !important;border-bottom: 1px solid #ddd !important;' id='' title='' tabindex='' disabled=''>"
						+ str(eval("col_name." + str(sefl_api)))
						+ "</textarea></div>"
					)    
				# elif sefl_api == "APPDTE_EXCH_RATE":
				# 	Trace.Write("sefl_api_APPDTE_EXCH_RATE_chk "+str(sefl_api))
				# 	current_obj_value = col_name.APPDTE_EXCH_RATE
				# 	onchange = ""
				# 	disable= "disabled"
				# 	sec_str += (
				# 		'''<div class='col-md-3 pad-0'> <select id="'''
				# 			+ str(sefl_api)
				# 			+ '''" '''
				# 			+ str(onchange)
				# 			+ ''' value="'''
				# 			+ current_obj_value
				# 			+ '''" type="text" title="'''
				# 			+ str(current_obj_value)
				# 			+ '''" class="form-control pop_up_brd_rad related_popup_css fltlt" onchange = "onchangeFunction(this)" '''
				# 			+ disable
				# 			+ '''" ><option value='Select'>..Select</option> </div>'''
				# 	)
					# else:
					# 	sec_str += (
					# 		'<td><input id="'
					# 		+ str(sefl_api)
					# 		+ '" type="CHECKBOX" value="False" class="custom" '
					# 		+ disable
					# 		+ '><span class="lbl"></span></td>'
					# 	)
				else:
					# if sefl_api != "REGION":
					#Trace.Write('At line 289-->arr2'+sefl_api)
					# if sefl_api == "APPDTE_EXCH_RATE" and str(eval("col_name." + str(sefl_api))) != "":
					# 	sec_str += (
					# 		"<div class='col-md-3 pad-0'> <input type='text' id ='"+str(sefl_api)+"' title = '"+  str(eval("col_name." + str(sefl_api)))+"' value = '"
					# 		+ str(eval("col_name." + str(sefl_api)))
					# 		+ " of month' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					# 	)
					# else:
					#sefl_api = sefl_api.encode('ascii', 'ignore').decode('ascii')
					if sefl_api=='CANCELLATION_PERIOD_NOTPER':
						len_restrict= 'oninput="this.value=this.value.slice(0,this.maxLength)" maxlength="3"'
					else :
						len_restrict=""

					try:
						sec_str += (
								"<div class='col-md-3 pad-0'> <input type='text' id ='"+sefl_api+"' title = '"+  eval("col_name." + sefl_api)+"' "+len_restrict+" value = '"
								+ eval("col_name." + sefl_api)
								+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
						)
					except Exception:
						sec_str += (
							"<div class='col-md-3 pad-0'> <input type='text' id ='"+str(sefl_api)+"' title = '"+  str(eval("col_name." + str(sefl_api)))+"' "+len_restrict+" value = '"
							+ str(eval("col_name." + str(sefl_api)))
							+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
						)
						

					# else:
					#     sec_str += (
					#         "<div class='col-md-3 pad-0'> <input type='text' value = '' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					#     )
			else:

				sec_str += "<div class='col-md-3 pad-0'> <input type='text' value = '' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
			sec_str += "<div class='col-md-3' style='display:none;'> <span class='' data-bind='attr:{'id': $data.name()}' id=''>  </div>"
			##edit_lock_icon in quote based on permission starts
			permission_chk_query = Sql.GetFirst("""SELECT DISTINCT SYOBJD.OBJECT_NAME, SYOBJD.FIELD_LABEL,case when SYOBJD.EDITABLE_ONINSERT ='TRUE' then 'EDITABLE' 
				Else 'READ ONLY' end AS PERMISSION,SYPRSF.EDITABLE 
				FROM SYOBJD (NOLOCK)
				INNER JOIN SYSECT (NOLOCK) ON SYSECT.PRIMARY_OBJECT_NAME = SYOBJD.OBJECT_NAME
				INNER JOIN SYSEFL (NOLOCK) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID
				INNER JOIN SYPRSF (NOLOCK) ON SYPRSF.SECTIONFIELD_RECORD_ID = SYSEFL.RECORD_ID
				INNER JOIN USERS_PERMISSIONS UP ON UP.PERMISSION_ID = SYPRSF.PROFILE_RECORD_ID
				AND SYSEFL.API_FIELD_NAME = SYOBJD.API_NAME
				WHERE SYSEFL.RECORD_ID = '{0}' AND UP.USER_ID ='{1}' AND SYSEFL.SECTION_RECORD_ID = '{2}'""".format(str(sefl.RECORD_ID), str(User.Id),str(sect.RECORD_ID)))
			if permission_chk_query:
				if str(permission_chk_query.PERMISSION) == "EDITABLE" and str(col_name.REVISION_STATUS).upper() != "APPROVED":
					edit_lock_icon = "fa fa-pencil"
				else:
					edit_lock_icon = "fa fa-lock"  
			else:
				edit_lock_icon = "fa fa-lock"
			##edit_lock_icon in quote based on permission ends
			sec_str += "<div class='col-md-1' style='float: right;'> <div class='col-md-12 editiconright'><a href='#' onclick='editclick_row(this)' class='editclick'>	<i class='{icon}' aria-hidden='true'></i></a></div></div>".format(icon = edit_lock_icon)
			sec_str += "</div>"

			sec_str += "</div>"
		sec_str += "</div>"


			
	sec_str += '<table class="wth100mrg8"><tbody>'
	#Trace.Write("111111" + str(Qt_rec_id))

	sec_str += "</tbody></table></div>"
	sec_str += "</div>"
	#Trace.Write(str(sec_str))
	##Commented the below code because we dont need to return these fields..
	# if ACTION == "QUOTE_INFO" :
	# 	quote_id = str(eval("col_name.QUOTE_ID"))
	# 	accunt_id = str(eval("col_name.ACCOUNT_ID"))
	# 	accunt_name = str(eval("col_name.ACCOUNT_NAME"))
	# 	quote_type = str(eval("col_name.QUOTE_TYPE"))
	# 	sale_type = str(eval("col_name.SALE_TYPE"))
	# 	valid_from=str(eval("col_name.CONTRACT_VALID_FROM")).split(" ")[0]
	# 	valid_to = str(eval("col_name.CONTRACT_VALID_TO")).split(" ")[0]
	# else:
	# 	quote_id = ""
	# 	accunt_id = ""
	# 	accunt_name = ""
	# 	quote_type = ""
	# 	sale_type = ""
	# 	valid_from= ""
	# 	valid_to = ""	

	#return sec_str,quote_id,accunt_id,accunt_name,quote_type,sale_type,valid_from,valid_to
	#Trace.Write("sec_str --->"+str(sec_str))
	return sec_str


def constructCBC(Qt_rec_id, Quote, MODE):
	#Trace.Write('Constructing Clean Book Checklist')
	sec_str = ""      
	new_value_dict = {}
	ObjectName = "SAQCBC"
	table_id = "clean_booking_checklist"
	Header_details = {
		"CHECKLIST_ID": "SEQ",
		"CHECKLIST_DESCRIPTION":"QUESTIONS",
		"SERVICE_CONTRACT": "CM REVIEW",
		"SPECIALIST_REVIEW": "N/A",
		"COMMENT": "COMMENTS",    
	}
	ordered_keys = [
		"CHECKLIST_ID",
		"CHECKLIST_DESCRIPTION",
		"SERVICE_CONTRACT",
		"SPECIALIST_REVIEW",
		"COMMENT",    
	]
	dynamic_sect = Sql.GetList("SELECT TOP 1000 RECORD_ID,SECTION_NAME FROM SYSECT WHERE SECTION_DESC = '' AND PRIMARY_OBJECT_NAME = 'SAQCBC' AND SECTION_NAME NOT IN ('BASIC INFORMATION','AUDIT INFORMATION') ORDER BY DISPLAY_ORDER")
	for sect in dynamic_sect:
		sec_str += '<div id="container" class="wdth100 margtop10 ' + str(sect.RECORD_ID) + '">'
		sec_str += '<div onclick="dyn_main_sec_collapse_arrow(this)" data-target="" id="dyn1577" data-toggle="collapse" class="g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer"><label data-bind="html: hint" class="onlytext"><div class="height_auto"><div id="ctr_drop" class="btn-group dropdown cbc_ctr_drop"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list"><a id="'+str(sect.RECORD_ID)+'" class="dropdown-item" href="#" onclick="cbcEDIT(this)">EDIT</a></li></ul></div></div>'+str(sect.SECTION_NAME)+'</div></label> </div>'		
		sec_str += ('<table id="'+ str(table_id)+'_'+str(sect.RECORD_ID)+'" data-escape="true"  data-search-on-enter-key="true" data-show-header="true"  data-filter-control="true" class="table table-hover JColResizer" ondblclick=""> <thead><tr>')	
	
	
		for key, invs in enumerate(list(ordered_keys)):

			invs = str(invs).strip()
			qstring = Header_details.get(str(invs)) or ""    
			sec_str += (
				'<th data-field="'
				+ invs
				+ '" data-title-tooltip="'
				+ str(qstring)
				+ '" data-sortable="true" data-filter-control="input">'
				+ str(qstring)
				+ "</th>"
			)
		sec_str +=('<th> </th>')	
		sec_str += '</tr></thead><tbody class ="cleanbook_chklst" >'
		checklist_vals = Sql.GetList("select TOP 1000 CHECKLIST_ID,CHECKLIST_DESCRIPTION,SERVICE_CONTRACT,SPECIALIST_REVIEW,COMMENT FROM SAQCBC(NOLOCK) WHERE QUOTE_RECORD_ID = '{quote_recid}' AND QTEREV_RECORD_ID = '{quote_revision_recid}' ORDER BY CpqTableEntryId ASC".format(quote_recid=Quote,quote_revision_recid=quote_revision_record_id))
		for value in checklist_vals:
			if sect.SECTION_NAME =="TERMS AND CONDITIONS VALIDATION" and str(value.CHECKLIST_ID) in ['1','2','3','4','4.1','4.2','4.3','4.4']:
				if '.' in str(value.CHECKLIST_ID):				
					sec_str +='<tr class ="cbc_child">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"></a></div></td>')
					sec_str += '</tr>'
				else:
					sec_str +='<tr class ="cbc_parent">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str += ('<td class="wid_90"><input id="SERVICE_CONTRACT" type="checkbox" value="'+str(value.SERVICE_CONTRACT)+'" title="'+str(value.SERVICE_CONTRACT)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SERVICE_CONTRACT).upper() == "TRUE" or str(value.SERVICE_CONTRACT) =="1" else ""))
					sec_str += ('<td class="wid_90"><input id="SPECIALIST_REVIEW" type="checkbox" value="'+str(value.SPECIALIST_REVIEW)+'" title="'+str(value.SPECIALIST_REVIEW)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SPECIALIST_REVIEW).upper() == "TRUE" or str(value.SPECIALIST_REVIEW) =="1" else ""))
					sec_str += ('<td class="wid_90"><textarea id="COMMENT" type="text" title="'+str(value.COMMENT)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.COMMENT)+'</textarea></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td>')
					sec_str += '</tr>'

			elif sect.SECTION_NAME =="IF THE CUSTOMER HAS A MASTER SERVICE AGREEMENT" and str(value.CHECKLIST_ID) in ['5','6','7','8','9','10','11','12','12.1','12.2','12.3']:
				if '.' in str(value.CHECKLIST_ID):				
					sec_str +='<tr class ="cbc_child">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"></a></div></td>')
					sec_str += '</tr>'
				else:
					sec_str +='<tr class ="cbc_parent">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str += ('<td class="wid_90"><input id="SERVICE_CONTRACT" type="checkbox" value="'+str(value.SERVICE_CONTRACT)+'" title="'+str(value.SERVICE_CONTRACT)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SERVICE_CONTRACT).upper() == "TRUE" or str(value.SERVICE_CONTRACT) =="1" else ""))
					sec_str += ('<td class="wid_90"><input id="SPECIALIST_REVIEW" type="checkbox" value="'+str(value.SPECIALIST_REVIEW)+'" title="'+str(value.SPECIALIST_REVIEW)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SPECIALIST_REVIEW).upper() == "TRUE" or str(value.SPECIALIST_REVIEW) =="1" else ""))
					sec_str += ('<td class="wid_90"><textarea id="COMMENT" type="text" title="'+str(value.COMMENT)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.COMMENT)+'</textarea></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td>')
					sec_str += '</tr>'

			elif sect.SECTION_NAME =="VALIDATE CANCELLATION FOR CONVENIENCE DAYS IN CRM ARE RECORDED ACCORDING TO TS&CS IN THE BOOKING PACKAGE (I.E. SOW, PO, CL, MSA, ETC...) AND ENTER 0, NA, OR THE NUMBER OF DAYS BASED ON THESE RULES:(DO NOT INCLUDE POSS CANCELLATION TERMS WITH SERVICE TERMS. IF MULTIPLE CANCELLATION TERMS FOR SERVICE PRODUCTS, SPLIT OUT)" and str(value.CHECKLIST_ID) in ['13','14','15','16','17']:
				if '.' in str(value.CHECKLIST_ID):				
					sec_str +='<tr class ="cbc_child">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"></a></div></td>')
					sec_str += '</tr>'
				else:
					sec_str +='<tr class ="cbc_parent">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str += ('<td class="wid_90"><input id="SERVICE_CONTRACT" type="checkbox" value="'+str(value.SERVICE_CONTRACT)+'" title="'+str(value.SERVICE_CONTRACT)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SERVICE_CONTRACT).upper() == "TRUE" or str(value.SERVICE_CONTRACT) =="1" else ""))
					sec_str += ('<td class="wid_90"><input id="SPECIALIST_REVIEW" type="checkbox" value="'+str(value.SPECIALIST_REVIEW)+'" title="'+str(value.SPECIALIST_REVIEW)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SPECIALIST_REVIEW).upper() == "TRUE" or str(value.SPECIALIST_REVIEW) =="1" else ""))
					sec_str += ('<td class="wid_90"><textarea id="COMMENT" type="text" title="'+str(value.COMMENT)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.COMMENT)+'</textarea></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td>')
					sec_str += '</tr>'

			elif sect.SECTION_NAME =="EQUIPMENT NUMBERS" and str(value.CHECKLIST_ID) in ['18']:
				if '.' in str(value.CHECKLIST_ID):				
					sec_str +='<tr class ="cbc_child">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"></a></div></td>')
					sec_str += '</tr>'
				else:
					sec_str +='<tr class ="cbc_parent">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str += ('<td class="wid_90"><input id="SERVICE_CONTRACT" type="checkbox" value="'+str(value.SERVICE_CONTRACT)+'" title="'+str(value.SERVICE_CONTRACT)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SERVICE_CONTRACT).upper() == "TRUE" or str(value.SERVICE_CONTRACT) =="1" else ""))
					sec_str += ('<td class="wid_90"><input id="SPECIALIST_REVIEW" type="checkbox" value="'+str(value.SPECIALIST_REVIEW)+'" title="'+str(value.SPECIALIST_REVIEW)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SPECIALIST_REVIEW).upper() == "TRUE" or str(value.SPECIALIST_REVIEW) =="1" else ""))
					sec_str += ('<td class="wid_90"><textarea id="COMMENT" type="text" title="'+str(value.COMMENT)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.COMMENT)+'</textarea></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td>')
					sec_str += '</tr>'

			elif sect.SECTION_NAME =="CUSTOMER PURCHASE ORDER OR SIGNED AGREEMENT" and str(value.CHECKLIST_ID) in ['19','20','21','22','23']:
				if '.' in str(value.CHECKLIST_ID):				
					sec_str +='<tr class ="cbc_child">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"></a></div></td>')
					sec_str += '</tr>'
				else:
					sec_str +='<tr class ="cbc_parent">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str += ('<td class="wid_90"><input id="SERVICE_CONTRACT" type="checkbox" value="'+str(value.SERVICE_CONTRACT)+'" title="'+str(value.SERVICE_CONTRACT)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SERVICE_CONTRACT).upper() == "TRUE" or str(value.SERVICE_CONTRACT) =="1" else ""))
					sec_str += ('<td class="wid_90"><input id="SPECIALIST_REVIEW" type="checkbox" value="'+str(value.SPECIALIST_REVIEW)+'" title="'+str(value.SPECIALIST_REVIEW)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SPECIALIST_REVIEW).upper() == "TRUE" or str(value.SPECIALIST_REVIEW) =="1" else ""))
					sec_str += ('<td class="wid_90"><textarea id="COMMENT" type="text" title="'+str(value.COMMENT)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.COMMENT)+'</textarea></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td>')
					sec_str += '</tr>'

			elif sect.SECTION_NAME =="BILL PLAN VERIFICATION" and str(value.CHECKLIST_ID) in ['24','25']:
				if '.' in str(value.CHECKLIST_ID):				
					sec_str +='<tr class ="cbc_child">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"></a></div></td>')
					sec_str += '</tr>'
				else:
					sec_str +='<tr class ="cbc_parent">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str += ('<td class="wid_90"><input id="SERVICE_CONTRACT" type="checkbox" value="'+str(value.SERVICE_CONTRACT)+'" title="'+str(value.SERVICE_CONTRACT)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SERVICE_CONTRACT).upper() == "TRUE" or str(value.SERVICE_CONTRACT) =="1" else ""))
					sec_str += ('<td class="wid_90"><input id="SPECIALIST_REVIEW" type="checkbox" value="'+str(value.SPECIALIST_REVIEW)+'" title="'+str(value.SPECIALIST_REVIEW)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SPECIALIST_REVIEW).upper() == "TRUE" or str(value.SPECIALIST_REVIEW) =="1" else ""))
					sec_str += ('<td class="wid_90"><textarea id="COMMENT" type="text" title="'+str(value.COMMENT)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.COMMENT)+'</textarea></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td>')
					sec_str += '</tr>'

			elif sect.SECTION_NAME =="NSOS/UPGRADES" and str(value.CHECKLIST_ID) in ['26','27']:
				if '.' in str(value.CHECKLIST_ID):				
					sec_str +='<tr class ="cbc_child">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"></a></div></td>')
					sec_str += '</tr>'
				else:
					sec_str +='<tr class ="cbc_parent">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str += ('<td class="wid_90"><input id="SERVICE_CONTRACT" type="checkbox" value="'+str(value.SERVICE_CONTRACT)+'" title="'+str(value.SERVICE_CONTRACT)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SERVICE_CONTRACT).upper() == "TRUE" or str(value.SERVICE_CONTRACT) =="1" else ""))
					sec_str += ('<td class="wid_90"><input id="SPECIALIST_REVIEW" type="checkbox" value="'+str(value.SPECIALIST_REVIEW)+'" title="'+str(value.SPECIALIST_REVIEW)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SPECIALIST_REVIEW).upper() == "TRUE" or str(value.SPECIALIST_REVIEW) =="1" else ""))
					sec_str += ('<td class="wid_90"><textarea id="COMMENT" type="text" title="'+str(value.COMMENT)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.COMMENT)+'</textarea></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td>')
					sec_str += '</tr>'

			elif sect.SECTION_NAME =="MULTI-ELEMENT ARRANGEMENT" and str(value.CHECKLIST_ID) in ['28','28.1','28.2','28.3']:
				if '.' in str(value.CHECKLIST_ID):				
					sec_str +='<tr class ="cbc_child">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str +=('<td class="wid_90"></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"></a></div></td>')
					sec_str += '</tr>'
				else:
					sec_str +='<tr class ="cbc_parent">'
					sec_str += ('<td><input id="CHECKLIST_ID" type="text" value="'+str(value.CHECKLIST_ID)+'" title="'+str(value.CHECKLIST_ID)+'" class="form-control related_popup_css fltlt" disabled></td>')
					sec_str += ('<td><abbr id="CHECKLIST_DESCRIPTION" title="'+str(value.CHECKLIST_DESCRIPTION)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.CHECKLIST_DESCRIPTION)+'</abbr></td>')
					sec_str += ('<td class="wid_90"><input id="SERVICE_CONTRACT" type="checkbox" value="'+str(value.SERVICE_CONTRACT)+'" title="'+str(value.SERVICE_CONTRACT)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SERVICE_CONTRACT).upper() == "TRUE" or str(value.SERVICE_CONTRACT) =="1" else ""))
					sec_str += ('<td class="wid_90"><input id="SPECIALIST_REVIEW" type="checkbox" value="'+str(value.SPECIALIST_REVIEW)+'" title="'+str(value.SPECIALIST_REVIEW)+'" class="custom" style = "z-index:-5" {checked}><span class="lbl"></span></td>'.format(checked = "checked disabled" if str(value.SPECIALIST_REVIEW).upper() == "TRUE" or str(value.SPECIALIST_REVIEW) =="1" else ""))
					sec_str += ('<td class="wid_90"><textarea id="COMMENT" type="text" title="'+str(value.COMMENT)+'" class="form-control related_popup_css fltlt" disabled>'+str(value.COMMENT)+'</textarea></td>')
					sec_str+=('<td class="wid_90"><div class="col-md-12 editiconright"><a href="#" class="editclick"><i class="fa fa-pencil" aria-hidden="true"></i></a></div></td>')
					sec_str += '</tr>'

		sec_str += '</tbody></table></div>'
		
	values_lists = ""
	a_test = []
	for invsk in list(Header_details):
		table_ids = "#" + str(table_id)
		filter_class = table_ids + " .bootstrap-table-filter-control-" + str(invsk)
		values_lists += "var " + str(invsk) + ' = $("' + str(filter_class) + '").val(); '
		values_lists += " ATTRIBUTE_VALUEList.push(" + str(invsk) + "); "
		a_test.append(invsk)
		
						
	return sec_str

def editcbc(Qt_rec_id, Quote, MODE):	
	for val in values:
		if '.' not in val['CHECKLIST_ID']:
			val['COMMENT'] = val['COMMENT'].replace("'", "").replace("<", "").replace(">", "")
			Sql.RunQuery("UPDATE SAQCBC SET SERVICE_CONTRACT = '{service_contract}',SPECIALIST_REVIEW = '{specialist_review}',COMMENT = '{comment}' WHERE CHECKLIST_ID = '{checklist_id}' AND QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_rev_recid}' ".format(checklist_id = val['CHECKLIST_ID'] if val['CHECKLIST_ID'] !="" else "",service_contract = val['SERVICE_CONTRACT'],specialist_review = val['SPECIALIST_REVIEW'],comment = val['COMMENT'],quote_rec_id = Quote,quote_rev_recid = quote_revision_record_id))
			
	return True

def countcbc(Qt_rec_id, Quote, MODE):
	popupquery=Sql.GetFirst("SELECT COUNT(*) as cnt FROM SAQCBC WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_rev_recid}' AND SERVICE_CONTRACT='False' AND SPECIALIST_REVIEW='FALSE' AND CHECKLIST_ID NOT IN('4.1','4.2','4.3','4.4','12.1','12.2','12.3','28.1','28.2','28.3')".format(quote_rec_id = Quote,quote_rev_recid = quote_revision_record_id))
	popupquery_value = popupquery.cnt
	return popupquery_value

def savecbc(Qt_rec_id, Quote, MODE):
	#CBD POPUP FUNCTIONALITY ADDED UPDATE QUERY
	Sql.RunQuery("UPDATE SAQTRV SET REVISION_STATUS = 'SUBMITTED FOR BOOKING' WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_rev_recid}' AND ACTIVE = '1' ".format(quote_rec_id = Quote,quote_rev_recid = quote_revision_record_id))	
	Sql.RunQuery("UPDATE SAQTRV SET WORKFLOW_STATUS = 'BOOKED' WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_rev_recid}' AND ACTIVE = '1' ".format(quote_rec_id = Quote,quote_rev_recid = quote_revision_record_id))
	get_quote_details = Sql.GetFirst("Select QUOTE_ID,QTEREV_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_rev_recid}' AND ACTIVE = '1' ".format(quote_rec_id = Quote,quote_rev_recid = quote_revision_record_id))
	##FPM QUOTE SCENARIO
	getfpm_quote_type = Sql.GetFirst("SELECT DOCTYP_ID,QUOTE_ID,QTEREV_ID FROM SAQTRV(NOLOCK) WHERE QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID ='{}' AND DOCTYP_ID = 'ZWK1' ".format(Quote,quote_revision_record_id))
	if getfpm_quote_type:
		Log.Info("====> QTPOSTACRM for FPM called from ==> "+str(getfpm_quote_type.QUOTE_ID)+'--'+str(getfpm_quote_type.QTEREV_ID))
		ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':getfpm_quote_type.QUOTE_ID,'REVISION_ID':getfpm_quote_type.QTEREV_ID, 'Fun_type':'CPQ_TO_ECC'})
	##Calling the iflow script to insert the records into SAQRSH custom table(Capture Date/Time for Quote Revision Status update.)
	CQREVSTSCH.Revisionstatusdatecapture(Quote,quote_revision_record_id)

	#Added query and condition to restrict calling contract creation webservice based on document type = ZWK1(Scripting logic to prevent ZWK1 quote from being pushed to CRM) - start
	revision_document_type_object = Sql.GetFirst("SELECT DOCTYP_ID FROM SAQTRV WHERE QUOTE_RECORD_ID = '{quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_rev_recid}' AND ACTIVE = '1' ".format(quote_rec_id = Quote,quote_rev_recid = quote_revision_record_id))
	if revision_document_type_object:
		if revision_document_type_object.DOCTYP_ID != "ZWK1" and revision_document_type_object.DOCTYP_ID != "":
			crm_result = ScriptExecutor.ExecuteGlobal('QTPOSTACRM',{'QUOTE_ID':str(get_quote_details.QUOTE_ID),'REVISION_ID':str(get_quote_details.QTEREV_ID),'Fun_type':'cpq_to_crm'})
	#Added query and condition to restrict calling contract creation webservice based on document type = ZWK1(Scripting logic to prevent ZWK1 quote from being pushed to CRM) - end	
	
	##Calling the iflow script to update the details in c4c..(cpq to c4c write back...)
	CQCPQC4CWB.writeback_to_c4c("quote_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
	CQCPQC4CWB.writeback_to_c4c("opportunity_header",Quote.GetGlobal("contract_quote_record_id"),Quote.GetGlobal("quote_revision_record_id"))
	return True

def save_annualiziedgrid_inline(Quote,line,CAT1,CAT2,CAT3,CAT4,CAT5,CAT6,CAT7,CAT8,CAT9,CAT10,CAT11,CAT12,CAT13,CAT14,MODE):
	Trace.Write("value===values"+str(Quote))
	#Trace.Write("value===values2"+str(list(eval(values))))
	get_quote_details =Sql.GetFirst("Select * FROM SAQTMT(NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID ='{Quote}' ".format(Quote = Quote))
	for index,val in enumerate(line):
		#Trace.Write("UPDATE SAQICO SET UIMVCI = '"+str(CAT1[index])+"' , UIMVPI = '"+str(CAT2[index])+"',CAVVCI = '"+str(CAT3[index])+"',CAVVPI = '"+str(CAT4[index])+"',ATGKEY = '"+str(CAT5[index])+"',ATGKEC = '"+str(CAT6[index])+"',ATGKEP = '"+str(CAT7[index])+"',NWPTOC = '"+str(CAT8[index])+"',NWPTOP = '"+str(CAT9[index])+"',AMNCCI = '"+str(CAT10[index])+"',AMNPPI = '"+str(CAT11[index])+"',USRPRC = '"+str(CAT12[index])+"',YOYPCT = '"+str(CAT13[index])+"',TGADJP = '"+str(CAT14[index])+"' WHERE LINE = '"+line[index]+"' AND QUOTE_RECORD_ID ='{quote_rec_id}' AND QTEREV_RECORD_ID ='{quo_rev_rec_id}'".format(quote_rec_id = get_quote_details.MASTER_TABLE_QUOTE_RECORD_ID,quo_rev_rec_id = get_quote_details.QTEREV_RECORD_ID))
		#update_saqico = "UPDATE SAQICO SET UIMVCI = '"+str(CAT1[index])+"' , UIMVPI = '"+str(CAT2[index])+"',CAVVCI = '"+str(CAT3[index])+"',CAVVPI = '"+str(CAT4[index])+"',ATGKEY = '"+str(CAT5[index])+"',ATGKEC = '"+str(CAT6[index])+"',ATGKEP = '"+str(CAT7[index])+"',NWPTOC = '"+str(CAT8[index])+"',NWPTOP = '"+str(CAT9[index])+"',AMNCCI = '"+str(CAT10[index])+"',AMNPPI = '"+str(CAT11[index])+"',USRPRC = '"+str(CAT12[index])+"',YOYPCT = '"+str(CAT13[index])+"',TGADJP = '"+str(CAT14[index])+"' WHERE LINE = '"+line[index]+"' AND QUOTE_RECORD_ID ='{quote_rec_id}' AND QTEREV_RECORD_ID ='{quo_rev_rec_id}'".format(quote_rec_id = get_quote_details.MASTER_TABLE_QUOTE_RECORD_ID,quo_rev_rec_id = get_quote_details.QTEREV_RECORD_ID)
		update_saqico = "UPDATE SAQICO SET UIMVCI = '"+str(CAT1[index])+"' , UIMVPI = '"+str(CAT2[index])+"' WHERE LINE = '"+line[index]+"' AND QUOTE_RECORD_ID ='{quote_rec_id}' AND QTEREV_RECORD_ID ='{quo_rev_rec_id}'".format(quote_rec_id = get_quote_details.MASTER_TABLE_QUOTE_RECORD_ID,quo_rev_rec_id = get_quote_details.QTEREV_RECORD_ID)
		Sql.RunQuery(update_saqico)
	return True
def constructlegalsow(Qt_rec_id, Quote, MODE):    
	VAR1 = ""
	sec_str = ""
	add_style = ""
	API_NAME_LIST = []
	PModel = "disabled"
	sec_rec_id = "AED0A92A-8644-46AE-ACF0-90D6E331E506"
	editclick = "legalsowEDIT(this)"
	#editclick = "CommonEDIT(this)"
	edit_action = ""
	Oppp_SECT = Sql.GetList(
		"SELECT TOP 1000 RECORD_ID,SECTION_NAME FROM SYSECT WHERE PRIMARY_OBJECT_NAME = 'SAQTRV' and RECORD_ID = 'AED0A92A-8644-46AE-ACF0-90D6E331E506' ORDER BY DISPLAY_ORDER"
	)
	for sect in Oppp_SECT:
		sec_str += '<div id="container" class="wdth100 margtop10 ' + str(sect.RECORD_ID) + '">'
		# if (str(sect.SECTION_NAME) == "CONTRACT BOOKING INFORMATION" or str(sect.SECTION_NAME) == "AUDIT INFORMATION" ):
		#     sec_str += (
		#         '<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down mt-10px" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_'
		#         + str(sect.RECORD_ID)
		#         + '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>'
		#         + str(sect.SECTION_NAME)
		#         + "</div></label></div>"
		#     )
		
		# else:
		sec_html_btn = Sql.GetFirst("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE ACTION_NAME = 'EDIT' AND SECTION_RECORD_ID = '"+str(sect.RECORD_ID)+"'")
		if sec_html_btn is not None:
			edit_action = str(sec_html_btn.HTML_CONTENT).format(rec_id = str(sect.RECORD_ID), edit_click = str(editclick))
		else:
			edit_action = ''
		sec_str += (
			'''<div onclick="dyn_main_sec_collapse_arrow(this)" 
			data-bind="attr: {'data-toggle':'collapse','data-target':'.col'+stdAttrCode(), 
			'id':'dyn'+stdAttrCode(),'class': isWholeRow() ? 'g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer' : 'g1 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer'}" 
				data-target=".sec_'''+str(sect.RECORD_ID)+'''"  id="dyn1577"  data-toggle="collapse"  class="g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer"> 
			<label data-bind="html: hint" class="onlytext"><div>'''+ str(edit_action) + str(sect.SECTION_NAME)+'''</div></label> </div>'''
		)

		Oppp_SEFL = Sql.GetList(
			"SELECT TOP 1000 SYSEFL.FIELD_LABEL, SYSEFL.API_FIELD_NAME,SYSEFL.API_NAME,SYOBJD.REQUIRED FROM SYSEFL SYSEFL JOIN SYOBJD SYOBJD ON SYSEFL.API_FIELD_NAME = SYOBJD.API_NAME WHERE SYSEFL.SECTION_RECORD_ID = '" + str(sect.RECORD_ID) + "' and OBJECT_NAME='SAQTRV' ORDER BY SYSEFL.DISPLAY_ORDER"
		)
		for sefl in Oppp_SEFL:
			sec_str += '<div id="sec_' + str(sect.RECORD_ID) + '" class= "sec_' + str(sect.RECORD_ID) + ' collapse in">'
			sec_str += "<div style='height:30px;border-left: 0;border-right: 0;border-bottom:1px solid  #dcdcdc;' data-bind='attr: {'id':'mat'+stdAttrCode(),'class': isWholeRow() ? 'g4  except_sec removeHorLine iconhvr' : 'g1 except_sec removeHorLine iconhvr' }' id='mat1578' class='g4  except_sec removeHorLine iconhvr'>"
			if sefl.REQUIRED == "True" or sefl.REQUIRED == "1" or sefl.REQUIRED == True:
				mandatory = '<span class="req-field mrg3fltltmt7"  >*</span>'
				sec_str += (
					"<div class='col-md-5'>	<abbr data-bind='attr:{'title':label}' title='"
					+ str(sefl.FIELD_LABEL)
					+ "'> <label class='col-md-11 pull-left' style='padding: 5px 5px;margin: 0;' data-bind='html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), 'pull-left': hint() }'>"
					+ str(sefl.FIELD_LABEL)
					+ "</label><span class='req-field mrg3fltltmt7' >*</span></abbr> <a href='#' title='"+str(sefl.FIELD_LABEL)+"' data-placement='auto top' data-toggle='popover' data-trigger='focus' data-content='"+str(sefl.FIELD_LABEL)+"' class='col-md-1 bgcccwth10' style='text-align:right;padding: 7px 5px;color:green;' data-original-title=''><i title='"+str(sefl.FIELD_LABEL)+"' class='fa fa-info-circle fltlt'></i></a> </div>"
				)
			else:
				sec_str += (
					"<div class='col-md-5'>	<abbr data-bind='attr:{'title':label}' title='"
					+ str(sefl.FIELD_LABEL)
					+ "'> <label class='col-md-11 pull-left' style='padding: 5px 5px;margin: 0;' data-bind='html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), 'pull-left': hint() }'>"
					+ str(sefl.FIELD_LABEL)
					+ "</label></abbr> <a href='#' title='"+str(sefl.FIELD_LABEL)+"' data-placement='auto top' data-toggle='popover' data-trigger='focus' data-content='"+str(sefl.FIELD_LABEL)+"' class='col-md-1 bgcccwth10' style='text-align:right;padding: 7px 5px;color:green;' data-original-title=''><i title='"+str(sefl.FIELD_LABEL)+"' class='fa fa-info-circle fltlt'></i></a> </div>"
				)
			sefl_api = sefl.API_FIELD_NAME
			object_name = sefl.API_NAME
			syobjd_obj = Sql.GetFirst("SELECT DATA_TYPE FROM SYOBJD WHERE API_NAME = '{}' and OBJECT_NAME ='{}'".format(sefl_api,object_name))
			data_type = syobjd_obj.DATA_TYPE
			col_name = Sql.GetFirst("SELECT * FROM SAQTRV WHERE QUOTE_RECORD_ID = '" + str(Quote) + "'")
			if col_name:
				if sefl_api == "CpqTableEntryModifiedBy":
					current_obj_value = col_name.CpqTableEntryModifiedBy
					current_user = Sql.GetFirst(
						"SELECT USERNAME FROM USERS WHERE ID = " + str(current_obj_value) + ""
					).USERNAME
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' value = '"
						+ str(current_user)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					)
				elif data_type =="CHECKBOX":
					act_status = (eval("col_name." + str(sefl_api)))
					if act_status == True  or act_status == 1:
						sec_str += (
							'<div class="col-md-3 padtop5 padleft10"><input id="'
							+ str(sefl_api)
							+ '" type="CHECKBOX" value="'
							+ str(act_status)
							+ '" class="custom" '
							+ 'disabled checked><span class="lbl"></span></div>'
						)
					else:
						sec_str += (
							'<div class="col-md-3 padtop5 padleft10"><input id="'
							+ str(sefl_api)
							+ '" type="CHECKBOX" value="'
							+ str(act_status)
							+ '" class="custom" '
							+ 'disabled ><span class="lbl"></span></div>'
						)
				elif data_type =="PICKLIST":
					Sql_Quality_Tier = Sql.GetFirst(
						"select PICKLIST_VALUES FROM  SYOBJD WITH (NOLOCK) where OBJECT_NAME='SAQTRV' and DATA_TYPE='PICKLIST' and API_NAME = '"
						+ str(sefl_api)
						+ "' "
					)
					sec_str += (
						'<div class="col-md-3 padtop5 padleft10"><select id="'
						+ str(sefl_api) 
						+ '" type="text" class="form-control pop_up_brd_rad related_popup_css fltlt" value="'
						+ str(eval("col_name." + str(sefl_api)))
						+ '" class="custom" '
						+ 'disabled ><option value="Select"></option>'
					)
					if (
						str(Sql_Quality_Tier.PICKLIST_VALUES).strip() is not None
						and str(Sql_Quality_Tier.PICKLIST_VALUES).strip() != ""
					):						
						Tier_List = (Sql_Quality_Tier.PICKLIST_VALUES).split(",")		
						for req1 in Tier_List:
							req1 = req1.strip()							
							if str(eval("col_name." + str(sefl_api))) == req1:								
								sec_str += "<option selected>" + str(req1) + "</option>"
							else:								
								sec_str += "<option>" + str(req1) + "</option>"
					else:						
						sec_str += "<option selected>" + str(sefl_api) + "</option>"
					sec_str += "</select></div>"
				else:
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' value = '"
						+ str(eval("col_name." + str(sefl_api)))
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='"
						+ str(eval("col_name." + str(sefl_api)))
						+ "' tabindex='' disabled=''> </div>"
					)
			else:

				sec_str += "<div class='col-md-3 pad-0'> <input type='text' value = '' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
			sec_str += "<div class='col-md-3' style='display:none;'> <span class='' data-bind='attr:{'id': $data.name()}' id=''>  </div>"
			permission_chk_query = Sql.GetFirst("SELECT PERMISSION FROM SYOBJD where OBJECT_NAME = 'SAQTRV' and API_NAME = '"+str(sefl_api)+"'")
				
			if permission_chk_query:
				if str(permission_chk_query.PERMISSION) == "EDITABLE" and str(col_name.REVISION_STATUS).upper() != "APPROVED":
					edit_lock_icon = "fa fa-pencil"
				else:
					edit_lock_icon = "fa fa-lock"  
			else:
				edit_lock_icon = "fa fa-lock"
			##edit_lock_icon in quote based on permission ends
			sec_str += "<div class='col-md-1' style='float: right;'> <div class='col-md-12 editiconright'><a href='#' onclick='editclick_row(this)' class='editclick'>	<i class='{icon}' aria-hidden='true'></i></a></div></div>".format(icon = edit_lock_icon)
			#sec_str += "<div class='col-md-1' style='float: right;'> <div class='col-md-12 editiconright'><a href='#' onclick='editclick_row(this)' class='editclick'>	<i class='fa fa-lock' aria-hidden='true'></i></a></div></div>"
			sec_str += "</div>"

			sec_str += "</div>"
		sec_str += "</div>"
	sec_str += '<table class="wth100mrg8"><tbody>'
	#Trace.Write("111111" + str(Qt_rec_id))

	sec_str += "</tbody></table></div>"
	sec_str += "</div>"
	#Trace.Write(str(sec_str))
	return sec_str
# def constructidlingattributes(Qt_rec_id, Quote, MODE):    
# 	anchor_tag_id_value = ""
# 	VAR1 = ""
# 	sec_str = ""
# 	quote_id=""
# 	add_style = ""
# 	API_NAME_LIST = []
# 	PModel = "disabled"
# 	editclick = "QuoteinformationEDIT(this)"
# 	edit_action = ""
# 	#sec_rec_id = "B0B5E48B-DC63-4B1A-95AC-695973D3AA06"
# 	if ACTION == "CONTRACT_ATTR":
# 		primary_objname = "CTCNRT"
# 	else:
# 		primary_objname = "SAQTMT"

# 	Oppp_SECT = Sql.GetList(
# 		"SELECT TOP 1000 RECORD_ID,SECTION_NAME FROM SYSECT WHERE SECTION_DESC != '' AND PRIMARY_OBJECT_NAME = '{primary_objname}' ORDER BY DISPLAY_ORDER".format(primary_objname = primary_objname)
# 	)
# 	for sect in Oppp_SECT:
# 		sec_str += '<div id="container" class="wdth100 margtop10 ' + str(sect.RECORD_ID) + '">'
# 		# if (str(sect.SECTION_NAME) == "CONTRACT BOOKING INFORMATION" or str(sect.SECTION_NAME) == "AUDIT INFORMATION" ):
# 		#     sec_str += (
# 		#         '<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down mt-10px" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_'
# 		#         + str(sect.RECORD_ID)
# 		#         + '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>'
# 		#         + str(sect.SECTION_NAME)
# 		#         + "</div></label></div>"
# 		#     )
		
# 		# else:
# 		sec_html_btn = Sql.GetFirst("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE ACTION_NAME = 'EDIT' AND SECTION_RECORD_ID = '"+str(sect.RECORD_ID)+"'")
# 		if sec_html_btn is not None:
# 			edit_action = str(sec_html_btn.HTML_CONTENT).format(rec_id = str(sect.RECORD_ID), edit_click = str(editclick))
# 		else:
# 			edit_action = ''
# 		sec_str += (
# 			'''<div onclick="dyn_main_sec_collapse_arrow(this)" 
# 			data-bind="attr: {'data-toggle':'collapse','data-target':'.col'+stdAttrCode(), 
# 			'id':'dyn'+stdAttrCode(),'class': isWholeRow() ? 'g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer' : 'g1 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer'}" 
# 				data-target=".sec_'''+str(sect.RECORD_ID)+'''"  id="dyn1577"  data-toggle="collapse"  class="g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer"> 
# 			<label data-bind="html: hint" class="onlytext"><div>'''+ str(edit_action) + str(sect.SECTION_NAME)+'''</div></label> </div>'''
# 		)
		


# 		Oppp_SEFL = Sql.GetList(
# 			"SELECT TOP 1000 FIELD_LABEL, API_FIELD_NAME,RECORD_ID FROM SYSEFL WHERE SECTION_RECORD_ID = '" + str(sect.RECORD_ID) + "' ORDER BY DISPLAY_ORDER"
# 		)
# 		for sefl in Oppp_SEFL:
# 			sec_str += '<div id="sec_' + str(sect.RECORD_ID) + '" class=  "sec_' + str(sect.RECORD_ID) + ' collapse in "> '
# 			if (sefl.FIELD_LABEL) == "Key":
# 				sec_str += "<div style='height:30px;border-left: 0;border-right: 0;border-bottom:1px solid  #dcdcdc; display:none' data-bind='attr: {'id':'mat'+stdAttrCode(),'class': isWholeRow() ? 'g4  except_sec removeHorLine iconhvr' : 'g1 except_sec removeHorLine iconhvr' }' id='mat1578' class='g4  except_sec removeHorLine iconhvr'>"
# 				sec_str += (
# 					"<div class='col-md-5'>	<abbr data-bind='attr:{'title':label}' title='"
# 					+ str(sefl.FIELD_LABEL)
# 					+ "'> <label class='col-md-11 pull-left' style='padding: 5px 5px;margin: 0;' data-bind='html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), 'pull-left': hint() }'>"
# 					+ str(sefl.FIELD_LABEL)
# 					+ "</label> </abbr> <a href='#' title='' data-placement='auto top' data-toggle='popover' data-trigger='focus' data-content='"+str(sefl.FIELD_LABEL)+"' class='col-md-1 bgcccwth10' style='text-align:right;padding: 7px 5px;color:green;' data-original-title=''><i title='"+str(sefl.FIELD_LABEL)+"' class='fa fa-info-circle fltlt'></i></a> </div>"
# 				)
# 			else:	
# 				sec_str += "<div style='height:30px;border-left: 0;border-right: 0;border-bottom:1px solid  #dcdcdc;' data-bind='attr: {'id':'mat'+stdAttrCode(),'class': isWholeRow() ? 'g4  except_sec removeHorLine iconhvr' : 'g1 except_sec removeHorLine iconhvr' }' id='mat1578' class='g4  except_sec removeHorLine iconhvr'>"
# 				sec_str += (
# 					"<div class='col-md-5'>	<abbr data-bind='attr:{'title':label}' title='"
# 					+ str(sefl.FIELD_LABEL)
# 					+ "'> <label class='col-md-11 pull-left' style='padding: 5px 5px;margin: 0;' data-bind='html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), 'pull-left': hint() }'>"
# 					+ str(sefl.FIELD_LABEL)
# 					+ "</label> </abbr> <a href='#' title='' data-placement='auto top' data-toggle='popover' data-trigger='focus' data-content='"+str(sefl.FIELD_LABEL)+"' class='col-md-1 bgcccwth10' style='text-align:right;padding: 7px 5px;color:green;' data-original-title=''><i title='"+str(sefl.FIELD_LABEL)+"' class='fa fa-info-circle fltlt'></i></a> </div>"
# 				)
# 			sefl_api = sefl.API_FIELD_NAME
# 			if ACTION == "CONTRACT_ATTR": 
# 				col_name = Sql.GetFirst("SELECT * from CTCNRT (NOLOCK) WHERE CONTRACT_RECORD_ID = '{contract_record_id}' ".format(contract_record_id= str(contract_record_id) ))
				
# 			else:
# 				col_name = Sql.GetFirst("SELECT * FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '" + str(Quote) + "' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) + "'") 
# 			if col_name:
# 				if sefl_api == "MASTER_TABLE_QUOTE_RECORD_ID":
# 					cpq_key_id = CPQID.KeyCPQId.GetCPQId("SAQTMT", str(eval("col_name." + str(sefl_api))))
# 					sec_str += (
# 						"<div class='col-md-3 pad-0'> <input id= 'key_field_id' type='text' title = '"+ str(cpq_key_id)+"' value = '"
# 						+ str(cpq_key_id)
# 						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
# 					)				
# 				else:
# 					# if sefl_api != "REGION":
# 					Trace.Write('At line 289-->'+str(sefl_api))
# 					sec_str += (
# 						"<div class='col-md-3 pad-0'> <input type='text' id ='"+str(sefl_api)+"' title = '"+  str(eval("col_name." + str(sefl_api)))+"' value = '"
# 						+ str(eval("col_name." + str(sefl_api)))
# 						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
# 					)
# 					# else:
# 					#     sec_str += (
# 					#         "<div class='col-md-3 pad-0'> <input type='text' value = '' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
# 					#     )
# 			else:

# 				sec_str += "<div class='col-md-3 pad-0'> <input type='text' value = '' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
# 			sec_str += "<div class='col-md-3' style='display:none;'> <span class='' data-bind='attr:{'id': $data.name()}' id=''>  </div>"
# 			##edit_lock_icon in quote based on permission starts
# 			edit_lock_icon = ''
# 			permission_chk_query = Sql.GetFirst("""SELECT DISTINCT SYOBJD.OBJECT_NAME, SYOBJD.FIELD_LABEL,case when SYOBJD.EDITABLE_ONINSERT ='TRUE' then 'EDITABLE' 
# 				Else 'READ ONLY' end AS PERMISSION,SYPRSF.EDITABLE 
# 				FROM SYOBJD (NOLOCK)
# 				INNER JOIN SYSECT (NOLOCK) ON SYSECT.PRIMARY_OBJECT_NAME = SYOBJD.OBJECT_NAME
# 				INNER JOIN SYSEFL (NOLOCK) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID
# 				INNER JOIN SYPRSF (NOLOCK) ON SYPRSF.SECTIONFIELD_RECORD_ID = SYSEFL.RECORD_ID
# 				INNER JOIN USERS_PERMISSIONS UP ON UP.PERMISSION_ID = SYPRSF.PROFILE_RECORD_ID
# 				AND SYSEFL.API_FIELD_NAME = SYOBJD.API_NAME
# 				WHERE SYSEFL.RECORD_ID = '{0}' AND UP.USER_ID ='{1}' AND SYSEFL.SECTION_RECORD_ID = '{2}'""".format(str(sefl.RECORD_ID), str(User.Id),str(sect.RECORD_ID)))
# 			if permission_chk_query:
# 				# if str(permission_chk_query.PERMISSION) == "EDITABLE" and str(col_name.QUOTE_STATUS).upper() != "APPROVED":
# 				# 	edit_lock_icon = "fa fa-pencil"
# 				if str(permission_chk_query.PERMISSION) == "EDITABLE":
# 					edit_lock_icon = "fa fa-pencil"	
# 				else:
# 					edit_lock_icon = "fa fa-lock"  
# 			##edit_lock_icon in quote based on permission ends
# 			sec_str += "<div class='col-md-1' style='float: right;'> <div class='col-md-12 editiconright'><a href='#' onclick='editclick_row(this)' class='editclick'>	<i class='{icon}' aria-hidden='true'></i></a></div></div>".format(icon = edit_lock_icon)
# 			sec_str += "</div>"

# 			sec_str += "</div>"
# 		sec_str += "</div>"


			
# 	sec_str += '<table class="wth100mrg8"><tbody>'
# 	#Trace.Write("111111" + str(Qt_rec_id))

# 	sec_str += "</tbody></table></div>"
# 	sec_str += "</div>"
# 	#Trace.Write(str(sec_str))
# 	# if ACTION == "QUOTE_INFO" :
# 	# 	quote_id = str(eval("col_name.QUOTE_ID"))
# 	# 	accunt_id = str(eval("col_name.ACCOUNT_ID"))
# 	# 	accunt_name = str(eval("col_name.ACCOUNT_NAME"))
# 	# 	quote_type = str(eval("col_name.QUOTE_TYPE"))
# 	# 	sale_type = str(eval("col_name.SALE_TYPE"))
# 	# 	valid_from=str(eval("col_name.CONTRACT_VALID_FROM")).split(" ")[0]
# 	# 	valid_to = str(eval("col_name.CONTRACT_VALID_TO")).split(" ")[0]
# 	# else:
# 	# 	quote_id = ""
# 	# 	accunt_id = ""
# 	# 	accunt_name = ""
# 	# 	quote_type = ""
# 	# 	sale_type = ""
# 	# 	valid_from= ""
# 	# 	valid_to = ""	

# 	return sec_str

# def sales_org_info(Qt_rec_id, Quote, MODE):    
# 	anchor_tag_id_value = ""
# 	VAR1 = ""
# 	sec_str = ""
# 	quote_id=""
# 	add_style = ""
# 	API_NAME_LIST = []
# 	PModel = "disabled"
# 	editclick = "QuoteinformationEDIT(this)"
# 	edit_action = ""
# 	#sec_rec_id = "B0B5E48B-DC63-4B1A-95AC-695973D3AA06"
# 	if ACTION == "CONTRACT_SALES_INFO":
# 		primary_objname = "CTCTSO"
# 	else:
# 		primary_objname = "SAQTSO"

# 	Oppp_SECT = Sql.GetList(
# 		"SELECT TOP 1000 RECORD_ID,SECTION_NAME FROM SYSECT WHERE PRIMARY_OBJECT_NAME = '{primary_objname}' ORDER BY DISPLAY_ORDER".format(primary_objname = primary_objname)
# 	)
# 	for sect in Oppp_SECT:
# 		sec_str += '<div id="container" class="wdth100 margtop10 ' + str(sect.RECORD_ID) + '">'
# 		# if (str(sect.SECTION_NAME) == "CONTRACT BOOKING INFORMATION" or str(sect.SECTION_NAME) == "AUDIT INFORMATION" ):
# 		#     sec_str += (
# 		#         '<div class="dyn_main_head master_manufac glyphicon pointer   glyphicon-chevron-down mt-10px" onclick="dyn_main_sec_collapse_arrow(this)" data-target=".sec_'
# 		#         + str(sect.RECORD_ID)
# 		#         + '" data-toggle="collapse"><label class="onlytext"><label class="onlytext"><div>'
# 		#         + str(sect.SECTION_NAME)
# 		#         + "</div></label></div>"
# 		#     )
		
# 		# else:
# 		sec_html_btn = Sql.GetFirst("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE ACTION_NAME = 'EDIT' AND SECTION_RECORD_ID = '"+str(sect.RECORD_ID)+"'")
# 		if sec_html_btn is not None:
# 			edit_action = str(sec_html_btn.HTML_CONTENT).format(rec_id = str(sect.RECORD_ID), edit_click = str(editclick))
# 		else:
# 			edit_action = ''
# 		sec_str += (
# 			'''<div onclick="dyn_main_sec_collapse_arrow(this)" 
# 			data-bind="attr: {'data-toggle':'collapse','data-target':'.col'+stdAttrCode(), 
# 			'id':'dyn'+stdAttrCode(),'class': isWholeRow() ? 'g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer' : 'g1 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer'}" 
# 				data-target=".sec_'''+str(sect.RECORD_ID)+'''"  id="dyn1577"  data-toggle="collapse"  class="g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer"> 
# 			<label data-bind="html: hint" class="onlytext"><div>'''+ str(edit_action) + str(sect.SECTION_NAME)+'''</div></label> </div>'''
# 		)
		


# 		Oppp_SEFL = Sql.GetList(
# 			"SELECT TOP 1000 FIELD_LABEL, API_FIELD_NAME,RECORD_ID FROM SYSEFL WHERE SECTION_RECORD_ID = '" + str(sect.RECORD_ID) + "' ORDER BY DISPLAY_ORDER"
# 		)
# 		for sefl in Oppp_SEFL:
# 			sec_str += '<div id="sec_' + str(sect.RECORD_ID) + '" class=  "sec_' + str(sect.RECORD_ID) + ' collapse in "> '
# 			# if (sefl.FIELD_LABEL) == "Key":
# 			# 	sec_str += "<div style='height:30px;border-left: 0;border-right: 0;border-bottom:1px solid  #dcdcdc; display:none' data-bind='attr: {'id':'mat'+stdAttrCode(),'class': isWholeRow() ? 'g4  except_sec removeHorLine iconhvr' : 'g1 except_sec removeHorLine iconhvr' }' id='mat1578' class='g4  except_sec removeHorLine iconhvr'>"
# 			# 	sec_str += (
# 			# 		"<div class='col-md-5'>	<abbr data-bind='attr:{'title':label}' title='"
# 			# 		+ str(sefl.FIELD_LABEL)
# 			# 		+ "'> <label class='col-md-11 pull-left' style='padding: 5px 5px;margin: 0;' data-bind='html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), 'pull-left': hint() }'>"
# 			# 		+ str(sefl.FIELD_LABEL)
# 			# 		+ "</label> </abbr> <a href='#' title='' data-placement='auto top' data-toggle='popover' data-trigger='focus' data-content='"+str(sefl.FIELD_LABEL)+"' class='col-md-1 bgcccwth10' style='text-align:right;padding: 7px 5px;color:green;' data-original-title=''><i title='"+str(sefl.FIELD_LABEL)+"' class='fa fa-info-circle fltlt'></i></a> </div>"
# 			# 	)
# 			# else:	
# 			sec_str += "<div style='height:30px;border-left: 0;border-right: 0;border-bottom:1px solid  #dcdcdc;' data-bind='attr: {'id':'mat'+stdAttrCode(),'class': isWholeRow() ? 'g4  except_sec removeHorLine iconhvr' : 'g1 except_sec removeHorLine iconhvr' }' id='mat1578' class='g4  except_sec removeHorLine iconhvr'>"
# 			sec_str += (
# 				"<div class='col-md-5'>	<abbr data-bind='attr:{'title':label}' title='"
# 				+ str(sefl.FIELD_LABEL)
# 				+ "'> <label class='col-md-11 pull-left' style='padding: 5px 5px;margin: 0;' data-bind='html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), 'pull-left': hint() }'>"
# 				+ str(sefl.FIELD_LABEL)
# 				+ "</label> </abbr> <a href='#' title='' data-placement='auto top' data-toggle='popover' data-trigger='focus' data-content='"+str(sefl.FIELD_LABEL)+"' class='col-md-1 bgcccwth10' style='text-align:right;padding: 7px 5px;color:green;' data-original-title=''><i title='"+str(sefl.FIELD_LABEL)+"' class='fa fa-info-circle fltlt'></i></a> </div>"
# 			)
# 			sefl_api = sefl.API_FIELD_NAME
# 			if ACTION == "CONTRACT_SALES_INFO": 
# 				col_name = Sql.GetFirst("SELECT * from CTCTSO (NOLOCK) WHERE CONTRACT_RECORD_ID = '{contract_record_id}' ".format(contract_record_id= str(contract_record_id) ))
				
# 			else:
# 				col_name = Sql.GetFirst("SELECT * FROM SAQTSO WHERE QUOTE_RECORD_ID = '" + str(Quote) + "' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) + "'") 
# 			if col_name:
# 				if sefl_api == "CpqTableEntryModifiedBy":
# 					current_obj_value = col_name.CpqTableEntryModifiedBy	
# 					current_user = Sql.GetFirst(
# 						"SELECT USERNAME FROM USERS WHERE ID = " + str(current_obj_value) + ""
# 					).USERNAME
# 					sec_str += (
# 						"<div class='col-md-3 pad-0'> <input type='text' title = '"+ str(current_user)+"' value = '"
# 						+ str(current_user)
# 						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
# 					)
# 				elif sefl_api == "QUOTE_SALESORG_RECORD_ID":
# 					cpq_key_id = CPQID.KeyCPQId.GetCPQId("SAQTSO", str(eval("col_name." + str(sefl_api))))
# 					sec_str += (
# 						"<div class='col-md-3 pad-0'> <input id= 'key_field_id' type='text' title = '"+ str(cpq_key_id)+"' value = '"
# 						+ str(cpq_key_id)
# 						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
# 					)
# 				elif sefl_api == "CONTRACT_SALES_ORG_RECORD_ID":
# 					cpq_key_id = CPQID.KeyCPQId.GetCPQId("CTCTSO", str(eval("col_name." + str(sefl_api))))
# 					sec_str += (
# 						"<div class='col-md-3 pad-0'> <input id= 'key_field_id' type='text' title = '"+ str(cpq_key_id)+"' value = '"
# 						+ str(cpq_key_id)
# 						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
# 					)					
# 				else:
# 					# if sefl_api != "REGION":
# 					Trace.Write('At line 289-->'+str(sefl_api))
# 					sec_str += (
# 						"<div class='col-md-3 pad-0'> <input type='text' id ='"+str(sefl_api)+"' title = '"+  str(eval("col_name." + str(sefl_api)))+"' value = '"
# 						+ str(eval("col_name." + str(sefl_api)))
# 						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
# 					)
# 					# else:
# 					#     sec_str += (
# 					#         "<div class='col-md-3 pad-0'> <input type='text' value = '' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
# 					#     )
# 			else:

# 				sec_str += "<div class='col-md-3 pad-0'> <input type='text' value = '' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
# 			sec_str += "<div class='col-md-3' style='display:none;'> <span class='' data-bind='attr:{'id': $data.name()}' id=''>  </div>"
# 			##edit_lock_icon in quote based on permission starts
# 			edit_lock_icon = ''
# 			permission_chk_query = Sql.GetFirst("""SELECT DISTINCT SYOBJD.OBJECT_NAME, SYOBJD.FIELD_LABEL,case when SYOBJD.EDITABLE_ONINSERT ='TRUE' then 'EDITABLE' 
# 				Else 'READ ONLY' end AS PERMISSION,SYPRSF.EDITABLE 
# 				FROM SYOBJD (NOLOCK)
# 				INNER JOIN SYSECT (NOLOCK) ON SYSECT.PRIMARY_OBJECT_NAME = SYOBJD.OBJECT_NAME
# 				INNER JOIN SYSEFL (NOLOCK) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID
# 				INNER JOIN SYPRSF (NOLOCK) ON SYPRSF.SECTIONFIELD_RECORD_ID = SYSEFL.RECORD_ID
# 				INNER JOIN USERS_PERMISSIONS UP ON UP.PERMISSION_ID = SYPRSF.PROFILE_RECORD_ID
# 				AND SYSEFL.API_FIELD_NAME = SYOBJD.API_NAME
# 				WHERE SYSEFL.RECORD_ID = '{0}' AND UP.USER_ID ='{1}' AND SYSEFL.SECTION_RECORD_ID = '{2}'""".format(str(sefl.RECORD_ID), str(User.Id),str(sect.RECORD_ID)))
# 			if permission_chk_query:
# 				# if str(permission_chk_query.PERMISSION) == "EDITABLE" and str(col_name.QUOTE_STATUS).upper() != "APPROVED":
# 				# 	edit_lock_icon = "fa fa-pencil"
# 				if str(permission_chk_query.PERMISSION) == "EDITABLE":
# 					edit_lock_icon = "fa fa-pencil"	
# 				else:
# 					edit_lock_icon = "fa fa-lock"  
# 			##edit_lock_icon in quote based on permission ends
# 			sec_str += "<div class='col-md-1' style='float: right;'> <div class='col-md-12 editiconright'><a href='#' onclick='editclick_row(this)' class='editclick'>	<i class='{icon}' aria-hidden='true'></i></a></div></div>".format(icon = edit_lock_icon)
# 			sec_str += "</div>"

# 			sec_str += "</div>"
# 		sec_str += "</div>"


			
# 	sec_str += '<table class="wth100mrg8"><tbody>'
# 	#Trace.Write("111111" + str(Qt_rec_id))

# 	sec_str += "</tbody></table></div>"
# 	sec_str += "</div>"
		

# 	return sec_str	

def constructapprovalchaininformation(MODE,record_id):    
	#anchor_tag_id_value = ""
	#VAR1 = ""
	sec_str = ""
	add_style = ""
	API_NAME_LIST = []
	PModel = "disabled"
	editclick = "QuoteinformationEDIT(this)"
	edit_action = ""
	cancel_save = ""
	#sec_rec_id = "B0B5E48B-DC63-4B1A-95AC-695973D3AA06"    
	Oppp_SECT = Sql.GetList(
		"SELECT TOP 1000 RECORD_ID,SECTION_NAME FROM SYSECT WHERE PRIMARY_OBJECT_NAME = 'ACAPCH' ORDER BY DISPLAY_ORDER"
	)
	for sect in Oppp_SECT:
		sec_str += '<div id="container" class="wdth100 ' + str(sect.RECORD_ID) + '">'        
		sec_html_btn = Sql.GetList("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE SECTION_RECORD_ID = '"+str(sect.RECORD_ID)+"'")      
		edit_action = ""  
		if len(sec_html_btn) > 0:            
			for btn in sec_html_btn:                
				if "EDIT" in btn.HTML_CONTENT:
					section_edit_btn = str(btn.HTML_CONTENT).format(rec_id= sect.RECORD_ID, edit_click= editclick)
					edit_action = section_edit_btn

				if "CANCEL" in btn.HTML_CONTENT:
					cancel_btn = str(btn.HTML_CONTENT)                    
				if "SAVE" in btn.HTML_CONTENT:                    
					save_btn = str(btn.HTML_CONTENT)

			cancel_save = '<div  class="g4 sec_' + str(sect.RECORD_ID) + ' collapse in except_sec removeHorLine iconhvr sec_edit_sty">'+ str(cancel_btn) + str(save_btn) +'</div>'
			

		# sec_html_btn = Sql.GetFirst("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE ACTION_NAME = 'EDIT' AND SECTION_RECORD_ID = '"+str(sect.RECORD_ID)+"'")
		# if sec_html_btn is not None:
		#     edit_action = str(sec_html_btn.HTML_CONTENT).format(rec_id = str(sect.RECORD_ID), edit_click = str(editclick))
		# else:
		#     edit_action = ''
		sec_str += (
			'''<div onclick="dyn_main_sec_collapse_arrow(this)" style="padding-left:10px;" 
			data-bind="attr: {'data-toggle':'collapse','data-target':'.col'+stdAttrCode(), 
			'id':'dyn'+stdAttrCode(),'class': isWholeRow() ? 'g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer' : 'g1 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer'}" 
				data-target=".sec_'''+str(sect.RECORD_ID)+'''"  id="dyn1577"  data-toggle="collapse"  class="g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer"> 
			<label data-bind="html: hint" class="onlytext"><div>'''+ str(edit_action) + str(sect.SECTION_NAME)+'''</div></label> </div>'''
		)
		# sec_str += (
		#         '''<div onclick="dyn_main_sec_collapse_arrow(this)" style="padding-left:10px;" 
		#         data-bind="attr: {'data-toggle':'collapse','data-target':'.col'+stdAttrCode(), 
		#         'id':'dyn'+stdAttrCode(),'class': isWholeRow() ? 'g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer' : 'g1 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer'}" 
		#          data-target=".sec_'''+str(sect.RECORD_ID)+'''"  id="dyn1577"  data-toggle="collapse"  class="g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer"> 
		#         <label data-bind="html: hint" class="onlytext"><div><div id="ctr_drop" class="btn-group dropdown"><div class="dropdown"><i data-toggle="dropdown" 
		#         class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li class="edit_list">
		#         <a id="'''+str(sect.RECORD_ID)+'''" 
		#         class="dropdown-item" href="#" onclick="QuoteinformationEDIT(this)">EDIT</a></li></ul></div></div>'''+str(sect.SECTION_NAME)+'''</div></label> </div>''')
			
		

		Oppp_SEFL = Sql.GetList(
			"SELECT TOP 1000 FIELD_LABEL, API_FIELD_NAME,API_NAME FROM SYSEFL WHERE SECTION_RECORD_ID = '" + str(sect.RECORD_ID) + "' ORDER BY DISPLAY_ORDER"
		)
		
		for sefl in Oppp_SEFL:
			sec_str += '<div id="sec_' + str(sect.RECORD_ID) + '" class=  "sec_' + str(sect.RECORD_ID) + ' collapse in "> '
			sec_str += "<div style='height:30px;border-left: 0;border-right: 0;border-bottom:1px solid  #dcdcdc;' data-bind='attr: {'id':'mat'+stdAttrCode(),'class': isWholeRow() ? 'g4  except_sec removeHorLine iconhvr' : 'g1 except_sec removeHorLine iconhvr' }' id='mat1578' class='g4  except_sec removeHorLine iconhvr'>"
			sec_str += (
				"<div class='col-md-5'>	<abbr data-bind='attr:{'title':label}' title='"
				+ str(sefl.FIELD_LABEL)
				+ "'> <label class='col-md-11 pull-left' style='padding: 5px 5px;margin: 0;' data-bind='html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), 'pull-left': hint() }'>"
				+ str(sefl.FIELD_LABEL)
				+ "</label> </abbr> <a href='#' title='' data-placement='auto top' data-toggle='popover' data-trigger='focus' data-content='"+str(sefl.FIELD_LABEL)+"' class='col-md-1 bgcccwth10' style='text-align:right;padding: 7px 5px;color:green;' data-original-title=''><i  class='fa fa-info-circle fltlt'></i></a> </div>"
			)
			sefl_api = sefl.API_FIELD_NAME			
			object_name = sefl.API_NAME
			syobjd_obj = Sql.GetFirst("SELECT DATA_TYPE FROM SYOBJD WHERE API_NAME = '{}' and OBJECT_NAME ='{}'".format(sefl_api,object_name))
			data_type = syobjd_obj.DATA_TYPE
			col_name = Sql.GetFirst("SELECT * FROM ACAPCH WHERE APPROVAL_CHAIN_RECORD_ID = '"+str(record_id)+"'")
												
			if col_name:
				if sefl_api == "CpqTableEntryModifiedBy":
					current_obj_value = col_name.CpqTableEntryModifiedBy
					current_user = Sql.GetFirst(
						"SELECT USERNAME FROM USERS WHERE ID = " + str(current_obj_value) + ""
					).USERNAME
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' value = '"
						+ str(current_user)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					)
				elif sefl_api == "APPROVAL_CHAIN_RECORD_ID":
					cpq_key_id = CPQID.KeyCPQId.GetCPQId("ACAPCH", str(eval("col_name." + str(sefl_api))))
					sec_str += (
						"<div class='col-md-3 pad-0'> <input id= 'key_field_id' type='text' value = '"
						+ str(cpq_key_id)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					)
				# To get the hyperlink for source contract id field in Quote information node - start    
				elif sefl_api == "SOURCE_CONTRACT_ID":                    
					if str(eval("col_name." + str(sefl_api))):
					#parent_rec_id = get_value_from_obj(record_obj, column_name)
						contract_obj = Sql.GetFirst("SELECT CONTRACT_RECORD_ID FROM CTCNRT (NOLOCK) WHERE CONTRACT_ID = '"+str(eval("col_name." + str(sefl_api)))+"'")
						if contract_obj:
							parent_rec_id = contract_obj.CONTRACT_RECORD_ID
							anchor_tag_id_value = parent_rec_id + '|Contracts'
						sec_str += (
							"<div class='col-md-1 col-xs-2 col-sm-1 pad-0 pt-5px pb-5px'><a id='"+str(anchor_tag_id_value)+"' onclick='Move_to_parent_obj(this)' class='curptr''>"+str(eval("col_name." + str(sefl_api)))+"</a></div>"
						)
					else:
						sec_str += (
							"<div class='col-md-3 pad-0'> <input type='text' value = '"
							+ str(eval("col_name." + str(sefl_api)))
							+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
						)  
				# To get the hyperlink for source contract id field in Quote information node - end              
				##to get date from datetime for CONTRACT_VALID_FROM and CONTRACT_VALID_TO strts
				elif sefl_api in ("CONTRACT_VALID_FROM","CONTRACT_VALID_TO"):
					#Trace.Write(str(eval("col_name." + str(sefl_api))))
					try:
						datetime_value = datetime.strptime(str(eval("col_name." + str(sefl_api))), '%m/%d/%Y %I:%M:%S %p').strftime('%m/%d/%Y')
					except:
						datetime_value  = str(eval("col_name." + str(sefl_api)))                    
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' value = '"
						+ str(datetime_value)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					)
				##to get date from datetime for CONTRACT_VALID_FROM and CONTRACT_VALID_TO ends
				elif sefl_api == "APROBJ_RECORD_ID":
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' value = '"
						+ str(eval("col_name." + str(sefl_api)))
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled='' style = 'display':'none'> </div>"
					) 
				elif data_type =="CHECKBOX":
					act_status = (eval("col_name." + str(sefl_api)))
					#Trace.Write("act_status---->"+str(act_status))
					if act_status == True  or act_status == 1:
						sec_str += (
							'<div class="col-md-3 padtop5 padleft10"><input id="'
							+ str(sefl_api)
							+ '" type="CHECKBOX" value="'
							+ str(act_status)
							+ '" class="custom" '
							+ 'disabled checked><span class="lbl"></span></div>'
						)
					else:
						sec_str += (
							'<div class="col-md-3 padtop5 padleft10"><input id="'
							+ str(sefl_api)
							+ '" type="CHECKBOX" value="'
							+ str(act_status)
							+ '" class="custom" '
							+ 'disabled ><span class="lbl"></span></div>'
						)	
				else:
					# if sefl_api != "REGION":                    
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' value = '"
						+ str(eval("col_name." + str(sefl_api)))
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					)
					# else:
					#     sec_str += (
					#         "<div class='col-md-3 pad-0'> <input type='text' value = '' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
					#     )
			else:

				sec_str += "<div class='col-md-3 pad-0'> <input type='text' value = '' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
			sec_str += "<div class='col-md-3' style='display:none;'> <span class='' data-bind='attr:{'id': $data.name()}' id=''>  </div>"
			sec_str += "<div class='col-md-1' style='float: right;'> <div class='col-md-12 editiconright'><a href='#' onclick='editclick_row(this)' class='editclick'>	<i class='fa fa-lock' aria-hidden='true'></i></a></div></div>"
			# field_permission = Sql.GetList("SELECT API_NAME, DATA_TYPE, PERMISSION, FIELD_LABEL FROM SYOBJD (NOLOCK) WHERE OBJECT_NAME = 'ACAPCH' ")
			# for inn in field_permission:  
			#     if inn:
			#         Trace.Write("permisssion====")
			#         if inn.PERMISSION == 'READ ONLY':
			#             Trace.Write("readonly====")
			#             sec_str += "<div class='col-md-1' style='float: right;'> <div class='col-md-12 editiconright'><a href='#' onclick='editclick_row(this)' class='editclick'>	<i class='fa fa-lock' aria-hidden='true'></i></a></div></div>"
			#         if inn.PERMISSION == 'EDITABLE':
			#             Trace.Write("editable====")
			#             sec_str += "<div class='col-md-1' style='float: right;'> <div class='col-md-12 editiconright'><a href='#' onclick='editclick_row(this)' class='editclick'>	<i class='fa fa-pencil' aria-hidden='true'></i></a></div></div>"    
			sec_str += "</div>"

			sec_str += "</div>"

	sec_str += '<table class="wth100mrg8"><tbody>'
	#Trace.Write("111111" + str(Qt_rec_id))

	sec_str += "</tbody></table></div>"
	sec_str += "</div>"
	#Trace.Write(str(sec_str))
	return sec_str,cancel_save


# commented the code(Approvals node functionality in Quotes explorer) -start

# def aprvrapproved():
#     sec_str = ""
#     sec_str += """<div class="drop-boxess" style="display: none;">
#                 <div class="col-md-3 pl-0 rolling_popup">
#                 <div class="col-md-2 p-0">
#                     <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/info_icon.svg" class="img-responsive center-block">
#                 </div>
#                 <div class="col-md-10 p-0">
#                     <h3>Approval Submitted <button type="button"
#                     class="close" data-dismiss="modal" 
#                     aria-label="Close" onclick="close_popup()"> 
#                 <span aria-hidden="true">×</span> 
#             </button></h3>
#                 <p>You have successfully approved the transaction. The requestor will be notified by an email of your approval.</p>
#                 </div>
#                 </div>
#                 </div>"""  
#     return sec_str


# def aprvrrejected():
#     sec_str = ""
#     sec_str += """<div class="drop-boxess" style="display: none;">
#                 <div class="col-md-3 pl-0 rolling_popup">
#                 <div class="col-md-2 p-0">
#                     <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/info_icon.svg" class="img-responsive center-block">
#                 </div>
#                 <div class="col-md-10 p-0">
#                     <h3>Approval Rejected <button type="button"
#                     class="close" data-dismiss="modal" 
#                     aria-label="Close" onclick="close_popup()"> 
#                 <span aria-hidden="true">×</span> 
#             </button></h3>
#                 <p>You have successfully rejected the transaction. The requestor will be notified by an email of your rejection.</p>
#                 </div>
#                 </div>
#                 </div>"""  
#     return sec_str
# commented the code(Approvals node functionality in Quotes explorer) -end

ACTION = Param.ACTION
#Trace.Write('ACTION---1041--'+str(ACTION))
try:
	AllTreeParam = Param.AllTreeParam
	TreeParam = AllTreeParam['TreeParam']
except:
	AllTreeParam = ""
	TreeParam = ""
try: 
	Qt_rec_id = Param.QT_REC_ID
except:
	Qt_rec_id = ""
#Trace.Write("QT_REC_ID"+str(Qt_rec_id))
try: 
	params = Param.params
except:
	params = ""
try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = ""
try:
	line = Param.line
except:
	line = ""
try:
	CAT1 = Param.CAT1
except:
	CAT1 = ""
try:
	CAT2 = Param.CAT2
except:
	CAT2 = ""
try:
	CAT3 = Param.CAT3
except:
	CAT3 = ""
try:
	CAT4 = Param.CAT4
except:
	CAT4 = ""
try:
	CAT5 = Param.CAT5
except:
	CAT5 = ""
try:
	CAT6 = Param.CAT6
except:
	CAT6 = ""
try:
	CAT2 = Param.CAT2
except:
	CAT2 = ""
try:
	CAT7 = Param.CAT7
except:
	CAT7 = ""
try:
	CAT8 = Param.CAT8
except:
	CAT8 = ""
try:
	CAT9 = Param.CAT9
except:
	CAT9 = ""
try:
	CAT10 = Param.CAT10
except:
	CAT10 = ""
try:
	CAT11 = Param.CAT11
except:
	CAT11 = ""
try:
	CAT12 = Param.CAT12
except:
	CAT12 = ""
try:
	CAT13 = Param.CAT13
except:
	CAT13 = ""
try:
	CAT14 = Param.CAT14
except:
	CAT14 = ""
try: 
	params = Param.params
except:
	params = ""
if ACTION == 'QIPOPUPSER':
	#ApiResponse = ApiResponseFactory.JsonResponse(popupuser())
	pass

# commented the code(Approvals node functionality in Quotes explorer) -start    
# elif ACTION == 'SUBMITQUOTE':
#     ApiResponse = ApiResponseFactory.JsonResponse(submitapproval())
# elif ACTION == 'QTAPPROVE':
#     ApiResponse = ApiResponseFactory.JsonResponse(aprvrapproved())
# elif ACTION == 'QTREJECT':
#     ApiResponse = ApiResponseFactory.JsonResponse(aprvrrejected())

# commented the code(Approvals node functionality in Quotes explorer) -end
elif ACTION == "LEGALSOW_VIEW":
	if TreeParam == "Contract Information":
		contract_record_id = Quote.GetGlobal("contract_record_id")
		contract_id = Sql.GetFirst("SELECT CONTRACT_ID FROM CTCNRT (NOLOCK) WHERE CONTRACT_RECORD_ID = '"+str(contract_record_id)+"'")
		quote_id = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT (NOLOCK) WHERE CRM_CONTRACT_ID ='"+str(contract_id.CONTRACT_ID)+"'")
		Quote = quote_id.MASTER_TABLE_QUOTE_RECORD_ID
	elif TreeParam == "Quote Information":
		Quote = Quote.GetGlobal("contract_quote_record_id")
	#Trace.Write("Quote---->" + str(Quote))
	MODE = "VIEW"
	ApiResponse = ApiResponseFactory.JsonResponse(constructlegalsow(Qt_rec_id, Quote, MODE))
elif ACTION == "CBC_VIEW":
	if TreeParam == "Quote Information":
		Quote = Quote.GetGlobal("contract_quote_record_id")
	MODE = "VIEW"
	ApiResponse = ApiResponseFactory.JsonResponse(constructCBC(Qt_rec_id, Quote, MODE))
elif ACTION == "CBC_EDIT":
	MODE = "EDIT"
	Quote = Quote.GetGlobal("contract_quote_record_id")
	ApiResponse = ApiResponseFactory.JsonResponse(editcbc(Qt_rec_id, Quote, MODE))
elif ACTION == "CBC_COUNT":
	MODE = "COUNT"
	Quote = Quote.GetGlobal("contract_quote_record_id")
	ApiResponse = ApiResponseFactory.JsonResponse(countcbc(Qt_rec_id, Quote, MODE))	
elif ACTION == "CBC_SAVE":
	MODE = "SAVE"
	Quote = Quote.GetGlobal("contract_quote_record_id")
	ApiResponse = ApiResponseFactory.JsonResponse(savecbc(Qt_rec_id, Quote, MODE))
elif ACTION == "ANNUAL_ITEM_SAVE":
	MODE = "SAVE"
	Quote = Quote.GetGlobal("contract_quote_record_id")
	ApiResponse = ApiResponseFactory.JsonResponse(save_annualiziedgrid_inline(Quote,line,CAT1,CAT2,CAT3,CAT4,CAT5,CAT6,CAT7,CAT8,CAT9,CAT10,CAT11,CAT12,CAT13,CAT14,MODE))		
elif ACTION == "OPPORTUNITY_VIEW":
	if TreeParam == "Contract Information":
		contract_record_id = Quote.GetGlobal("contract_record_id")
		contract_id = Sql.GetFirst("SELECT CONTRACT_ID FROM CTCNRT (NOLOCK) WHERE CONTRACT_RECORD_ID = '"+str(contract_record_id)+"'")
		quote_id = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT (NOLOCK) WHERE CRM_CONTRACT_ID ='"+str(contract_id.CONTRACT_ID)+"'")
		Quote = quote_id.MASTER_TABLE_QUOTE_RECORD_ID
	elif TreeParam == "Quote Information":
		Quote = Quote.GetGlobal("contract_quote_record_id")
	#Trace.Write("Quote---->" + str(Quote))
	MODE = "VIEW"
	ApiResponse = ApiResponseFactory.JsonResponse(constructopportunity(Qt_rec_id, Quote, MODE))
elif ACTION in ("QUOTE_INFO","CONTRACT_INFO"):
	if ACTION == "QUOTE_INFO" :
		Quote = Quote.GetGlobal("contract_quote_record_id")	
	## Contract 1st node 
	elif ACTION == "CONTRACT_INFO" :
		contract_record_id =  Quote.GetGlobal("contract_record_id")
		#Trace.Write("contract_record_id---->" + str(contract_record_id))
	MODE = "VIEW"
	ApiResponse = ApiResponseFactory.JsonResponse(constructquoteinformation(Qt_rec_id, Quote, MODE))
# elif ACTION in ("QUOTE_ATTR","CONTRACT_ATTR"):
# 	if ACTION == "QUOTE_ATTR" :
# 		Quote = Quote.GetGlobal("contract_quote_record_id")	
# 	## Contract 1st node 
# 	elif ACTION == "CONTRACT_ATTR" :
		
		
# 		Trace.Write("contract_record_id---->" + str(contract_record_id))
# 	MODE = "VIEW"
# 	ApiResponse = ApiResponseFactory.JsonResponse(constructidlingattributes(Qt_rec_id, Quote, MODE))	
elif ACTION == "Approval_Chain_INFO":
	record_id = Param.RECORD_ID
	record_id = record_id[:36]
	# record_id = Quote.GetGlobal("contract_quote_record_id")
	#Trace.Write("record_idrecord_id"+str(record_id))
	MODE = "VIEW"
	ApiResponse = ApiResponseFactory.JsonResponse(constructapprovalchaininformation(MODE,record_id))
# elif ACTION in ("SALES_INFO","CONTRACT_SALES_INFO"):
# 	if ACTION == "SALES_INFO":
# 		Quote = Quote.GetGlobal("contract_quote_record_id")
# 	elif ACTION == "CONTRACT_SALES_INFO":
# 		contract_record_id =  Quote.GetGlobal("contract_record_id")		
# 	MODE = "VIEW"
# 	ApiResponse = ApiResponseFactory.JsonResponse(sales_org_info(Qt_rec_id, Quote, MODE))

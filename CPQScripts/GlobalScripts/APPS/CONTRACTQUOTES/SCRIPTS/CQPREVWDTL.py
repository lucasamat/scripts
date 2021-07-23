# =========================================================================================================================================
#   __script_name : CQPREVWDTL.PY
#   __script_description : THIS SCRIPT IS USED TO  TRIGGER POPUP WHILE SAVING THE DRIVERS, PRICE,ENTITLEMENTS 
#   __primary_author__ : WASIM ABDUL
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import datetime
from datetime import datetime
Sql = SQL()
import SYCNGEGUID as CPQID
import CQVLDRIFLW

# import CMGTRULRAC as CMRUL
# Get_UserID = ScriptExecutor.ExecuteGlobal("SYGETUSDID")
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

def popupser(params):
	sec_str = ""
	sec_str += """<div class="drop-boxess" style="display: none;">
				<div class="col-md-3 pl-0 rolling_popup">
				<div class="col-md-2 p-0">
					<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/info_icon.svg" class="img-responsive center-block">
				</div>
				<div class="col-md-10 p-0">
					<h3>"""+str(params)+""" Cost and Value Driver Roll Down <button type="button"
					class="close"
					aria-label="Close" onclick="close_popup()"> 
				<span aria-hidden="true">×</span> 
			</button></h3>
				<p>The <q>"""+str(params)+""" Cost and Value Driver</q> settings are being applied to the Equipment in this quote. You will be notified by email when this background job completes.</p>
				</div>
				</div>
				</div>"""  
	return sec_str

def popupuser():
	sec_str = ""
	sec_str += """<div class="drop-boxess" style="display: none;">
				<div class="col-md-3 pl-0 rolling_popup">
				<div class="col-md-2 p-0">
					<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/info_icon.svg" class="img-responsive center-block">
				</div>
				<div class="col-md-10 p-0">
					<h3>Price Calculation <button type="button"
					class="close"
					aria-label="Close" onclick="close_popup()"> 
				<span aria-hidden="true">×</span> 
			</button></h3>
				<p>Price calculation is currently in progress. You will be notified by email notification when this background job completes.</p>
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
			"SELECT TOP 1000 FIELD_LABEL, API_FIELD_NAME FROM SYSEFL WHERE SECTION_RECORD_ID = '" + str(sect.RECORD_ID) + "' ORDER BY DISPLAY_ORDER"
		)
		for sefl in Oppp_SEFL:
			sec_str += '<div id="sec_' + str(sect.RECORD_ID) + '" class= "sec_' + str(sect.RECORD_ID) + ' collapse in">'
			sec_str += "<div style='height:30px;border-left: 0;border-right: 0;border-bottom:1px solid  #dcdcdc;' data-bind='attr: {'id':'mat'+stdAttrCode(),'class': isWholeRow() ? 'g4  except_sec removeHorLine iconhvr' : 'g1 except_sec removeHorLine iconhvr' }' id='mat1578' class='g4  except_sec removeHorLine iconhvr'>"
			sec_str += (
				"<div class='col-md-5'>	<abbr data-bind='attr:{'title':label}' title='"
				+ str(sefl.FIELD_LABEL)
				+ "'> <label class='col-md-11 pull-left' style='padding: 5px 5px;margin: 0;' data-bind='html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), 'pull-left': hint() }'>"
				+ str(sefl.FIELD_LABEL)
				+ "</label> </abbr> <a href='#' title='"+str(sefl.FIELD_LABEL)+"' data-placement='auto top' data-toggle='popover' data-trigger='focus' data-content='"+str(sefl.FIELD_LABEL)+"' class='col-md-1 bgcccwth10' style='text-align:right;padding: 7px 5px;color:green;' data-original-title=''><i  class='fa fa-info-circle fltlt'></i></a> </div>"
			)
			sefl_api = sefl.API_FIELD_NAME
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
		primary_objname = "SAQTMT"

	Oppp_SECT = Sql.GetList(
		"SELECT TOP 1000 RECORD_ID,SECTION_NAME FROM SYSECT WHERE PRIMARY_OBJECT_NAME = '{primary_objname}' ORDER BY DISPLAY_ORDER".format(primary_objname = primary_objname)
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
			"SELECT TOP 1000 FIELD_LABEL, API_FIELD_NAME,RECORD_ID FROM SYSEFL WHERE SECTION_RECORD_ID = '" + str(sect.RECORD_ID) + "' ORDER BY DISPLAY_ORDER"
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
			if ACTION == "CONTRACT_INFO": 
				col_name = Sql.GetFirst("SELECT * from CTCNRT (NOLOCK) WHERE CONTRACT_RECORD_ID = '{contract_record_id}' ".format(contract_record_id= str(contract_record_id) ))
				
			else:
				col_name = Sql.GetFirst("SELECT * FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '" + str(Quote) + "'") 
			if col_name:
				if sefl_api == "CpqTableEntryModifiedBy":
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
				elif sefl_api in ("CONTRACT_VALID_FROM","CONTRACT_VALID_TO"):
					try:
						datetime_value = datetime.strptime(str(eval("col_name." + str(sefl_api))), '%m/%d/%Y %I:%M:%S %p').strftime('%m/%d/%Y')
					except:
						datetime_value  = str(eval("col_name." + str(sefl_api)))
					
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' title = '"+ str(datetime_value)+"' value = '"
						+ str(datetime_value)
						+ "' 'title':userInput}, incrementalTabIndex, enable: isEnabled' class='form-control' style='height: 28px;border-top: 0 !important;border-bottom: 0 !important;' id='' title='' tabindex='' disabled=''> </div>"
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
				else:
					# if sefl_api != "REGION":
					Trace.Write('At line 289-->'+str(sefl_api))
					sec_str += (
						"<div class='col-md-3 pad-0'> <input type='text' id ='"+str(sefl_api)+"' title = '"+  str(eval("col_name." + str(sefl_api)))+"' value = '"
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
				if str(permission_chk_query.PERMISSION) == "EDITABLE" and str(col_name.QUOTE_STATUS).upper() != "APPROVED":
					edit_lock_icon = "fa fa-pencil"
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
	if ACTION == "QUOTE_INFO" :
		quote_id = str(eval("col_name.QUOTE_ID"))
		accunt_id = str(eval("col_name.ACCOUNT_ID"))
		accunt_name = str(eval("col_name.ACCOUNT_NAME"))
		quote_type = str(eval("col_name.QUOTE_TYPE"))
		sale_type = str(eval("col_name.SALE_TYPE"))
		valid_from=str(eval("col_name.CONTRACT_VALID_FROM")).split(" ")[0]
		valid_to = str(eval("col_name.CONTRACT_VALID_TO")).split(" ")[0]
	else:
		quote_id = ""
		accunt_id = ""
		accunt_name = ""
		quote_type = ""
		sale_type = ""
		valid_from= ""
		valid_to = ""	

	return sec_str,quote_id,accunt_id,accunt_name,quote_type,sale_type,valid_from,valid_to

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
			"SELECT TOP 1000 FIELD_LABEL, API_FIELD_NAME FROM SYSEFL WHERE SECTION_RECORD_ID = '" + str(sect.RECORD_ID) + "' ORDER BY DISPLAY_ORDER"
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

if ACTION == 'POPUPS':
	ApiResponse = ApiResponseFactory.JsonResponse(popups(params))
elif ACTION == 'POPUPSER':
	ApiResponse = ApiResponseFactory.JsonResponse(popupser(params))
elif ACTION == 'QIPOPUPSER':
	ApiResponse = ApiResponseFactory.JsonResponse(popupuser())

# commented the code(Approvals node functionality in Quotes explorer) -start    
# elif ACTION == 'SUBMITQUOTE':
#     ApiResponse = ApiResponseFactory.JsonResponse(submitapproval())
# elif ACTION == 'QTAPPROVE':
#     ApiResponse = ApiResponseFactory.JsonResponse(aprvrapproved())
# elif ACTION == 'QTREJECT':
#     ApiResponse = ApiResponseFactory.JsonResponse(aprvrrejected())

# commented the code(Approvals node functionality in Quotes explorer) -end
elif ACTION == "OPPORTUNITY_VIEW":
	if TreeParam == "Contract Information":
		contract_record_id = Quote.GetGlobal("contract_record_id")
		contract_id = Sql.GetFirst("SELECT CONTRACT_ID FROM CTCNRT (NOLOCK) WHERE CONTRACT_RECORD_ID = '"+str(contract_record_id)+"'")
		quote_id = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT (NOLOCK) WHERE CRM_CONTRACT_ID ='"+str(contract_id.CONTRACT_ID)+"'")
		Quote = quote_id.MASTER_TABLE_QUOTE_RECORD_ID
	elif TreeParam == "Quote Information":
		Quote = Quote.GetGlobal("contract_quote_record_id")
	Trace.Write("Quote---->" + str(Quote))
	MODE = "VIEW"
	ApiResponse = ApiResponseFactory.JsonResponse(constructopportunity(Qt_rec_id, Quote, MODE))
elif ACTION in ("QUOTE_INFO","CONTRACT_INFO"):
	if ACTION == "QUOTE_INFO" :
		Quote = Quote.GetGlobal("contract_quote_record_id")	
	## Contract 1st node 
	elif ACTION == "CONTRACT_INFO" :
		contract_record_id =  Quote.GetGlobal("contract_record_id")
		Trace.Write("contract_record_id---->" + str(contract_record_id))
	MODE = "VIEW"
	ApiResponse = ApiResponseFactory.JsonResponse(constructquoteinformation(Qt_rec_id, Quote, MODE))
elif ACTION == "Approval_Chain_INFO":
	record_id = Param.RECORD_ID
	record_id = record_id[:36]
	# record_id = Quote.GetGlobal("contract_quote_record_id")
	Trace.Write("record_idrecord_id"+str(record_id))
	MODE = "VIEW"
	ApiResponse = ApiResponseFactory.JsonResponse(constructapprovalchaininformation(MODE,record_id))
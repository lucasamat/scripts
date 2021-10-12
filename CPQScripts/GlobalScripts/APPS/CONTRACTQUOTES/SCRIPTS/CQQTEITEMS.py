# =========================================================================================================================================
#   __script_name : CQQTEITEMS.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD SUMMARY IN QUOTE ITEMS
#   __primary_author__ : NAMRATA SIVAKUMAR
#   __create_date : 12/10/2021
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import SYTABACTIN as Table
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
Sql = SQL()

def LoadSummary():
    sec_str = ""
    # #Oppp_SECT = Sql.GetList(
    #     "SELECT TOP 1000 RECORD_ID,SECTION_NAME FROM SYSECT WHERE SECTION_DESC = '' AND PRIMARY_OBJECT_NAME = '{primary_objname}' ORDER BY DISPLAY_ORDER".format(primary_objname = primary_objname))
    #for sect in Oppp_SECT: 
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
    #sec_html_btn = Sql.GetFirst("SELECT HTML_CONTENT FROM SYPSAC (NOLOCK) WHERE ACTION_NAME = 'EDIT' AND SECTION_RECORD_ID = '"+str(sect.RECORD_ID)+"'")
    # if sec_html_btn is not None:
    #     edit_action = str(sec_html_btn.HTML_CONTENT).format(rec_id = str(sect.RECORD_ID), edit_click = str(editclick))
    # else:
    #     edit_action = ''
    sec_str += (
        '''<div id="container" class="wdth100 margtop10"><div onclick="dyn_main_sec_collapse_arrow(this)" 
        data-bind="attr: {'data-toggle':'collapse','data-target':'.col'+stdAttrCode(), 
        'id':'dyn'+stdAttrCode(),'class': isWholeRow() ? 'g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer' : 'g1 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer'}" 
            data-target=".sec_"  id="dyn1577"  data-toggle="collapse"  class="g4 dyn_main_head master_manufac add_level glyphicon glyphicon-chevron-down pointer"> 
        <label data-bind="html: hint" class="onlytext"><div>'''+str("TOOL IDLING")+'''</div></label> </div>'''
    )
    sec_str += '<div id="sec_" class=  "sec_" collapse in "> '
    sec_str += "<div style='height:30px;border-left: 0;border-right: 0;border-bottom:1px solid  #dcdcdc;' data-bind='attr: {'id':'mat'+stdAttrCode(),'class': isWholeRow() ? 'g4  except_sec removeHorLine iconhvr' : 'g1 except_sec removeHorLine iconhvr' }' id='mat1578' class='g4  except_sec removeHorLine iconhvr'>"
    sec_str += (
        "<div class='col-md-5'>	<abbr data-bind='attr:{'title':label}' title='"
        + str("Idling Allowed")
        + "'> <label class='col-md-11 pull-left' style='padding: 5px 5px;margin: 0;' data-bind='html: label, css: { requiredLabel: incomplete() &amp;&amp; $root.highlightIncomplete(), 'pull-left': hint() }'>"
        + str("Idling Allowed")
        + "</label> </abbr> <a href='#' title='' data-placement='auto top' data-toggle='popover' data-trigger='focus' data-content='"+str("Idling Allowed")+"' class='col-md-1 bgcccwth10' style='text-align:right;padding: 7px 5px;color:green;' data-original-title=''><i title='"+str("Idling Allowed")+"' class='fa fa-info-circle fltlt'></i></a> </div>"
    )


    '''Oppp_SEFL = Sql.GetList(
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
            col_name = Sql.GetFirst("SELECT * FROM SAQTRV WHERE QUOTE_RECORD_ID = '" + str(Quote) + "' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) + "' ") 
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
                Trace.Write("date---->"+str(eval("col_name." + str(sefl_api))))
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
                Trace.Write("313")
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
        sec_str += "<div class='col-md-3' style='display:none;'> <span class='' data-bind='attr:{'id': $data.name()}' id=''>  </div>"'''
        ##edit_lock_icon in quote based on permission starts
        # permission_chk_query = Sql.GetFirst("""SELECT DISTINCT SYOBJD.OBJECT_NAME, SYOBJD.FIELD_LABEL,case when SYOBJD.EDITABLE_ONINSERT ='TRUE' then 'EDITABLE' 
        #     Else 'READ ONLY' end AS PERMISSION,SYPRSF.EDITABLE 
        #     FROM SYOBJD (NOLOCK)
        #     INNER JOIN SYSECT (NOLOCK) ON SYSECT.PRIMARY_OBJECT_NAME = SYOBJD.OBJECT_NAME
        #     INNER JOIN SYSEFL (NOLOCK) ON SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID
        #     INNER JOIN SYPRSF (NOLOCK) ON SYPRSF.SECTIONFIELD_RECORD_ID = SYSEFL.RECORD_ID
        #     INNER JOIN USERS_PERMISSIONS UP ON UP.PERMISSION_ID = SYPRSF.PROFILE_RECORD_ID
        #     AND SYSEFL.API_FIELD_NAME = SYOBJD.API_NAME
        #     WHERE SYSEFL.RECORD_ID = '{0}' AND UP.USER_ID ='{1}' AND SYSEFL.SECTION_RECORD_ID = '{2}'""".format(str(sefl.RECORD_ID), str(User.Id),str(sect.RECORD_ID)))
        # if permission_chk_query:
        #     if str(permission_chk_query.PERMISSION) == "EDITABLE" and str(col_name.REVISION_STATUS).upper() != "APPROVED":
        #         edit_lock_icon = "fa fa-pencil"
        #     else:
        #         edit_lock_icon = "fa fa-lock"  
        # else:
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
    Trace.Write("sec_str --->"+str(sec_str))
    return sec_str

SubtabName = Param.SUBTAB
if SubtabName == "Summary":
    LoadSummary()


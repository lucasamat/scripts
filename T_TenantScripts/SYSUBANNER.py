# =========================================================================================================================================
#   __script_name : SYSUBANNER.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE SUB BANNER FOR THE RELATED LISTS BASED ON HIERARCHY.
#   __primary_author__ : JOE EBENEZER
#   __create_date : 28/08/2020
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
import SYCNGEGUID as CPQID
import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL

Sql = SQL()
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct() or "Sales"

def Related_Sub_Banner(
    subTabName,
    ObjName,
    CurrentRecordId,
    TreeParentNodeRecId,
    TreeParam,
    TreeParentParam,
    TreeSuperParentParam,
    TreeTopSuperParentParam,
    Sub_banner_text,
    page_type
):
    msg_txt = ''
    TreeParam = Product.GetGlobal("TreeParam")
    TreeParentParam = Product.GetGlobal("TreeParentLevel0")
    TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
    TopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
    TreeSuperTopParentParam = Product.GetGlobal("TreeParentLevel3")
    quote_add_button = ""
    quote_multi_buttons = ""
    try:
        contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
    except:
        contract_quote_record_id = ''
    try:
        quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
    except:
        quote_revision_record_id = ""
    try:
        current_prod = Product.Name        
    except:
        current_prod = "Sales"
    try:
        TabName = TestProduct.CurrentTab
    except:
        TabName = CurrentTab    
    user_id = User.Id
    buttonvisibility = dropdown_multi_btn_str = ''
    price_bar = '' # Not Used
    LOGIN_CREDENTIALS = Sql.GetFirst("SELECT top 1 Domain FROM SYCONF (nolock) order by CpqTableEntryId")
    if LOGIN_CREDENTIALS is not None:
        Login_Domain = str(LOGIN_CREDENTIALS.Domain)
    else:
        Login_Domain = "APPLIEDMATERIALS_UAT"
    ListKey = ""
    if TreeParam == 'Z0103 - BASE FEE':
        TreeParam ='Z0103'
    sec_rel_sub_bnr = (
        PrimaryLable
    ) = (
        PrimaryValue
    ) = SecondLable = SecondValue = ThirdLable = ThirdValue = FourthLable = FourthValue = FifthLable = FifthValue = SixthLable = SixthValue = Image = RelatedRecId = ""
    PMEvents = SeventhLable = SeventhValue = EightLable = EightValue = ""
    recall_edit =""
    try:
        CurrentTabName = TestProduct.CurrentTab
    except:
        CurrentTabName = ""
    # Getting Dynamic buttons for secondary banner - Starts
    try:
        quote_status = Sql.GetFirst("SELECT QUOTE_STATUS FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
    except:
        quote_status = ''    
    try:
        revision_status = Sql.GetFirst("SELECT REVISION_STATUS,WORKFLOW_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
    except:
        revision_status = ''
    dynamic_Button = None
    add_button = ""
    # Getting page details
    multi_buttons = []
    dropdown_multi_btn_str = '''<div id="ctr_drop" class="btn-group dropdown dropdown_multi_btn_str"><div class="dropdown"><i data-toggle="dropdown" class="fa fa-sort-desc dropdown-toggle"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton">'''
    Trace.Write('ObjName---103--'+str(ObjName))
    if ObjName == "SAQIGS" or ObjName == "SAQRIB":
        ObjName ="SAQRIB"
        page_type = "OBJECT PAGE LAYOUT"
    if ObjName == "SAQDOC":
        page_details = Sql.GetFirst("SELECT RECORD_ID FROM SYPAGE WHERE OBJECT_APINAME = '{}' ".format(str(ObjName)))
    else:
        page_details = Sql.GetFirst("SELECT RECORD_ID FROM SYPAGE WHERE OBJECT_APINAME = '{}' AND PAGE_TYPE = '{}'".format(str(ObjName),str(page_type)))
    if page_details:
        if ObjName =="SAQDOC":
            get_quote_status = Sql.GetFirst("SELECT REVISION_STATUS,WORKFLOW_STATUS,CONTRACT_VALID_FROM FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))            
            if get_quote_status:
                if str(get_quote_status.REVISION_STATUS).upper() in ("APR-APPROVED","OPD-PREPARING QUOTE DOCUMENTS"):
                    dynamic_Button = Sql.GetList("SELECT TOP 10 HTML_CONTENT,RELATED_LIST_RECORD_ID,DISPLAY_ORDER  FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '"+str(page_details.RECORD_ID)+"' AND TAB_NAME LIKE '%"+str(CurrentTab)+"%' AND SUBTAB_NAME = '"+str(subTabName)+"' ORDER BY DISPLAY_ORDER ")
                    if not dynamic_Button:
                        dynamic_Button = Sql.GetList("SELECT TOP 10 HTML_CONTENT,RELATED_LIST_RECORD_ID,DISPLAY_ORDER FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '"+str(page_details.RECORD_ID)+"' AND TAB_NAME LIKE '%"+str(CurrentTab)+"%' AND ISNULL(SUBTAB_NAME,'')='' ORDER BY DISPLAY_ORDER")
                else:
                    dynamic_Button = ""
        else:
            dynamic_Button = Sql.GetList("SELECT TOP 10 HTML_CONTENT,RELATED_LIST_RECORD_ID,DISPLAY_ORDER  FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '"+str(page_details.RECORD_ID)+"' AND TAB_NAME LIKE '%"+str(CurrentTab)+"%' AND SUBTAB_NAME = '"+str(subTabName)+"' ORDER BY DISPLAY_ORDER ")            
            get_quote_status = Sql.GetFirst("SELECT REVISION_STATUS,WORKFLOW_STATUS,CONTRACT_VALID_FROM FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
            if not dynamic_Button and not subTabName == 'Inclusions':
                dynamic_Button = Sql.GetList("SELECT TOP 10 HTML_CONTENT,RELATED_LIST_RECORD_ID,DISPLAY_ORDER FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '"+str(page_details.RECORD_ID)+"' AND TAB_NAME LIKE '%"+str(CurrentTab)+"%' AND ISNULL(SUBTAB_NAME,'')='' ORDER BY DISPLAY_ORDER")
        # Binding button Id's based on Related list Table record id
        if len(dynamic_Button) > 0:
            for btn in dynamic_Button:
                if ("CANCEL" not in str(btn.HTML_CONTENT) and "SAVE" not in str(btn.HTML_CONTENT)):
                    if btn.RELATED_LIST_RECORD_ID:
                        SYOBJH_ID = Sql.GetFirst("SELECT SYOBJH.SAPCPQ_ATTRIBUTE_NAME AS REC_ID,SYOBJR.SAPCPQ_ATTRIBUTE_NAME,SYOBJR.NAME AS NAME FROM SYOBJR (NOLOCK) INNER JOIN SYOBJH (NOLOCK) ON SYOBJR.OBJ_REC_ID = SYOBJH.RECORD_ID WHERE SYOBJR.SAPCPQ_ATTRIBUTE_NAME = '{syobjr_rec_id}'".format(syobjr_rec_id = btn.RELATED_LIST_RECORD_ID))
                    if len(dynamic_Button) > 1:
                        if str(btn.HTML_CONTENT) != "" and str(btn.RELATED_LIST_RECORD_ID) != "":
                            button_id = str(btn.RELATED_LIST_RECORD_ID).replace("-","_")+"_"+str(SYOBJH_ID.REC_ID).replace("-","_")
                            if btn.RELATED_LIST_RECORD_ID == SYOBJH_ID.SAPCPQ_ATTRIBUTE_NAME:
                                div_id = "div_CTR_"+str(SYOBJH_ID.NAME).replace(" ","_")
                                if "div_id" in str(btn.HTML_CONTENT):
                                    add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id), div_id= str(div_id))
                                else:
                                    add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id))
                            else:
                                add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id))
                            multi_buttons.append(add_button)
                        else:
                            add_button = btn.HTML_CONTENT
                            if btn.RELATED_LIST_RECORD_ID:
                                div_id = "div_CTR_"+str(SYOBJH_ID.NAME).replace(" ","_")
                                if "div_id" in str(btn.HTML_CONTENT):
                                    add_button = add_button.format(div_id = div_id)
                            multi_buttons.append(add_button)
                    else:
                        if str(btn.HTML_CONTENT) != "" and str(btn.RELATED_LIST_RECORD_ID) != "":
                            button_id = str(btn.RELATED_LIST_RECORD_ID).replace("-","_")+"_"+str(SYOBJH_ID.REC_ID).replace("-","_")
                            if btn.RELATED_LIST_RECORD_ID == SYOBJH_ID.SAPCPQ_ATTRIBUTE_NAME:
                                div_id = "div_CTR_"+str(SYOBJH_ID.NAME).replace(" ","_")
                                if "div_id" in str(btn.HTML_CONTENT):
                                    add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id), div_id= str(div_id))
                                else:
                                    add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id))
                            else:
                                add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id))                            
                        else:
                            add_button = btn.HTML_CONTENT
                            if btn.RELATED_LIST_RECORD_ID:
                                div_id = "div_CTR_"+str(SYOBJH_ID.NAME).replace(" ","_")
                                if "div_id" in add_button:
                                    add_button = add_button.format(div_id = div_id)
                else:
                    try:
                        if subTabName.startswith("Year") and str(ObjName) == "SAQRIB":                            
                            add_button = '<button id="billingmatrix_save" onclick="showSBillMatBulksave(this)" style= "display: none;" class="btnconfig" >SAVE</button><button id="billingmatrix_cancel" onclick="showSBillMatBulkcancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>'
                        if subTabName =="Delivery Schedule"  and str(ObjName) == "SAQSPD":                            
                            add_button = '<button id="delivery_save" onclick="showSdeliverysave(this)" style= "display: none;" class="btnconfig" >SAVE</button><button id="delivery_cancel" onclick="showSdeliverycancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>'
                    except:
                        add_button = ""
                quote_add_button = add_button
                quote_multi_buttons = multi_buttons
                if (str(revision_status.REVISION_STATUS).upper() in ("CBC-CBC COMPLETED","BOK-CONTRACT CREATED","BOK-CONTRACT BOOKED","LGL-LEGAL SOW ACCEPTED","LGL-LEGAL SOW REJECTED","LGL-PREPARING LEGAL SOW","CBC-PREPARING CBC")) or (str(revision_status.REVISION_STATUS).upper() in ("CFG-ACQUIRING","PRR-ON HOLD PRICING","CFG-ON HOLD - COSTING","PRI-PRICING") and str(TreeParam).upper() not in ("QUOTE ITEMS","BILLING","APPROVALS","QUOTE DOCUMENTS")) or (str(revision_status.REVISION_STATUS).upper() in ("APR-APPROVED","APR-REJECTED","APR-RECALLED","APR-APPROVAL PENDING","OPD-PREPARING QUOTE DOCUMENTS","OPD-CUSTOMER ACCEPTED","OPD-CUSTOMER REJECTED") and str(TreeParam).upper() not in ("APPROVALS","QUOTE DOCUMENTS")):
                    add_button = ""
                    multi_buttons = []
                else:
                    pass
                if (str(revision_status.REVISION_STATUS).upper() not in ("BOK-CONTRACT BOOKED","BOK-CONTRACT CREATED","CBC-CBC COMPLETED") and str(TreeParam).upper() == "REVISIONS"):
                    add_button = quote_add_button
                    multi_buttons = quote_multi_buttons
                else:
                    pass
        Trace.Write("Button_check--- "+str(add_button)+" - "+str(multi_buttons)) 
        try:
            if subTabName.startswith("Year") and str(ObjName) == "SAQRIB":
                sec_rel_sub_bnr +=('<button id="billingmatrix_save" onclick="showSBillMatBulksave(this)" style= "display: none;" class="btnconfig" >SAVE</button><button id="billingmatrix_cancel" onclick="showSBillMatBulkcancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>')
            if subTabName =="Delivery Schedule"  and str(ObjName) == "SAQSPD":
                add_button = '<button id="delivery_save" onclick="showSdeliverysave(this)" style= "display: none;" class="btnconfig" >SAVE</button><button id="delivery_cancel" onclick="showSdeliverycancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>'
        except:
            Trace.Write('176--------EXCEPT-------')
            add_button = ""        
            # Getting Dynamic buttons for secondary banner -  Ends
    getmainservice =""
    if TreeParam == "Quote Information" or TreeParam == "Quote Preview":
        if ObjName == 'SAQTIP' and subTabName == 'Detail':
            ObjName = "SAQTIP"
        elif ObjName == 'SAQSCF' and (subTabName == 'Source Fab Location Details' or subTabName == 'Source Fab Location'):
            ObjName = "SAQSCF"
        elif ObjName == 'SAQSTE' and (subTabName == 'Equipment' or subTabName == 'Equipment details' or subTabName == 'Tool Relocation Matrix' or subTabName == 'Tool Relocation Matrix details'):
            ObjName = "SAQSTE"
        else:
            ObjName = "SAQTMT"    
    elif (TreeParam.startswith("Sending") or TreeParam.startswith("Receiving")):
        ObjName = "SAQSRA"
    ParentObjNameQuery = Sql.GetFirst(
        "select SYSECT.PRIMARY_OBJECT_NAME from SYTABS (nolock) inner join SYPAGE (nolock) on SYPAGE.TAB_NAME = SYTABS.TAB_LABEL INNER JOIN SYSECT (NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID where SYTABS.SAPCPQ_ALTTAB_NAME = '"
        + str(TabName)
        + "' AND SYSECT.SECTION_NAME = 'BASIC INFORMATION' "
    )
    ObjNameQuery = Sql.GetFirst(
        "select SYOBJH.OBJECT_NAME, SYOBJH.IMAGE_URL from SYOBJH (nolock) WHERE SYOBJH.OBJECT_NAME = '" + str(ObjName) + "'"
    )
    if ObjNameQuery is not None:
        ObjName = str(ObjNameQuery.OBJECT_NAME)
        ImageUrl = str(ObjNameQuery.IMAGE_URL)
        if TreeParentParam == "Contract Information" and TreeParam == 'Documents':
            ImageUrl = ImageUrl.replace("Secondary Icon.svg","Contract_Information.svg")
        if str(ImageUrl) != "":
            Image = "/mt/" + str(Login_Domain) + "/Additionalfiles/Icons/" + str(ImageUrl)        
        if CurrentRecordId.startswith("SYOBJR", 0) == True:
            ThirdQuery = Sql.GetFirst(
                "select * from SYOBJD (nolock) where OBJECT_NAME = '" + str(ObjName) + "' AND IS_KEY = 'True' "
            )
            if TreeParam == "Customer Information":
                involved_parties_object = Sql.GetFirst("SELECT PARTY_ID,PARTY_NAME,CPQ_PARTNER_FUNCTION FROM SAQTIP WHERE PARTY_ID = '{}' ".format(Product.GetGlobal("stp_account_Id")))
                if(subTabName == "Details" or subTabName == "Sending Fab Locations" or subTabName == "Sending Fab Location Details" or subTabName == "Sending Equipment") and TreeParam == "Customer Information":
                    Trace.Write("subTabName"+str(subTabName)+str(CurrentRecordId))
                    PrimaryLable = "Party ID"
                    PrimaryValue = involved_parties_object.PARTY_ID
                    SecondLable = "Party Name"
                    SecondValue = involved_parties_object.PARTY_NAME.upper()
                    ThirdLable = "Role"
                    ThirdValue = "SENDING ACCOUNT"
                    if subTabName == "Sending Fab Location Details" or subTabName == "Sending Equipment":
                        FourthLable = "Fab Location ID"
                        FourthValue = Product.GetGlobal("sending_fab_id")
                    else:
                        FourthLable = "Fab Locations"
                        FourthValue = "ALL"
                elif(subTabName == "Details" or subTabName == "Receiving Fab Locations" or subTabName == "Receiving Fab Location Details" or subTabName == "Receiving Equipment") and TreeParam == "Customer Information":
                    PrimaryLable = "Party ID"
                    PrimaryValue = involved_parties_object.PARTY_ID.upper()
                    SecondLable = "Party Name"
                    SecondValue = involved_parties_object.PARTY_NAME
                    ThirdLable = "Role"
                    ThirdValue = "RECEIVING ACCOUNT"
                    if subTabName == "Receiving Fab Locations Details" or subTabName == "Receiving Equipment":
                        FourthLable = "Fab Location ID"
                        FourthValue = Product.GetGlobal("receiving_fab_id")
                    else:
                        FourthLable = "Fab Locations"
                        FourthValue = "ALL"
            if TreeParam == 'Revisions':
                rev_quote = Sql.GetFirst(" SELECT * FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_record_id}' AND ACTIVE = 'TRUE' ".format(contract_quote_record_id = contract_quote_record_id))
                if rev_quote:
                    if TreeParam == 'Revisions':
                        PrimaryLable = 'Quote Revision'
                        PrimaryValue = rev_quote.QTEREV_ID
                        SecondLable = 'Revision Creation Date'
                        rev_create_date = rev_quote.REV_CREATE_DATE
                        rev_create_date = str(rev_create_date).upper().split(" ")[0].strip()
                        SecondValue = rev_create_date
                        ThirdLable = 'Revision Description'
                        ThirdValue = rev_quote.REVISION_DESCRIPTION
                        FourthLable = 'Status'
                        FourthValue = rev_quote.REVISION_STATUS
                        #ThirdLable = 'Status'
                        #ThirdValue = rev_quote.REVISION_STATUS            
            if str(CurrentRecordId) == 'SYOBJR-00014' and str(TreeParentParam) == 'Approval Chain Steps':
                PrimaryLable = "Approval Chain Step Number"
                PrimaryValue = str(TreeParentParam)
                SecondLable = "Approvers"
                SecondValue = "All"
            if str(CurrentRecordId) == 'SYOBJR-00015' and str(TreeParentParam) == 'Approval Chain Steps':
                PrimaryLable = "Approval Chain Step Number"
                PrimaryValue = str(TreeParam)
                SecondLable = "Tracked Fields"
                SecondValue = "ALL"
            if TabName == "Profile" and TreeParam != "" and str(ObjName) == "SYPRTB":
                SecondLable = "Tab Name"
                Query = Sql.GetFirst("select APP_ID FROM SYPRTB(nolock)  WHERE PROFILE_TAB_RECORD_ID ='" + CurrentRecordId + "'")
                SecondValue = str(Query.APP_ID) if Query else "ALL"
            elif TabName == "Profile" and TreeParam != "" and str(ObjName) == "SYPRSN":
                SecondLable = "Sections"
                Query = Sql.GetFirst("select TAB_ID FROM SYPRSN(nolock)  WHERE PROFILE_SECTION_RECORD_ID='" + CurrentRecordId + "'")
                SecondValue = str(Query.TAB_ID) if Query else "ALL"
            elif TabName == "Profile" and TreeParam != "" and str(ObjName) == "SYPRSF":
                SecondLable = "Section Fields"
                Query = Sql.GetFirst(
                    "select SECTION_FIELD_ID  FROM SYPRSF(nolock)  WHERE PROFILE_SECTIONFIELD_RECORD_ID='" + CurrentRecordId + "'"
                )
                SecondValue = str(Query.SECTION_FIELD_ID ) if Query else "ALL"
            elif TabName == "Profile" and TreeParam != "" and str(ObjName) == "SYPRAC":
                SecondLable = "Actions"
                Query = Sql.GetFirst(
                    "select ACTION_NAME FROM SYPRAC(nolock)  WHERE PROFILE_ACTION_RECORD_ID='" + CurrentRecordId + "'"
                )
                SecondValue = str(Query.ACTION_NAME) if Query else "ALL"
            elif TabName == "Profile" and TreeParam != "" and str(ObjName) == "SYPROD":
                SecondLable = "Fields"
                Query = Sql.GetFirst(
                    "select OBJECT_FIELD_ID FROM SYPROD(nolock)  WHERE PROFILE_OBJECTFIELD_RECORD_ID='" + CurrentRecordId + "'"
                )
                SecondValue = str(Query.OBJECT_FIELD_ID) if Query else "ALL"
            elif TabName == "App" and str(TreeParam) == "Sections" and str(ObjName) == "SYSECT":
                PrimaryLable = "Sections"
                PrimaryValue = "All"
            elif TabName == "App" and str(TreeParam) == "Section Fields" and str(ObjName) == "SYSEFL":
                PrimaryLable = "Section Fields"
                PrimaryValue = "All"
            elif TabName == "Quotes" and str(TreeParam) == "Approvals" :
                Trace.Write("309")
                PrimaryLable = "Approvals"
                PrimaryValue = "All"
            elif TabName == "Quotes"  and str(TreeParentParam) == "Product Offerings" and str(TreeParam) != "" and str(ObjName) == "SAQTSV" :
                PrimaryLable = "Product Offerings"
                PrimaryValue = "All"
                if TabName == "Quotes":
                    SecondLable = "Product Offering Type"
                elif TabName == "Contract":
                    SecondLable = "Product Type"
                SecondValue = str(TreeParam)
            elif TabName == "Quotes"  and str(TreeParam) == "Product Offerings" and str(ObjName) == "SAQTSV":
                PrimaryLable = "Product Offerings"
                PrimaryValue = "The Following Offerings Have been added to your quote..."           
            elif (TreeParam.startswith("Sending") or TreeParam.startswith("Receiving")):                
                if subTabName == "Fab Locations"  and TreeParam.startswith("Sending"):
                    PrimaryLable = "Sending Account ID"
                    PrimaryValue = str(TreeParam).split("-")[1].strip()
                    SecondLable = "Sending Fab Locations"
                    SecondValue = "ALL"
                elif subTabName == "Fab Locations"  and TreeParam.startswith("Receiving"):
                    PrimaryLable = "Receiving Account ID"
                    PrimaryValue = str(TreeParam).split("-")[1].strip()
                    SecondLable = "Receiving Fab Locations"
                    SecondValue = "ALL"
                elif (subTabName == "Equipment" or subTabName == "Fab Value Drivers") and TreeParam.startswith("Sending"):
                    PrimaryLable = "Sending Account ID"
                    PrimaryValue = str(TreeParam).split("-")[1].strip()
                    SecondLable = "Sending Fab Locations"
                    SecondValue = "ALL"
                    ThirdLable = "Equipment"
                    ThirdValue = "ALL"
                elif (subTabName == "Equipment" or subTabName == "Fab Value Drivers") and TreeParam.startswith("Receiving"):
                    PrimaryLable = "Receiving Account ID"
                    PrimaryValue = str(TreeParam).split("-")[1].strip()
                    SecondLable = "Receiving Fab Locations"
                    SecondValue = "ALL"
                    ThirdLable = "Equipment"
                    ThirdValue = "ALL"
            elif TreeParentNodeRecId.startswith("SYOBJR", 0) == True:
                if CurrentRecordId == "SYOBJR-00014" or CurrentRecordId == "SYOBJR-00015":
                    PrimaryLable = "Approval Chain Steps"
                    PrimaryValue = str(TreeParam)
                else:
                    PrimaryLable = str(TreeParentParam)
                    PrimaryValue = "ALL"
                if ThirdQuery is not None:
                    SecondLable = str(ThirdQuery.FIELD_LABEL)
                    SecondValue = str(TreeParam)
            elif (
                CurrentRecordId.startswith("SYOBJR", 0) == True and str(TreeParentNodeRecId) != ""
            ) and TabName == "Invoice":
                PrimaryLable = str(TreeParam)
                PrimaryValue = "ALL"
            elif TabName == "Page" and str(TreeParam) == "Tabs" and str(ObjName) == "SYTABS":
                PrimaryLable = "Tabs"
                PrimaryValue = "All"
            elif TabName == "Page" and str(TreeParam) == "Trees" and str(ObjName) == "SYTREE":
                #A055S000P01-3536 removed key
                SecondLable = "Trees"
                SecondValue = "All"
            elif TabName == "Page" and str(TreeParam) == "Sections" and str(ObjName) == "SYSECT":
                PrimaryLable = "Sections"
                PrimaryValue = "All"
                #SecondLable = "Sections"
                #SecondValue = "All"
            elif TabName == "Section" and str(TreeParam) == "Sub Sections" and str(ObjName) == "SYSECT":
                PrimaryLable = "Sections"
                PrimaryValue = "All"
                #SecondLable = "Sections"
                #SecondValue = "All"
            elif TabName == "Tab" and str(TreeParam) == "Actions" and str(ObjName) == "SYPGAC":
                PrimaryLable = "Actions"
                PrimaryValue = "All"
                #SecondLable = "Sections"
                #SecondValue = "All"
            elif TabName == "Tab" and str(TreeParam) == "Page" and str(ObjName) == "SYPAGE":
                PrimaryLable = "Pages"
                PrimaryValue = "All"
                #SecondLable = "Sections"
                #SecondValue = "All"
            elif TabName == "Object" and str(TreeParentParam) == "Indexes" and str(ObjName) == "SYOBJX":
                PrimaryLable = "Index Name"
                PrimaryValue = "All"
            elif TabName == "App" and str(TreeParam) == "Tabs" and str(ObjName) == "SYTABS":
                PrimaryLable = "Tabs"
                PrimaryValue = "All"
                #SecondLable = "Sections"
                #SecondValue = "All"
            elif TabName == "Section" and str(TreeParam) == "Section Actions" and str(ObjName) == "SYPSAC":
                PrimaryLable = "Section Actions"
                PrimaryValue = "All"
                #SecondLable = "Section Actions"
                #SecondValue = "All"
            elif TabName == "Section" and str(TreeParam) == "Section Fields" and str(ObjName) == "SYSEFL":
                PrimaryLable = "Section Fields"
                PrimaryValue = "All"
                #SecondLable = "Section Fields"
                #SecondValue = "All"
            elif TabName == "Section" and str(TreeParam) == "Messages" and str(ObjName) == "SYMSGS":
                PrimaryLable = "Messages"
                PrimaryValue = "All"
                #SecondLable = "Messages"
                #SecondValue = "All"
            elif TabName == "Variable" and str(TreeParam) == "Tabs" and str(ObjName) == "SYTABS":
                PrimaryLable = "Tabs"
                PrimaryValue = "All"
                #SecondLable = "Tabs"
                #SecondValue = "All"
            elif TabName == "Variable" and str(TreeParam) == "Messages" and str(ObjName) == "SYMSGS":
                PrimaryLable = "Messages"
                PrimaryValue = "All"
                #SecondLable = "Messages"
                #SecondValue = "All"
            elif TabName == "Variable" and str(TreeParam) == "Actions" and str(ObjName) == "SYPSAC":
                PrimaryLable = "Actions"
                PrimaryValue = "All"
                #SecondLable = "Actions"
                #SecondValue = "All"
            elif TabName == "Profile" and str(TreeParam) == "Object Level Permissions" and str(ObjName) == "SYPROH":
                PrimaryLable = "Object Level Permissions"
                PrimaryValue = "All"
            elif TabName == "My Approvals Queue" and TreeParam == "Approval History" and str(ObjName) == "ACAPTX":
                Querya = Product.AttributesGetByName("QSTN_SYSEFL_AC_00210").GetValue()
                Query = Sql.GetFirst(
                    "select APRCHN_ID, CUR_APRCHNSTP_ENTRYDATE, CUR_APPCHNSTP_APPROVER_ID FROM ACAPMA (nolock) WHERE APPROVAL_RECORD_ID='"
                    + str(Querya)
                    + "'"
                )
                PrimaryLable = "Approval Chain ID"
                PrimaryValue = str(Query.APRCHN_ID)
                SecondLable = "Current Chain Step Approver"
                SecondValue = str(Query.CUR_APPCHNSTP_APPROVER_ID)
                ThirdLable = "Step Entry Date"
                ThirdValue = str(Query.CUR_APRCHNSTP_ENTRYDATE)
            elif TabName == "Team Approvals Queue" and TreeParam == "Approval History" and str(ObjName) == "ACAPTX":
                Querya = Product.AttributesGetByName("QSTN_SYSEFL_AC_04210").GetValue()
                Query = Sql.GetFirst(
                    "select APRCHN_ID, CUR_APRCHNSTP_ENTRYDATE, CUR_APPCHNSTP_APPROVER_ID FROM ACAPMA (nolock) WHERE APPROVAL_RECORD_ID='"
                    + str(Querya)
                    + "'"
                )
                PrimaryLable = "Approval Chain ID"
                PrimaryValue = str(Query.APRCHN_ID)
                SecondLable = "Current Chain Step Approver"
                SecondValue = str(Query.CUR_APPCHNSTP_APPROVER_ID)
                ThirdLable = "Step Entry Date"
                ThirdValue = str(Query.CUR_APRCHNSTP_ENTRYDATE)
            elif TabName == "Approval Chain" and str(ObjName) == "ACACSC":
                if str(TreeParentParam) == "Approval Chain Steps":
                    PrimaryLable = "Approval Chain Steps"
                    PrimaryValue = "ALL"
                    SecondLable = "Approval Chain Steps Conditions"
                    SecondValue = "ALL"
            elif TabName == "Approval Chain" and str(TreeParentParam) == "Approval Chain Steps" and CurrentRecordId.startswith("SYOBJR", 0) == True:
                if str(ObjName) == "ACACSA":
                    PrimaryLable = "Approval Chain Step Number"
                    PrimaryValue = str(TreeParam)
                    SecondLable = "Approvers"
                    SecondValue = "ALL"
                elif str(ObjName) == "ACAPTF":
                    PrimaryLable = "Approval Chain Step Number"
                    PrimaryValue = str(TreeParam)
                    SecondLable = "Tracked Fields"
                    SecondValue = "ALL"
            elif str(CurrentRecordId) == 'SYOBJR-98857' and str(ObjName) == "SAQSCF":
                PrimaryLable = "Source Account ID"
                PrimaryValue = str(Product.GetGlobal("stp_account_Id"))
                SecondLable = "Source Account Name"
                SecondValue = str(Product.GetGlobal("stp_account_name"))
                # ThirdLable = "Sales Orgs"
                # ThirdValue = "ALL"
                ThirdLable = "Source Fab Location ID"
                ThirdValue = "All"
            elif str(CurrentRecordId) == 'SYOBJR-98858' and str(ObjName) == "SAQSTE":
                PrimaryLable = "Source Account ID"
                PrimaryValue = str(Product.GetGlobal("stp_account_Id"))
                SecondLable = "Source Account Name"
                SecondValue = str(Product.GetGlobal("stp_account_name"))
                ip_equipment = Sql.GetFirst("SELECT QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID,SRCFBL_NAME,SRCFBL_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                ThirdLable = "Source Fab Location ID"
                ThirdValue = "All"
                FourthLable = "Equipment ID"
                FourthValue = "ALL"
            elif str(CurrentRecordId) == 'SYOBJR-00028':
                PrimaryLable = "Source Account ID"
                PrimaryValue = str(Product.GetGlobal("stp_account_Id"))
                SecondLable = "Source Account Name"
                SecondValue = str(Product.GetGlobal("stp_account_name"))
                ip_equipment = Sql.GetFirst("SELECT QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID,SRCFBL_NAME,SRCFBL_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                ThirdLable = "Source Fab Location ID"
                ThirdValue = "All"
                FourthLable = "Equipment ID"
                FourthValue = "ALL"
            elif subTabName =='Entitlements' and str(ObjName) == "SAQSAO" and TreeParam == "Add-On Products" :
                Trace.Write("addon entitlement")
                get_addon_service_desc = Sql.GetFirst("SELECT * FROM SAQSGB (NOLOCK) WHERE QUOTE_SERVICE_GREENBOOK_RECORD_ID  = '{}'".format(CurrentRecordId))
                if get_addon_service_desc:
                    PrimaryLable = "Product Offering ID"
                    PrimaryValue = get_addon_service_desc.SERVICE_ID
                    SecondLable = "Product Offering Description"
                    SecondValue = get_addon_service_desc.SERVICE_DESCRIPTION
            elif str(CurrentRecordId) == 'SYOBJR-98859' and str(ObjName) == "SAQSAO":
                TreeParentParam = Product.GetGlobal("TreeParentLevel0")
                getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV(nolock) where SERVICE_ID = '"+str(TreeParentParam)+"'")
                PrimaryLable = "Product Offering ID"
                PrimaryValue = str(TreeParentParam)
                if getService is not None:
                        SecondLable = "Product Offering Description"
                        SecondValue = getService.SERVICE_DESCRIPTION
                ThirdLable = "Add-On Products"
                ThirdValue = "All"
            elif (subTabName != "Details" and TabName == "Quotes" and str(TreeParam) == "Customer Information") and (subTabName == "Accounts" or subTabName == "Contacts"):
                PrimaryLable = "Customer Information"
                PrimaryValue = "Use the Customer Information functionality to manage your quote Accounts Contacts..."
            elif TreeParam =="Sales Team":
                PrimaryLable = "Sales Team"
                PrimaryValue = "Use the Sale Team functionality to manage all contributors to your Quote..."
            elif TreeParam == "Quote Items" and str(subTabName)=="Entitlements" and str(CurrentRecordId) == "SYOBJR-00010":
                query_result = Sql.GetFirst("select * from SAQRIT (nolock) where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND QUOTE_REVISION_CONTRACT_ITEM_ID ='"+str(CurrentRecordId)+"' ")
                PrimaryLable = "Product Offering ID"
                PrimaryValue = str(query_result.SERVICE_ID)
                SecondLable = "Product Offering Description"
                SecondValue = str(query_result.SERVICE_DESCRIPTION)
                ThirdLable = "Fab Location ID"
                ThirdValue = str(query_result.FABLOCATION_ID)
                FourthLable = "Greenbook"
                FourthValue =  str(query_result.GREENBOOK)
                FifthLable = "Equipment ID"
                FifthValue = str(query_result.OBJECT_ID)
            elif TreeParam == "Quote Documents":
                if subTabName == "Attachments":
                    PrimaryLable = "Attachments"
                    PrimaryValue = "Use this page to upload .pdf attachments to your quote revision"
                else:
                    PrimaryLable = "Dynamic Document Generator"
                    PrimaryValue = "Use the settings below to control the conditional display of information on your Customer Facing Documents"
            else:
                ThirdQuery = Sql.GetFirst(
                "select * from SYOBJD (nolock) where OBJECT_NAME = '" + str(ObjName) + "' AND IS_KEY = 'True' "
            )
                if TreeParam != 'Revisions' and TreeParam != 'Customer Information':
                    PrimaryLable = str(TreeParam)
                    PrimaryValue = "ALL"
                elif TreeParam == 'Revisions' and (rev_quote is None or rev_quote == '') :
                    PrimaryLable = str(TreeParam)
                    PrimaryValue = "ALL"
                if (
                    ThirdQuery is not None
                ):
                    SecondLable = str(ThirdQuery.FIELD_LABEL)
                    SecondValue = "ALL"
        elif CurrentRecordId.startswith("SYOBJR", 0) == False:           
            if TreeParam == "Customer Information" or TreeParam == "Quote Preview":                
                if ObjName == 'SAQSCF' and (subTabName == 'Source Fab Location Details' or subTabName == 'Source Fab Location'):
                    ObjName = "SAQSCF"
                elif ObjName == 'SAQSTE' and (subTabName == 'Equipment details' or subTabName == 'Tool Relocation Matrix details'):
                    ObjName = "SAQSTE"
                else:
                    ObjName = "SAQTMT"
            elif TreeParam =="Quote Documents":
                if subTabName == "Attachments":
                    PrimaryLable = "Attachments"
                    PrimaryValue = "Use this page to upload .pdf attachments to your quote revision"
                else:
                    PrimaryLable = "Dynamic Document Generator"
                    PrimaryValue = "Use the settings below to control the conditional display of information on your Customer Facing Documents"
            elif subTabName == "Equipment" and (TreeParentParam == "Fab Locations" or TreeSuperParentParam == "Product Offerings" or TreeParentParam == "Add-On Products" and sec_rel_sub_bnr == "") and CurrentTab == 'Quotes':
                sale_type = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))               
                if quote_status.QUOTE_STATUS != 'APR-APPROVED':
                    if len(multi_buttons)>0:
                        for btn in multi_buttons:
                            if "Sending Account" in TreeParam:
                                if "ADD UNMAPPED EQUIPMENTS" in btn:
                                    sec_rel_sub_bnr += (str(btn))
                                    if (subTabName == "Equipment" or subTabName == "Fab Value Drivers") and TreeParam.startswith("Sending"):
                                        PrimaryLable = "Sending Account ID"
                                        PrimaryValue = str(TreeParam).split("-")[1].strip()
                                        SecondLable = "Sending Fab Locations"
                                        SecondValue = "ALL"
                                        ThirdLable = "Equipment"
                                        ThirdValue = "ALL"
                            else:
                                if "ADD FROM LIST" or "ADD TEMP TOOL" in btn:
                                    sec_rel_sub_bnr += (str(btn))
                    else:
                        sec_rel_sub_bnr += str(add_button)            
            elif TreeSuperParentParam == "Fab Locations" and subTabName == "Equipment Fab Value Drivers":
                PrimaryLable = ""
                PrimaryValue = ""
            elif TreeParam == "Billing":
                ObjName = "SAQRIB"
                PrimaryLable = str(TreeParam)
                PrimaryValue = "All"            
            elif (TreeSuperParentParam == "Fab Locations" or TreeTopSuperParentParam == "Fab Locations") and (subTabName == 'Equipment' or subTabName == "Details" or subTabName == "Customer Value Drivers"):                
                if ("Sending" in TreeParentParam or "Receiving" in TreeParentParam):
                    getFab = Sql.GetFirst("select FABLOCATION_NAME from SAQFBL(nolock) where FABLOCATION_ID = '"+str(TreeParam)+"'")
                    if subTabName == 'Equipment Fab Value Drivers' or subTabName == "Equipment Details":
                        PrimaryLable = "Fab Location ID"
                        PrimaryValue = str(TreeParam)
                        SecondLable = "Fab Location Name"
                        SecondValue = getFab.FABLOCATION_NAME
                        ThirdLable = "Greenbook"
                        ThirdValue = str(TreeParam)
                        FourthLable = "Equipment ID"
                        FourthValue = str(EquipmentId)
                        FifthLable = "Serial Number"
                        FifthValue = str(SerialNumber)
                        SixthLable = ""
                        SixthValue = ""
                    elif subTabName == "Details":
                        Trace.Write("Fab")
                        PrimaryLable = "Fab Location ID"
                        PrimaryValue = str(TreeParentParam)
                        SecondLable = "Fab Location Name"
                        SecondValue = getFab.FABLOCATION_NAME
                        ThirdLable = "Greenbook"
                        ThirdValue = str(TreeParam)
                    else:
                        if subTabName == "Equipment":
                            PrimaryLable = "Fab Location ID"
                            PrimaryValue = str(TreeParam)
                            SecondLable = "Fab Location Name"
                            SecondValue = getFab.FABLOCATION_NAME
                            ThirdLable = "Greenbook"
                            ThirdValue = str(TreeParam)
                            ThirdLable = "Equipment"
                            ThirdValue = "All"
                elif ("Sending" in TreeSuperParentParam or "Receiving" in TreeSuperParentParam):
                    getFab = Sql.GetFirst("select FABLOCATION_NAME from SAQFBL(nolock) where FABLOCATION_ID = '"+str(TreeParentParam)+"'")
                    if subTabName == "Greenbook Fab Value Drivers":
                        get_val = Sql.GetFirst(" SELECT EQUIPMENT_ID,SERIAL_NO FROM SAQSCO(nolock) WHERE GREENBOOK = '"+str(TreeParam)+"'")
                        PrimaryLable = "Fab Location ID"
                        PrimaryValue = str(TreeParentParam)
                        SecondLable = "Fab Location Name"
                        SecondValue = getFab.FABLOCATION_NAME
                        ThirdLable = "Greenbook"
                        ThirdValue = str(TreeParam)
                        FourthLable = "Equipment ID"
                        FourthValue = get_val.EQUIPMENT_ID
                        FifthLable = "Serial Number"
                        FifthValue = get_val.SERIAL_NO
                        #SixthLable = ""
                        #SixthValue = ""
                    elif subTabName == 'Equipment Fab Value Drivers' or subTabName == "Equipment Details":
                        PrimaryLable = "Fab Location ID"
                        PrimaryValue = str(TreeParentParam)
                        SecondLable = "Fab Location Name"
                        SecondValue = getFab.FABLOCATION_NAME
                        ThirdLable = "Greenbook"
                        ThirdValue = str(TreeParam)
                        FourthLable = "Equipment ID"
                        FourthValue = str(EquipmentId)
                        FifthLable = "Serial Number"
                        FifthValue = str(SerialNumber)
                        SixthLable = ""
                        SixthValue = ""
                    elif subTabName == "Details":
                        PrimaryLable = "Fab Location ID"
                        PrimaryValue = str(TreeParentParam)
                        SecondLable = "Fab Location Name"
                        SecondValue = getFab.FABLOCATION_NAME
                        ThirdLable = "Greenbook"
                        ThirdValue = str(TreeParam)
                    elif subTabName == "Equipment":
                        PrimaryLable = "Fab Location ID"
                        PrimaryValue = str(TreeParentParam)
                        SecondLable = "Fab Location Name"
                        SecondValue = getFab.FABLOCATION_NAME
                        ThirdLable = "Greenbook"
                        ThirdValue = str(TreeParam)
                        FourthLable = "Equipment"
                        FourthValue = "All"
                    else:
                        PrimaryLable = "Fab Location ID"
                        PrimaryValue = str(TreeParam)
                        SecondLable = "Fab Location Name"
                        SecondValue = getFab.FABLOCATION_NAME
                        ThirdLable = "Greenbook"
                        ThirdValue = str(TreeParam)
                        FourthLable = "Equipment"
                        FourthValue = "All"
            elif TreeParam == "Approvals"  and TabName == "Quotes":
                if subTabName == '':
                    getChain = Sql.GetFirst("SELECT APRCHN_ID FROM ACAPMA (NOLOCK) WHERE APRTRXOBJ_RECORD_ID = '{}' ORDER BY APRCHN_ID ASC".format(quote_revision_record_id))
                    if getChain:
                        subTabName = getChain.APRCHN_ID                
                getval = Sql.GetFirst(" select DISTINCT TOP 10 APRCHN_ID, APRCHN_NAME, APPROVAL_METHOD FROM ACAPCH (nolock) WHERE APRCHN_ID = '"+str(subTabName)+"'")
                getown = Sql.GetFirst(" select DISTINCT TOP 10 OWNER_NAME from SAQTMT(nolock) where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                PrimaryLable = "Approval Chain ID"
                if getval:
                    PrimaryValue = getval.APRCHN_ID
                    SecondLable = "Approval Chain Name"
                    SecondValue = getval.APRCHN_NAME
                    ThirdLable = "Approval Chain Method"
                    ThirdValue = getval.APPROVAL_METHOD
                    #FourthLable = "Quote Owner"
                else:
                    PrimaryLable = "Approvals"
                    PrimaryValue = "All"
                    SecondLable = ""
                    SecondValue = ""
            elif (TreeParam.startswith('Sending') or TreeParam.startswith('Receiving')):                
                if subTabName == "Details" and TreeParam.startswith('Sending Account'):
                    account_name = Sql.GetFirst("SELECT PARTY_NAME,PARTY_ID  FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' AND CPQ_PARTNER_FUNCTION LIKE '%SENDING%'"+" AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                    PrimaryLable = "Sending Account ID"
                    #PrimaryValue = str(TreeParam).split("-")[1].strip()
                    PrimaryValue = account_name.PARTY_ID
                    SecondLable = "Sending Account Name"
                    SecondValue = account_name.PARTY_NAME
                elif subTabName == "Details" and TreeParam.startswith('Receiving Account'):
                    account_name = Sql.GetFirst("SELECT PARTY_NAME,PARTY_ID FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' AND CPQ_PARTNER_FUNCTION LIKE '%RECEIVING%'"+" AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                    PrimaryLable = "Receiving Account ID"
                    PrimaryValue = account_name.PARTY_ID
                    SecondLable = "Receiving Account Name"
                    SecondValue = account_name.PARTY_NAME
                elif (subTabName == "Sending Equipment" or subTabName == "Service Fab Value Drivers" or subTabName == "Service Cost and Value Drivers" or subTabName == "Entitlements") and TreeParam.startswith("Sending Equipment"):                    
                    account_id = Sql.GetFirst("SELECT ACCOUNT_ID FROM SAQSRA (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND RELOCATION_TYPE LIKE '%SENDING%' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                    PrimaryLable = "Sending Account ID"
                    PrimaryValue = str(account_id.ACCOUNT_ID)
                    SecondLable = str(subTabName)
                    SecondValue = "ALL"
                elif (subTabName == "Receiving Equipment" or subTabName == "Service Fab Value Drivers" or subTabName == "Service Cost and Value Drivers" or subTabName == "Entitlements") and TreeParam.startswith("Receiving Equipment"):                    
                    account_id = Sql.GetFirst("SELECT ACCOUNT_ID FROM SAQSRA (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND RELOCATION_TYPE LIKE '%RECEIVING%'  AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                    PrimaryLable = "Receiving Account ID"
                    PrimaryValue = str(account_id.ACCOUNT_ID)
                    SecondLable = str(subTabName)
                    SecondValue = "ALL"
            else:
                ThirdQuery = Sql.GetFirst(
                "select * from SYOBJD (nolock) where OBJECT_NAME = '" + str(ObjName) + "' AND IS_KEY = 'True' "
                )
            Tab_Obj_Name = Sql.GetFirst(
                "SELECT REPLACE(REPLACE(SYOBJS.COLUMNS,'[',''),']','') as COLUMNS, OBJ_REC_ID from SYOBJS (nolock) where CONTAINER_NAME = '"
                + str(ObjName)
                + "' and NAME = 'Secondary Header list' "
            )
            if Tab_Obj_Name is not None:
                column = (Tab_Obj_Name.COLUMNS).replace("'", "").replace('"', "").replace(" ", "")
                columns = column.split(",")
                table_name = ""
                objd_records_obj = Sql.GetList(
                    """SELECT TOP 10 DISPLAY_ORDER,FIELD_LABEL, OBJECT_NAME,DATA_TYPE FROM SYOBJD (NOLOCK) WHERE API_NAME IN %s AND PARENT_OBJECT_RECORD_ID ='%s' ORDER BY abs(DISPLAY_ORDER) """
                    % (tuple(columns), Tab_Obj_Name.OBJ_REC_ID)
                )
                ListKey = [str(objd_records.FIELD_LABEL) for objd_records in objd_records_obj]
                ListKeyType = [str(objd_records.DATA_TYPE) for objd_records in objd_records_obj]                
                ListKey[0] = ''
                if "DEFAULT" in str(column):
                    column = str(column).replace("DEFAULT", "[DEFAULT]")
                if str(ObjName) == "SAQRIB":                    
                    getbillid = Sql.GetFirst("select QUOTE_BILLING_PLAN_RECORD_ID from SAQRIB(nolock) where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                    if getbillid:
                        CurrentRecordId = getbillid.QUOTE_BILLING_PLAN_RECORD_ID
                if ObjName == "SAQTMT":                    
                    itm_gb_node = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                    if itm_gb_node:
                        CurrentRecordId = itm_gb_node.MASTER_TABLE_QUOTE_RECORD_ID
                elif TabName == "Profile" and TreeParentParam == "Assigned Members":
                    getname = Sql.GetFirst("select ID,NAME from USERS (NOLOCK) where USERNAME ='"+str(TreeParam)+"' ")
                    PrimaryLable = "Key"
                    PrimaryValue = getname.ID
                    SecondLable = "Name"
                    SecondValue = str(TreeParam)
                    ThirdLable = "User Name"
                    ThirdValue = getname.NAME
                elif TabName == "Object" and TreeParentParam == "Indexes":
                    getname = Sql.GetFirst("select INDEX_NAME from SYOBJX (NOLOCK) where RECORD_ID ='"+str(CurrentRecordId)+"' ")
                    PrimaryLable = "Index Name"
                    PrimaryValue = str(TreeParam)
                elif TabName == "Object" and TreeParentParam == "Constraints":                    
                    getname = Sql.GetFirst("select CONSTRAINT_TYPE from SYOBJC (NOLOCK) where OBJECT_CONSTRAINT_RECORD_ID ='"+str(CurrentRecordId)+"' ")
                    PrimaryLable = "Constraint Type"
                    PrimaryValue = str(TreeParam)
                    #SecondLable = "Name"
                    #SecondValue = str(TreeParam)
                elif ObjName == "SAQICO":
                    CurrentRecordId = CPQID.KeyCPQId.GetKEYId('SAQICO',str(CurrentRecordId))
                    #Trace.Write("CurrentRecordId--->"+str(CurrentRecordId))              
                    # annualized_details = Sql.GetFirst("SELECT QUOTE_ITEM_COVERED_OBJECT_RECORD_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"' AND LINE = '"+str(CurrentRecordId)+"'")
                    #if rec_value:
                    #CurrentRecordId = rec_value.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID
                elif ObjName == "SAQSGB" and TreeSuperParentParam == "Receiving Equipment" and subTabName == "Equipment Details":                    
                    get_val = Sql.GetFirst("select FABLOCATION_ID from SAQSGB(nolock) where SERVICE_ID = '"+str(TreeTopSuperParentParam)+"' and FABLOCATION_ID = '"+str(TreeParentParam)+"'")
                    PrimaryLable = "Fab Location ID "
                    PrimaryValue = get_val.FABLOCATION_ID
                    SecondLable = "Greenbook"
                    SecondValue = str(TreeParam)
                    ThirdLable = "Equipment"
                    ThirdValue = "ALL"
                elif ObjName == "SAQSFB":                    
                    qte_fab_node = Sql.GetFirst("SELECT QUOTE_SERVICE_FAB_LOCATION_RECORD_ID FROM SAQSFB (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                    if qte_fab_node:
                        CurrentRecordId = qte_fab_node.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID
                if str(ObjName) not in ("SYPROH","SAQRIB"):
                    ValQuery = Sql.GetFirst(
                        "select "
                        + str(column)
                        + " from "
                        + str(ObjName)
                        + " where "
                        + str(columns[0])
                        + " = '"
                        + str(CurrentRecordId)
                        + "'"
                    )
                elif str(ObjName) == "SAQRIB" and TreeParam != "Billing":
                    ValQuery = Sql.GetFirst(
                        "select "
                        + str(column)
                        + " from "
                        + str(ObjName)
                        + " where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"' and SERVICE_ID = '"+str(TreeParam)+"'")
                elif str(ObjName) == "SAQRIB" and TreeParam == "Billing":
                    ValQuery = Sql.GetFirst(
                        "select QUOTE_RECORD_ID,CONTRACT_VALID_FROM,CONTRACT_VALID_TO SAQTRV from SAQTRV where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QUOTE_REVISION_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                else:
                    ValQuery = Sql.GetFirst(
                        "select "
                        + str(column)
                        + " from "
                        + str(ObjName)
                        + " where "
                        + "PROFILE_OBJECT_RECORD_ID"
                        + " = '"
                        + str(CurrentRecordId)
                        + "'"
                    )
                ListVal = []
                if ValQuery:
                    for key, val in enumerate(ValQuery):
                        a = str(val).split(",")
                        valu = ",".join(a[1:])
                        value = valu.replace("]", "").lstrip()
                        ListVal.append(value)
                        PrimaryLable = ListKey[0]
                        PrimaryValue = CPQID.KeyCPQId.GetCPQId(str(ObjName), str(ListVal[0]))
                try:
                    if ObjName == "SAQRIB":
                        SecondLable = ListKey[1]
                        SecondValue = str(ListVal[1].split(" ")[0])
                    else:
                        if (ObjName == "SAQFGB" or ObjName == "SAQFEQ"):
                            Trace.Write("SecondLable objectName"+str(SecondLable))
                        elif (ObjName != "SAQSRA"):
                            SecondLable = ListKey[1]
                            SecondValue = ListVal[1]
                except Exception as e:
                    Trace.Write("error1"+str(e))
                    Trace.Write("SecondLable"+str(SecondLable))
                try:
                    if str(ObjName) == "SYPROH":
                        ThirdLable = ListKey[2]
                        ThirdLablevall = ListKeyType[2]
                        ThirdValue = str(ListVal[2]).encode("ascii", "ignore")
                        if str(ThirdValue).upper() == "TRUE":
                            ThirdValue = (
                                '<input id="VISIBLE_H" type="CHECKBOX" value="'
                                + ThirdLablevall
                                + '" class="custom"  disabled checked><span class="lbl"></span>'
                            )
                        else:
                            ThirdValue = (
                                '<input id="VISIBLE_H" type="CHECKBOX" value="'
                                + ThirdLablevall
                                + '" class="custom"  disabled><span class="lbl"></span>'
                            )
                    else:
                        ##changed if to elif A055S000P01-3182
                        if (ObjName == "SAQFGB" or ObjName == "SAQFEQ"):
                            Trace.Write("ThirdLable objectName"+str(ThirdLable))
                        elif ObjName == "SAQRIB":
                            ThirdLable = ListKey[2]
                            ThirdValue = str(ListVal[2].split(" ")[0])
                        elif ObjName == "SAQTIP":
                            Trace.Write("SHP_Sub "+str(ListVal[3]))
                            ThirdLable = "Party ID"
                            ThirdValue = str(ListVal[2])
                            # FourthLable = "Party Name"
                            # FourthValue = str(ListVal[3])
                        elif ObjName == "CTCTIP":
                            ThirdLable = "Party ID"
                            ThirdValue = str(ListVal[2])
                        else:
                            ThirdLable = ListKey[2]
                            ThirdValue = str(ListVal[2]).encode("ascii", "ignore")
                except:
                    Trace.Write("error2")
                try:
                    getQuotetype = ""
                    if ObjName == 'ACACHR' or  TreeSuperParentParam == "Approvals":
                        Trace.Write("1097---")
                        FourthLable = "Approval Round"
                        FourthValue = TreeParam
                    #CurrentTabName = TestProduct.CurrentTab
                    if TabName == "Quote":
                        getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()
                    elif TabName == "Contract":
                        getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_016912").GetValue()
                    if ObjName == "SAQTIP":
                        FourthLable = "Source Account Name"
                        FourthValue = ListVal[3]
                    if ObjName == "CTCTIP":
                        FourthLable = "Party Name"
                        FourthValue = ListVal[3]
                    else:
                        FourthLable = ListKey[3]
                        FourthValue = ListVal[3]                    
                except Exception as e:
                    Trace.Write("error3"+str(e))
                try:
                    FifthLable = ListKey[4]
                    FifthValue = ListVal[4]
                except:
                    Trace.Write("error4")
                try:
                    if ObjName =="SAQSCO":
                        SixthLable = ""
                        SixthValue = ""
                    else:
                        SixthLable = ListKey[5]
                        SixthValue = ListVal[5]
                except:
                    Trace.Write("error5")                
                if str(ObjName) == 'SYPGAC' and TabName == 'Tab':
                    PrimaryLable = "Key"
                    PrimaryValue = PrimaryValue                    
                if (TreeParentParam == "Sending Equipment" or TreeParentParam == "Receiving Equipment") and (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Fab Value Drivers" or subTabName == "Fab Cost and Value Drivers"):
                    get_val = Sql.GetFirst("select SERVICE_ID,SERVICE_DESCRIPTION,SERVICE_TYPE,FABLOCATION_ID from SAQSFB(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
                    PrimaryLable = "Product Offering ID "
                    PrimaryValue = get_val.SERVICE_ID
                    SecondLable = "Product Offering Description"
                    SecondValue = get_val.SERVICE_DESCRIPTION
                    ThirdLable = "Product Offering Type"
                    ThirdValue = get_val.SERVICE_TYPE
                    FourthLable = "Fab Location ID"
                    FourthValue = str(TreeParam)
                    FifthLable = "Equipment"
                    FifthValue = "ALL"
                elif (ObjName == 'ACACHR' or TreeSuperParentParam == "Approvals"):
                    Trace.Write("inside round")
                    getchain = Sql.GetFirst("SELECT APRCHN_NAME FROM ACAPCH WHERE APRCHN_ID = '{}'".format(str(TreeParentParam)))
                    PrimaryLable = 'Approval Chain ID'
                    PrimaryValue = str(TreeParentParam)
                    SecondLable = 'Approval Chain Name'
                    SecondValue = getchain.APRCHN_NAME
                    ThirdLable = 'Approval Round'
                    ThirdValue = str(TreeParam).split(' ')[1]
                    FourthLable = ''
                    FourthValue = ''
                if (TreeSuperParentParam == "Sending Equipment" or TreeSuperParentParam == "Receiving Equipment") and (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Greenbook Fab Value Drivers" or subTabName == "Greenbook Cost and Value Drivers" or subTabName == "Equipment Fab Value Drivers" or subTabName =="Details" ):
                    if subTabName == "Equipment Fab Value Drivers":
                        get_val = Sql.GetFirst(" select FABLOCATION_ID,FABLOCATION_NAME,EQUIPMENT_ID,SERIAL_NUMBER from SAQFEQ where FABLOCATION_ID = '"+str(TreeParentParam)+"'")
                        PrimaryLable = "Fab Location ID "
                        PrimaryValue = get_val.FABLOCATION_ID
                        SecondLable = "Fab Location Name"
                        SecondValue = get_val.FABLOCATION_NAME
                        ThirdLable = "Greenbook"
                        ThirdValue = str(TreeParam)
                        FourthLable = "Equipment ID"
                        FourthValue = get_val.EQUIPMENT_ID
                        FifthLable = "Serial Number"
                        FifthValue = get_val.SERIAL_NUMBER
                    else:
                        get_val = Sql.GetFirst("select FABLOCATION_ID from SAQSGB(nolock) where SERVICE_ID = '"+str(TreeTopSuperParentParam)+"' and FABLOCATION_ID = '"+str(TreeParentParam)+"'")
                        PrimaryLable = "Fab Location ID "
                        PrimaryValue = get_val.FABLOCATION_ID
                        SecondLable = "Greenbook"
                        SecondValue = str(TreeParam)
                        ThirdLable = "Equipment"
                        ThirdValue = "ALL"
                        # FourthLable = "Fab Location ID"
                        # FourthValue = get_val.FABLOCATION_ID
                        # FifthLable = "Equipment"
                        # FifthValue = "ALL"
                if (TopSuperParentParam == "Product Offerings") and (subTabName == "Exclusions" or subTabName == "New Parts" or subTabName == "Inclusions"):
                    try:
                        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
                        desc = getService.SERVICE_DESCRIPTION
                    except:
                        desc = ""
                    PrimaryLable = "Product Offering ID"
                    PrimaryValue = str(TreeParentParam)
                    SecondLable = "Product Offering Description"
                    SecondValue = getService.SERVICE_DESCRIPTION
                    FourthLable = "Greenbook"
                    FourthValue = str(TreeParam)
                    FifthLable = "Equipment"
                    FifthValue = "All"
                if (TreeTopSuperParentParam == "Complementary Products" ) and (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Greenbook Fab Value Drivers" or subTabName == "Greenbook Cost and Value Drivers" or subTabName == "Equipment Fab Value Drivers" or subTabName =="Details" or subTabName =="Customer Value Drivers" or subTabName =="Product Value Drivers"):
                    if TreeParentParam == "Sending Equipment" or TreeParentParam == "Receiving Equipment":
                        if TreeParam == "Receiving Equipment":
                            get_val = Sql.GetFirst("select FABLOCATION_ID from SAQSGB(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"' and FABLOCATION_ID = '"+str(TreeParam)+"'")
                        else:
                            get_val = Sql.GetFirst("select FABLOCATION_ID from SAQSGB(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"' and FABLOCATION_ID = '"+str(TreeParentParam)+"'")
                        Trace.Write("Fab_NODE_J")
                        PrimaryLable = "Product Offering ID"
                        PrimaryValue = str(TreeSuperParentParam)
                        SecondLable = "Fab Location ID"
                        SecondValue = str(TreeParentParam)
                        # ThirdLable = ""
                        # ThirdValue = ""
                    if subTabName == "Equipment Fab Value Drivers":
                        get_val = Sql.GetFirst(" select FABLOCATION_ID,FABLOCATION_NAME,EQUIPMENT_ID,SERIAL_NUMBER from SAQFEQ where FABLOCATION_ID = '"+str(TreeParentParam)+"'")
                        PrimaryLable = "Fab Location ID "
                        PrimaryValue = get_val.FABLOCATION_ID
                        SecondLable = "Fab Location Name"
                        SecondValue = get_val.FABLOCATION_NAME
                        ThirdLable = "Greenbook"
                        ThirdValue = str(TreeParam)
                        FourthLable = "Equipment ID"
                        FourthValue = get_val.EQUIPMENT_ID
                        FifthLable = "Serial Number"
                        FifthValue = get_val.SERIAL_NUMBER
                    elif (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Fab Value Drivers" or subTabName == "Fab Cost and Value Drivers"):
                        try:
                            getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
                            desc = getService.SERVICE_DESCRIPTION
                        except:
                            desc = ""
                        PrimaryLable = "Product Offering ID"
                        PrimaryValue = str(TreeSuperParentParam)
                        SecondLable = "Product Offering Description"
                        SecondValue = getService.SERVICE_DESCRIPTION
                        ThirdLable = "Product Offering Type"
                        ThirdValue = str(TreeTopSuperParentParam)
                        #FourthLable = "Fab Location ID"
                        #FourthValue = str(TreeParam)
                        FourthLable = "Greenbooks"
                        FourthValue = "All"
                        FifthLable = "Equipment"
                        FifthValue = "All"
                    else:
                        Trace.Write("Lineno:1179")
                        PrimaryLable = "Product Offering ID"
                        PrimaryValue = str(TreeSuperParentParam)
                        #SecondLable = "Fab Location ID"
                        #SecondValue = str(TreeParentParam)
                        SecondLable = "Greenbook"
                        SecondValue = str(TreeParam)
                        # FourthLable = "Fab Location ID"
                        # FourthValue = get_val.FABLOCATION_ID
                        # FifthLable = "Equipment"
                        # FifthValue = "ALL"
                if str(ObjName) == 'SAQSFB':
                    if (TreeParentParam == "Sending Equipment" or TreeParentParam == "Receiving Equipment") and TreeSuperParentParam != 'Add-On Products':
                        get_val = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQSFB(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
                        ThirdLable = "Product Offering Description"
                        ThirdValue = get_val.SERVICE_DESCRIPTION
                        FourthLable = "Product Offering Type"
                        FourthValue = TreeTopSuperParentParam
                        FifthLable = " Fab Location ID"
                        FifthValue = TreeParam
                    else:
                        if TreeSuperParentParam != 'Add-On Products':                            
                            get_val = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQSFB(nolock) where SERVICE_ID = '"+str(TreeParentParam)+"'")
                            PrimaryLable = "Product Offering ID"
                            PrimaryValue = str(TreeParentParam)
                            SecondLable = "Product Offering Description"
                            SecondValue = get_val.SERVICE_DESCRIPTION
                            ThirdLable = "Product Offering Type"
                            ThirdValue = str(TreeSuperParentParam)
                            FourthLable = " Fab Location ID"
                            FourthValue = TreeParam
                if (str(ObjName) == 'SAQSCO' and (str(TreeTopSuperParentParam) == "COMPREHENSIVE SERVICES" or str(TreeSuperParentParam) == "COMPREHENSIVE SERVICES")):
                    get_val = Sql.GetFirst(" SELECT EQUIPMENT_ID,SERIAL_NO FROM SAQSCO WHERE GREENBOOK = '"+str(TreeParam)+"'")
                    FifthLable = "Equipment ID"
                    FifthValue = get_val.EQUIPMENT_ID
                    SixthLable = "Serial No"
                    SixthValue = get_val.SERIAL_NO
                if (str(ObjName) == 'SAQTSV'or str(ObjName) == 'SAQSCO' or str(ObjName) == 'SAQSPT') and TreeSuperParentParam == 'Product Offerings'and TabName == "Quotes":
                    ##Added the sixth label value....
                    entitlement_obj = Sql.GetFirst("select replace(ENTITLEMENT_XML,'&',';#38') as ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id,TreeParam))
                    if entitlement_obj:
                        entitlement_xml = entitlement_obj.ENTITLEMENT_XML
                        import re
                        quote_item_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                        quote_type_id = re.compile(r'<ENTITLEMENT_ID>AGS_'+str(TreeParam)+'[^>]*?_PQB_QTETYP</ENTITLEMENT_ID>')
                        quote_type_value = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>')
                        for m in re.finditer(quote_item_tag, entitlement_xml):
                            sub_string = m.group(1)
                            type_id = re.findall(quote_type_id,sub_string)
                            if type_id:
                                type_value = re.findall(quote_type_value,sub_string)
                                type_value = type_value[0]
                                SeventhLable = "Quote Type"
                                SeventhValue = str(type_value) if type_value else ""
                                break
                    try:
                        TreeParam = Quote.GetGlobal("TreeParam")
                    except Exception:
                        TreeParam = ''
                    try:
                        TreeParentParam = Quote.GetGlobal("TreeParentLevel0")
                    except Exception:
                        TreeParentParam = ''
                    getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV(nolock) where SERVICE_ID = '"+str(TreeParam)+"'")
                    PrimaryLable = "Product Offering ID"
                    PrimaryValue = TreeParam
                    ThirdLable = "POA Product Offering Quote Item Grouping"
                    ThirdValue = TreeParentParam
                    if ObjName == "SAQSPT":
                        parts_obj = Sql.GetFirst("select PART_NUMBER from SAQSPT(nolock) where QUOTE_SERVICE_PART_RECORD_ID = '{}'".format(CurrentRecordId))
                        FourthLable = "Equipment"
                        FourthValue = "All"
                        FifthLable = "Part Number"
                        FifthValue = parts_obj.PART_NUMBER
                    ##adding configuration status in offering subtab                    
                    where_cond = "WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}'".format(contract_quote_record_id, quote_revision_record_id, TreeParam )
                    status_image =''
                    try:                       
                        get_status = Sql.GetFirst("SELECT CONFIGURATION_STATUS FROM SAQTSE (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}'".format(contract_quote_record_id, quote_revision_record_id, TreeParam ) )
                        if get_status:
                            if get_status.CONFIGURATION_STATUS == 'COMPLETE':
                                status_image = 'config_status_icon.png'
                            elif get_status.CONFIGURATION_STATUS == 'INCOMPLETE':
                                status_image = 'config_pend_status_icon.png'
                            elif get_status.CONFIGURATION_STATUS == 'ERROR':
                                status_image = 'config_incomp_status_icon.png'
                    except:
                        status_image = ''
                    if ObjName == "SAQSPT":
                        SixthLable = "Configuration Status"
                    else:
                        FourthLable = "Configuration Status"
                        FifthLable  = ""
                        FifthValue = ""
                    if status_image:
                        if ObjName == "SAQSPT":
                            SixthValue = '<img class="treeinsideicon" src="/mt/APPLIEDMATERIALS_SIT/Additionalfiles/AMAT/Quoteimages/{image}"/>'.format(image = status_image)
                        else:
                            FourthValue = '<img class="treeinsideicon" src="/mt/APPLIEDMATERIALS_SIT/Additionalfiles/AMAT/Quoteimages/{image}"/>'.format(image = status_image)
                    # FifthLable = ""
                    # FifthValue = ""
                    if getService is not None:
                        SecondLable = "Product Offering Description"
                        SecondValue = getService.SERVICE_DESCRIPTION
                    if 'SPARE' in getQuotetype:
                        FourthLable = ""
                        FourthValue = ""
                    covered_obj = Sql.GetFirst("select EQUIPMENT_ID from SAQSCO(nolock) where QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(contract_quote_record_id = contract_quote_record_id,quote_revision_record_id=quote_revision_record_id))
                    if covered_obj is not None and (subTabName == "Equipment" or subTabName == 'Entitlements' or subTabName == 'Service Fab Value Drivers' or subTabName == 'Service Cost and Value Drivers' or subTabName == 'Customer Value Drivers' or subTabName == 'Product Value Drivers'):
                        FourthLable = "Equipment"
                        FourthValue = "All"
                        ##adding configuration status in offering subtab                        
                        FifthLable = "Configuration Status"
                        if status_image:
                            FifthValue = '<img class="treeinsideicon" src="/mt/appliedmaterials_sit/Additionalfiles/AMAT/Quoteimages/{image}"/>'.format(image = status_image)                        
                    elif covered_obj is not None and (subTabName == "Sending Equipment" or subTabName == 'Entitlements' or subTabName == 'Service Fab Value Drivers' or subTabName == 'Service Cost and Value Drivers' or subTabName == 'Customer Value Drivers' or subTabName == 'Product Value Drivers'):
                        FourthLable = "Sending Equipment"
                        FourthValue = "All"
                        FifthLable = ""
                        FifthValue = ""
                    elif covered_obj is not None and (subTabName == "Receiving Equipment" or subTabName == 'Entitlements' or subTabName == 'Service Fab Value Drivers' or subTabName == 'Service Cost and Value Drivers' or subTabName == 'Customer Value Drivers' or subTabName == 'Product Value Drivers'):
                        FourthLable = "Receiving Equipment"
                        FourthValue = "All"
                        FifthLable = ""
                        FifthValue = ""                
                elif (TreeSuperParentParam == "Fab Locations" or TreeTopSuperParentParam == "Fab Locations") and (subTabName == 'Equipment' or subTabName == "Details" or subTabName == "Customer Value Drivers" or subTabName == "Fab Value Drivers"):                   
                    if subTabName == "Details" and TreeParentParam.startswith("Sending"):
                        Trace.Write("Fab1")
                        PrimaryLable = "Sending Account ID"
                        PrimaryValue = str(TreeParentParam).split("-")[1].strip()
                        SecondLable = "Fab Location ID"
                        SecondValue = str(TreeParam)
                        ThirdLable = "Fab Location Name"
                        ThirdValue = getFab.FABLOCATION_NAME
                    elif subTabName == "Details" and TreeParentParam.startswith("Receiving"):
                        PrimaryLable = "Receiving Account ID"
                        PrimaryValue = str(TreeParentParam).split("-")[1].strip()
                        SecondLable = "Fab Location ID"
                        SecondValue = str(TreeParam)
                        ThirdLable = "Fab Location Name"
                        ThirdValue = getFab.FABLOCATION_NAME
                    elif subTabName == "Equipment" and TreeParentParam.startswith("Sending"):                        
                        PrimaryLable = "Sending Account ID"
                        PrimaryValue = str(TreeParentParam).split("-")[1].strip()
                        SecondLable = "Fab Location ID"
                        SecondValue = str(TreeParam)
                        ThirdLable = "Fab Location Name"
                        ThirdValue = getFab.FABLOCATION_NAME
                        FourthLable = "Equipment"
                        FourthValue = "ALL"
                    elif subTabName == "Equipment" and TreeParentParam.startswith("Receiving"):
                        PrimaryLable = "Receiving Account ID"
                        PrimaryValue = str(TreeParentParam).split("-")[1].strip()
                        SecondLable = "Fab Location ID"
                        SecondValue = str(TreeParam)
                        ThirdLable = "Fab Location Name"
                        ThirdValue = getFab.FABLOCATION_NAME
                        FourthLable = "Equipment"
                        FourthValue = "ALL"
                    elif subTabName == "Fab Value Drivers" and TreeParentParam.startswith("Sending"):
                        TreeParam = str(TreeParam).split("-")[0].strip()
                        getFab = Sql.GetFirst("select FABLOCATION_NAME from SAQFBL(nolock) where FABLOCATION_ID = '"+str(TreeParam)+"'")
                        PrimaryLable = "Sending Account ID"
                        PrimaryValue = str(TreeParentParam).split("-")[1].strip()
                        SecondLable = "Fab Location ID"
                        SecondValue = str(TreeParam)
                        ThirdLable = "Fab Location Name"
                        ThirdValue = getFab.FABLOCATION_NAME
                        FourthLable = "Equipment"
                        FourthValue = "ALL"
                    elif subTabName == "Fab Value Drivers" and TreeParentParam.startswith("Receiving"):
                        TreeParam = str(TreeParam).split("-")[0].strip()
                        getFab = Sql.GetFirst("select FABLOCATION_NAME from SAQFBL(nolock) where FABLOCATION_ID = '"+str(TreeParam)+"'")
                        PrimaryLable = "Receiving Account ID"
                        PrimaryValue = str(TreeParentParam).split("-")[1].strip()
                        SecondLable = "Fab Location ID"
                        SecondValue = str(TreeParam)
                        ThirdLable = "Fab Location Name"
                        ThirdValue = getFab.FABLOCATION_NAME
                        FourthLable = "Equipment"
                        FourthValue = "ALL"
                elif str(ObjName) == 'ACACSA' and str(TreeParentParam) == 'Approval Chain Steps':
                    PrimaryLable = ListKey[0]
                    PrimaryValue = PrimaryValue
                elif str(ObjName) == 'ACAPTF' and str(TreeParentParam) == 'Approval Chain Steps':
                    PrimaryLable = ListKey[0]
                    PrimaryValue = PrimaryValue
    if (TreeParam == "Quote Information" and str(ObjName) == 'SAQTMT') and (str(CurrentRecordId) != 'SYOBJR-98857' and str(CurrentRecordId) != 'SYOBJR-98858' and str(CurrentRecordId) != 'SYOBJR-00028'):
        PrimaryLable = ListKey[1]
        PrimaryValue = ListVal[1]
        SecondLable = ListKey[2]
        SecondValue = ListVal[2]
        try:
            ThirdLable = ListKey[3]
            ThirdValue = ListVal[3]
        except:
            ThirdLable = ''
            ThirdValue = ''        
    if  TreeTopSuperParentParam == "Quote Items" and str(TreeParam) != "" and (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Greenbook Fab Value Drivers" or subTabName == "Greenbook Cost and Value Drivers" or subTabName == "Details"):       
        PrimaryLable = "Product Offering ID"
        PrimaryValue = TreeSuperParentParam.split('-')[1]
        SecondLable = "Fab Location ID"
        SecondValue = TreeParentParam
        ThirdLable = "Greenbook"
        ThirdValue = TreeParam
        FourthLable = "Equipment"
        FourthValue = "All"
    elif TreeSuperParentParam == 'Quote Items':
        TreeParentParam = TreeParentParam.split('-')
        PrimaryLable = "Line Item ID"
        PrimaryValue = TreeParentParam[0].strip()
        SecondLable = "Product Offering ID"
        SecondValue = TreeParentParam[1].strip()
        ThirdLable = "Fab Location ID"
        ThirdValue = TreeParam
        FourthLable = "Greenbooks"
        FourthValue = "All"
        FifthLable = "Equipment"
        FifthValue = "All"
    elif TreeParam == "Approvals" and CurrentTabName == "My Approval Queue":
        transaction_rec_id = Product.Attr("QSTN_SYSEFL_AC_00063").GetValue()
        chain_information = Sql.GetFirst(" select DISTINCT TOP 10 ACAPCH.APRCHN_ID, ACAPMA.APRCHN_RECORD_ID ,ACAPCH.APPROVAL_CHAIN_RECORD_ID, ACAPCH.APRCHN_NAME, ACAPCH.APPROVAL_METHOD FROM ACAPMA (nolock) inner join ACAPCH (nolock) on ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID inner join ACAPTX(nolock) on ACAPTX.APRCHN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID where ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"+str(transaction_rec_id)+"' ")
        if chain_information:
            PrimaryLable = "Approval Chain ID"
            PrimaryValue = chain_information.APRCHN_ID
            SecondLable = "Approval Chain Name"
            SecondValue = chain_information.APRCHN_NAME
            ThirdLable = "Approval Chain Method"
            ThirdValue = chain_information.APPROVAL_METHOD
        else:
            PrimaryLable = "Approvals"
            PrimaryValue = "All"
            SecondLable = ""
            SecondValue = ""
    elif TreeParam == "Approvals" and CurrentTabName == "Team Approvals Queue":
        transaction_rec_id = Product.Attr("QSTN_SYSEFL_AC_00063").GetValue()
        chain_information = Sql.GetFirst(" select DISTINCT TOP 10 ACAPCH.APRCHN_ID, ACAPMA.APRCHN_RECORD_ID ,ACAPCH.APPROVAL_CHAIN_RECORD_ID, ACAPCH.APRCHN_NAME, ACAPCH.APPROVAL_METHOD FROM ACAPMA (nolock) inner join ACAPCH (nolock) on ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID inner join ACAPTX(nolock) on ACAPTX.APRCHN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID where ACAPTX.APPROVAL_TRANSACTION_RECORD_ID = '"+str(transaction_rec_id)+"' ")
        PrimaryLable = "Approval Chain ID"
        if chain_information:
            PrimaryValue = chain_information.APRCHN_ID
            SecondLable = "Approval Chain Name"
            SecondValue = chain_information.APRCHN_NAME
            ThirdLable = "Approval Chain Method"
            ThirdValue = chain_information.APPROVAL_METHOD
        else:
            PrimaryLable = "Approvals"
            PrimaryValue = "All"
            SecondLable = ""
            SecondValue = ""
    elif TreeParam == "Quote Preview":
        PrimaryLable = ListKey[1]
        PrimaryValue = ListVal[1]
        SecondLable = ListKey[2]
        SecondValue = ListVal[2]
        ThirdLable = ListKey[3]
        ThirdValue = ListVal[3]        
    elif TreeParentParam == "Sales" and str(CurrentTabName) != "Profile":
        if ListVal:
            PrimaryLable = ListKey[1]
            PrimaryValue = ListVal[1]
            SecondLable = ListKey[2]
            SecondValue = ListVal[2]
        else:
            PrimaryLable = ListKey[1]
            PrimaryValue = TreeParam
            SecondLable = ListKey[2]
            SecondValue = ""
        ThirdLable = ""
        ThirdValue = ""
    # SHP Contract Document Starts
    elif TreeParam == "Contract Documents" and  ObjName == "SAQDOC":
        PrimaryLable = "Account ID"
        PrimaryValue = "ALL"
        SecondLable = "Account Name"
        SecondValue = "ALL"
    # SHP Contract Document Ends
    elif ObjName == "SAQSCA" and (TreeSuperParentParam == "Receiving Equipment" or TreeSuperParentParam == "Sending Equipment"):        
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeTopSuperParentParam)
        SecondLable = "Fab Location ID"
        SecondValue = str(TreeParentParam)
        ThirdLable = "Greenbook"
        ThirdValue = str(TreeParam)
        FourthLable = "Equipment ID"
        FourthValue = str(EquipmentId)
        FifthLable = "Serial Number"
        FifthValue = str(SerialNumber)
        SixthLable = "Assembly ID"
        SixthValue = str(AssemblyId)
    elif subTabName == "Assembly Entitlements" and (TreeSuperParentParam == "Receiving Equipment" or TreeSuperParentParam == "Sending Equipment"):
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeTopSuperParentParam)
        SecondLable = "Fab Location ID"
        SecondValue = str(TreeParentParam)
        ThirdLable = "Greenbook"
        ThirdValue = str(TreeParam)
        FourthLable = "Equipment ID"
        FourthValue = str(EquipmentId)
        FifthLable = "Serial Number"
        FifthValue = str(SerialNumber)
        SixthLable = "Assembly ID"
        SixthValue = str(AssemblyId)
    elif subTabName == "Events" or subTabName == "Assembly Entitlements" :
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV(nolock) where SERVICE_ID = '"+str(TreeParam)+"'")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeParam)
        SecondLable = "Product Offering Description"
        if getService is not None:
            SecondValue = getService.SERVICE_DESCRIPTION
        else:
            SecondValue =" "
        ThirdLable = "Greenbook"
        ThirdValue = "ALL"
        PreventiveMaintainenceobj = Sql.GetFirst("select EQUIPMENT_ID from SAQSAP(nolock) where QUOTE_RECORD_ID = '{contract_quote_record_id}' and EQUIPMENT_ID = '{Equipment_Id}' and ASSEMBLY_ID = '{Assembly_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(contract_quote_record_id = contract_quote_record_id,Equipment_Id = EquipmentId,Assembly_id =AssemblyId,quote_revision_record_id=quote_revision_record_id ))
        if PreventiveMaintainenceobj is not None:
            FifthLable = "Events"
            FifthValue = "All"
        PMEvents = "False"
    elif ObjName == "SAQSCA":
        #A055S000P01-3208 start        
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeSuperParentParam)
        SecondLable = "Fab Location ID"
        SecondValue = str(TreeParentParam)
        #A055S000P01-3208 end
        ThirdLable = "Greenbook"
        ThirdValue = str(TreeParam)
        FourthLable = "Equipment ID"
        FourthValue = str(EquipmentId)
        FifthLable = "Serial Number"
        FifthValue = str(SerialNumber)
        SixthLable = "Assembly ID"
        SixthValue = str(AssemblyId)
    elif TopSuperParentParam == "Product Offerings" and (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Fab Value Drivers" or subTabName == "Fab Cost and Value Drivers" or subTabName == "Service Fab Value Drivers" or subTabName == "Service Cost and Value Drivers" or subTabName == "Customer Value Drivers" or subTabName == "Product Value Drivers") and current_prod !='SYSTEM ADMIN' and CurrentTab == 'Quotes':
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeParentParam)
        SecondLable = "Product Offering Description"
        SecondValue = getService.SERVICE_DESCRIPTION
        #ThirdLable = "Fab Location ID"
        #ThirdValue = str(TreeParam)
        ThirdLable = "Greenbooks"
        ThirdValue = "ALL"
        FourthLable = "Equipment"
        FourthValue = "ALL"    
    elif TreeParentParam == "Quote Items" and subTabName == "Entitlements" and getQuotetype == "ZWK1 - SPARES":
        PrimaryLable = ""
        PrimaryValue = ""
    elif TopSuperParentParam == "Quote Items" and (subTabName == "Equipment Entitlements" or subTabName == "Equipment Fab Value Drivers" or subTabName == "Equipment Cost and Value Drivers" or subTabName == "Equipment Details" or subTabName == "Customer Value Drivers" or subTabName == "Product Value Drivers"):
        #PrimaryLable = "Product Offering ID"
        #PrimaryValue = str(TreeSuperParentParam)
        #SecondLable = "Line Item Id"
        #SecondValue = "ALL"
        if subTabName != "Equipment Details":
            PrimaryLable = ""
            PrimaryValue = ""
        ThirdLable = "Fab Location ID"
        ThirdValue = str(TreeParentParam)
        FourthLable = "Greenbook"
        FourthValue = str(TreeParam)
        FifthLable = "Equipment Id"
        FifthValue = str(EquipmentId)
        SixthLable = "Serial Number"
        SixthValue = str(SerialNumber)
    elif TopSuperParentParam == "Comprehensive Services" or TopSuperParentParam == "Add-On Products" or TopSuperParentParam == "Complementary Products":
        try:
            getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
            desc = getService.SERVICE_DESCRIPTION
        except:
            desc = ""
        if (subTabName == "Equipment Details" or subTabName == "Equipment Assemblies" or subTabName == "Equipment Entitlements" or subTabName == "Equipment Fab Value Drivers" or subTabName == "Equipment Cost and Value Drivers" or subTabName == "Customer Value Drivers" or subTabName == "Product Value Drivers"):
            PrimaryLable = "Product Offering ID"
            PrimaryValue = str(TreeSuperParentParam)
            SecondLable = "Product Offering Description"
            SecondValue = getService.SERVICE_DESCRIPTION
            #ThirdLable = "Fab Location ID"
            #ThirdValue = str(TreeParentParam)
            ThirdLable = "Greenbook"
            ThirdValue = str(TreeParam)
            FourthLable = "Equipment ID"
            FourthValue = str(EquipmentId)
            FifthLable = "Serial Number"
            FifthValue = str(SerialNumber)
        elif(str(ObjName)=="SAQRGG" or str(ObjName) == "SAQSKP") and (subTabName == 'Details' or subTabName == 'Events' or subTabName == 'Kit Detials' or subTabName == 'BoM'):
            PrimaryLable = "Product Offering ID"
            PrimaryValue = str(TreeSuperParentParam)
            SecondLable = "Product Offering Description"
            SecondValue = desc
            ThirdLable = "Greenbook"
            ThirdValue = str(TreeParentParam)
            FourthLable = "Got Code"
            FourthValue = str(TreeParam)
        elif((subTabName == "Details" or subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Greenbook Fab Value Drivers" or subTabName == "Greenbook Cost and Value Drivers" or subTabName == "Credits") and subTabName != "Assembly Details" or subTabName == "Customer Value Drivers" or subTabName == "Product Value Drivers"):
            if subTabName =='Entitlements' and str(ObjName) == "SAQSAO" and TreeParam == "Add-On Products":                
                get_addon_service_desc = Sql.GetFirst("SELECT * FROM SAQSGB (NOLOCK) WHERE QUOTE_SERVICE_GREENBOOK_RECORD_ID  = '{}'".format(CurrentRecordId))
                if get_addon_service_desc:
                    PrimaryLable = "Product Offering ID"
                    PrimaryValue = get_addon_service_desc.SERVICE_ID
                    SecondLable = "Product Offering Description"
                    SecondValue = get_addon_service_desc.SERVICE_DESCRIPTION
            else:
                addon_prd_rec_id = Product.GetGlobal('addon_prd_rec_id')
                if (TreeTopSuperParentParam == "Comprehensive Services" or TreeTopSuperParentParam == "Product Offerings" or TreeTopSuperParentParam == "Complementary Products" )and TreeParam != "Add-On Products" and (subTabName == "Details" or subTabName == "Events" ):
                    get_addon_service_desc = Sql.GetFirst("SELECT SERVICE_ID,SERVICE_DESCRIPTION FROM SAQRGG (NOLOCK) WHERE QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID = '{}'".format(CurrentRecordId))
                else:
                    get_addon_service_desc = Sql.GetFirst("SELECT * FROM SAQSGB (NOLOCK) WHERE QUOTE_SERVICE_GREENBOOK_RECORD_ID  = '"+str(addon_prd_rec_id)+"'")
                PrimaryLable = "Product Offering ID"
                PrimaryValue = str(get_addon_service_desc.SERVICE_ID)
                SecondLable = "Product Offering Description"
                SecondValue = str(get_addon_service_desc.SERVICE_DESCRIPTION)
                #ThirdLable = "Fab Location ID"
                #ThirdValue = str(TreeParentParam)
                ThirdLable = "Greenbook"
                ThirdValue = str(TreeParentParam) if "Add" in TreeParam else str(TreeParam)
                # if subTabName != "Details":
                #     FourthLable = "Equipment"
                #     FifthValue = "All"
        elif subTabName == "Details":
            PrimaryLable = ListKey[0]
            PrimaryValue = PrimaryValue
    elif TreeSuperTopParentParam == "Product Offerings" and (subTabName == "Equipment Assemblies" or subTabName == "Equipment Entitlements" or subTabName == "Equipment Fab Value Drivers" or subTabName == "Equipment Cost and Value Drivers" or subTabName == "Equipment Details" or subTabName == "Customer Value Drivers" or subTabName == "Product Value Drivers"):
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeSuperParentParam)
        #SecondLable = "Fab Location ID"
        #SecondValue = str(TreeParentParam)
        SecondLable = "Greenbook"
        SecondValue = str(TreeParam)
        ThirdLable = "Equipment ID"
        ThirdValue = str(EquipmentId)
        FourthLable = "Serial Number"
        FourthValue = str(SerialNumber)
        Trace.Write("check345"+str(FifthValue))
        #FourthLable = "Equipment"
        #FourthValue = "ALL"
    elif (TreeSuperParentParam == "Sending Equipment" and TreeSuperTopParentParam =="Complementary Products" and (subTabName == "Details")):
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeTopSuperParentParam)
        #SecondLable = "Fab Location ID"
        #SecondValue = str(TreeParentParam)
        SecondLable = "Greenbook"
        SecondValue = str(TreeParam)
    elif TreeTopSuperParentParam == "Complementary Products"  and (subTabName == "Details"):             
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeSuperParentParam)
        SecondLable = ""
        SecondValue = ""
        #ThirdLable = ""
        #ThirdValue = ""
    elif (TreeSuperParentParam == "Sending Equipment" or TreeSuperTopParentParam =="Complementary Products" and (subTabName == "Equipment Fab Value Drivers" or subTabName == "Equipment Entitlements" or subTabName == "Equipment Cost and Value Drivers" or subTabName == "Equipment Details" or subTabName == "Customer Value Drivers" or subTabName == "Product Value Drivers")):        
        if str(subTabName) != "Equipment":
            PrimaryLable = "Product Offering ID"
            PrimaryValue = str(TreeTopSuperParentParam)
            SecondLable = "Fab Location ID"
            SecondValue = str(TreeParentParam)
            ThirdLable = "Greenbook"
            ThirdValue = str(TreeParam)
            FourthLable = "Equipment ID"
            FourthValue = str(EquipmentId)
            FifthLable = "Serial Number"
            FifthValue = str(SerialNumber)
            Trace.Write("check345"+str(FifthValue))
            #FourthLable = "Equipment"
            #FourthValue = "ALL"
    elif (TreeTopSuperParentParam == "Fab Locations" or TreeSuperParentParam == "Fab Locations" and (subTabName == 'Equipment' or subTabName == 'Equipment Details' or subTabName == 'Customer Value Drivers' or subTabName == 'Details'  or subTabName == 'Equipment Fab Value Drivers')) and ("Sending" not in TreeParam or "Receiving" not in TreeParam):
        if ("Sending" not in TreeParam and "Receiving" not in TreeParam) and ("Sending" not in TreeParentParam and "Receiving" not in TreeParentParam):
            TreeParentParam = str(TreeParentParam).split("-")[0].strip()
            getFab = Sql.GetFirst("select FABLOCATION_NAME from SAQFBL(nolock) where FABLOCATION_ID = '"+str(TreeParentParam)+"'")
            if (subTabName == 'Equipment Fab Value Drivers' or subTabName == "Equipment Details") and TreeSuperParentParam.startswith("Sending"):
                PrimaryLable = "Sending Account ID"
                PrimaryValue = str(TreeSuperParentParam).split("-")[1].strip()
                SecondLable = "Fab Location ID"
                SecondValue = str(TreeParentParam)
                ThirdLable = "Fab Location Name"
                ThirdValue = getFab.FABLOCATION_NAME
                FourthLable = "Greenbook"
                FourthValue = str(TreeParam)
                FifthLable = "Equipment ID"
                FifthValue = str(EquipmentId)
                SixthLable = "Serial Number"
                SixthValue = str(SerialNumber)
            elif (subTabName == 'Equipment Fab Value Drivers' or subTabName == "Equipment Details") and TreeSuperParentParam.startswith("Receiving"):
                PrimaryLable = "Receiving Account ID"
                PrimaryValue = str(TreeSuperParentParam).split("-")[1].strip()
                SecondLable = "Fab Location ID"
                SecondValue = str(TreeParentParam)
                ThirdLable = "Fab Location Name"
                ThirdValue = getFab.FABLOCATION_NAME
                FourthLable = "Greenbook"
                FourthValue = str(TreeParam)
                FifthLable = "Equipment ID"
                FifthValue = str(EquipmentId)
                SixthLable = "Serial Number"
                SixthValue = str(SerialNumber)
            elif subTabName == "Details":
                PrimaryLable = "Fab Location ID"
                PrimaryValue = str(TreeParentParam)
                SecondLable = "Fab Location Name"
                SecondValue = getFab.FABLOCATION_NAME
                ThirdLable = "Greenbook"
                ThirdValue = str(TreeParam)
            else:
                PrimaryLable = "Fab Location ID"
                PrimaryValue = str(TreeParentParam)
                SecondLable = "Fab Location Name"
                SecondValue = getFab.FABLOCATION_NAME
                # ThirdLable = "Greenbook"
                # ThirdValue = str(TreeParam)
                # FourthLable = "Equipment"
                # FourthValue = "All"
        elif ("Sending" in TreeParam and "Receiving" in TreeParam) or ("Sending" in TreeParentParam and "Receiving" in TreeParentParam):
            TreeParam = str(TreeParam).split("-")[0].strip()
            getFab = Sql.GetFirst("select FABLOCATION_NAME from SAQFBL(nolock) where FABLOCATION_ID = '"+str(TreeParam)+"'")
            if subTabName == 'Equipment Fab Value Drivers' or subTabName == "Equipment Details":
                PrimaryLable = "Fab Location ID"
                PrimaryValue = str(TreeParentParam)
                SecondLable = "Fab Location Name"
                SecondValue = getFab.FABLOCATION_NAME
                ThirdLable = "Greenbook"
                ThirdValue = str(TreeParam)
                FourthLable = "Equipment ID"
                FourthValue = str(EquipmentId)
                FifthLable = "Serial Number"
                FifthValue = str(SerialNumber)
                SixthLable = ""
                SixthValue = ""
            elif subTabName == "Details":
                PrimaryLable = "Fab Location ID"
                PrimaryValue = str(TreeParentParam)
                SecondLable = "Fab Location Name"
                SecondValue = getFab.FABLOCATION_NAME
                ThirdLable = "Greenbook"
                ThirdValue = str(TreeParam)
            else:
                PrimaryLable = "Fab Location ID"
                PrimaryValue = str(TreeParentParam)
                SecondLable = "Fab Location Name"
                SecondValue = getFab.FABLOCATION_NAME
                ThirdLable = "Greenbook"
                ThirdValue = str(TreeParam)
                # FourthLable = "Equipment"
                # FourthValue = "All"    
    elif (TreeParentParam == "Fab Locations" and (subTabName == 'Equipment' or subTabName == 'Details' or subTabName == 'Customer Value Drivers')) and ("Sending" not in TreeParam and "Receiving" not in TreeParam):
        TreeParam = str(TreeParam).split("-")[0].strip()
        getFab = Sql.GetFirst("select FABLOCATION_NAME from SAQFBL(nolock) where FABLOCATION_ID = '"+str(TreeParam)+"'")
        PrimaryLable = "Fab Location ID"
        PrimaryValue = str(TreeParam)
        SecondLable = "Fab Location Name"
        SecondValue = getFab.FABLOCATION_NAME
        ThirdLable = "Greenbooks"
        ThirdValue = "All"
        FourthLable = "Equipment"
        FourthValue = "All"
    elif TreeParam == "Fab Locations":
        if subTabName == 'Equipment':
            PrimaryLable = "Fab Locations"
            PrimaryValue = "All"
            SecondLable = "Greenbooks"
            SecondValue = "All"
            ThirdLable = "Equipment"
            ThirdValue = "All"
        else:
            SecondLable = ""
            SecondValue = ""
            ThirdLable = ""
            ThirdValue = ""      
    if TreeParam == 'Quote Items' and (subTabName == "Summary" or subTabName == "Offerings" or subTabName == "Items" or subTabName == "Annualized Items" or subTabName == "Entitlement Cost/price"):        
        get_quote_details = Sql.GetFirst("select * from SAQTRV (nolock) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(contract_quote_record_id,quote_revision_record_id))        
        curr = get_quote_details.GLOBAL_CURRENCY
        Total=(get_quote_details.TOTAL_AMOUNT_INGL_CURR)        
        get_rounding_place = Sql.GetFirst("SELECT * FROM PRCURR (nolock) WHERE CURRENCY_RECORD_ID = '{}' ".format(get_quote_details.GLOBAL_CURRENCY_RECORD_ID))
        decimal_format = "{:,." + str(get_rounding_place.DISPLAY_DECIMAL_PLACES) + "f}"
        if subTabName == "Summary":
            PrimaryLable = "Total Excluding Tax/VAT/GST"
            PrimaryValue = decimal_format.format(float(get_quote_details.NET_VALUE_INGL_CURR))+" "+ curr if str(get_quote_details.NET_VALUE_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
            SecondLable = "Total Est Net Val"
            SecondValue = decimal_format.format(float(get_quote_details.ESTVAL_INGL_CURR))+" "+ curr if str(get_quote_details.ESTVAL_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
            ThirdLable = "Total Tax/VAT/GST"
            ThirdValue = decimal_format.format(float(get_quote_details.TAX_AMOUNT_INGL_CURR))+" "+ curr if str(get_quote_details.TAX_AMOUNT_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
            # ThirdLable = "Total Net Val"
            # ThirdValue = decimal_format.format(float(Total))+" "+ curr if str(Total) != '' else decimal_format.format(float("0.00"))+" "+curr
            FourthLable = "Total Amt"
            FourthValue = decimal_format.format(float(get_quote_details.TOTAL_AMOUNT_INGL_CURR))+" "+ curr if str(get_quote_details.TOTAL_AMOUNT_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
            FifthLable = "Total Margin Pct"
            FifthValue = decimal_format.format(float(get_quote_details.TOTAL_MARGIN_PERCENT))+" "+ "%" if str(get_quote_details.TOTAL_MARGIN_PERCENT) != '' else decimal_format.format(float("0.00"))+"%"
        elif get_quote_details:
            if subTabName == "Items":
                
                PrimaryLable = "Total Excluding Tax/VAT"
                PrimaryValue = decimal_format.format(float(get_quote_details.NET_VALUE_INGL_CURR))+" "+ curr if str(get_quote_details.NET_VALUE_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
                SecondLable = "Tax/VAT"
                #SecondValue = str("%.2f" % round(float(get_quote_details.TAX_AMOUNT_INGL_CURR),2))+" "+curr if str(get_quote_details.TAX_AMOUNT_INGL_CURR) != '' else '0.00'+" "+curr
                SecondValue = decimal_format.format(float(get_quote_details.TAX_AMOUNT_INGL_CURR))+" "+ curr if str(get_quote_details.TAX_AMOUNT_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
                ThirdLable = "Total Est Net Value"
                ThirdValue = decimal_format.format(float(get_quote_details.ESTVAL_INGL_CURR))+" "+ curr if str(get_quote_details.ESTVAL_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
                FourthLable = "Total Net Value"
                FourthValue = decimal_format.format(float(get_quote_details.NET_VALUE_INGL_CURR))+" "+ curr if str(get_quote_details.NET_VALUE_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
                FifthLable = "Total Margin"
                FifthValue = decimal_format.format(float("0.00"))+" "+curr
            elif subTabName == "Offerings":
                saqris_details = Sql.GetFirst("SELECT SUM(ESTIMATED_VALUE) AS ESTIMATED_VALUE, SUM(NET_VALUE_INGL_CURR) AS NET_VALUE, SUM(TAX_AMOUNT_INGL_CURR) AS TOTAL_TAX, SUM(TOTAL_AMOUNT_INGL_CURR) AS TOTAL_AMT FROM SAQRIS (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID != 'Z0117'".format(contract_quote_record_id,quote_revision_record_id))
                PrimaryLable = "Total Tax/VAT/GST"
                PrimaryValue = decimal_format.format(float(saqris_details.TOTAL_TAX))+" "+curr if saqris_details.TOTAL_TAX else decimal_format.format(float("0.00"))+" "+curr
                SecondLable = "Total Est Net Val"
                # SecondValue = str("%.2f" % round(float(get_quote_details.TOTAL_AMOUNT_INGL_CURR),2))+" "+curr if str(get_quote_details.TOTAL_AMOUNT_INGL_CURR) != '' else '0.00'+" "+curr
                #SecondValue = str("%.2f" % round(float(saqris_details.ESTIMATED_VALUE),2))+" "+curr if str(saqris_details.ESTIMATED_VALUE) != '' else '0.00'+" "+curr
                SecondValue = decimal_format.format(float(saqris_details.ESTIMATED_VALUE))+" "+ curr if str(saqris_details.ESTIMATED_VALUE) != '' else decimal_format.format(float("0.00"))+" "+curr
                ThirdLable = "Total Net Val"
                ThirdValue = decimal_format.format(float(saqris_details.NET_VALUE))+" "+ curr if str(saqris_details.NET_VALUE) != '' else decimal_format.format(float("0.00"))+" "+curr
                FourthLable = "Total  Amt"
                FourthValue = decimal_format.format(float(saqris_details.TOTAL_AMT))+" "+ curr if str(saqris_details.TOTAL_AMT) != '' else decimal_format.format(float("0.00"))+" "+curr
                FifthLable = "Total Margin"
                FifthValue = decimal_format.format(float("0.00"))+" "+curr
            else:
                PrimaryLable = "Total Sales Price"
                #PrimaryValue = str("%.2f" % round(float(get_quote_details.SALES_PRICE_INGL_CURR),2))+" "+curr if str(get_quote_details.SALES_PRICE_INGL_CURR) != '' else '0.00'+" "+curr
                PrimaryValue = decimal_format.format(float(get_quote_details.SALES_PRICE_INGL_CURR))+" "+ curr if str(get_quote_details.SALES_PRICE_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
                SecondLable = "Total Discount %"
                #SecondValue = str("%.2f" % round(float(get_quote_details.DISCOUNT_PERCENT),2))+" "+curr if str(get_quote_details.DISCOUNT_PERCENT) != '' else '0.00'+" "+curr
                SecondValue = decimal_format.format(float(get_quote_details.DISCOUNT_PERCENT))+" "+ curr if str(get_quote_details.DISCOUNT_PERCENT) != '' else decimal_format.format(float("0.00"))+" "+curr
                ThirdLable = "Total Discount Amount"
                #ThirdValue = str("%.2f" % round(float(get_quote_details.DISCOUNT_AMOUNT_INGL_CURR),2))+" "+curr if str(get_quote_details.DISCOUNT_AMOUNT_INGL_CURR) != '' else '0.00'+" "+curr
                ThirdValue = decimal_format.format(float(get_quote_details.DISCOUNT_AMOUNT_INGL_CURR))+" "+ curr if str(get_quote_details.DISCOUNT_AMOUNT_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
                FourthLable = "Total Credit"
                #FourthValue = str("%.2f" % round(float(get_quote_details.CREDIT_INGL_CURR),2))+" "+curr if str(get_quote_details.CREDIT_INGL_CURR) != '' else '0.00'+" "+curr
                FourthValue = decimal_format.format(float(get_quote_details.CREDIT_INGL_CURR))+" "+ curr if str(get_quote_details.CREDIT_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
                FifthValue = "Total Excluding Tax/VAT"
                FifthValue = decimal_format.format(float("0.00"))+" "+curr
                SixthLable = "Tax/VAT"
                #SixthValue = str("%.2f" % round(float(get_quote_details.TAX_AMOUNT_INGL_CURR),2))+" "+curr if str(get_quote_details.TAX_AMOUNT_INGL_CURR) != '' else '0.00'+" "+curr
                SixthValue = decimal_format.format(float(get_quote_details.TAX_AMOUNT_INGL_CURR))+" "+ curr if str(get_quote_details.TAX_AMOUNT_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
                SeventhLable = "Total Amount Including Tax/VAT"
                #SeventhValue = str("%.2f" % round(float(get_quote_details.TOTAL_AMOUNT_INGL_CURR),2))+curr if str(get_quote_details.TOTAL_AMOUNT_INGL_CURR) != '' else '0.00'+" "+curr
                SeventhValue = decimal_format.format(float(get_quote_details.TOTAL_AMOUNT_INGL_CURR))+" "+ curr if str(get_quote_details.TOTAL_AMOUNT_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
    elif TreeParam == 'Quote Items' and (subTabName == "Details" or subTabName == "Entitlements" or subTabName == "Object List" or subTabName == "Product List" or subTabName == "Billing Plan" or subTabName == "Assortment Module"):
        item_detail = Sql.GetFirst(" SELECT * FROM SAQRIT (NOLOCK) WHERE QUOTE_REVISION_CONTRACT_ITEM_ID ='"+str(CurrentRecordId)+"'")
        if item_detail:
            if subTabName == "Details" or subTabName == "Object List" or subTabName == "Product List" or subTabName == "Billing Plan" or subTabName == "Assortment Module":
                valid_from = str(item_detail.CONTRACT_VALID_FROM).split(" ")[0]                
                valid_date = str(item_detail.CONTRACT_VALID_TO).split(" ")[0]
                #if item_detail:
                PrimaryLable = "Product Offering Id"
                PrimaryValue =  item_detail.SERVICE_ID
                SecondLable = ""
                SecondValue = ""
                ThirdLable = "Contract Start Date"
                ThirdValue = valid_from
                FourthLable = "Contract End Date"
                FourthValue = valid_date
            elif subTabName == "Entitlements":
                PrimaryLable = "Product Offering ID"
                PrimaryValue = str(item_detail.SERVICE_ID)
                SecondLable = "Product Offering Description"
                SecondValue = str(item_detail.SERVICE_DESCRIPTION)
                ThirdLable = "Fab Location ID"
                ThirdValue = str(item_detail.FABLOCATION_ID)
                FourthLable = "Greenbook"
                FourthValue =  str(item_detail.GREENBOOK)
                FifthLable = "Equipment ID"
                FifthValue = str(item_detail.OBJECT_ID)        
    elif TreeParam == 'Cart Items':
        PrimaryLable = "Cart Items"
        PrimaryValue = "ALL"
        SecondLable = "Product Offering ID"
        SecondValue = "ALL"
        ThirdLable = ""
        ThirdValue = ""
    elif TreeParentParam == 'Quote Items' and (subTabName == 'Equipment' or subTabName == 'Quote Item Fab Value Drivers' or subTabName == 'Quote Item Cost and Value Drivers' or subTabName == "Customer Value Drivers" or subTabName == "Product Value Drivers"):
        TreeParam = TreeParam.split('-')
        PrimaryLable = "Line"
        PrimaryValue = TreeParam[0].strip()
        SecondLable = "Product Offering ID"
        SecondValue = TreeParam[1].strip()
        FifthLable = "Greenbooks"
        FifthValue = "All"
        SixthLable = "Equipment"
        SixthValue = "All"    
    elif TreeParentParam == "Add-On Products" and subTabName != "Equipment":
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION,ADNPRD_DESCRIPTION from SAQSAO(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"' and ADNPRD_ID = '"+str(TreeParam)+"'")
        PrimaryLable = "Parent Product Offering ID"
        PrimaryValue = str(TreeSuperParentParam)
        if getService is not None:
            SecondLable = "Parent Product Offering Description"
            SecondValue = getService.SERVICE_DESCRIPTION
        ThirdLable = "Add-On Product Offering ID"
        ThirdValue = str(TreeParam)
        if getService is not None:
            FourthLable = "Add-On Product Offering Description"
            FourthValue = getService.ADNPRD_DESCRIPTION
        try:
            FifthLable = ListKey[1]
            FifthValue = ListVal[1]
        except:
            FifthLable = ""
            FifthValue = ""
        SixthLable = ''
        SixthValue = ''
    elif TreeSuperParentParam == "Add-On Products":
        getService = Sql.GetFirst("select ADNPRD_DESCRIPTION from SAQSAO(nolock) where SERVICE_ID = '"+str(TopSuperParentParam)+"' and ADNPRD_ID = '"+str(TreeParentParam)+"'")
        PrimaryLable = "Add-On Product Offering ID"
        PrimaryValue = str(TreeParentParam)
        if getService is not None:
            SecondLable = "Add-On Product Offering Description"
            SecondValue = getService.ADNPRD_DESCRIPTION
        ThirdLable = "Fab Location ID"
        ThirdValue = str(TreeParam)
        FourthLable = "Greenbooks"
        FourthValue = "ALL"
        FifthLable = "Equipment"
        FifthValue = "All"
    elif TopSuperParentParam == "Add-On Products" and subTabName != "Equipment Details" and subTabName != "Assembly Details":
        getService = Sql.GetFirst("select ADNPRD_DESCRIPTION from SAQSAO(nolock) where SERVICE_ID = '"+str(TreeSuperTopParentParam)+"' and ADNPRD_ID = '"+str(TreeSuperParentParam)+"'")
        PrimaryLable = "Add-On Product Offering ID"
        PrimaryValue = str(TreeSuperParentParam)
        if getService is not None:
            SecondLable = "Add-On Product Offering Description"
            SecondValue = getService.ADNPRD_DESCRIPTION
        ThirdLable = "Fab Location ID"
        ThirdValue = str(TreeParentParam)
        FourthLable = "Greenbooks"
        FourthValue = str(TreeParam)
        FifthLable = "Equipment"
        FifthValue = "All"
    elif TreeParentParam == "Add-On Products" and subTabName == "Equipment":
        getService = Sql.GetFirst("select ADNPRD_DESCRIPTION from SAQSAO(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"' and ADNPRD_ID = '"+str(TreeParam)+"'")
        PrimaryLable = "Add-On Product Offering ID"
        PrimaryValue = str(TreeParam)
        if getService is not None:
            SecondLable = "Add-On Product Offering Description"
            SecondValue = getService.ADNPRD_DESCRIPTION
        ThirdLable = 'Equipment'
        ThirdValue = 'All'
        FourthLable = ''
        FourthValue = ''
        FifthLable = ''
        FifthValue = ''
        SixthLable = ''
        SixthValue = ''
    elif ObjName == "SAQSGB" and subTabName == "Details":
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '{service_id}'".format(service_id=TreeSuperParentParam if "Add" in TreeParam else TreeParentParam))
        try:
            PrimaryLable = "Product Offering ID"
            PrimaryValue = str(TreeSuperParentParam) if "Add" in TreeParam else str(TreeParentParam)
            SecondLable = "Product Offering Description"
            SecondValue = getService.SERVICE_DESCRIPTION
            ThirdLable = "Greenbook"
            ThirdValue = str(TreeParentParam) if "Add" in TreeParam else str(TreeParam)
            FourthLable = ''
            FourthValue = ''
            FifthLable = ''
            FifthValue = ''
            SixthLable = ''
            SixthValue = ''
        except:
            PrimaryLable = "Product Offering ID"
            PrimaryValue = str(TreeSuperParentParam)
            SecondLable = "Greenbook"
            SecondValue = str(TreeParentParam)
            ThirdLable = "Got Code"
            ThirdValue = str(TreeParam)
            FourthLable = ''
            FourthValue = ''
            FifthLable = ''
            FifthValue = ''
            SixthLable = ''
            SixthValue = ''
    elif ObjName == "SAQSGB" and (subTabName == "Entitlements" or subTabName == "Got Code") and TreeTopSuperParentParam == "Product Offerings":
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeParentParam)
        SecondLable = "Product Offering Description"
        SecondValue = getService.SERVICE_DESCRIPTION
        ThirdLable = "Greenbook"
        ThirdValue = str(TreeParam)
        FourthLable = "Equipment"
        FourthValue = "ALL"
        FifthLable = ""
        FifthValue = ""
        SixthLable = ''
        SixthValue = ''
    elif (ObjName == "SAQRGG" or ObjName == "SAQSKP")and (subTabName == "Events" or subTabName == 'Kit Details' or subTabName == "BoM"):
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeSuperParentParam)
        SecondLable = "Greenbook"
        SecondValue = str(TreeParentParam)
        ThirdLable = "Got Code"
        ThirdValue = str(TreeParam)
    elif ObjName == "SAQGPM" or ObjName == "SAQGPA":
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TopSuperParentParam)
        SecondLable = "Greenbook"
        SecondValue = str(TreeSuperParentParam)
        ThirdLable = "Got Code"
        ThirdValue = str(TreeParentParam)
        FourthLable = "PM ID"
        FourthValue = str(TreeParam)
    elif ObjName == "SAQSGB" and TreeTopSuperParentParam == "Product Offerings" and (subTabName in("Equipment Details","Equipment Entitlements","Equipment Assemblies")):
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeParentParam)
        SecondLable = "Product Offering Description"
        SecondValue = getService.SERVICE_DESCRIPTION
        ThirdLable = "Greenbook"
        ThirdValue = str(TreeParam)
        FourthLable = "Equipment ID"
        FourthValue = str(EquipmentId)
        FifthLable = "Serial Number"
        FifthValue = str(SerialNumber)
        SixthLable = ''
        SixthValue = ''
    elif ObjName in ("SAQSGB") and TreeTopSuperParentParam == "Product Offerings" and (subTabName in("Events")):
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeParentParam)
        SecondLable = "Product Offering Description"
        SecondValue = getService.SERVICE_DESCRIPTION
        ThirdLable = "Greenbook"
        ThirdValue = str(TreeParam)
        FourthLable = "Assembly ID"
        FourthValue = str(AssemblyId)
    elif ObjName in ("SAQSGB","SAQSCA") and TreeTopSuperParentParam == "Product Offerings" and (subTabName in("Assembly Details","Assembly Entitlements","Kit Details","BoM")):
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeParentParam)
        SecondLable = "Product Offering Description"
        SecondValue = getService.SERVICE_DESCRIPTION
        ThirdLable = "Greenbook"
        ThirdValue = str(TreeParam)
        FourthLable = "Equipment ID"
        FourthValue = str(EquipmentId)
        FifthLable = "Serial Number"
        FifthValue = str(SerialNumber)
        SixthLable = "Assembly ID"
        SixthValue = str(AssemblyId)
    elif ObjName == "SAQSCO" and subTabName in ("Equipment","Equipment Details") and TreeTopSuperParentParam == "Product Offerings":
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        if subTabName == "Equipment Details":
            PrimaryLable = "Product Offering ID"
            PrimaryValue = str(TreeParentParam)
            SecondLable = "Product Offering Description"
            SecondValue = getService.SERVICE_DESCRIPTION
            ThirdLable = "Greenbook"
            ThirdValue = str(TreeParam)
            FourthLable = "Equipment"
            FourthValue = str(EquipmentId)
            FifthLable = "Serial No"
            FifthValue = str(SerialNumber)
            SixthLable = ''
            SixthValue = ''
        else:
            PrimaryLable = "Product Offering ID"
            PrimaryValue = str(TreeParentParam)
            SecondLable = "Product Offering Description"
            SecondValue = getService.SERVICE_DESCRIPTION
            ThirdLable = "Greenbook"
            ThirdValue = str(TreeParam)
            FourthLable = "Equipment"
            FourthValue = "ALL"
            FifthLable = ""
            FifthValue = ""
            SixthLable = ''
            SixthValue = ''
    if str(Image) != "":
        sec_rel_sub_bnr += (
            '<div class="product_tab_icon"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="'
            + str(Image)
            + '"/></div>'
        )
    if str(PrimaryLable) != "":
        sec_rel_sub_bnr += (
            '<div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="'
            + str(PrimaryLable)
            + '">'
            + str(PrimaryLable)
            + '</abbr></div><div class="product_txt_to_top_child"><abbr title="'
            + str(PrimaryValue)
            + '">'
            + str(PrimaryValue)
            + "</abbr></div></div>"
        )
    if str(SecondLable) != "":
        sec_rel_sub_bnr += (
            '<div class="segment_part_number_child secondary_highlight subellipsisdot" style="display: block;"><div class="segment_part_number_heading_child"><abbr title="'
            + str(SecondLable)
            + '">'
            + str(SecondLable)
            + '</abbr></div><div class="segment_part_number_text_child"><abbr title="'
            + str(SecondValue)
            + '">'
            + str(SecondValue)
            + "</abbr></div></div>"
        )
    if str(ThirdLable) != "":
        if str(TabName) == "CM Class":
            if str(ThirdValue).upper() == "TRUE":
                ThirdValueDiv = (
                    '<input type="checkbox" value = "True" class="custom" checked disabled><span class="lbl"></span>'
                )
            elif str(ThirdValue).upper() == "FALSE":
                ThirdValueDiv = '<input type="checkbox" value = "False" class="custom" disabled><span class="lbl"></span>'
            else:
                ThirdValueDiv = ThirdValue
            sec_rel_sub_bnr += (
                '<div class="segment_part_description_child secondary_highlight" style="display: block;"><div class="segment_part_heading_child"><abbr title="'
                + str(ThirdLable)
                + '">'
                + str(ThirdLable)
                + "</abbr></div><div class='segment_part_text_child'><abbr title='"
                + str(ThirdValue)
                + "'>"
                + str(ThirdValueDiv)
                + "</abbr></div></div>"
            )
        else:
            sec_rel_sub_bnr += (
                '<div class="segment_part_description_child secondary_highlight" style="display: block;"><div class="segment_part_heading_child"><abbr title="'
                + str(ThirdLable)
                + '">'
                + str(ThirdLable)
                + "</abbr></div><div class='segment_part_text_child'><abbr title='"
                #+ str(ThirdValue)
                + "'>"
                + str(ThirdValue)
                + "</abbr></div></div>"
            )
    if str(FourthLable) != "" and (ObjName != "SAQTMT") and str(TreeParam) != "Quote Preview":
        sec_rel_sub_bnr += (
                '<div class="segment_part_description_child secondary_highlight" style="display: block;"><div class="segment_part_heading_child"><abbr title="'
                + str(FourthLable)
                + '">'
                + str(FourthLable)
                + "</abbr></div><div class='segment_part_text_child'><abbr title='"
                + str(FourthValue)
                + "'>"
                + str(FourthValue)
                + "</abbr></div></div>"
            )
    if str(FifthLable) != "" and str(TreeParam) != "Quote Preview":
        sec_rel_sub_bnr += (
                '<div class="segment_part_description_child secondary_highlight" style="display: block;"><div class="segment_part_heading_child"><abbr title="'
                + str(FifthLable)
                + '">'
                + str(FifthLable)
                + "</abbr></div><div class='segment_part_text_child'><abbr title='"
                + str(FifthValue)
                + "'>"
                + str(FifthValue)
                + "</abbr></div></div>"
            )
    if str(SixthLable) != "" and (str(TreeParam) != "Quote Information" and str(TreeParam) != "Quote Preview"):
        sec_rel_sub_bnr += (
                '<div class="segment_part_description_child secondary_highlight" style="display: block;"><div class="segment_part_heading_child"><abbr title="'
                + str(SixthLable)
                + '">'
                + str(SixthLable)
                + "</abbr></div><div class='segment_part_text_child'><abbr title='"
                + str(SixthValue)
                + "'>"
                + str(SixthValue)
                + "</abbr></div></div>"
            )
    if str(SeventhLable) != "" and (str(TreeParam) != "Quote Information" and str(TreeParam) != "Quote Preview" and str(TreeSuperParentParam) != "Product Offerings"):
        sec_rel_sub_bnr += (
                '<div class="segment_part_description_child secondary_highlight" style="display: block;"><div class="segment_part_heading_child"><abbr title="'
                + str(SeventhLable)
                + '">'
                + str(SeventhLable)
                + "</abbr></div><div class='segment_part_text_child'><abbr title='"
                + str(SeventhValue)
                + "'>"
                + str(SeventhValue)
                + "</abbr></div></div>"
            )
    if str(SeventhLable) != "" and str(TreeSuperParentParam) == "Product Offerings":
        sec_rel_sub_bnr += (
                '<div class="segment_part_description_child secondary_highlight" style="display: block;"><div class="quote_type_heading"><abbr title="'
                + str(SeventhLable)
                + '">'
                + str(SeventhLable)
                + "</abbr></div><div class='quote_type_value'><abbr title='"
                + str(SeventhValue)
                + "'>"
                + str(SeventhValue)
                + "</abbr></div></div>"
            )
    if str(EightLable) != "" and str(EightValue) != "" and (str(TreeParam) != "Quote Information" and str(TreeParam) != "Quote Preview"):
        sec_rel_sub_bnr += (
                '<div class="segment_part_description_child secondary_highlight" style="display: block;"><div class="segment_part_heading_child"><abbr title="'
                + str(EightLable)
                + '">'
                + str(EightLable)
                + "</abbr></div><div class='segment_part_text_child'><abbr title='"
                + str(EightValue)
                + "'>"
                + str(EightValue)
                + "</abbr></div></div>"
            )
    if CurrentRecordId.startswith("SYOBJR", 0) == True:
        currecId = Sql.GetFirst(
            "select a.SAPCPQ_ATTRIBUTE_NAME,a.NAME,a.CAN_ADD,a.CAN_EDIT,a.CAN_DELETE,a.RELATED_LIST_SINGULAR_NAME,(b.SAPCPQ_ATTRIBUTE_NAME) as OBJ_REC_ID,(b.RECORD_ID) as SYOBJH_RECORD_ID from SYOBJR (nolock) a inner join SYOBJH (nolock) b on a.OBJ_REC_ID = b.RECORD_ID where a.SAPCPQ_ATTRIBUTE_NAME = '"
            + str(CurrentRecordId)
            + "' "
        )
        if currecId:
            buttonid = str(currecId.SAPCPQ_ATTRIBUTE_NAME) + "_" + str(currecId.OBJ_REC_ID)
            buttonid = str(buttonid).replace("-", "_")
            SYOBJH_RECORD_ID = str(currecId.SYOBJH_RECORD_ID).replace("-", "_")
            divid = str(currecId.NAME).replace(" ", "_")
            if str(currecId.CAN_ADD).upper() == "TRUE":
                if CurrentRecordId == "SYOBJR-95800":
                    sec_rel_sub_bnr += (add_button)                    
                elif CurrentRecordId == "SYOBJR-95825":
                    for btn in multi_buttons:
                        sec_rel_sub_bnr += (btn)
                elif TreeParam == "Billing" and ObjName == "SAQRIB":
                    for btn in multi_buttons:
                        sec_rel_sub_bnr += (btn)
                elif CurrentRecordId == "SYOBJR-98789" and TreeParentParam != "Fab Locations":                    
                    FabList = Sql.GetList(
                        "SELECT FAB_LOCATION_RECORD_ID FROM MAFBLC (NOLOCK) JOIN SAQTMT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND FAB_LOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' )".format(
                            contract_quote_record_id,contract_quote_record_id,quote_revision_record_id
                        )
                    )
                    if TreeParam == "Fab Locations" and subTabName == "Equipment":                        
                        sec_rel_sub_bnr += ""
                    elif FabList is not None and len(FabList) >0:                      
                        send_and_receive = Sql.GetList("SELECT CPQ_PARTNER_FUNCTION FROM SAQTIP (NOLOCK) WHERE CPQ_PARTNER_FUNCTION IN ('SENDING ACCOUNT','RECEIVING ACCOUNT') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(str(contract_quote_record_id),quote_revision_record_id))
                        sale_type = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))                       
                        for btn in multi_buttons:
                            if "ADD FAB" in btn:
                                if quote_status.QUOTE_STATUS != 'APR-APPROVED':
                                    sec_rel_sub_bnr += (str(btn))
                        else:
                            sec_rel_sub_bnr += ""
                    elif TreeParam == "Fab Locations":                        
                        send_and_receive = Sql.GetList("SELECT CPQ_PARTNER_FUNCTION FROM SAQTIP (NOLOCK) WHERE CPQ_PARTNER_FUNCTION IN ('SENDING ACCOUNT','RECEIVING ACCOUNT') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(str(contract_quote_record_id),quote_revision_record_id))
                        sale_type = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))                        
                        for btn in multi_buttons:
                            if "ADD FAB" in btn:
                                sec_rel_sub_bnr += (str(btn))
                    else:
                        if CurrentRecordId == "SYOBJR-98789" and TreeParam == "Fab Locations":                            
                            if quote_status.QUOTE_STATUS != 'APPROVED':                                
                                sec_rel_sub_bnr += (str(add_button))
                        else:
                            sec_rel_sub_bnr += (str(add_button))                        
                elif CurrentRecordId == "SYOBJR-98788":
                    if quote_status.QUOTE_STATUS != 'APR-APPROVED':                        
                        if "ADD OFFERINGS" in str(add_button):
                            if str(TreeParam) == "Product Offerings":
                                sec_rel_sub_bnr += ""
                        else:
                            sec_rel_sub_bnr += (str(add_button))
                elif CurrentRecordId =="SYOBJR-00005":
                    if quote_status.QUOTE_STATUS !='APPROVED':                        
                        if str(TreeParam) == "Z0110" or str(Treeparam) == "Z0108":
                            sec_rel_sub_bnr += ( '<button id="PRICE__' + str(buttonid) + '" onclick="Pricing(this,' ')" class="btnconfig" data-target="" data-toggle="modal">PRICING</button>')
                elif CurrentRecordId == "SYOBJR-98800" and TreeParam != "Fab Locations":                    
                    sale_type = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                    if sale_type == 'TOOL RELOCATION':
                        sec_rel_sub_bnr += ''
                    else:
                        if quote_status.QUOTE_STATUS != 'APPROVED':
                            sec_rel_sub_bnr += (str(add_button))
                elif CurrentRecordId == "SYOBJR-00010" and TreeParam != "Fab Locations" and subTabName != "Items":                    
                    sec_rel_sub_bnr += (str(add_button))
                else:
                    if TreeParam == "Fab Locations":
                        GetToolReloc = Sql.GetList("SELECT CpqTableEntryId FROM SAQTIP WHERE (CPQ_PARTNER_FUNCTION = 'RECEIVING ACCOUNT' OR CPQ_PARTNER_FUNCTION = 'SENDING ACCOUNT') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                        if len(GetToolReloc) == 0:
                            for btn in multi_buttons:
                                if "ADD FAB" in str(btn):
                                    if quote_status.QUOTE_STATUS != 'APPROVED':
                                        sec_rel_sub_bnr += (str(btn))
                    if subTabName == 'Fab Locations':
                        if TreeParam.startswith("Sending"):
                            for btn in multi_buttons:
                                if "ADD SENDING FAB" in str(btn):
                                    if quote_status.QUOTE_STATUS != 'APPROVED':
                                        sec_rel_sub_bnr += (str(btn))
                        elif TreeParam.startswith("Receiving"):
                            for btn in multi_buttons:
                                if "ADD RECEIVING FAB" in str(btn):
                                    if quote_status.QUOTE_STATUS != 'APPROVED':
                                        sec_rel_sub_bnr += (str(btn))
                    elif TreeParam == "Fab Locations" and subTabName == "Equipment":
                        sec_rel_sub_bnr += ""
                    elif TreeParam == "Sales Team":                        
                        contract_manager_info = Sql.GetFirst("SELECT * from SAQDLT where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND C4C_PARTNERFUNCTION_ID = 'CONTRACT MANAGER' ".format(contract_quote_record_id,quote_revision_record_id))
                        if contract_manager_info:
                            sec_rel_sub_bnr += ""
                        else:
                            sec_rel_sub_bnr += (str(add_button))
                    else:
                        if str(TabName) == 'Quotes':
                            if quote_status.QUOTE_STATUS != 'APPROVED' and subTabName != 'Items':
                                sec_rel_sub_bnr += (str(add_button))
                        else:
                            sec_rel_sub_bnr += (str(add_button))
            if (str(TabName) == "Quotes" or str(TabName == "Quote")):
                getQuotetype = ""
                getsaletypeloc = Sql.GetFirst("select SALE_TYPE,QUOTE_TYPE from SAQTMT (NOLOCk) where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                if getsaletypeloc:
                    if TreeParam == "Add-On Products" and "INCLUDE ADD-ON PRODUCTS" not in str(add_button) and ("ADD CREDITS" not in sec_rel_sub_bnr):
                        Trace.Write("multi_buttons--2754-J"+str(add_button))  
                        sec_rel_sub_bnr += str(add_button)
                    if len(multi_buttons)>0:                        
                        if TreeParam.startswith("Sending Account"):
                            for btn in multi_buttons:
                                if getsaletypeloc.SALE_TYPE == "TOOL RELOCATION":
                                    if "ADD FROM LIST" in btn:
                                        sec_rel_sub_bnr += ""
                                else:
                                    if "ADD UNMAPPED EQUIPMENTS" in btn:
                                        sec_rel_sub_bnr += str(btn)
                        elif TreeParam == "Delivery Schedule":
                            for btn in multi_buttons:
                                sec_rel_sub_bnr += (btn)
        elif TreeParam == "Billing":
            for btn in multi_buttons:
                sec_rel_sub_bnr += (btn)
        elif TreeParam == "Delivery Schedule":            
            for btn in multi_buttons:
                sec_rel_sub_bnr += (btn)
    elif TreeParam == 'Approvals' and (TabName == "Quotes" or TabName == "Quote"):
        quote_status = Sql.GetFirst("SELECT REVISION_STATUS,QUOTE_ID FROM SAQTRV (NOLOCk) WHERE QUOTE_REVISION_RECORD_ID = '{}'".format(quote_revision_record_id))
        Quote_Owner = Sql.GetFirst("SELECT CPQTABLEENTRYADDEDBY FROM SAQTMT (NOLOCk) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
        User_Name = User.UserName
        Submit_approval = ''
        if Quote_Owner.CPQTABLEENTRYADDEDBY == User_Name:
            Submit_approval = "True"
        else:
            Submit_approval = "False"
        get_quote_status = Sql.GetList("SELECT CpqTableEntryId FROM ACAPTX (NOLOCK) WHERE APPROVAL_ID LIKE '%{}%'".format(quote_status.QUOTE_ID))
        if not get_quote_status and str(quote_status.REVISION_STATUS) != 'APR-APPROVED':
            sec_rel_sub_bnr += (
                    '<button class="btnconfig cust_def_btn" id="APPROVE" onclick="quote_approval(this.id)">APPROVE</button>'
                )
        if get_quote_status and (str(quote_status.REVISION_STATUS) == 'CFG-CONFIGURATION' or str(quote_status.REVISION_STATUS) == 'NEW REVISION' or str(quote_status.REVISION_STATUS) == 'APR-RECALLED'  or str(quote_status.REVISION_STATUS) == 'CFG-ACQUIRING' or (quote_status.REVISION_STATUS) == 'PRI-PRICING') and Submit_approval == "True":
            Trace.Write("submit for approval")
            GetSelfAppr = Sql.GetFirst("SELECT CpqTableEntryId FROM ACAPTX (NOLOCK) WHERE APRTRXOBJ_ID = '{}' AND APRCHN_ID = 'SELFAPPR'".format(quote_status.QUOTE_ID))
            if GetSelfAppr is not None:
                sec_rel_sub_bnr += ""
            else:
                sec_rel_sub_bnr += (
                    '<button class="btnconfig cust_def_btn submitbutton" data-target="#SUBMIT_MODAL_SECTION" data-toggle="modal" id="submit_for_approval" onclick="submit_comment()">SUBMIT FOR APPROVAL</button>'
                    )
    elif TreeParam == "Quote Documents":
        sec_rel_sub_bnr += (add_button)        
    if subTabName == 'Summary' and TreeParam == "Quote Items" and (str(TabName) == "Quotes" or str(TabName) == "Quote") and current_prod == "Sales":
        getQuotetype = ""       
        getsaletypeloc = Sql.GetFirst("select SALE_TYPE,QUOTE_TYPE from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
        if getsaletypeloc:
            buttonvisibility = ''
            if len(multi_buttons)>0:
                if TreeParam == "Quote Items":
                    # Appending Price button in Quote Items Node                    
                    for btn in multi_buttons:
                        fts_scenario_check = Sql.GetList("SELECT CpqTableEntryId FROM SAQTIP (NOLOCK) WHERE CPQ_PARTNER_FUNCTION IN ('SENDING ACCOUNT','RECEIVING ACCOUNT') AND QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
                        #A055S000P01-7512 Start Enable/Disable the PRICE button in Quote items based on Required fields validation
                        if str(TreeParam) == "Quote Items":
                            getsalesorg_ifo = Sql.GetFirst("SELECT SALESORG_ID from SAQTRV (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                            getfab_info = Sql.GetFirst("SELECT FABLOCATION_NAME from SAQSFB (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                            get_service_ifo = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as SERVICE_ID from SAQTSV (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                            get_equip_details = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as SERVICE_ID from SAQSCO (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                            if getsalesorg_ifo and getfab_info:
                                if get_service_ifo.SERVICE_ID == get_equip_details.SERVICE_ID:                                    
                                    buttonvisibility = "Hide_button"
                                else:
                                    buttonvisibility = "Hide_button"
                            else:
                                buttonvisibility = "Hide_button"
                        else:
                            buttonvisibility = "Hide_button"
                        #A055S000P01-7512 end Enable/Disable the PRICE button in Quote items based on Required fields validation
                        if len(fts_scenario_check) == 2:
                            Trace.Write("hide PRICING for fts--2411--")                       
                        else:
                            if quote_status.QUOTE_STATUS != 'APPROVED':
                                sec_rel_sub_bnr += (btn)
                if TreeParam == "Quote Items":
                    # Appending REFRESH button in Quote Items Node
                    for btn in multi_buttons:
                        if "REFRESH" in btn:
                            if quote_status.QUOTE_STATUS != 'APPROVED':
                                sec_rel_sub_bnr += (btn)
    if subTabName == 'Involved Parties' and TreeParam == "Quote Information":
        sec_rel_sub_bnr += (add_button)
    if TreeParam == "Billing" and subTabName =="Details" and ObjName == "SAQRIB":    
        if quote_status.QUOTE_STATUS != 'APPROVED':
            sec_rel_sub_bnr += (add_button)
    if subTabName == 'Add On Products' and TreeParentParam == "Comprehensive Services":
        sec_rel_sub_bnr += (
                '<button class="btnconfig cust_def_btn" data-target="" data-toggle="modal" id="activate_btn" onclick="addon_products()">ACTIVATE</button>'
                )
    elif str(TabName) == "Approval Chain" and str(TreeParentParam) == "Approval Chain Steps":
        if str(ObjName) == "ACACST" and  subTabName == "Chain Step Conditions":
            style = 'style="display: block;"'
        else:
            style = 'style="display: none;"'
        sec_rel_sub_bnr += (
            """<div class="segmentButtons" style=""><button """+str(style)+""" class="btnconfig QBeditbtn" """
            + """ onclick="QBeditbtn()">EDIT CRITERIA</button><button class="
        btnconfig QBsavebtn" style="display:none;" onclick="QBsavebtn()">SAVE</button>
        <button class=" btnconfig QBcanclbtn" onclick="QBcanclbtn()" style="display:none;">CANCEL</button>
        </div>"""
        )
    elif (str(TabName) == "My Approvals Queue" or str(TabName) == "Team Approvals Queue") and (
        str(TreeParentParam) == "Approval History"
    ):
        ApprovalQueuePrimaryKey = Product.Attr("QSTN_SYSEFL_AC_00210").GetValue()
        Status = Product.Attr("QSTN_SYSEFL_AC_00214").GetValue()        
        ACAPTXStatus = Sql.GetFirst(
            "SELECT * FROM ACAPTX WHERE ACAPTX.APPROVAL_RECIPIENT_RECORD_ID  = '"
            + str(user_id)
            + "' AND APPROVAL_TRANSACTION_RECORD_ID = '"
            + str(CurrentRecordId)
            + "' AND APPROVALSTATUS = 'REQUESTED' AND ARCHIVED = 0 "
        )
        if ACAPTXStatus:
            sec_rel_sub_bnr += """<button id="approve" onclick="approve_request()" data-target="#preview_approval" data-toggle="modal"
            class="btnconfig SegmentRevBtn fltrt">APPROVE</button> <button id="reject"
            data-target="#preview_approval" onclick="reject_request()" data-toggle="modal" class="btnconfig SegmentRevBtn fltrt">REJECT
            </button> </div>"""
    else:
        if TabName == "Quotes" or TabName == "Quote":           
            Quote_Owner = Sql.GetFirst("SELECT CPQTABLEENTRYADDEDBY FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+  "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
            User_Name = User.UserName
            recall_edit = ''
            if Quote_Owner:
                if Quote_Owner.CPQTABLEENTRYADDEDBY == User_Name:
                    recall_edit = "True"
                else:
                    recall_edit = "False"
            else:
                recall_edit = "False"
        if str(TreeParam).upper() == "QUOTE INFORMATION" and subTabName == "Involved Parties" and TabName == "Quotes":
            sec_rel_sub_bnr += (
                        '<button id="ADDNEW__SYOBJR_98798_7F4F4C8D_73C7_4779_9BE5_38C695" onclick="cont_openaddnew(this, \'div_CTR_Involved_Parties\')" class="btnconfig addNewRel HideAddNew">ADD NEW</button>'
                    )
        elif (str(TreeParentParam).upper() == "FAB LOCATIONS" or str(TreeParam).upper() == "QUOTE INFORMATION" or str(TreeSuperParentParam).upper() == "FAB LOCATIONS" )  and TabName == "Quotes":
            sec_rel_sub_bnr += ('<button id="fablocate_save" onclick="fablocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fablocate_cancel" onclick="fablocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>'  )
        elif str(TreeParam) == "Quote Information" and TabName == "Quotes":
            sec_rel_sub_bnr += ('<button id="fabcostlocate_save" onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fabcostlocate_cancel" onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>')
        elif (str(TreeSuperParentParam).upper() == "PRODUCT OFFERINGS") and TabName == "Quotes" and str(subTabName)!="Exclusions" and str(subTabName)!="New Parts" and str(subTabName)!="Inclusions" and str(subTabName)!= "New Parts Only":
            sec_rel_sub_bnr += ('<button id="fabcostlocate_save" onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig hidebtn">SAVE</button><button id="fabcostlocate_cancel" onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig hidebtn">CANCEL</button>'  )
            if str(subTabName)=="Events" and revision_status.REVISION_STATUS != 'APR-APPROVED':
                sec_rel_sub_bnr += str(add_button)
            elif str(subTabName) == "Spare Parts" and str(TreeParentParam)=="Complementary Products":
                acquiring_status= Sql.GetFirst("""select count(PRICING_STATUS) as cnt from SAQSPT(NOLOCK) WHERE PRICING_STATUS ='ACQUIRING' AND QUOTE_RECORD_ID = '{ContractRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(ContractRecordId =contract_quote_record_id,quote_revision_record_id =quote_revision_record_id))
                acquired_status= Sql.GetFirst("""select count(PRICING_STATUS) as cnt from SAQSPT(NOLOCK) WHERE PRICING_STATUS ='ACQUIRED' AND QUOTE_RECORD_ID = '{ContractRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(ContractRecordId =contract_quote_record_id,quote_revision_record_id =quote_revision_record_id))
                error_status = Sql.GetFirst("""select count(PRICING_STATUS) as cnt from SAQSPT(NOLOCK) WHERE PRICING_STATUS ='ERROR' AND QUOTE_RECORD_ID = '{ContractRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(ContractRecordId =contract_quote_record_id,quote_revision_record_id =quote_revision_record_id))
                not_priced= Sql.GetFirst("""select count(PRICING_STATUS) as cnt from SAQSPT(NOLOCK) WHERE PRICING_STATUS ='NOT PRICED' AND QUOTE_RECORD_ID = '{ContractRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' """.format(ContractRecordId =contract_quote_record_id,quote_revision_record_id =quote_revision_record_id))
                if revision_status.REVISION_STATUS == 'CFG-CONFIGURING':
                    if str(multi_buttons) != "":
                        for btn in multi_buttons:
                            if acquiring_status.cnt==0:
                                    if ('REFRESH'in str(btn) or 'PRICE'in str(btn)or 'EXPORT' in str(btn)):
                                        sec_rel_sub_bnr += str(btn)
                                    else:
                                        dropdown_multi_btn_str += '<li>'+str(btn)+'</li>'
                            elif 'REFRESH' in btn:
                                    sec_rel_sub_bnr += str(btn)
                        dropdown_multi_btn_str += '''</ul></div></div>'''
                        if acquiring_status.cnt==0 :
                            sec_rel_sub_bnr =dropdown_multi_btn_str + sec_rel_sub_bnr
                    else:
                        sec_rel_sub_bnr += str(add_button)
                else:
                    sec_rel_sub_bnr += ('<button id="export-spare-parts-data-as-excel" onclick="exportSparePartsDataAsExcel(this)" class="btnconfig">EXPORT</button>')
            elif str(subTabName)=="Periods":
                sec_rel_sub_bnr += str(add_button)
        elif (str(TreeSuperParentParam).upper() == "COMPREHENSIVE SERVICES")  and TabName == "Quotes" and str(subTabName)!="Exclusions" and str(subTabName)!="New Parts" and str(subTabName)!="Inclusions":
            sec_rel_sub_bnr += ('<button id="fabcostlocate_save" onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fabcostlocate_cancel" onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>'  )
            if str(subTabName)=="Events" and revision_status.REVISION_STATUS != 'APR-APPROVED':
                sec_rel_sub_bnr += str(add_button)
        elif  (str(TreeTopSuperParentParam).upper() == "COMPREHENSIVE SERVICES")  and TabName == "Quotes" and (subTabName)!="Exclusions" and str(subTabName)!="New Parts" and str(subTabName)!="Inclusions":
            if str(subTabName)=="Events" and str(TreeSuperParentParam)!="Z0009":
                sec_rel_sub_bnr += ('<button id="ADDNEW__SYOBJR_00011_SYOBJ_00974" onclick="PM_FrequencyInlineEdit()" class="btnconfig" >INLINE EDIT</button>')
            elif 'Add-On Products' in str(TreeParam) and ("INCLUDE ADD-ON PRODUCTS" not in sec_rel_sub_bnr) and ("ADD CREDITS" not in sec_rel_sub_bnr):
                if "ADD FROM LIST" in add_button:
                    sec_rel_sub_bnr+= ""
                else:
                    if str(multi_buttons) != "" and (subTabName == "NSO Catalog" or subTabName == "Credits"):

                        for btn in multi_buttons:
                            Trace.Write("multibttns=="+str(multi_buttons))
                            service_query= Sql.GetFirst("""select count(*) as cnt from SAQSCO(NOLOCK) WHERE QUOTE_RECORD_ID = '{ContractRecordId}'AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = 'Z0123'AND PAR_SERVICE_ID ='{TreeSuperParentParam}' """.format(ContractRecordId =contract_quote_record_id,quote_revision_record_id =quote_revision_record_id,TreeSuperParentParam=TreeSuperParentParam))


                            Trace.Write("servicequery=="+str(service_query.cnt))

                            if service_query.cnt > 0:
                                sec_rel_sub_bnr+= str(btn)
                                Trace.Write("sec_rel_sub_bnr=="+str(sec_rel_sub_bnr))
                            else:   
                                sec_rel_sub_bnr+= ''
                    else:
                        sec_rel_sub_bnr+= str(add_button)
            else:
                if str(subTabName)!="Exclusions" and str(subTabName)!="New Parts" and str(subTabName)!="Inclusions":
                    sec_rel_sub_bnr += ('<button id="fabcostlocate_save" onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fabcostlocate_cancel" onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>'  )        
        elif str(TreeParam) == "Fab Locations" and TabName =="Quotes" and subTabName =="Fab Locations":
            sec_rel_sub_bnr += ""
        elif subTabName =="Delivery Schedule":            
            sec_rel_sub_bnr += ('<button id="delivery_save" onclick="showSdeliverysave(this)" style= "display: none;" class="btnconfig" >SAVE</button><button id="delivery_cancel" onclick="showSdeliverycancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>')
        else:            
            import re
            if len(multi_buttons)>0: ##adding dynamic buttons from SYPGAC if we have more than one button
                for btn in multi_buttons:
                    if ('SPLIT' in btn or 'EDIT' in btn) and subTabName =='Items':
                        if 'SPLIT' in btn:
                            get_entitlement_xml =Sql.GetList("""select ENTITLEMENT_XML,SERVICE_ID from SAQTSE(NOLOCK) WHERE QUOTE_RECORD_ID = '{ContractRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(ContractRecordId =contract_quote_record_id,quote_revision_record_id =quote_revision_record_id))
                            if get_entitlement_xml:
                                split_flag = 0
                                for get_service in get_entitlement_xml:
                                    entitlement_service = get_service.ENTITLEMENT_XML
                                    quote_item_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                                    split_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_PQB_SPLQTE</ENTITLEMENT_ID>')
                                    split_value = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>Yes</ENTITLEMENT_DISPLAY_VALUE>')
                                    for m in re.finditer(quote_item_tag, entitlement_service):
                                        sub_string = m.group(1)
                                        split_1 =re.findall(split_pattern,sub_string)
                                        split_2 = re.findall(split_value,sub_string)
                                        if split_1 and split_2 and split_flag == 0:
                                            Trace.Write("a"+str(get_service.SERVICE_ID))
                                            sec_rel_sub_bnr += (btn)
                                            split_flag = 1
                                            break
                        if 'EDIT' in btn:
                            billing_variable_visible = Sql.GetFirst("""SELECT BILLING_TYPE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{ContractRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND BILLING_TYPE in ('VARIABLE','Variable')""".format(ContractRecordId =contract_quote_record_id,quote_revision_record_id =quote_revision_record_id))
                            if billing_variable_visible:
                                sec_rel_sub_bnr += (btn)                    
                    if quote_status.QUOTE_STATUS != 'APPROVED' and 'SPLIT' not in btn and 'EDIT' not in btn and 'CREDIT' not in btn:                        
                        sec_rel_sub_bnr += (btn)
                    if (subTabName == 'Inclusions'  or subTabName == 'Exclusions' or subTabName == 'New Parts')  and quote_status.QUOTE_STATUS != 'APPROVED' and 'INLINE EDIT' in btn:
                        sec_rel_sub_bnr += (btn)                        
            elif str(add_button)!='' and str(add_button) not in sec_rel_sub_bnr :
                if subTabName == 'Exclusions' and TreeSuperParentParam == 'Product Offerings':
                    sec_rel_sub_bnr += ""
                else:
                    ##adding dynamic buttons from SYPGAC if we have only one button
                    if TreeParam == 'Product Offerings':
                        sec_rel_sub_bnr+= ""
                    else:
                        sec_rel_sub_bnr += str(add_button)
        Trace.Write('sec_rel_sub_bnr--2941--'+str(sec_rel_sub_bnr))
        sec_rel_sub_bnr += "<div id = 'multibtn_drpdwn'></div>"

    get_bill_message_warning = ''
    #messgae notification started 2050
    bill_plan_years = Sql.GetList("SELECT DISTINCT BILLING_YEAR,SERVICE_ID from SAQIBP WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
    billing_message= []
    if bill_plan_years:
        for val in bill_plan_years:
            bill_year= val.BILLING_YEAR
            service_id= val.SERVICE_ID
            bill_years_gl_curr= bill_year.replace(' ','_')+'_INGL_CURR'
            item_bill_type = Sql.GetFirst("SELECT BILLING_TYPE,SUM("+bill_years_gl_curr+") as year_gc from SAQRIT where QUOTE_RECORD_ID= '"+str(contract_quote_record_id)+"' and QTEREV_RECORD_ID ='"+str(quote_revision_record_id)+"' and SERVICE_ID='"+str(service_id)+"' group by BILLING_TYPE")
            if item_bill_type:
                item_billing_type = item_bill_type.BILLING_TYPE
                if str(item_billing_type).upper() in ('FIXED','MILESTONE'):
                    get_bill_val ='SUM(BILLING_VALUE_INGL_CURR)'
                    get_dt_amt = 'BILLING_VALUE_INGL_CURR'
                
                else:
                    get_bill_val = 'SUM(ESTVAL_INGL_CURR)'
                    get_dt_amt = 'ESTVAL_INGL_CURR'
                get_year_amt = item_bill_type.year_gc
                
                get_total_bill_amt = Sql.GetFirst("SELECT  "+get_bill_val+" as total_monthly_billval from SAQIBP where QUOTE_RECORD_ID= '"+str(contract_quote_record_id)+"' and BILLING_YEAR= '"+str(bill_year)+"' and SERVICE_ID= '"+str(service_id)+"'  and QTEREV_RECORD_ID ='"+str(quote_revision_record_id)+"' ")
                if get_year_amt == get_total_bill_amt.total_monthly_billval:
                    billing_message.append('F')
                else:
                    billing_message.append('T')
            if  'T' in  billing_message  and not get_bill_message_warning:
                
                get_bill_message_warning += 'This Quote has the following notifications:'
                get_bill_message_warning += ('<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Warning"> 99999 | INCORRECT BILLING ITEMS | Billing Item price does not equal Annual Billing Amount.</label></div></div>')
            else:
                get_bill_message_warning = ''
    else:
        get_bill_message_warning = ''
    Trace.Write('get_bill_message_warning-->'+str(get_bill_message_warning))
  
    return sec_rel_sub_bnr,recall_edit,buttonvisibility,price_bar,msg_txt,get_bill_message_warning
try:
    CurrentRecordId = Param.CurrentRecordId
except:
    CurrentRecordId = ""
try:
    ObjName = Param.ObjName
except:
    ObjName = ""
try:
    subTabName = Param.subTabName
except:
    subTabName = ""
try:
    TreeParam = Param.TreeParam
except:
    TreeParam = ""
try:
    TreeParentParam = Param.TreeParentParam
except:
    TreeParentParam = ""
try:
    TreeSuperParentParam = Param.TreeSuperParentParam
except:
    TreeSuperParentParam = ""
try:
    TreeTopSuperParentParam = Param.TreeTopSuperParentParam
except:
    TreeTopSuperParentParam = ""
try:
    TreeSuperTopParentParam = Param.TreeSuperTopParentParam
except:
    TreeSuperTopParentParam = ""
try:
    TreeParentNodeRecId = Param.TreeParentNodeRecId
except:
    TreeParentNodeRecId = ""
try:
    TreeSuperParentRecId = Param.TreeSuperParentRecId
except:
    TreeSuperParentRecId = ""
try:
    TreeTopSuperParentRecId = Param.TreeTopSuperParentRecId
except:
    TreeTopSuperParentRecId = ""
try:
    TreeSuperTopParentRecId = Param.TreeSuperTopParentRecId
except:
    TreeSuperTopParentRecId = ""
try:
    TreeFirstSuperTopParentRecId = Param.TreeFirstSuperTopParentRecId
except:
    TreeFirstSuperTopParentRecId = ""
try:
    GrandTreeFirstSuperTopParentRecId = Param.GrandTreeFirstSuperTopParentRecId
except:
    GrandTreeFirstSuperTopParentRecId = ""
try:
    Grand_GrandTreeFirstSuperTopParentRecId = Param.Grand_GrandTreeFirstSuperTopParentRecId
except:
    Grand_GrandTreeFirstSuperTopParentRecId = ""
try:
    Sub_banner_text = Param.SubBannerText
except:
    Sub_banner_text = ""
try:
    AssemblyId = Param.AssemblyId
except:
    AssemblyId = ""
try:
    EquipmentId = Param.EquipmentId
    PMEvents = "True"
except:
    EquipmentId = ""
try:
    SerialNumber = Param.SerialNumber
except:
    SerialNumber = ""
try:
    page_type = Param.page_type
except:
    page_type = ""
try:
    CurrentTabName = TestProduct.CurrentTab
except:
    CurrentTabName = ""
try:
    CurrentTab = Param.CurrentTab
except:
    CurrentTabName = ""
if CurrentTabName == "Quote":
    try:
        getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()
    except:
        getQuotetype = ""
if CurrentTab == 'Quotes':
    try:
        getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()
    except:
        getQuotetype = ""
    if str(subTabName) == "Attachments":
        ObjName = "SAQRAT"
    if str(subTabName) == "Assembly Details":
        ObjName = "SAQSCA"
    if TreeSuperParentParam == "Fab Locations" and (subTabName == "Equipment Details" or subTabName == "Equipment Fab Value Drivers"):
        ObjName = "SAQFEQ"
    if str(subTabName) == "Equipment" and (TreeParam != "Fab Locations" and TreeParentParam != "Fab Locations" and TreeParam != "Quote Information" and TreeParentParam != "Sending Equipment" and TreeParentParam != "Receiving Equipment" ) :
        ObjName = "SAQSCO"
    if str(subTabName) == "Equipment" and (TreeParentParam == "Fab Locations" or TreeSuperParentParam == "Fab Locations" or TreeTopSuperParentParam == "Fab Locations" or TreeParentParam == "Sending Equipment" or TreeParentParam == "Receiving Equipment" ) :
        ObjName = "SAQFEQ"
    if TreeParentParam == "Quote Items" and (subTabName == "Spare Part Details" or subTabName == "Entitlements") and getQuotetype == "ZWK1 - SPARES":
        ObjName = "SAQIFP"
    if (TreeParam.startswith("Sending") or TreeParam.startswith("Receiving")):
        ObjectName = "SAQSRA"
ApiResponse = ApiResponseFactory.JsonResponse(
    Related_Sub_Banner(
        subTabName,
        ObjName,
        CurrentRecordId,
        TreeParentNodeRecId,
        TreeParam,
        TreeParentParam,
        TreeSuperParentParam,
        TreeTopSuperParentParam,
        Sub_banner_text,
        page_type
    )
)
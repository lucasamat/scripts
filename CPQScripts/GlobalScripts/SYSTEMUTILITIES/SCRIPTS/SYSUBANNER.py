# =========================================================================================================================================
#   __script_name : SYSUBANNER.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE SUB BANNER FOR THE RELATED LISTS BASED ON HIERARCHY.
#   __primary_author__ : JOE EBENEZER
#   __create_date : 28/08/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
# from CPQScripts.GlobalScripts.SYSTEMUTILITIES.SCRIPTS.SYBLKETRLG import SubtabName
import Webcom.Configurator.Scripting.Test.TestProduct
import SYTABACTIN as Table
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
Sql = SQL()
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct() or "Sales"

productAttributesGetByName = lambda productAttribute: Product.Attributes.GetByName(productAttribute) or ""


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
    
    TreeParam = Product.GetGlobal("TreeParam")
    TreeParentParam = Product.GetGlobal("TreeParentLevel0")
    TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
    TopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
    TreeSuperTopParentParam = Product.GetGlobal("TreeParentLevel3")
    try:
        contract_quote_record_id = Quote.QuoteId
    except:
        contract_quote_record_id = ''	
    
    # Trace.Write('contract_quote_record_id==='+str(Quote.GetGlobal("contract_quote_record_id")))
    try:
        current_prod = Product.Name
        #Trace.Write('current_prod==GLOBAL---='+str(Quote.GetGlobal("contract_quote_record_id")))
    except:
        current_prod = "Sales"
    try:
        TabName = TestProduct.CurrentTab
    except:
        TabName = CurrentTab
    """if TabName == "Quote" and TreeParam == "Quote Information":
        QID =  Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID  FROM SAQTMT (nolock) Where QUOTE_ID = '"+str(CurrentRecordId)+"'")
        CurrentRecordId = str(QID)
    else:
        CurrentRecordId = str(CurrentRecordId)"""    
    user_id = User.Id
    buttonvisibility = dropdown_multi_btn_str = ''
    price_bar = ''
    LOGIN_CREDENTIALS = Sql.GetFirst("SELECT top 1 Domain FROM SYCONF (nolock) order by CpqTableEntryId")
    if LOGIN_CREDENTIALS is not None:
        Login_Domain = str(LOGIN_CREDENTIALS.Domain)
    else:
        Login_Domain = "APPLIEDMATERIALS_TST"
    Trace.Write("TreeTopSuperParentParam"+str(TreeTopSuperParentParam)) 
    ListKey = ""   
    sec_rel_sub_bnr = (
        PrimaryLable
    ) = (
        PrimaryValue
    ) = SecondLable = SecondValue = ThirdLable = ThirdValue = FourthLable = FourthValue = FifthLable = FifthValue = SixthLable = SixthValue = Image = RelatedRecId = ""
    PMEvents = SeventhLable = SeventhValue = EightLable = EightValue = ""
    recall_edit =""
    CurrentTabName = ""

    crnt_prod_Qry = Sql.GetFirst(
        "SELECT APP_ID, APP_LABEL FROM SYAPPS (NOLOCK) WHERE APP_LABEL = '" + str(current_prod) + "' "
    )
    crnt_product = str(crnt_prod_Qry.APP_LABEL)
    try:
        CurrentTabName = TestProduct.CurrentTab
    except:
        CurrentTabName = ""
    Trace.Write("curr_tab@@"+str(CurrentTabName))
    # Getting Dynamic buttons for secondary banner - Starts
    try:
        quote_status = Sql.GetFirst("SELECT QUOTE_STATUS FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
    except:
        quote_status = ''    
    #if quote_status:
    try:
        revision_status = Sql.GetFirst("SELECT REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
    except:
        revision_status = ''

    #if revision_status.REVISION_STATUS == 'APPROVED':
    
    #elif quote_status.QUOTE_STATUS != 'APPROVED':
    #else:     
    #Trace.Write('status-----')
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
            get_quote_status = Sql.GetFirst("SELECT REVISION_STATUS FROM SAQTRV WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
            Trace.Write("get_quote_status--> "+str(get_quote_status.REVISION_STATUS))
            if str(get_quote_status.REVISION_STATUS).upper() == "APPROVED":
                dynamic_Button = Sql.GetList("SELECT TOP 10 HTML_CONTENT,RELATED_LIST_RECORD_ID,DISPLAY_ORDER  FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '"+str(page_details.RECORD_ID)+"' AND TAB_NAME LIKE '%"+str(CurrentTab)+"%' AND SUBTAB_NAME = '"+str(subTabName)+"' ORDER BY DISPLAY_ORDER ")
                if not dynamic_Button:
                    dynamic_Button = Sql.GetList("SELECT TOP 10 HTML_CONTENT,RELATED_LIST_RECORD_ID,DISPLAY_ORDER FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '"+str(page_details.RECORD_ID)+"' AND TAB_NAME LIKE '%"+str(CurrentTab)+"%' AND ISNULL(SUBTAB_NAME,'')='' ORDER BY DISPLAY_ORDER")
            else:
                dynamic_Button = ""
        else:
            dynamic_Button = Sql.GetList("SELECT TOP 10 HTML_CONTENT,RELATED_LIST_RECORD_ID,DISPLAY_ORDER  FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '"+str(page_details.RECORD_ID)+"' AND TAB_NAME LIKE '%"+str(CurrentTab)+"%' AND SUBTAB_NAME = '"+str(subTabName)+"' ORDER BY DISPLAY_ORDER ")
            Trace.Write('dynamic btn based on subtab====133')
            if not dynamic_Button and not subTabName == 'Inclusions': 
                dynamic_Button = Sql.GetList("SELECT TOP 10 HTML_CONTENT,RELATED_LIST_RECORD_ID,DISPLAY_ORDER FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '"+str(page_details.RECORD_ID)+"' AND TAB_NAME LIKE '%"+str(CurrentTab)+"%' AND ISNULL(SUBTAB_NAME,'')='' ORDER BY DISPLAY_ORDER")
        
    # if str(ObjName) == "SYOBJC":
    #     if page_details:
    #         dynamic_Button = Sql.GetList("SELECT HTML_CONTENT,RELATED_LIST_RECORD_ID FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '{}'".format(page_details.RECORD_ID))
    # else:
    #     add_button = ""
        # Binding button Id's based on Related list Table record id
        
        if len(dynamic_Button) > 0:
            Trace.Write('len----125---dynamic_Button--'+str(dynamic_Button))
            for btn in dynamic_Button:
                #Trace.Write('btn-----')
                if ("CANCEL" not in str(btn.HTML_CONTENT) and "SAVE" not in str(btn.HTML_CONTENT)):
                    Trace.Write("dynamic_Button--129---"+str(btn.HTML_CONTENT))
                    if btn.RELATED_LIST_RECORD_ID:
                        SYOBJH_ID = Sql.GetFirst("SELECT SYOBJH.SAPCPQ_ATTRIBUTE_NAME AS REC_ID,SYOBJR.SAPCPQ_ATTRIBUTE_NAME,SYOBJR.NAME AS NAME FROM SYOBJR (NOLOCK) INNER JOIN SYOBJH (NOLOCK) ON SYOBJR.OBJ_REC_ID = SYOBJH.RECORD_ID WHERE SYOBJR.SAPCPQ_ATTRIBUTE_NAME = '{syobjr_rec_id}'".format(syobjr_rec_id = btn.RELATED_LIST_RECORD_ID))
                    if len(dynamic_Button) > 1:
                        if str(btn.HTML_CONTENT) != "" and str(btn.RELATED_LIST_RECORD_ID) != "":
                            button_id = str(btn.RELATED_LIST_RECORD_ID).replace("-","_")+"_"+str(SYOBJH_ID.REC_ID).replace("-","_")
                            if btn.RELATED_LIST_RECORD_ID == SYOBJH_ID.SAPCPQ_ATTRIBUTE_NAME:
                                Trace.Write("Check SHP0")
                                div_id = "div_CTR_"+str(SYOBJH_ID.NAME).replace(" ","_")
                                # add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id))
                                if "div_id" in str(btn.HTML_CONTENT):
                                    Trace.Write("Check SHP1")
                                    add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id), div_id= str(div_id))
                                else:
                                    add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id))
                            else:
                                add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id))
                            Trace.Write("add_button--147---"+str(add_button))
                            multi_buttons.append(add_button)
                            
                        else:
                            #Trace.Write("Billing matrix 124--------")
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
                            Trace.Write("add_buttonadd_buttonadd_button----"+str(add_button))
                        else:
                            Trace.Write("Billing matrix 146-------")
                            add_button = btn.HTML_CONTENT
                            if btn.RELATED_LIST_RECORD_ID:
                                div_id = "div_CTR_"+str(SYOBJH_ID.NAME).replace(" ","_")
                                if "div_id" in add_button:
                                    add_button = add_button.format(div_id = div_id)
                else:
                    Trace.Write('173--'+str(subTabName))
                    try:
                        if subTabName.startswith("Year") and str(ObjName) == "SAQRIB":
                            Trace.Write('176---------------')
                            add_button = '<button id="billingmatrix_save" onclick="showSBillMatBulksave(this)" style= "display: none;" class="btnconfig" >SAVE</button><button id="billingmatrix_cancel" onclick="showSBillMatBulkcancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>'
                        if subTabName =="Delivery Schedule"  and str(ObjName) == "SAQSPD":
                            Trace.Write('176---------------')
                            add_button = '<button id="delivery_save" onclick="showSdeliverysave(this)" style= "display: none;" class="btnconfig" >SAVE</button><button id="delivery_cancel" onclick="showSdeliverycancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>'
                    except:
                        #Trace.Write('176--------EXCEPT-------')
                        add_button = ""
                    add_button = ""
        else:
            #Trace.Write('200-add_button--'+str(add_button))
            add_button = ""
        Trace.Write(str(sec_rel_sub_bnr)+"--sec_rel_sub_bnr----add_button_ Trace ------- "+str(add_button))
        try:
            if subTabName.startswith("Year") and str(ObjName) == "SAQRIB":
                Trace.Write('176---------------')
                sec_rel_sub_bnr +=('<button id="billingmatrix_save" onclick="showSBillMatBulksave(this)" style= "display: none;" class="btnconfig" >SAVE</button><button id="billingmatrix_cancel" onclick="showSBillMatBulkcancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>')
            if subTabName =="Delivery Schedule"  and str(ObjName) == "SAQSPD":
                Trace.Write('176---------------')
                add_button = '<button id="delivery_save" onclick="showSdeliverysave(this)" style= "display: none;" class="btnconfig" >SAVE</button><button id="delivery_cancel" onclick="showSdeliverycancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>'
        except:
            Trace.Write('176--------EXCEPT-------')
            add_button = ""
        # if str(ObjName) == "SAQRIB":
        #     Trace.Write('176---200------------'+str(sec_rel_sub_bnr))
        #     sec_rel_sub_bnr += add_button
        #     Trace.Write(str(add_button)+'176---200----212--------'+str(sec_rel_sub_bnr))
        Trace.Write(str(sec_rel_sub_bnr)+"--ObjName---178--ADD+BUT_J----"+str(add_button))
        
        Trace.Write("Multi buttons--> "+str(multi_buttons))
        # if subTabName == 'Inclusions' and (TreeSuperParentParam == 'Product Offerings' or TopSuperParentParam == 'Product Offerings'):
        #     multi_buttons_temp = multi_buttons
        #     multi_buttons = []
        #     if TopSuperParentParam == 'Product Offerings' and TreeParentParam in ('Z0009','Z0006'):
        #         multi_buttons = multi_buttons_temp 


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
    elif TreeParam == "Contract Information" or TreeParam == "Contract Preview" :
        if ObjName == 'CTCTIP' and subTabName == 'Detail':
            ObjName = "CTCTIP"
        else:
            ObjName = "CTCNRT"
    elif (TreeParam.startswith("Sending") or TreeParam.startswith("Receiving")):
        ObjName = "SAQSRA"
        Trace.Write('ObjName@@@'+str(ObjName))		
    # elif TreeParam == "Approvals":
    # 	Trace.Write('8888888888--------')
    # 	PrimaryLable = "Approvals"
    # 	PrimaryValue = "All"
            
    #CurrentRecordId = str(Product.GetGlobal("clone_id"))
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
            Image = "/mt/" + str(Login_Domain) + "/Additionalfiles/" + str(ImageUrl)
        # if str(ObjName) == "SYOBJX":
            
        # 	PrimaryLable = "Index Name"
        # 	PrimaryValue = "All"
        # 	#PrimaryValue = str(TreeParam)
        # 	Trace.Write("Tree "+str(TreeParam))  
        if CurrentRecordId.startswith("SYOBJR", 0) == True:
            Trace.Write("CurrentRecordIdCurrentRecordId----171----"+str(CurrentRecordId))            
            ThirdQuery = Sql.GetFirst(
                "select * from SYOBJD (nolock) where OBJECT_NAME = '" + str(ObjName) + "' AND IS_KEY = 'True' "
            )
            if TreeParam == 'Revisions':
                rev_quote = Sql.GetFirst(" SELECT * FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{contract_quote_record_id}' AND ACTIVE = 'TRUE' ".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")))
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
            # if str(CurrentRecordId) == 'SYOBJR-98799' and str(ObjName) == 'SAQDOC':                
            #     PrimaryLable = "Documents"
            #     PrimaryValue = "All"
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
                    "select 	OBJECT_FIELD_ID FROM SYPROD(nolock)  WHERE PROFILE_OBJECTFIELD_RECORD_ID='" + CurrentRecordId + "'"
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
            elif TabName == "Contracts"  and str(TreeParentParam) == "Product Offerings" and str(TreeParam) != "" and str(ObjName) == "CTCTSV" : 
                Trace.Write('999---')               
                PrimaryLable = "Offerings"
                PrimaryValue = "All"
                if TabName == "Quote":
                    SecondLable = "Product Offering Type"
                elif TabName == "Contract":
                    SecondLable = "Product Type"
                SecondValue = str(TreeParam)	                             
            elif (TreeParam.startswith("Sending") or TreeParam.startswith("Receiving")):
                #if subTabName == "Fab Locations":
                #	PrimaryLable = str(TreeParam).split("-")[0].strip()
                #	PrimaryValue = str(TreeParam).split("-")[1].strip()
                #	SecondLable = "Fab Locations"
                #	SecondValue = "ALL"
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
            
                    
            # elif (
            #     CurrentRecordId.startswith("SYOBJR", 0) == True and str(TreeParentNodeRecId) != ""
            # ) and TreeParam == 'Documents' and TabName == "Quote":                
            #     PrimaryLable = str(TreeParam)
            #     PrimaryValue = "ALL"
            elif (
                CurrentRecordId.startswith("SYOBJR", 0) == True and str(TreeParentNodeRecId) != ""
            ) and TabName == "Invoice":
                PrimaryLable = str(TreeParam)
                PrimaryValue = "ALL"
            elif TabName == "Page" and str(TreeParam) == "Tabs" and str(ObjName) == "SYTABS":
                PrimaryLable = "Tabs"
                PrimaryValue = "All"
                #SecondLable = "Tabs"
                #SecondValue = "All"
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
            elif TabName == "Quotes" and str(TreeParam) == "Customer Information":
                PrimaryLable = "Customer Information"
                PrimaryValue = "Use the Customer Information functionality to manage your quote Accounts Contacts..."    
            elif TreeParam =="Sales Team":
                PrimaryLable = "Sales Team"
                PrimaryValue = "Use the Sale Team functionality to manage all contributors to your Quote..."
            elif TreeParam == "Quote Items" and str(subTabName)=="Entitlements" and str(CurrentRecordId) == "SYOBJR-00010":
                query_result = Sql.GetFirst("select * from SAQRIT (nolock) where QUOTE_RECORD_ID = '"+str(Quote.GetGlobal("contract_quote_record_id"))+"' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' AND QUOTE_REVISION_CONTRACT_ITEM_ID ='"+str(CurrentRecordId)+"' ")                
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
                Trace.Write("qcdoc=====")
                if subTabName == "Attachments":
                    Trace.Write("qcdoc=====1111")
                    PrimaryLable = "Attachments"
                    PrimaryValue = "Use this page to upload .pdf attachments to your quote revision"
                else:                
                    PrimaryLable = "Dynamic Document Generator"
                    PrimaryValue = "Use the settings below to control the conditional display of information on your Customer Facing Documents" 
            else:
                ThirdQuery = Sql.GetFirst(
                "select * from SYOBJD (nolock) where OBJECT_NAME = '" + str(ObjName) + "' AND IS_KEY = 'True' "
            )
                
                if TreeParam != 'Revisions':
                    PrimaryLable = str(TreeParam)
                    PrimaryValue = "ALL"
                elif (rev_quote is None or rev_quote == '') and TreeParam == 'Revisions':
                    PrimaryLable = str(TreeParam)
                    PrimaryValue = "ALL"    
                if (
                    ThirdQuery is not None
                ):
                    SecondLable = str(ThirdQuery.FIELD_LABEL)
                    SecondValue = "ALL"
                
        elif CurrentRecordId.startswith("SYOBJR", 0) == False:    
            Trace.Write('8888888888')        
            try:
                if TabName == 'Quotes':
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
            except:				
                pass
            try:
                if TabName == 'Contracts':
                    Trace.Write('except--------')
                    contract_quote_record_id = Quote.GetGlobal("contract_record_id")
            except:				
                pass
            # if TreeParam == 'Sales Orgs':
            # 	PrimaryLable = "Sales Orgs"
            # 	PrimaryValue = "All"
            # if TreeParam == "Product Offerings" :
            # 	PrimaryLable = "Product offerings"
            # 	PrimaryValue = "All"
            # if TreeParentParam == "Product Offerings":
            # 	PrimaryLable = "Product offerings"
            # 	PrimaryValue = "All"
            # 	SecondLable = "Product Offering Type"
            # 	SecondValue = TreeParam
            if TreeParam == "Customer Information" or TreeParam == "Quote Preview":	
                if ObjName == 'SAQTIP':
                    ObjName = "SAQTIP"
                    PrimaryLable = "Source Account ID"
                    PrimaryValue = str(Product.GetGlobal("stp_account_Id"))
                    SecondLable = "Source Account Name"
                    SecondValue = str(Product.GetGlobal("stp_account_name"))
                elif ObjName == 'SAQSCF' and (subTabName == 'Source Fab Location Details' or subTabName == 'Source Fab Location'):
                    ObjName = "SAQSCF"
                elif ObjName == 'SAQSTE' and (subTabName == 'Equipment details' or subTabName == 'Tool Relocation Matrix details'):
                    ObjName = "SAQSTE"
                else:
                    ObjName = "SAQTMT"

            elif TreeParam =="Quote Documents":
                Trace.Write("qcdoc=====")
                if subTabName == "Attachments":
                    Trace.Write("qcdoc=====1111")
                    PrimaryLable = "Attachments"
                    PrimaryValue = "Use this page to upload .pdf attachments to your quote revision"
                else:                
                    PrimaryLable = "Dynamic Document Generator"
                    PrimaryValue = "Use the settings below to control the conditional display of information on your Customer Facing Documents"  
            
                    

            elif subTabName == "Equipment" and (TreeParentParam == "Fab Locations" or TreeSuperParentParam == "Product Offerings" or TreeParentParam == "Add-On Products" and sec_rel_sub_bnr == "") and CurrentTab == 'Quotes':		
                sale_type = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                if sale_type == 'TOOL RELOCATION' or TreeParam.startswith('Z0007'):
                    sec_rel_sub_bnr += ''
                
                else:
                    Trace.Write("Inside Else"+str(sec_rel_sub_bnr))
                    if quote_status.QUOTE_STATUS != 'APPROVED':
                        Trace.Write("Inside addbut")  
                        if len(multi_buttons)>0:
                            Trace.Write("lenmulti---")
                            for btn in multi_buttons:
                                if "Sending Account" in TreeParam:
                                    if "ADD UNMAPPED EQUIPMENTS" in btn:
                                        sec_rel_sub_bnr += (str(btn))
                                        if (subTabName == "Equipment" or subTabName == "Fab Value Drivers") and TreeParam.startswith("Sending"):
                                            Trace.Write('opp=====')
                                            PrimaryLable = "Sending Account ID"
                                            PrimaryValue = str(TreeParam).split("-")[1].strip()
                                            SecondLable = "Sending Fab Locations"
                                            SecondValue = "ALL"
                                            ThirdLable = "Equipment"
                                            ThirdValue = "ALL"
                                        
                                else:
                                    if "ADD FROM LIST" or "ADD TEMP TOOL" in btn:        
                                        sec_rel_sub_bnr += (str(btn))
                                        Trace.Write(str(btn))
                                # else:
                                #     sec_rel_sub_bnr += ''
                        else:
                            Trace.Write("lenmultibtn---+str"+str(sec_rel_sub_bnr))
                            sec_rel_sub_bnr += str(add_button)


            elif TreeParam == "Contract Information" or TreeParam == "Contract Preview":	
                if ObjName == 'CTCTIP' and subTabName == 'Detail':
                    ObjName = "CTCTIP"
                    PrimaryLable = "Source Account ID"
                    PrimaryValue = str(Product.GetGlobal("stp_account_Id"))
                    SecondLable = "Source Account Name"
                    SecondValue = str(Product.GetGlobal("stp_account_name"))
                else:
                    ObjName = "CTCNRT"
            elif TreeSuperParentParam == "Fab Locations" and subTabName == "Equipment Fab Value Drivers":
                PrimaryLable = ""
                PrimaryValue = "" 
            elif TreeParam == "Billing":
                ObjName = "SAQRIB"
                PrimaryLable = str(TreeParam)
                PrimaryValue = "All"   
            elif TreeSuperParentParam == "Fab Locations" and ObjName == 'CTCFEQ':
                getFab = Sql.GetFirst("select FABLOCATION_NAME from CTCFBL(nolock) where FABLOCATION_ID = '"+str(TreeParentParam)+"'")        
                PrimaryLable = "Fab Location ID"
                PrimaryValue = str(TreeParentParam)
                SecondLable = "Fab Location Name"
                SecondValue = getFab.FABLOCATION_NAME
                ThirdLable = "Greenbook"
                ThirdValue = str(TreeParam)
                FourthLable = "Equipment"
                FourthValue = "All"   
            elif (TreeSuperParentParam == "Fab Locations" or TreeTopSuperParentParam == "Fab Locations") and (subTabName == 'Equipment' or subTabName == "Details" or subTabName == "Customer Value Drivers"):	
                Trace.Write('su=========')		
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
                            Trace.Write('sendeqppp=========')     
                            PrimaryLable = "Fab Location ID"
                            PrimaryValue = str(TreeParam)
                            SecondLable = "Fab Location Name"
                            SecondValue = getFab.FABLOCATION_NAME
                            ThirdLable = "Greenbook"
                            ThirdValue = str(TreeParam)
                            ThirdLable = "Equipment"
                            ThirdValue = "All" 
                        
                elif ("Sending" in TreeSuperParentParam or "Receiving" in TreeSuperParentParam):	
                    Trace.Write('su11=========')
                    getFab = Sql.GetFirst("select FABLOCATION_NAME from SAQFBL(nolock) where FABLOCATION_ID = '"+str(TreeParentParam)+"'")
                    if subTabName == "Greenbook Fab Value Drivers":
                        get_val = Sql.GetFirst(" SELECT EQUIPMENT_ID,SERIAL_NO FROM SAQSCO WHERE GREENBOOK = '"+str(TreeParam)+"'")
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
                        Trace.Write('sendeqppp=========')     
                        PrimaryLable = "Fab Location ID"
                        PrimaryValue = str(TreeParam)
                        SecondLable = "Fab Location Name"
                        SecondValue = getFab.FABLOCATION_NAME
                        ThirdLable = "Greenbook"
                        ThirdValue = str(TreeParam)
                        FourthLable = "Equipment"
                        FourthValue = "All" 		
                        
                # elif subTabName == "Details":
                # 	PrimaryLable = "Fab Location ID"
                # 	PrimaryValue = str(TreeParentParam)
                # 	SecondLable = "Greenbook"
                # 	SecondValue = str(TreeParam)
                    Trace.Write("SLabel"+SecondLable)
            elif TreeParam == "Approvals"  and TabName == "Quotes":
                Trace.Write("760")
                if subTabName == '':
                    getChain = Sql.GetFirst("SELECT APRCHN_ID FROM ACAPMA (NOLOCK) WHERE APRTRXOBJ_RECORD_ID = '{}' ORDER BY APRCHN_ID ASC".format(quote_revision_record_id))
                    if getChain:
                        subTabName = getChain.APRCHN_ID
                contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                getval = Sql.GetFirst(" select DISTINCT TOP 10 APRCHN_ID, APRCHN_NAME, APPROVAL_METHOD FROM ACAPCH (nolock) WHERE APRCHN_ID = '"+str(subTabName)+"'")
                getown = Sql.GetFirst(" select DISTINCT TOP 10 OWNER_NAME from SAQTMT(nolock) where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                # acaptx_dat = Sql.GetFirst("SELECT * FROM ACAPCH (NOLOCK) WHERE APRCHN_ID = '{Subtab}'".format(Subtab=subTabName))
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
                Trace.Write("TreeParam--"+str(TreeParam))
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
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    account_id = Sql.GetFirst("SELECT ACCOUNT_ID FROM SAQSRA (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND RELOCATION_TYPE LIKE '%SENDING%' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                    PrimaryLable = "Sending Account ID"
                    PrimaryValue = str(account_id.ACCOUNT_ID)
                    SecondLable = str(subTabName)
                    SecondValue = "ALL"
                elif (subTabName == "Receiving Equipment" or subTabName == "Service Fab Value Drivers" or subTabName == "Service Cost and Value Drivers" or subTabName == "Entitlements") and TreeParam.startswith("Receiving Equipment"):
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    account_id = Sql.GetFirst("SELECT ACCOUNT_ID FROM SAQSRA (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND RELOCATION_TYPE LIKE '%RECEIVING%'  AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
                    PrimaryLable = "Receiving Account ID"
                    PrimaryValue = str(account_id.ACCOUNT_ID)
                    SecondLable = str(subTabName)
                    SecondValue = "ALL"
                # elif subTabName == "Fab Locations":
                # 	PrimaryLable = str(TreeParam).split("-")[0].strip()
                # 	PrimaryValue = str(TreeParam).split("-")[1].strip()
                # 	SecondLable = "Fab Locations"
                # 	SecondValue = "ALL"
                
            else:
                ThirdQuery = Sql.GetFirst(
                "select * from SYOBJD (nolock) where OBJECT_NAME = '" + str(ObjName) + "' AND IS_KEY = 'True' "
                )
                
                # PrimaryLable = str(TreeParam)
                # PrimaryValue = "ALL"
                # if (
                # 	ThirdQuery is not None
                # ):
                # 	SecondLable = str(ThirdQuery.FIELD_LABEL)
                # 	SecondValue = "ALL"
                    
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
                Trace.Write(ListKey)
                ListKey[0] = ''                
                if "DEFAULT" in str(column):
                    column = str(column).replace("DEFAULT", "[DEFAULT]")
                # if str(ObjName)  == "SYPROH" and str(TreeParentParam) == "Object Level Permissions": 					
                    #str(columns[0]) = str(column[0]).replace("OBJECT_RECORD_ID", "PROFILE_OBJECT_RECORD_ID")
                
                if str(ObjName) == "SAQRIB":
                    contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
                    getbillid = Sql.GetFirst("select QUOTE_BILLING_PLAN_RECORD_ID from SAQRIB(nolock) where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                    if getbillid:
                        CurrentRecordId = getbillid.QUOTE_BILLING_PLAN_RECORD_ID
                
                # for Quote Preview node sub-banner start
                # Rec_qt = Product.Attr('QSTN_SYSEFL_QT_00001').GetValue()
                # for Quote Preview node sub-banner end
                # if TreeParam == "Quote Preview":                    
                    # ValQuery = Sql.GetFirst(
                    #     "select "
                    #     + str(column)
                    #     + " from "
                    #     + str(ObjName)
                    #     + " where "
                    #     + str(columns[0])
                    #     + " = '"
                    #     + str(Rec_qt) 
                    #     + "'"
                    # ) 
                # else:
                
                # if ObjName == "SAQSGB":
                # 	contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                # 	prd_gb_node = Sql.GetFirst("SELECT QUOTE_SERVICE_GREENBOOK_RECORD_ID FROM SAQSGB (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' and GREENBOOK = '"+str(TreeParam)+"'")
                # 	if prd_gb_node:
                # 		CurrentRecordId = prd_gb_node.QUOTE_SERVICE_GREENBOOK_RECORD_ID
                        
                # if ObjName == "SAQFGB":
                # 	contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                # 	fab_gb_node = Sql.GetFirst("SELECT QUOTE_FAB_LOC_GB_RECORD_ID FROM SAQFGB (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
                # 	if fab_gb_node:
                # 		CurrentRecordId = fab_gb_node.QUOTE_FAB_LOC_GB_RECORD_ID
                # if ObjName == "SAQIGB":
                #     contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                #     itm_gb_node = Sql.GetFirst("SELECT QUOTE_ITEM_GREENBOOK_RECORD_ID FROM SAQIGB (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND GREENBOOK = '"+str(TreeParam)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                #     if itm_gb_node:
                #         CurrentRecordId = itm_gb_node.QUOTE_ITEM_GREENBOOK_RECORD_ID
                
                if ObjName == "SAQTMT":
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    itm_gb_node = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                    if itm_gb_node:
                        CurrentRecordId = itm_gb_node.MASTER_TABLE_QUOTE_RECORD_ID
                # elif ObjName == "SAQSTE":
                #     contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                #     ip_equipment = Sql.GetFirst("SELECT QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
                #     if ip_equipment:
                #         CurrentRecordId = ip_equipment.QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID
                # elif ObjName == "SAQIFL" and subTabName != 'Details':
                #     ListKey[0] = ''
                # elif ObjName == "CTCSCO":
                # 	Trace.Write('ctcsco=====')
                # 	contract_quote_record_id = Quote.GetGlobal("contract_record_id")		
                # 	cntract_gb_node = Sql.GetFirst("SELECT CONTRACT_SERVICE_EQUIPMENT_RECORD_ID FROM CTCSCO (NOLOCK) WHERE CONTRACT_RECORD_ID = '"+str(contract_quote_record_id)+"'")
                # 	get_banner = Sql.GetFirst("SELECT CONTRACT_SERVICE_EQUIPMENT_RECORD_ID,SERVICE_ID,SERVICE_DESCRIPTION,GREENBOOK,EQUIPMENT_ID from CTCSCO where CONTRACT_SERVICE_EQUIPMENT_RECORD_ID = '"+str(cntract_gb_node.CONTRACT_SERVICE_EQUIPMENT_RECORD_ID)+"'")
                # 	PrimaryLable = "Product Offering ID"
                # 	PrimaryLable = get_banner.SERVICE_ID
                # 	SecondLable = "Product Offering Description"
                # 	SecondValue = get_banner.SERVICE_DESCRIPTION
                # 	Trace.Write("Check")
                # 	ThirdLable = "Greenbook"
                # 	ThirdValue = "ALL"
                # 	if cntract_gb_node:
                # 		CurrentRecordId = cntract_gb_node.CONTRACT_SERVICE_EQUIPMENT_RECORD_ID
                elif ObjName == "CTCSGB":
                    contract_quote_record_id = Quote.GetGlobal("contract_record_id")
                    prd_gb_node = Sql.GetFirst("SELECT CNTSRVGB_RECORD_ID FROM CTCSGB (NOLOCK) WHERE CONTRACT_RECORD_ID = '"+str(contract_quote_record_id)+"' and GREENBOOK = '"+str(TreeParam)+"'")
                    if prd_gb_node:
                        CurrentRecordId = prd_gb_node.CNTSRVGB_RECORD_ID		
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
                    Trace.Write("Constraints SHP")
                    getname = Sql.GetFirst("select CONSTRAINT_TYPE from SYOBJC (NOLOCK) where OBJECT_CONSTRAINT_RECORD_ID ='"+str(CurrentRecordId)+"' ")
                    PrimaryLable = "Constraint Type"
                    PrimaryValue = str(TreeParam)
                    #SecondLable = "Name"
                    #SecondValue = str(TreeParam)
                ##commented the below code taking all the values in dynamic way...
                # elif ObjName == "SAQITM" and TreeParentParam == "Quote Items" and subTabName == "Annualized Items":
                #     Trace.Write("663")
                #     getname = Sql.GetFirst("select QUOTE_ITEM_RECORD_ID,LINE_ITEM_ID,SERVICE_ID,SERVICE_DESCRIPTION,PRICINGPROCEDURE_ID from SAQITM where QUOTE_ITEM_RECORD_ID ='"+str(CurrentRecordId)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                #     TreeParam = TreeParam.split('-')
                #     PrimaryLable = "Line"
                #     PrimaryValue = TreeParam[0].strip()
                #     SecondLable = "Product Offering ID"
                #     SecondValue = TreeParam[1].strip()
                # elif ObjName == "SAQIFL" and TreeSuperParentParam == "Quote Items" and subTabName == "Details":
                #     Trace.Write("Quote Items")
                #     get_fab = SqlHelper.GetList("select SERVICE_ID,SERVICE_DESCRIPTION,FABLOCATION_ID,FABLOCATION_NAME from SAQIFL where QUOTE_ITEM_FAB_LOCATION_RECORD_ID = '"+str(CurrentRecordId)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                #     PrimaryLable = "Fab Location ID"
                #     PrimaryValue = TreeParam
                elif ObjName == "SAQICO":
                    #contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    # qte_fab_node = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                    # if qte_fab_node:
                    #     CurrentRecordId = qte_fab_node.MASTER_TABLE_QUOTE_RECORD_ID
                    Trace.Write("saqico=====")
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    annualized_details = Sql.GetFirst("SELECT QUOTE_ITEM_COVERED_OBJECT_RECORD_ID FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"' AND LINE = '"+str(CurrentRecordId)+"'")
                    if annualized_details:
                        CurrentRecordId = annualized_details.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID   
                elif ObjName == "SAQSGB" and TreeSuperParentParam == "Receiving Equipment" and subTabName == "Equipment Details":
                    Trace.Write("SHP---Eq")
                    get_val = Sql.GetFirst("select FABLOCATION_ID from SAQSGB(nolock) where SERVICE_ID = '"+str(TreeTopSuperParentParam)+"' and FABLOCATION_ID = '"+str(TreeParentParam)+"'")
                    PrimaryLable = "Fab Location ID "
                    PrimaryValue = get_val.FABLOCATION_ID
                    SecondLable = "Greenbook"
                    SecondValue = str(TreeParam)
                    ThirdLable = "Equipment"
                    ThirdValue = "ALL"			
                elif ObjName == "SAQSFB":
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    qte_fab_node = Sql.GetFirst("SELECT QUOTE_SERVICE_FAB_LOCATION_RECORD_ID FROM SAQSFB (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" +str(quote_revision_record_id)+"'")
                    if qte_fab_node:
                        CurrentRecordId = qte_fab_node.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID                
                                            
                if str(ObjName) != "SYPROH":
                    Trace.Write("Test668")
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
                    Trace.Write("check"+str(ValQuery))                
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
                            FourthLable = "Party Name"
                            FourthValue = str(ListVal[3])   
                        elif ObjName == "CTCTIP":
                            ThirdLable = "Party ID"
                            ThirdValue = str(ListVal[2])
                        else:
                            Trace.Write('list222--------')
                            ThirdLable = ListKey[2]
                            ThirdValue = str(ListVal[2]).encode("ascii", "ignore")
                                    
                except:
                    Trace.Write("error2")
                try:
                    Trace.Write("727")
                    getQuotetype = ""   
                    if ObjName == 'ACACHR' or  TreeSuperParentParam == "Approvals":
                        Trace.Write("1097---")
                        FourthLable = "Approval Round"
                        FourthValue = TreeParam
                    #CurrentTabName = TestProduct.CurrentTab
                    
                    if TabName == "Quote":
                        getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()
                        Trace.Write("734")
                        
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
                    if ObjName == "CTCSCO":
                        Trace.Write('CT')
                        ThirdLable = "Greenbook"
                        ThirdValue = ListKey[3]
                    

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
                Trace.Write("LISTVAL---"+str(ListVal))
                if str(ObjName) == 'SYPGAC' and TabName == 'Tab':
                    PrimaryLable = "Key"
                    PrimaryValue = PrimaryValue
                    # SecondLable = "Action Name"
                    # SecondValue = ListVal[1]
                    #ThirdLable = "Product Offering Type"
                    #ThirdValue = TreeParentParam
                
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
                    Trace.Write("Fab23")
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
                        Trace.Write("Fab24")				
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
                    Trace.Write("Fab2333")
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
                        Trace.Write("Line No:1182 - Testing")
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
                        Trace.Write("ObjectName:{}".format(str(ObjName)))
                        get_val = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQSFB(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
                        Trace.Write("Line no:1194")
                        ThirdLable = "Product Offering Description"
                        ThirdValue = get_val.SERVICE_DESCRIPTION
                        FourthLable = "Product Offering Type"
                        FourthValue = TreeTopSuperParentParam 
                        FifthLable = " Fab Location ID"
                        FifthValue = TreeParam
                    else:
                        if TreeSuperParentParam != 'Add-On Products':
                            Trace.Write("Line No:1220")
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
                    Trace.Write("check")
                    get_val = Sql.GetFirst(" SELECT EQUIPMENT_ID,SERIAL_NO FROM SAQSCO WHERE GREENBOOK = '"+str(TreeParam)+"'")
                    FifthLable = "Equipment ID"
                    FifthValue = get_val.EQUIPMENT_ID
                    SixthLable = "Serial No"
                    SixthValue = get_val.SERIAL_NO
                if (str(ObjName) == 'SAQTSV'or str(ObjName) == 'SAQSCO' or str(ObjName) == 'SAQSPT') and TreeSuperParentParam == 'Product Offerings'and TabName == "Quotes":
                    Trace.Write('*subb--')					
                    TreeParam = Quote.GetGlobal("TreeParam")
                    TreeParentParam = Quote.GetGlobal("TreeParentLevel0")
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
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    where_cond = "WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}'".format(contract_quote_record_id, quote_revision_record_id, TreeParam )
                    status_image =''
                    try:
                        #get_status = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'GET_STATUS','partnumber':TreeParam,'where_cond':where_cond,'ent_level_table':'SAQTSE'})
                        get_status = Sql.GetFirst("SELECT CONFIGURATION_STATUS FROM SAQTSE WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}'".format(contract_quote_record_id, quote_revision_record_id, TreeParam ) )
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
                            SixthValue = '<img class="treeinsideicon" src="/mt/appliedmaterials_tst/Additionalfiles/AMAT/Quoteimages/{image}"/>'.format(image = status_image)
                        else:
                            FourthValue = '<img class="treeinsideicon" src="/mt/appliedmaterials_tst/Additionalfiles/AMAT/Quoteimages/{image}"/>'.format(image = status_image)
                    # FifthLable = ""
                    # FifthValue = ""
                    if getService is not None:
                        SecondLable = "Product Offering Description"
                        SecondValue = getService.SERVICE_DESCRIPTION
                    if 'SPARE' in getQuotetype:
                        FourthLable = ""
                        FourthValue = ""
                    covered_obj = Sql.GetFirst("select EQUIPMENT_ID from SAQSCO(nolock) where QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id=quote_revision_record_id))
                    if covered_obj is not None and (subTabName == "Equipment" or subTabName == 'Entitlements' or subTabName == 'Service Fab Value Drivers' or subTabName == 'Service Cost and Value Drivers' or subTabName == 'Customer Value Drivers' or subTabName == 'Product Value Drivers'):                        
                        FourthLable = "Equipment"
                        FourthValue = "All"
                        ##adding configuration status in offering subtab
                        Trace.Write('status_image--'+str(status_image))
                        FifthLable = "Configuration Status"
                        if status_image:
                            FifthValue = '<img class="treeinsideicon" src="/mt/appliedmaterials_tst/Additionalfiles/AMAT/Quoteimages/{image}"/>'.format(image = status_image)
                        # contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                        # where_cond = "WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}'".format(contract_quote_record_id, quote_revision_record_id, TreeParam )
                        # try:
                        #     get_status = ScriptExecutor.ExecuteGlobal("CQENTLNVAL", {'action':'GET_STATUS','partnumber':TreeParam,'where_cond':where_cond,'ent_level_table':'SAQTSE'})
                        #     if get_status == 'true':
                        #         status_image = 'config_status_icon.png'
                        #     else:
                        #         status_image = 'config_pend_status_icon.png'
                        #     SixthLable = "Configuration Status"
                        #     SixthValue = '<img class="treeinsideicon" src="/mt/appliedmaterials_tst/Additionalfiles/AMAT/Quoteimages/{image}"/>'.format(image = status_image)
                        # except:
                        #     pass

                        
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
                elif (str(ObjName) == 'CTCTSV'or str(ObjName) == 'CTCSCO' or str(ObjName == 'CTCSPT')) and TreeSuperParentParam == 'Product Offerings'and CurrentTab == "Contracts":					
                    TreeParam = Quote.GetGlobal("TreeParam")
                    TreeParentParam = Quote.GetGlobal("TreeParentLevel0")
                    getService = Sql.GetFirst("select SERVICE_DESCRIPTION from CTCTSV(nolock) where SERVICE_ID = '"+str(TreeParam)+"'")
                    PrimaryLable = "Product Offering ID"
                    PrimaryValue = TreeParam
                    ThirdLable = "Product Offering Type"
                    ThirdValue = TreeParentParam
                    FourthLable = ""
                    FourthValue = ""
                    FifthLable = ""
                    FifthValue = ""
                    if getService is not None:
                        SecondLable = "Product Offering Description"
                        SecondValue = getService.SERVICE_DESCRIPTION
                    if 'SPARE' in getQuotetype:
                        FourthLable = ""
                        FourthValue = ""
                    covered_obj = Sql.GetFirst("select EQUIPMENT_ID from CTCSCO(nolock) where CONTRACT_RECORD_ID = '{contract_quote_record_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_record_id")))
                    if covered_obj is not None and (subTabName == "Equipment" or subTabName == 'Entitlements' or subTabName == 'Service Fab Value Drivers' or subTabName == 'Service Cost and Value Drivers'):
                        FourthLable = "Equipment"
                        FourthValue = "All"
                        FifthLable = ""
                        FifthValue = ""
                elif (TreeSuperParentParam == "Fab Locations" or TreeTopSuperParentParam == "Fab Locations") and (subTabName == 'Equipment' or subTabName == "Details" or subTabName == "Customer Value Drivers" or subTabName == "Fab Value Drivers"):
                    #getFab = Sql.GetFirst("select FABLOCATION_NAME from SAQFBL(nolock) where FABLOCATION_ID = '"+str(TreeParentParam)+"'")
                    Trace.Write("Fab Locations")
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
                        Trace.Write("Fab2")
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
                # SecondLable = "Approvers"
                # SecondValue = "All"
                # elif TopSuperParentParam == "Quote Items" and ObjName == "SAQICO" and CurrentRecordId == 'SAQICOJ':
                
                #     TreeSuperParentParam = TreeSuperParentParam.split("-")[1]
                #     PrimaryLable = "Product Offering ID"
                #     PrimaryValue = str(TreeSuperParentParam)
                #     SecondLable = "Line Item Id"
                #     SecondValue = "ALL"
                #     ThirdLable = "Fab Location ID" 
                #     ThirdValue = str(TreeParentParam) 
                    
    Trace.Write(str(TreeSuperTopParentParam)+"CHECK"+str(CurrentRecordId))           
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
        # try:
        #     FourthLable = ListVal[4]
        #     FourthValue = ListVal[4]
        # except:
        #     FourthLable = ''
        #     FourthValue = ''
        # try:            
        #     FifthLable = ListKey[5]
        #     FifthValue = ListVal[5]
        # except:
        #     FifthLable = ''
        #     FifthValue = ''
        # try:        
        #     SixthLable = ListKey[6]
        #     SixthValue = ListVal[6]
        # except:
        #     SixthLable = ''
        #     SixthValue = ''    
    Trace.Write("tab name--"+str(TabName)+" REC_ID "+str(CurrentRecordId))
    Trace.Write("ObjectName changed or not:"+str(ObjName))
    if  TreeTopSuperParentParam == "Quote Items" and str(TreeParam) != "" and (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Greenbook Fab Value Drivers" or subTabName == "Greenbook Cost and Value Drivers" or subTabName == "Details"):
        Trace.Write("check --1668")
        #TreeParentParam = TreeParentParam.split('-')
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
        # FourthLable = ListKey[4]
        # FourthValue = ListVal[4]
        # FifthLable = ListKey[5]
        # FifthValue = ListVal[5]
        #SixthLable = ListKey[6]
        #SixthValue = ListVal[6]
        
    # elif TreeParam == 'Approvals' and str(TabName == 'Quote'):
    #     PrimaryLable = "Approvals"
    #     PrimaryValue = "All"     
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
        Trace.Write(1497)		
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
        Trace.Write(1511)		
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
        Trace.Write("PM 1638")
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
        PreventiveMaintainenceobj = Sql.GetFirst("select EQUIPMENT_ID from SAQSAP(nolock) where QUOTE_RECORD_ID = '{contract_quote_record_id}' and EQUIPMENT_ID = '{Equipment_Id}' and ASSEMBLY_ID = '{Assembly_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Equipment_Id = EquipmentId,Assembly_id =AssemblyId,quote_revision_record_id=quote_revision_record_id ))
        if PreventiveMaintainenceobj is not None:
            FifthLable = "Events"
            FifthValue = "All"
        PMEvents = "False"
    elif ObjName == "SAQSCA":
        #A055S000P01-3208 start
        Trace.Write(1244)		
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
    elif TopSuperParentParam == "Product Offerings" and (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Fab Value Drivers" or subTabName == "Fab Cost and Value Drivers" or subTabName == "Service Fab Value Drivers" or subTabName == "Service Cost and Value Drivers" or subTabName == "Customer Value Drivers" or subTabName == "Product Value Drivers") and current_prod !='SYSTEM ADMIN' and CurrentTab == 'Contracts':
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from CTCTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
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
        FifthLable = ""
        FifthValue = ""
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
    
    elif TopSuperParentParam == "Comprehensive Services" or TopSuperParentParam == "Add-On Products":	
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
        elif(str(ObjName)=="SAQRGG" and (subTabName == 'Details' or subTabName == 'Events')):
            PrimaryLable = "Product Offering ID"
            PrimaryValue = str(TreeSuperParentParam)
            SecondLable = "Product Offering Description"
            SecondValue = desc
            ThirdLable = "Greenbook"
            ThirdValue = str(TreeParentParam)
            FourthLable = "Got Code"
            FourthValue = str(TreeParam)
        elif((subTabName == "Details" or subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Greenbook Fab Value Drivers" or subTabName == "Greenbook Cost and Value Drivers" or subTabName == "Credits") and subTabName != "Assembly Details" or subTabName == "Customer Value Drivers" or subTabName == "Product Value Drivers"):
            if subTabName =='Entitlements' and str(ObjName) == "SAQSAO" and TreeParam == "Add-On Products" :
                Trace.Write("addon entitlement")
                get_addon_service_desc = Sql.GetFirst("SELECT * FROM SAQSGB (NOLOCK) WHERE QUOTE_SERVICE_GREENBOOK_RECORD_ID  = '{}'".format(CurrentRecordId))
                if get_addon_service_desc:
                    PrimaryLable = "Product Offering ID"
                    PrimaryValue = get_addon_service_desc.SERVICE_ID
                    SecondLable = "Product Offering Description"
                    SecondValue = get_addon_service_desc.SERVICE_DESCRIPTION 
            else:
                Trace.Write('addon enti11')
                addon_prd_rec_id = Product.GetGlobal('addon_prd_rec_id')
                if (TreeTopSuperParentParam == "Comprehensive Services" or TreeTopSuperParentParam == "Product Offerings"  )and TreeParam != "Add-On Products" and (subTabName == "Details" or subTabName == "Events" ):
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
        #getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        Trace.Write("1356")
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
        #getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        Trace.Write("1359")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeTopSuperParentParam)
        #SecondLable = "Fab Location ID"
        #SecondValue = str(TreeParentParam)
        SecondLable = "Greenbook"
        SecondValue = str(TreeParam)
    elif TreeTopSuperParentParam == "Complementary Products"  and (subTabName == "Details"):		
        #getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        Trace.Write("1359===========")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeSuperParentParam)
        SecondLable = ""
        SecondValue = ""
        #ThirdLable = ""
        #ThirdValue = ""	

    elif (TreeSuperParentParam == "Sending Equipment" or TreeSuperTopParentParam =="Complementary Products" and (subTabName == "Equipment Fab Value Drivers" or subTabName == "Equipment Entitlements" or subTabName == "Equipment Cost and Value Drivers" or subTabName == "Equipment Details" or subTabName == "Customer Value Drivers" or subTabName == "Product Value Drivers")):		
        #getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        if str(subTabName) != "Equipment":
            Trace.Write("1358")
            Trace.Write(subTabName)
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
            
            '''try:
                FifthLable = ListKey[2]
                FifthValue = ListVal[2]
            except:
                FifthLable = ""
                FifthValue = ""
            Trace.Write("4 th "+str(FourthLable) + "4 th val" +str(FourthValue) + " 5 th " +str(FifthLable) + "5 th val" +str(FifthValue))'''
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
            
            '''try:
                FifthLable = ListKey[2]
                FifthValue = ListVal[2]
            except:
                FifthLable = ""
                FifthValue = ""
            Trace.Write("4 th "+str(FourthLable) + "4 th val" +str(FourthValue) + " 5 th " +str(FifthLable) + "5 th val" +str(FifthValue))'''
            
    elif TreeSuperParentParam == "Fab Locations" and ObjName == 'CTCFEQ':
        getFab = Sql.GetFirst("select FABLOCATION_NAME from CTCFBL(nolock) where FABLOCATION_ID = '"+str(TreeParentParam)+"'")        
        PrimaryLable = "Fab Location ID"
        PrimaryValue = str(TreeParentParam)
        SecondLable = "Fab Location Name"
        SecondValue = getFab.FABLOCATION_NAME
        ThirdLable = "Greenbook"
        ThirdValue = str(TreeParam)
        FourthLable = "Equipment"
        FourthValue = "All"
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
    elif TreeParentParam == "Fab Locations" and ObjName == "CTCFEQ":
        getFab = Sql.GetFirst("select FABLOCATION_NAME from CTCFBL(nolock) where FABLOCATION_ID = '"+str(TreeParam)+"'")        
        PrimaryLable = "Fab Location ID"
        PrimaryValue = str(TreeParam)
        SecondLable = "Fab Location Name"
        SecondValue = getFab.FABLOCATION_NAME
        ThirdLable = "Greenbooks"
        ThirdValue = "All"
        FourthLable = "Equipment"
        FourthValue = "All"
    # if TreeParentParam == 'Quote Items' and ObjName == 'SAQITM' and subTabName == 'Details':	
    #     Trace.Write("1207")	
    #     PrimaryLable = ListKey[0]
    #     PrimaryValue = PrimaryValue
    #     SecondLable = ListKey[1]
    #     SecondValue = ListVal[1]
    #     ThirdLable = ListKey[2]
    #     ThirdValue = ListVal[2]
    #     FourthValue = ListKey[4]
    #     FourthValue = ListVal[4]
    #     getQuotetype = ""
    #     getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()		
    #     if str(getQuotetype) == "ZTBC - TOOL BASED":
    #         FourthLable = ""                        
    #         FourthValue = ""
    #     else:
    #         FourthLable = ListKey[3]
    #         FourthValue = "RVCEU1" if ListVal[3]=="" else ListVal[3]
    # if TreeParentParam == 'Quote Items' and ObjName == 'SAQITM' and subTabName == 'Spare Parts':
    #     PrimaryLable = ""
    #     PrimaryValue = ""       
    if TreeParam == 'Quote Items' and (subTabName == "Summary" or subTabName == "Offerings" or subTabName == "Items" or subTabName == "Annualized Items" or subTabName == "Entitlement Cost/price"):
        Trace.Write("quoteitemshp===")
        get_quote_details = Sql.GetFirst("select CREDIT_INGL_CURR,NET_VALUE_INGL_CURR,DISCOUNT_AMOUNT_INGL_CURR,SALES_PRICE_INGL_CURR,DISCOUNT_PERCENT,SLSDIS_PRICE_INGL_CURR,TAX_AMOUNT_INGL_CURR,TOTAL_AMOUNT_INGL_CURR,GLOBAL_CURRENCY_RECORD_ID,GLOBAL_CURRENCY from SAQTRV (nolock) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
        # currency = Sql.GetFirst("SELECT GLOBAL_CURRENCY FROM SAQTRV (NOLOCK) WHERE QTEREV_RECORD_ID = '{}'".format(quote_revision_record_id))
        curr = get_quote_details.GLOBAL_CURRENCY
        Total=(get_quote_details.TOTAL_AMOUNT_INGL_CURR)
        get_service_id=Sql.GetFirst("SELECT SERVICE_ID FROM SAQTSV WHERE  QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
        #if get_service_id:
        #    if get_service_id.SERVICE_ID in('Z0110','Z0108'):
        #        Total=(get_quote_details.NET_VALUE_INGL_CURR)
        get_rounding_place = Sql.GetFirst("SELECT * FROM PRCURR WHERE CURRENCY_RECORD_ID = '{}' ".format(get_quote_details.GLOBAL_CURRENCY_RECORD_ID))
        decimal_format = "{:,." + str(get_rounding_place.DISPLAY_DECIMAL_PLACES) + "f}"
        if subTabName == "Summary":
            Trace.Write("summar_SHP")
            PrimaryLable = "Total Excluding Tax/VAT"
            #PrimaryValue = '0.00'+" "+curr
            PrimaryValue = decimal_format.format(float(get_quote_details.NET_VALUE_INGL_CURR))+" "+ curr if str(get_quote_details.NET_VALUE_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
            #PrimaryValue = str("%.2f" % round(float(get_quote_details.TOTAL_AMOUNT_INGL_CURR),2))+curr if str(get_quote_details.TOTAL_AMOUNT_INGL_CURR) != '' else '0.00'+" "+curr
            SecondLable = "Tax/VAT"
            SecondValue = decimal_format.format(float(get_quote_details.TAX_AMOUNT_INGL_CURR))+" "+ curr if str(get_quote_details.TAX_AMOUNT_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
            
            #SecondValue = str("%.2f" % round(float(get_quote_details.TAX_AMOUNT_INGL_CURR),2))+" "+curr if str(get_quote_details.TAX_AMOUNT_INGL_CURR) != '' else '0.00'+" "+curr
            ThirdLable = "Total Amount Including Tax/VAT"
            #ThirdValue = str("%.2f" % round(float(Total),2))+curr if str(Total) != '' else '0.00'+" "+curr
            ThirdValue = decimal_format.format(float(Total))+" "+ curr if str(Total) != '' else decimal_format.format(float("0.00"))+" "+curr
        elif get_quote_details:
            Trace.Write("subTabName_CHK "+str(subTabName))
            if subTabName == "Items":
                #saqrit_details = Sql.GetFirst("SELECT SUM(TOTAL_AMOUNT_INGL_CURR) AS TOTAL_AMOUNT_INGL_CURR, SUM(TAX_AMOUNT_INGL_CURR) AS TAX_AMOUNT_INGL_CURR, SUM(TOTAL_AMOUNT_INGL_CURR) AS TOTAL_AMOUNT_INGL_CURR FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                PrimaryLable = "Total Excluding Tax/VAT"
                PrimaryValue = decimal_format.format(float("0.00"))+" "+curr
                SecondLable = "Tax/VAT"
                #SecondValue = str("%.2f" % round(float(get_quote_details.TAX_AMOUNT_INGL_CURR),2))+" "+curr if str(get_quote_details.TAX_AMOUNT_INGL_CURR) != '' else '0.00'+" "+curr
                SecondValue = decimal_format.format(float(get_quote_details.TAX_AMOUNT_INGL_CURR))+" "+ curr if str(get_quote_details.TAX_AMOUNT_INGL_CURR) != '' else decimal_format.format(float("0.00"))+" "+curr
                ThirdLable = "Total Est Net Value"
                ThirdValue = decimal_format.format(float("0.00"))+" "+curr
                FourthLable = "Total Net Value"
                FourthValue =decimal_format.format(float("0.00"))+" "+curr
                FifthLable = "Total Margin"
                FifthValue = decimal_format.format(float("0.00"))+" "+curr
            elif subTabName == "Offerings":
                saqris_details = Sql.GetFirst("SELECT SUM(ESTIMATED_VALUE) AS ESTIMATED_VALUE, SUM(NET_VALUE_INGL_CURR) AS NET_VALUE_INGL_CURR FROM SAQRIS (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                PrimaryLable = "Total Tax/VAT/GST"
                PrimaryValue = decimal_format.format(float("0.00"))+" "+curr
                SecondLable = "Total Est Net Val"
                # SecondValue = str("%.2f" % round(float(get_quote_details.TOTAL_AMOUNT_INGL_CURR),2))+" "+curr if str(get_quote_details.TOTAL_AMOUNT_INGL_CURR) != '' else '0.00'+" "+curr
                #SecondValue = str("%.2f" % round(float(saqris_details.ESTIMATED_VALUE),2))+" "+curr if str(saqris_details.ESTIMATED_VALUE) != '' else '0.00'+" "+curr
                SecondValue = decimal_format.format(float(saqris_details.ESTIMATED_VALUE))+" "+ curr if str(saqris_details.ESTIMATED_VALUE) != '' else decimal_format.format(float("0.00"))+" "+curr
                ThirdLable = "Total Net Val"
                ThirdValue = decimal_format.format(float("0.00"))+" "+curr
                FourthLable = "Total  Amt"
                FourthValue = decimal_format.format(float("0.00"))+" "+curr
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
    
    elif TreeParam == 'Quote Items' and (subTabName == "Details" or subTabName == "Object List" or subTabName == "Product List" or subTabName == "Billing Plan" or subTabName == "Assortment Module"):
        item_detail = Sql.GetFirst(" SELECT * FROM SAQRIT (NOLOCK) WHERE QUOTE_REVISION_CONTRACT_ITEM_ID ='"+str(CurrentRecordId)+"'")
        if item_detail:
            #if subTabName == "Details" or subTabName == "Entitlements" or subTabName == "Object List" or subTabName == "Product List" or subTabName == "Billing Plan" or subTabName == "Assortment Module" and ObjName == "SAQRIT":
            if subTabName == "Details" or subTabName == "Object List" or subTabName == "Product List" or subTabName == "Billing Plan" or subTabName == "Assortment Module":
                Trace.Write("SAQRIT-DETAIL222===")
                valid_from = str(item_detail.CONTRACT_VALID_FROM).split(" ")[0]
                Trace.Write("valid_from===="+str(valid_from))
                valid_date = str(item_detail.CONTRACT_VALID_TO).split(" ")[0]            
                #if item_detail:
                PrimaryLable = "Product Offering Id"
                PrimaryValue =  item_detail.SERVICE_ID
                SecondLable = "Quantity"
                SecondValue = item_detail.QUANTITY
                ThirdLable = "Contract Start Date"
                ThirdValue = valid_from
                FourthLable = "Contract End Date"
                FourthValue = valid_date

            elif subTabName == "Entitlements":
                Trace.Write("entitlements===")
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
        # if subTabName == "Entitlements" or subTabName == "Object List" or subTabName == "Product List" or subTabName == "Billing Plan" or subTabName == "Assortment Module":
        #     Trace.Write("SAQRIT-DETAIL333===")            
        #     if item_detail:
        #         valid_from = str(item_detail.CONTRACT_VALID_FROM).split(" ")[0]
        #         valid_date = str(item_detail.CONTRACT_VALID_TO).split(" ")[0]
        #         PrimaryLable = "Line"
        #         PrimaryValue =  item_detail.LINE
        #         SecondLable = "Product Offering Id"
        #         SecondValue = item_detail.SERVICE_ID
        #         # ThirdLable = "Fab Location Id"
        #         # ThirdValue = item_detail.FABLOCATION_ID
        #         # FourthLable = "Fab Location Name"
        #         # FourthValue = item_detail.FABLOCATION_NAME
        #         FifthLable = "Start Date"
        #         FifthValue = valid_from
        #         SixthLable = "End Date"
        #         SixthValue =  valid_date        
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
    elif TreeParentParam == 'Cart Items' and subTabName == 'Equipment':
        TreeParam = TreeParam.split('-')
        PrimaryLable = "Line"
        PrimaryValue = TreeParam[0].strip()
        SecondLable = "Product Offering ID"
        SecondValue = TreeParam[1].strip()
        ThirdLable = "Greenbooks"
        ThirdValue = "All"
        FourthLable = "Equipment"
        FourthValue = "All"
    elif TreeParentParam == 'Cart Items' and (subTabName == 'Cart Item Fab Value Drivers' or subTabName == 'Cart Item Cost and Value Drivers'):
        TreeParam = TreeParam.split('-')
        PrimaryLable = "Line"
        PrimaryValue = TreeParam[0].strip()
        SecondLable = "Product Offering ID"
        SecondValue = TreeParam[1].strip()
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from CTCTSV(nolock) where SERVICE_ID = '"+str(SecondValue)+"'")
        ThirdLable = "Product Offering Description"
        ThirdValue = getService.SERVICE_DESCRIPTION
        FourthLable = "Greenbooks"
        FourthValue = "All"
        FifthLable = "Equipment"
        FifthValue = "All"
    elif TreeParentParam == 'Cart Items' and ObjName == 'CTCITM' and subTabName == 'Details':	
        PrimaryLable = ListKey[0]
        PrimaryValue = PrimaryValue
        SecondLable = ListKey[1]
        SecondValue = ListVal[1]
        ThirdLable = ListKey[2]
        ThirdValue = ListVal[2]
        FourthValue = ListKey[4]
        FourthValue = ListVal[4]
        
    # elif  TreeSuperParentParam == "Quote Items" and ObjName == "SAQICO" and TabName == "Quote" and str(TreeParam) != "":
    #     PrimaryLable = ListKey[0]
    #     PrimaryValue = PrimaryValue
    #     Trace.Write(str(ListKey)+"------459=--------------->"+str(ListVal))
    #     # Trace.Write("ListKey[4]-1->"+str(ListKey[2]))
    #     # Trace.Write("ListKey[4]-0->"+str(ListKey[0]))

    #     PrimaryLable = ListKey[0]
    #     PrimaryValue = PrimaryValue
    #     SecondLable = ListKey[1]
    #     SecondValue = ListVal[1]
    #     ThirdLable = ListKey[2]
    #     ThirdValue = ListVal[2]
    #     FourthLable = ListKey[3]
    #     FourthValue = ListVal[3]
    #     try:
    #         FifthLable = ListKey[4]
    #         FifthValue = ListVal[4]
    #         SixthLable =ListKey[5]
    #         SixthValue = ListVal[5]
    #     except:
    #         FifthLable = ""
    #         FifthValue = ""
    #         SixthLable = ""
    #         SixthValue = ""
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
        Trace.Write("@2221")
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
        Trace.Write("@2236")
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
    elif ObjName == "SAQRGG" and subTabName == "Events":
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
    elif ObjName in ("SAQSGB","SAQSCA") and TreeTopSuperParentParam == "Product Offerings" and (subTabName in("Assembly Details","Assembly Entitlements","Events")):
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
    #elif TreeSuperTopParentParam == "Product Offerings" and TreeTopSuperParentParam == "Complementary Products" and (TreeParentParam == "Receiving Equipment" or TreeParentParam == "Sending Equipment") and (ObjName == "SAQSSF" or ObjName == "SAQSSF"):
    #	getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
    #	PrimaryLable = "Product Offering ID"
    #	PrimaryValue = str(TreeSuperParentParam)
    #	SecondLable = "Product Offering Description"
    #	SecondValue = getService.SERVICE_DESCRIPTION
    #	ThirdLable = "Product Offering Type"
    #	ThirdValue = str(TreeTopSuperParentParam)
    #	FourthLable = "Fab Location ID"
    #	FourthValue = str(TreeParam)
    #	FifthLable = ""
    #	FifthValue = ""
    #	SixthLable = ""
    #	SixthValue = ""
    Trace.Write(str(ObjName)+str(subTabName)+str(PrimaryLable)+str(SecondLable)+str(ThirdLable)+str(FourthLable)+str(FifthLable)+str(SixthLable))            

    if str(Image) != "":
        sec_rel_sub_bnr += (
            '<div class="product_tab_icon"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="'
            + str(Image)
            + '"/></div>'
        )

    #if str(PrimaryLable) != "" and str(PrimaryValue) != "":
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
    #if str(SecondLable) != "" and str(SecondValue) != "":
    if str(SecondLable) != "":
        Trace.Write("SSLA"+str(SecondLable))
        Trace.Write("SSVAL"+str(SecondValue))
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
    #if str(ThirdLable) != "" and str(ThirdValue) != "":
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
            Trace.Write("Line no:1995")
            Trace.Write(sec_rel_sub_bnr)
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
            Trace.Write("Line no:1945")
            Trace.Write(sec_rel_sub_bnr)
    #if str(FourthLable) != "" and str(FourthValue) != "" and (ObjName != "SAQTMT") and str(TreeParam) != "Quote Preview":
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
    #if str(FifthLable) != "" and str(FifthValue) != "" and str(TreeParam) != "Quote Preview":
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
    #if str(SixthLable) != "" and str(SixthValue) != "" and (str(TreeParam) != "Quote Information" and str(TreeParam) != "Quote Preview"):
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
    #if str(SeventhLable) != "" and str(SeventhValue) != "" and (str(TreeParam) != "Quote Information" and str(TreeParam) != "Quote Preview"):
    if str(SeventhLable) != "" and (str(TreeParam) != "Quote Information" and str(TreeParam) != "Quote Preview"):    		
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
    '''if CurrentRecordId == "0512D225-C324-4C18-80D0-83BE5C8E9A0A":
        sec_rel_sub_bnr += (
            '<button id="ADDNEW__QUOTECHK onclick="cont_openaddnew(this,'
            ')" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD NEW</button>'
        )'''       
    if CurrentRecordId.startswith("SYOBJR", 0) == True:
        Trace.Write("CurrentRecordIdCurrentRecordIdCurrentRecordId" + str(CurrentRecordId))
        currecId = Sql.GetFirst(
            "select a.SAPCPQ_ATTRIBUTE_NAME,a.NAME,a.CAN_ADD,a.CAN_EDIT,a.CAN_DELETE,a.RELATED_LIST_SINGULAR_NAME,(b.SAPCPQ_ATTRIBUTE_NAME) as OBJ_REC_ID,(b.RECORD_ID) as SYOBJH_RECORD_ID from SYOBJR (nolock) a inner join SYOBJH (nolock) b on a.OBJ_REC_ID = b.RECORD_ID where a.SAPCPQ_ATTRIBUTE_NAME = '"
            + str(CurrentRecordId)
            + "' "
        )		
        # if CurrentRecordId == "SYOBJR-98799":
        #     get_quote_status = Sql.GetFirst("SELECT QUOTE_STATUS FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
        #     if str(get_quote_status.QUOTE_STATUS).upper() in  ["APPROVED","BOOKING SUBMITTED"]:			
        #         sec_rel_sub_bnr += (
        #             '<button class="btnconfig cust_def_btn" id="Generate_Documents" onclick="btn_banner_content(this)" style="display: block;">GENERATE DOCUMENTS</button>'
        #         )
        # elif str(TreeParam).upper() == "QUOTE INFORMATION" and subTabName == "Source Fab Location" and TabName == "Quote":
        #     sec_rel_sub_bnr += (
        #         '<button id="ADDNEW__SYOBJR_98857_SYOBJ_01033" onclick="cont_openaddnew(this, \'div_CTR_Source_Fab_Locations\')" class="btnconfig addNewRel HideAddNew">ADD NEW</button>'
        #     )
        # elif str(TreeParam).upper() == "QUOTE INFORMATION" and CurrentRecordId == "SYOBJR-98858":
        # 	sec_rel_sub_bnr += (
        # 				'<button id="ADDNEW__SYOBJR_98858_SYOBJ_01034" onclick="cont_openaddnew(this, \'div_CTR_Involved_Parties_Equipments\')" class="btnconfig addNewRel">ADD EQUIPMENT</button>'
        # 			)
        if currecId:			
            buttonid = str(currecId.SAPCPQ_ATTRIBUTE_NAME) + "_" + str(currecId.OBJ_REC_ID)
            buttonid = str(buttonid).replace("-", "_")
            SYOBJH_RECORD_ID = str(currecId.SYOBJH_RECORD_ID).replace("-", "_")			
            divid = str(currecId.NAME).replace(" ", "_")
            
            if str(currecId.CAN_ADD).upper() == "TRUE":				
                if CurrentRecordId == "SYOBJR-95800":
                    sec_rel_sub_bnr += (add_button)
                    # sec_rel_sub_bnr += (
                    #     '<button id="ADDNEW__' + str(buttonid) + '" onclick="cont_openaddnew(this,'
                    #     ')" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD MEMBERS</button>'
                    # )
                elif CurrentRecordId == "SYOBJR-95825":					
                    for btn in multi_buttons:
                        sec_rel_sub_bnr += (btn)
                elif TreeParam == "Billing" and ObjName == "SAQRIB":
                    Trace.Write("Billing")
                    for btn in multi_buttons:
                        sec_rel_sub_bnr += (btn)		

                elif CurrentRecordId == "SYOBJR-98789" and TreeParentParam != "Fab Locations":
                    Trace.Write("Comming Inside fab condition_J")
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    FabList = Sql.GetList(
                        "SELECT FAB_LOCATION_RECORD_ID FROM MAFBLC (NOLOCK) JOIN SAQTMT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND FAB_LOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' )".format(
                            contract_quote_record_id,contract_quote_record_id,quote_revision_record_id
                        )
                    )
                    if TreeParam == "Fab Locations" and subTabName == "Equipment":
                        Trace.Write("CHK_2")
                        Trace.Write("Fab node equipment add hide")
                        sec_rel_sub_bnr += ""
                    elif FabList is not None and len(FabList) >0:
                        Trace.Write("CHK_1")
                        #Product.Attributes.GetByName("BTN_SYACTI_QT_00011_ADDFAB").Allowed = True
                        ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
                        send_and_receive = Sql.GetList("SELECT CPQ_PARTNER_FUNCTION FROM SAQTIP (NOLOCK) WHERE CPQ_PARTNER_FUNCTION IN ('SENDING ACCOUNT','RECEIVING ACCOUNT') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(str(ContractRecordId),quote_revision_record_id))
                        sale_type = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                        if len(send_and_receive) == 0 and TreeParam == "Fab Locations":
                            # if sale_type.SALE_TYPE == "NEW":
                            for btn in multi_buttons:
                                if "ADD FAB" in btn:
                                    if quote_status.QUOTE_STATUS != 'APPROVED':
                                        sec_rel_sub_bnr += (str(btn))
                        else:
                            sec_rel_sub_bnr += ""
                        # sec_rel_sub_bnr += (
                        #     '<button id="ADDNEW__' + str(buttonid) + '" onclick="cont_openaddnew(this,'
                        #     ')" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD FAB</button>'
                        # )
                    # if TreeParam == "Customer Information":
                    # ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
                    # send_and_receive = Sql.GetList("SELECT CPQ_PARTNER_FUNCTION FROM SAQTIP (NOLOCK) WHERE CPQ_PARTNER_FUNCTION IN ('SENDING ACCOUNT','RECEIVING ACCOUNT') AND QUOTE_RECORD_ID = '{}'".format(str(ContractRecordId)))
                    # if len(send_and_receive) > 0 and TreeParam != 'Fab Locations':
                    #     sec_rel_sub_bnr += str(add_button)
                    # else:
                    #     sec_rel_sub_bnr += ""
                    elif TreeParam == "Fab Locations":
                        ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
                        send_and_receive = Sql.GetList("SELECT CPQ_PARTNER_FUNCTION FROM SAQTIP (NOLOCK) WHERE CPQ_PARTNER_FUNCTION IN ('SENDING ACCOUNT','RECEIVING ACCOUNT') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(str(ContractRecordId),quote_revision_record_id))
                        sale_type = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                        if len(send_and_receive) == 0 and TreeParam == "Fab Locations":
                            for btn in multi_buttons:
                                if "ADD FAB" in btn:
                                    sec_rel_sub_bnr += (str(btn))
                    else:
                        Trace.Write("CHK_3")
                        if CurrentRecordId == "SYOBJR-98789" and TreeParam == "Fab Locations":
                            Trace.Write("No Button are required!!!")
                            if quote_status.QUOTE_STATUS != 'APPROVED':
                                Trace.Write('add======')
                                sec_rel_sub_bnr += (str(add_button))
                        else:	
                            sec_rel_sub_bnr += (str(add_button))
                        # sec_rel_sub_bnr += (
                        #     '<button id="ADDNEW__' + str(buttonid) + '" onclick="cont_openaddnew(this,'
                        #     ')" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal" disabled>ADD FAB</button>'
                        # )
                
                elif CurrentRecordId == "SYOBJR-98788":
                    if quote_status.QUOTE_STATUS != 'APPROVED':
                        Trace.Write('add======')
                        if "ADD OFFERINGS" in str(add_button):
                            if str(TreeParam) == "Product Offerings":
                                sec_rel_sub_bnr += (str(add_button))
                        else:
                            sec_rel_sub_bnr += (str(add_button))
                    # sec_rel_sub_bnr += (
                    #     '<button id="ADDNEW__' + str(buttonid) + '" onclick="cont_openaddnew(this,'
                    #     ')" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD OFFERINGS</button>'
                    # )
                # elif CurrentRecordId == "SYOBJR-98859":
                # 	On_prod = Sql.GetList("SELECT * FROM SAQSCO (NOLOCK) WHERE SERVICE_ID = '"+str(TreeParentParam)+"' AND QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' ")
                # 	if On_prod:
                # 		sec_rel_sub_bnr += (str(add_button))
                        # sec_rel_sub_bnr += (
                        #     '<button id="ADDNEW__' + str(buttonid) + '" onclick="cont_openaddnew(this,'
                        #     ')" class="btnconfig" data-target="" data-toggle="modal">INCLUDE ADD-ON PRODUCTS</button>'
                        # )
                    # else:
                    # 	Trace.Write("check for Add On_Prod")
                    # sec_rel_sub_bnr += (
                    #         '<button id="ADDNEW__' + str(buttonid) + '" onclick="cont_openaddnew(this,'
                    #         ')" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">INCLUDE ADD-ON PRODUCTS</button>'
                    #     )     
                
                

                elif CurrentRecordId == "SYOBJR-98800" and TreeParam != "Fab Locations":
                    Trace.Write('98800=====')
                    sale_type = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                    if sale_type == 'TOOL RELOCATION':
                        sec_rel_sub_bnr += ''
                    else:
                        if quote_status.QUOTE_STATUS != 'APPROVED':
                            sec_rel_sub_bnr += (str(add_button))
                        
                        # sec_rel_sub_bnr += (
                        #     '<button id="ADDNEW__' + str(buttonid) + '" onclick="cont_openaddnew(this,'
                        #     ')" class="btnconfig" data-target="" data-toggle="modal">ADD FROM LIST</button>'
                        # )
                # elif CurrentRecordId == "SYOBJR-98800":
                #     sec_rel_sub_bnr += (
                #         '<button id="ADDNEW__' + str(buttonid) + '" onclick="cont_openaddnew(this,'
                #         ')" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD FROM LIST</button>'
                #     )           
                # 
                elif CurrentRecordId == "SYOBJR-00010" and TreeParam != "Fab Locations" and subTabName != "Items":
                    Trace.Write("Summary Refresh button condition")
                    sec_rel_sub_bnr += (str(add_button))
                else:	
                    Trace.Write('elseeee')

                    
                    if TreeParam == "Fab Locations":
                        GetToolReloc = Sql.GetList("SELECT CpqTableEntryId FROM SAQTIP WHERE (CPQ_PARTNER_FUNCTION = 'RECEIVING ACCOUNT' OR CPQ_PARTNER_FUNCTION = 'SENDING ACCOUNT') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
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
                        Trace.Write("sales===")
                        contract_manager_info = Sql.GetFirst("SELECT  * from SAQDLT where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND C4C_PARTNERFUNCTION_ID = 'CONTRACT MANAGER' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))                       
                        if contract_manager_info:
                            Trace.Write("sales==btn===")
                            sec_rel_sub_bnr += ""
                        else:
                            Trace.Write("sales==btn===>>")
                            sec_rel_sub_bnr += (str(add_button))

                    # Removed Add New Button suppress functionality
                    
                    # elif TreeParam == "Customer Information":
                    #     send_receive =[]
                    #     ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
                    #     send_and_receive = Sql.GetList("SELECT CPQ_PARTNER_FUNCTION FROM SAQTIP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}'".format(str(ContractRecordId)))
                    #     for acnt in send_and_receive:
                    #         send_receive.append(acnt.CPQ_PARTNER_FUNCTION)
                    #     Trace.Write("send_receive_J"+str(send_receive))
                    #     if ("SENDING ACCOUNT" in send_receive and "RECEIVING ACCOUNT" in send_receive):
                    #         sec_rel_sub_bnr += ""
                    #     else:
                    #         sec_rel_sub_bnr += (str(add_button))
                    else:
                        Trace.Write('elseeee11')
                        if str(TabName) == 'Quotes':
                            if quote_status.QUOTE_STATUS != 'APPROVED' and subTabName != 'Items':
                                sec_rel_sub_bnr += (str(add_button))
                        else:
                            Trace.Write("add###---")                                        
                            sec_rel_sub_bnr += (str(add_button))
                    # else:
                    # 	Trace.Write("12345---- "+str(add_button))	
                    # 	sec_rel_sub_bnr += (str(add_button))
                    # sec_rel_sub_bnr += (
                    #     '<button id="ADDNEW__'
                    #     + str(buttonid)
                    #     + '" onclick="cont_openaddnew(this, \'div_CTR_'
                    #     + str(divid)
                    #     + '\')" class="btnconfig addNewRel HideAddNew">ADD NEW</button>'
                    # )
                    # sec_rel_sub_bnr += (
                    # 	'<button id="ADDNEW__'
                    # 	+ str(buttonid)
                    # 	+ '" onclick="cont_deleteall(this, \'div_CTR_'
                    # 	+ str(divid)
                    # 	+ '\')" style="display: none;" class="btnconfig deleteRel HideDelete">DELETE</button>'
                    # ) 
                
            Trace.Write("TabName"+str(TabName))
            if (str(TabName) == "Quotes" or str(TabName == "Quote")): 
                getQuotetype = ""
                #getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()
                try:
                    ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
                except:
                    ContractRecordId = ''		
                getsaletypeloc = Sql.GetFirst("select SALE_TYPE,QUOTE_TYPE from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(ContractRecordId,quote_revision_record_id))				
                if getsaletypeloc:
                    # dynamic_Button = Sql.GetList("SELECT HTML_CONTENT FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '{}'".format(page_details.RECORD_ID))
                    Trace.Write("multi_buttons--2754--"+str(multi_buttons))
                    if len(multi_buttons)>0:						
                        # if TreeParam == "Quote Items" and getsaletypeloc.QUOTE_TYPE =="ZTBC - TOOL BASED" and getsaletypeloc.SALE_TYPE != "TOOL RELOCATION":
                        #     # Appending Price button in Quote Items Node
                        #     Trace.Write("inside---> quote item"+str(multi_buttons))
                        #     for btn in multi_buttons:
                        #         if "PRICE" in btn:
                        #             sec_rel_sub_bnr += (btn)
                        #     # Appending Price button in Quote Items Node

                        #     sec_rel_sub_bnr += (
                        #         '<button id="CALCULATE_QItems" onclick="calculate_QItems(this)" class="btnconfig">PRICE</button>'
                        #     )    
                        # if TreeParam == "Quote Items":
                        #     # Appending REFRESH button in Quote Items Node
                        #     for btn in multi_buttons:
                        #         if "REFRESH" in btn:
                        #             sec_rel_sub_bnr += (btn)
                        # Appending REFRESH button in Quote Items Node

                        # sec_rel_sub_bnr += (
                        #         '<button id="REFRESH_MATRIX" onclick="refresh_billingmatrix(this)"  class="btnconfig">REFRESH</button>'
                        #     )  
                        if TreeParam.startswith("Sending Account"):
                            Trace.Write("Testing_EQUP_button"+str(multi_buttons)+" "+str(add_button))
                            for btn in multi_buttons:
                                if getsaletypeloc.SALE_TYPE == "TOOL RELOCATION":
                                    if "ADD FROM LIST" in btn:
                                        sec_rel_sub_bnr += ""
                                else:
                                    if "ADD UNMAPPED EQUIPMENTS" in btn:
                                        Trace.Write('add_button->unmapped--'+str(add_button))
                                        sec_rel_sub_bnr += str(btn)
                        elif TreeParam == "Delivery Schedule":
                            Trace.Write("2836--multi_buttons---2830-----"+str(multi_buttons))
                            for btn in multi_buttons:
                                sec_rel_sub_bnr += (btn)
                            Trace.Write(sec_rel_sub_bnr)
        elif TreeParam == "Billing":
            Trace.Write("BM 1740")
            for btn in multi_buttons:
                sec_rel_sub_bnr += (btn)
            Trace.Write(sec_rel_sub_bnr)
        elif TreeParam == "Delivery Schedule":
            Trace.Write("2836--multi_buttons------"+str(multi_buttons))
            for btn in multi_buttons:
                sec_rel_sub_bnr += (btn)
            Trace.Write(sec_rel_sub_bnr)
        

        

        

    elif TreeParam == 'Approvals' and (TabName == "Quotes" or TabName == "Quote"):
        quote_status = Sql.GetFirst("SELECT REVISION_STATUS,QUOTE_ID FROM SAQTRV WHERE QUOTE_REVISION_RECORD_ID = '{}'".format(Quote.GetGlobal("quote_revision_record_id")))
        #Trace.Write("quote status------->"+str(quote_status.QUOTE_STATUS))
        Quote_Owner = Sql.GetFirst("SELECT CPQTABLEENTRYADDEDBY FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
        # Quote_item_obj = Sql.GetFirst("SELECT QUOTE_ITEM_RECORD_ID FROM SAQITM WHERE QUOTE_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id")))
        User_Name = User.UserName 
        
        Submit_approval = ''
        if Quote_Owner.CPQTABLEENTRYADDEDBY == User_Name:
            Submit_approval = "True"
        else:
            Submit_approval = "False"
        get_quote_status = Sql.GetList("SELECT CpqTableEntryId FROM ACAPTX (NOLOCK) WHERE APPROVAL_ID LIKE '%{}%'".format(quote_status.QUOTE_ID))
        if not get_quote_status and str(quote_status.REVISION_STATUS) != 'APPROVED':
            sec_rel_sub_bnr += (
                    '<button class="btnconfig cust_def_btn" id="APPROVE" onclick="quote_approval(this.id)">APPROVE</button>'
                )
        Trace.Write("get_quote_status"+str(get_quote_status))
        Trace.Write("QUOTE_STATUS"+str(quote_status.REVISION_STATUS))
        Trace.Write("Submit_approval"+str(Submit_approval))
        # Trace.Write("Quote_item_obj"+str(Quote_item_obj))
        
        if get_quote_status and (str(quote_status.REVISION_STATUS) == 'PREPARING REVISION' or str(quote_status.REVISION_STATUS) == 'NEW REVISION' or str(quote_status.REVISION_STATUS) == 'RECALLED') and Submit_approval == "True":
            Trace.Write("submit for approval")
            GetSelfAppr = Sql.GetFirst("SELECT CpqTableEntryId FROM ACAPTX (NOLOCK) WHERE APRTRXOBJ_ID = '{}' AND APRCHN_ID = 'SELFAPPR'".format(quote_status.QUOTE_ID))
            if GetSelfAppr is not None:
                sec_rel_sub_bnr += ""
            else:
                sec_rel_sub_bnr += (
                    '<button class="btnconfig cust_def_btn submitbutton" data-target="#SUBMIT_MODAL_SECTION" data-toggle="modal" id="submit_for_approval" onclick="submit_comment()">SUBMIT FOR APPROVAL</button>'
                    )
        # else:
        # 	Trace.Write("elseeee")
    elif TreeParam == "Quote Documents":
        Trace.Write("Qdd----")
        #for btn in multi_buttons:
        sec_rel_sub_bnr += (add_button)
        Trace.Write("Qddd----"+str(sec_rel_sub_bnr))    
    Trace.Write("tabNameeee"+str(TabName))
    Trace.Write("sec_rel_sub_bnr--2678-->"+str(sec_rel_sub_bnr))
    # Added to update configure status in work flow status bar - start
    # if (str(TabName) == "Quotes" or str(TabName) == "Quote") and current_prod == "Sales":
    #     Trace.Write('sales11=======')
    #     getsalesorg_ifo = Sql.GetFirst("SELECT SALESORG_ID from SAQTRV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
    #     getfab_info = Sql.GetFirst("SELECT FABLOCATION_NAME from SAQSFB where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
    #     get_service_ifo = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as SERVICE_ID from SAQTSV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
    #     get_equip_details = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as SERVICE_ID from SAQSCO where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))

    #     # item_covered_obj = Sql.GetFirst("SELECT COUNT(STATUS) AS STATUS FROM SAQICO WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND STATUS NOT IN ('ACQUIRED')".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
    #     #for status in item_covered_obj:
    #     price_preview_status = []
    #     item_covered_obj = Sql.GetList("SELECT DISTINCT STATUS FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
    #     if item_covered_obj:
    #         for status in item_covered_obj:
    #             price_preview_status.append(status.STATUS)
    #         Trace.Write("price_preview_status_CHK"+str(price_preview_status))
    #         if len(price_preview_status) > 1:
    #             price_bar = "acquired_status"
    #         elif 'ACQUIRED' in price_preview_status:
    #             price_bar = "not_acquired_status"
    #         else:
    #             price_bar = "acquired_status"
    #     else:
    #         Trace.Write("NO Quote Items")
    #         price_bar = "no_quote_items"
        # if item_covered_obj.STATUS > 0:
        #     price_bar = "acquired_status"
        #     Trace.Write("config status==="+str(price_bar))
        # else:
        #     price_bar = "not_acquired_status"
        #     Trace.Write("config status111==="+str(price_bar))                    
        # if getsalesorg_ifo and getfab_info:
        #     Trace.Write('salesorg--present---')
        #     if get_service_ifo.SERVICE_ID == get_equip_details.SERVICE_ID:
                # get_quote_details = Sql.GetFirst("SELECT  SERVICE_ID from SAQITM where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                # if get_quote_details:
                #     get_quote = Quote.GetGlobal("contract_quote_record_id")
                #     Trace.Write('button process--')
                #     buttonvisibility = "Show_button"   
                # else:
                # Trace.Write('No button-2454-')
                # buttonvisibility = "Hide_button"
            # elif TreeParam == "Approvals" and CurrentTabName == 'Quotes':
            # 	Trace.Write("SUBMIT FOR APP Button")
            # 	sec_rel_sub_bnr = add_button
        #     else:
        #         Trace.Write('No button--1')
        #         buttonvisibility = "Hide_button"
        # else:
        #     Trace.Write('No button--2')
        #     buttonvisibility = "Hide_button"
    # Added to update configure status in work flow status bar - end        
    

    if subTabName == 'Summary' and TreeParam == "Quote Items" and (str(TabName) == "Quotes" or str(TabName) == "Quote") and current_prod == "Sales":
        Trace.Write("Offering"+str(TabName))
        getQuotetype = ""
        #getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()
        ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
        getsaletypeloc = Sql.GetFirst("select SALE_TYPE,QUOTE_TYPE from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(ContractRecordId,quote_revision_record_id))				
        if getsaletypeloc:
            # dynamic_Button = Sql.GetList("SELECT HTML_CONTENT FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '{}'".format(page_details.RECORD_ID))
            Trace.Write("multi_buttons--2917---"+str(len(multi_buttons)))
            buttonvisibility = ''
            if len(multi_buttons)>0:						
                if TreeParam == "Quote Items":
                    # Appending Price button in Quote Items Node
                    Trace.Write("inside---> quote item")
                    for btn in multi_buttons:
                        Trace.Write("btn---12"+str(btn))
                        # if "PRICE" in btn:
                        fts_scenario_check = Sql.GetList("SELECT CpqTableEntryId FROM SAQTIP (NOLOCK) WHERE CPQ_PARTNER_FUNCTION IN ('SENDING ACCOUNT','RECEIVING ACCOUNT') AND QUOTE_RECORD_ID = '"+str(ContractRecordId)+"'")
                        Trace.Write('2409----'+str(TreeParam))
                        Trace.Write("len_CHK_J "+str(len(fts_scenario_check)))
                        #A055S000P01-7512 Start Enable/Disable the PRICE button in Quote items based on Required fields validation
                        if str(TreeParam) == "Quote Items":
                            getsalesorg_ifo = Sql.GetFirst("SELECT SALESORG_ID from SAQTRV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                            getfab_info = Sql.GetFirst("SELECT FABLOCATION_NAME from SAQSFB where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                            get_service_ifo = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as SERVICE_ID from SAQTSV where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                            get_equip_details = Sql.GetFirst("SELECT COUNT(DISTINCT SERVICE_ID) as SERVICE_ID from SAQSCO where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                            if getsalesorg_ifo and getfab_info:
                                Trace.Write('salesorg--present---')
                                if get_service_ifo.SERVICE_ID == get_equip_details.SERVICE_ID:
                                    # get_quote_details = Sql.GetFirst("SELECT  SERVICE_ID from SAQITM where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' ".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                                    # if get_quote_details:
                                    #     get_quote = Quote.GetGlobal("contract_quote_record_id")
                                    #     Trace.Write('button process--')
                                    #     buttonvisibility = "Show_button"
                                    #     Quote.SetGlobal('Show_button','Show_button')
                                    # else:
                                    Trace.Write('No button-2454-')
                                    buttonvisibility = "Hide_button"
                                else:
                                    Trace.Write('No button--')
                                    buttonvisibility = "Hide_button"
                            else:
                                Trace.Write('No button--')
                                buttonvisibility = "Hide_button"
                        else:
                            Trace.Write('No button--')
                            buttonvisibility = "Hide_button"
                        #A055S000P01-7512 end Enable/Disable the PRICE button in Quote items based on Required fields validation
                        if len(fts_scenario_check) == 2:
                            Trace.Write("hide PRICING for fts--2411--")
                        #    if 'UPDATE LINES' in btn:

                        #        if quote_status.QUOTE_STATUS != 'APPROVED':
                        #            sec_rel_sub_bnr += (btn)
                            
                        else:
                            Trace.Write("hide PRICING for fts")
                            if quote_status.QUOTE_STATUS != 'APPROVED':
                                Trace.Write(str(buttonvisibility)+'---2469--btn----'+str(btn))
                                # if buttonvisibility == "Hide_button" and 'UPDATE PRICING' in btn:
                                # 	Trace.Write('---2469--btn----'+str(btn))
                                # 	btn += '<button id="CALCULATE_QItems"  style = "display:none;" onclick="calculate_QItems(this)" class="btnconfig" data-target="" data-toggle="modal">UPDATE PRICING</button>'
                                # 	sec_rel_sub_bnr += (btn)
                                # else:
                                    #btn = '<button id="CALCULATE_QItems"  onclick="calculate_QItems(this)" class="btnconfig" data-target="" data-toggle="modal">UPDATE PRICING</button>'
                                sec_rel_sub_bnr += (btn)   
                if TreeParam == "Quote Items":
                    # Appending REFRESH button in Quote Items Node
                    for btn in multi_buttons:
                        if "REFRESH" in btn:
                            if quote_status.QUOTE_STATUS != 'APPROVED':
                                sec_rel_sub_bnr += (btn) 

    Trace.Write("subtaname"+str(subTabName))
    if subTabName == 'Involved Parties' and TreeParam == "Quote Information":
        Trace.Write("Involved Parties button")
        sec_rel_sub_bnr += (add_button)
    if TreeParam == "Billing" and subTabName =="Details" and ObjName == "SAQRIB":
    # 	Trace.Write("button")
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
        # sec_rel_sub_bnr += '<button class="btnconfig" name="SUBMIT FOR APPROVAL">SUBMIT FOR APPROVAL</button>'
        
        """ACAPTXStatus = Sql.GetFirst(
            " SELECT ACAPTX.* FROM ACAPMA (NOLOCK) INNER JOIN ACAPTX (NOLOCK) ON ACAPMA.APRCHNSTP_RECORD_ID "
            + " = ACAPTX.APRCHNSTP_RECORD_ID WHERE ACAPTX.APPROVAL_RECIPIENT_RECORD_ID  = '"
            + str(user_id)
            + "' AND APPROVAL_TRANSACTION_RECORD_ID = '"
            + str(CurrentRecordId)
            + "' AND APPROVALSTATUS = 'REQUESTED' AND APRSTAMAP_APPROVALSTATUS = 'REQUESTED' "
        )"""
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
            ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
            Quote_Owner = Sql.GetFirst("SELECT CPQTABLEENTRYADDEDBY FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(ContractRecordId)+  "' AND QTEREV_RECORD_ID = '"+str(quote_revision_record_id)+"' ")
            User_Name = User.UserName 
            
            recall_edit = ''
            if Quote_Owner.CPQTABLEENTRYADDEDBY == User_Name:
                recall_edit = "True"
            else:
                recall_edit = "False"
        
        if str(TreeParam).upper() == "QUOTE INFORMATION" and subTabName == "Involved Parties" and TabName == "Quotes":
            sec_rel_sub_bnr += (
                        '<button id="ADDNEW__SYOBJR_98798_7F4F4C8D_73C7_4779_9BE5_38C695" onclick="cont_openaddnew(this, \'div_CTR_Involved_Parties\')" class="btnconfig addNewRel HideAddNew">ADD NEW</button>'
                    )

        elif  (str(TreeParentParam).upper() == "FAB LOCATIONS" or str(TreeParam).upper() == "QUOTE INFORMATION" or str(TreeSuperParentParam).upper() == "FAB LOCATIONS" )  and TabName == "Quotes":
            
            sec_rel_sub_bnr += ('<button id="fablocate_save" onclick="fablocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fablocate_cancel" onclick="fablocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>'  )
        elif str(TreeParam) == "Quote Information" and TabName == "Quotes":
            Trace.Write("@@@2473")
            sec_rel_sub_bnr += ('<button id="fabcostlocate_save" onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fabcostlocate_cancel" onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>') 
        # elif str(TreeParentParam) == "Comprehensive Services" and TabName == "Quotes" and subTabName == "Parts List":
        #     Trace.Write("@@@2473")
        #     sec_rel_sub_bnr += ('<button id="delete_parts" onclick="bulk_del_yes()"  class="btnconfig" disabled = "">DELETE</button>') 
        elif  (str(TreeSuperParentParam).upper() == "PRODUCT OFFERINGS")  and TabName == "Quotes" and str(subTabName)!="Exclusions" and str(subTabName)!="New Parts" and str(subTabName)!="Inclusions" and str(subTabName)!= "New Parts Only":     
            sec_rel_sub_bnr += ('<button id="fabcostlocate_save" onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig hidebtn">SAVE</button><button id="fabcostlocate_cancel" onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig hidebtn">CANCEL</button>'  )    
            Trace.Write('### _ Multi_buttons'+str(type(multi_buttons)))
            if str(subTabName)=="Events" and revision_status.REVISION_STATUS != 'APPROVED':
                sec_rel_sub_bnr += str(add_button)
            elif str(subTabName) == "Spare Parts" and str(TreeParentParam)=="Complementary Products" and revision_status.REVISION_STATUS != 'APPROVED':
                if str(multi_buttons) != "":
                    Trace.Write('### _ 3094----Multi_buttons'+str(type(multi_buttons)))
                    for btn in multi_buttons:
                        Trace.Write('3095----')
                        dropdown_multi_btn_str += '<li>'+str(btn)+'</li>'
                        #sec_rel_sub_bnr += (btn)
                    dropdown_multi_btn_str += '''</ul></div></div>'''
                    Trace.Write('3095--dropdown_multi_btn_str--'+str(dropdown_multi_btn_str))
                    sec_rel_sub_bnr += (dropdown_multi_btn_str)
                    Trace.Write('3095--sec_rel_sub_bnr--'+str(sec_rel_sub_bnr))
                else:
                    sec_rel_sub_bnr += str(add_button)
            elif str(subTabName)=="Periods":
                sec_rel_sub_bnr += str(add_button)
        elif  (str(TreeSuperParentParam).upper() == "COMPREHENSIVE SERVICES")  and TabName == "Quotes" and str(subTabName)!="Exclusions" and str(subTabName)!="New Parts" and str(subTabName)!="Inclusions":
            sec_rel_sub_bnr += ('<button id="fabcostlocate_save" onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fabcostlocate_cancel" onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>'  )
            if str(subTabName)=="Events" and revision_status.REVISION_STATUS != 'APPROVED':
                sec_rel_sub_bnr += str(add_button)
        elif  (str(TreeTopSuperParentParam).upper() == "COMPREHENSIVE SERVICES")  and TabName == "Quotes" and (subTabName)!="Exclusions" and str(subTabName)!="New Parts" and str(subTabName)!="Inclusions":
            if str(subTabName)=="Events" and str(TreeSuperParentParam)!="Z0009":
                sec_rel_sub_bnr += ('<button id="ADDNEW__SYOBJR_00011_SYOBJ_00974" onclick="PM_FrequencyInlineEdit()" class="btnconfig" >INLINE EDIT</button>')
            elif 'Add-On Products' in str(TreeParam) and ("INCLUDE ADD-ON PRODUCTS" not in sec_rel_sub_bnr) and ("ADD CREDITS" not in sec_rel_sub_bnr):
                sec_rel_sub_bnr+= str(add_button)
            else:
                if str(subTabName)!="Exclusions" and str(subTabName)!="New Parts" and str(subTabName)!="Inclusions":
                    sec_rel_sub_bnr += ('<button id="fabcostlocate_save" onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fabcostlocate_cancel" onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>'  )
        # elif str(TreeParam) == "Quote Items" and TabName == "Quotes" and subTabName == "Summary":
        #     sec_rel_sub_bnr =''
        #     sec_rel_sub_bnr += ('<div class="product_tab_icon"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="/mt/appliedmaterials_tst/Additionalfiles/Secondary Icon.svg"/></div><div class="product_txt_div_child secondary_highlight" style="display: block;"><div class="product_txt_child"><abbr title="Quote Items">Quote Items</abbr></div><div class="product_txt_to_top_child"><abbr title="ALL">ALL</abbr></div></div><div class="segment_part_number_child secondary_highlight subellipsisdot" style="display: block;"><div class="segment_part_number_heading_child"><abbr title="Product Offering ID">Product Offering ID</abbr></div><div class="segment_part_number_text_child"><abbr title="ALL">ALL</abbr></div></div><button id="generate-line-items" onclick="generateLineItems()"  class="btnconfig"style="display: none;">UPDATE LINES</button>')
        elif str(TreeParam) == "Fab Locations" and TabName =="Quotes" and subTabName =="Fab Locations":
            sec_rel_sub_bnr += ""
        elif subTabName =="Delivery Schedule":
            Trace.Write('sec_rel_sub_bnr---3123---'+str(sec_rel_sub_bnr))
            sec_rel_sub_bnr += ('<button id="delivery_save" onclick="showSdeliverysave(this)" style= "display: none;" class="btnconfig" >SAVE</button><button id="delivery_cancel" onclick="showSdeliverycancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>')
        else:
            # Trace.Write("TreeParam-->"+str(TreeParam))
            # Trace.Write("subTabName-->"+str(subTabName))
            # Trace.Write("Multi_buttons--->"+str(multi_buttons))
            Trace.Write("Single_button--->"+str(sec_rel_sub_bnr))
            if len(multi_buttons)>0: ##adding dynamic buttons from SYPGAC if we have more than one button
                for btn in multi_buttons:
                    Trace.Write("btn---"+str(btn))
                    if ('SPLIT' in btn or 'EDIT' in btn) and subTabName =='Items':
                        if 'SPLIT' in btn:   
                            get_entitlement_xml =Sql.GetList("""select ENTITLEMENT_XML,SERVICE_ID from SAQTSE(NOLOCK) WHERE QUOTE_RECORD_ID = '{ContractRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(ContractRecordId =ContractRecordId,quote_revision_record_id =quote_revision_record_id))
                            if get_entitlement_xml:
                                for get_service in get_entitlement_xml:
                                    entitlement_service = get_service.ENTITLEMENT_XML
                                    quote_item_tag = re.compile(r'(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)')
                                    split_pattern = re.compile(r'<ENTITLEMENT_ID>AGS_[^>]*?_PQB_SPLQTE</ENTITLEMENT_ID>')
                                    split_value = re.compile(r'<ENTITLEMENT_DISPLAY_VALUE>Yes</ENTITLEMENT_DISPLAY_VALUE>')
                                    for m in re.finditer(quote_item_tag, entitlement_service):
                                        sub_string = m.group(1)
                                        split_1 =re.findall(split_pattern,sub_string)
                                        split_2 = re.findall(split_value,sub_string)
                                        if split_1 and split_2:
                                            Trace.Write("a"+str(get_service.SERVICE_ID))
                                            sec_rel_sub_bnr += (btn)
                                            break
                        if 'EDIT' in btn:
                            billing_variable_visible = Sql.GetFirst("""SELECT BILLING_TYPE FROM SAQRIT (NOLOCK) WHERE QUOTE_RECORD_ID = '{ContractRecordId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND BILLING_TYPE in ('VARIABLE','Variable')""".format(ContractRecordId =ContractRecordId,quote_revision_record_id =quote_revision_record_id))
                            if billing_variable_visible:
                                sec_rel_sub_bnr += (btn)
                    Trace.Write("sec_rel_sub_bnr==sec_rel_sub_bnr"+str(sec_rel_sub_bnr))
                    if quote_status.QUOTE_STATUS != 'APPROVED' and 'SPLIT' not in btn and 'EDIT' not in btn:
                        Trace.Write("555"+str(btn))
                        sec_rel_sub_bnr += (btn)
                    if (subTabName == 'Inclusions'  or subTabName == 'Exclusions' or subTabName == 'New Parts')  and quote_status.QUOTE_STATUS != 'APPROVED' and 'INLINE EDIT' in btn:
                        Trace.Write("btn-ifff--"+str(btn))
                        sec_rel_sub_bnr += (btn)
                        #sec_rel_sub_bnr += '<button id="partsListInlineEdit" onclick="PartsListInlineEdit()" class="btnconfig" >INLINE EDIT</button>'

                    # else: commented because of duplicate button
                    #     Trace.Write("btn222"+str(btn))
                    #     sec_rel_sub_bnr += (btn)
            elif str(add_button)!='' and str(add_button) not in sec_rel_sub_bnr :
                if subTabName == 'Exclusions' and TreeSuperParentParam == 'Product Offerings':
                    sec_rel_sub_bnr += ""
                else:
                    Trace.Write("btn===============") ##adding dynamic buttons from SYPGAC if we have only one button
                    sec_rel_sub_bnr+= str(add_button)
        Trace.Write('sec_rel_sub_bnr--2941--'+str(sec_rel_sub_bnr))
        sec_rel_sub_bnr += "<div id = 'multibtn_drpdwn'></div>"
    return sec_rel_sub_bnr,recall_edit,buttonvisibility,price_bar
try:
    CurrentRecordId = Param.CurrentRecordId
    Trace.Write('CurrentRecordId111'+str(CurrentRecordId))
except:
    CurrentRecordId = ""
try:
    ObjName = Param.ObjName
    Trace.Write('ObjName'+str(ObjName))
except:
    ObjName = ""
try:
    subTabName = Param.subTabName
    Trace.Write('subTabName---1'+str(subTabName))
except:
    subTabName = ""
    Trace.Write('subTabName---2'+str(subTabName))    
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
    Trace.Write("eqppp"+str(EquipmentId))
    PMEvents = "True"
    
except:
    EquipmentId = ""
    Trace.Write("eqppp11"+str(EquipmentId))
    
try:
    SerialNumber = Param.SerialNumber
    Trace.Write("Serial"+str(SerialNumber))
except:
    SerialNumber = ""            
try:
    page_type = Param.page_type
    Trace.Write('page_type'+str(page_type))
except:
    page_type = ""
try:	
    CurrentTabName = TestProduct.CurrentTab
except:
    CurrentTabName = ""
try:	
    CurrentTab = Param.CurrentTab
    Trace.Write('CurrentTab'+str(CurrentTab))
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
    # if str(ObjName) == "SAQRIB":
    # 	CurrentRecordId = "8A70EAA9-094B-4D42-AB91-111DCE26DD52"
    # 	crnt_Qry = Sql.GetFirst("SELECT SAPCPQ_ATTRIBUTE_NAME FROM SYOBJR (NOLOCK) WHERE RECORD_ID = '" + str(CurrentRecordId) + "'")
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
    # if crnt_Qry is not None:
    # 	if str(ObjName) != "SAQRIB":
    # 		CurrentRecordId = str(crnt_Qry.SAPCPQ_ATTRIBUTE_NAME)
try:
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
    quote_revision_record_id = ""
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
# =========================================================================================================================================
#   __script_name : SYSUBANNER.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD THE SUB BANNER FOR THE RELATED LISTS BASED ON HIERARCHY.
#   __primary_author__ : JOE EBENEZER
#   __create_date : 28/08/2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import re
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
    
    
    try:
        current_prod = Product.Name
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
    
    LOGIN_CREDENTIALS = Sql.GetFirst("SELECT top 1 Domain FROM SYCONF (nolock) order by CpqTableEntryId")
    if LOGIN_CREDENTIALS is not None:
        Login_Domain = str(LOGIN_CREDENTIALS.Domain)
    else:
        Login_Domain = "APPLIEDMATERIALS_TST"
        
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

    dynamic_Button = None
    # Getting page details
    multi_buttons = []
    
    page_details = Sql.GetFirst("SELECT RECORD_ID FROM SYPAGE WHERE OBJECT_APINAME = '{}' AND PAGE_TYPE = '{}'".format(str(ObjName),str(page_type)))
    if page_details:
        dynamic_Button = Sql.GetList("SELECT HTML_CONTENT,RELATED_LIST_RECORD_ID FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '{}'".format(page_details.RECORD_ID))



    # if str(ObjName) == "SYOBJC":
    #     if page_details:
    #         dynamic_Button = Sql.GetList("SELECT HTML_CONTENT,RELATED_LIST_RECORD_ID FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '{}'".format(page_details.RECORD_ID))

    # Binding button Id's based on Related list Table record id
        
        if len(dynamic_Button) > 0:
            for btn in dynamic_Button:
                if ("CANCEL" not in str(btn.HTML_CONTENT) and "SAVE" not in str(btn.HTML_CONTENT)):
                    Trace.Write("dynamic_Button---"+str(btn.HTML_CONTENT))
                    if btn.RELATED_LIST_RECORD_ID:
                        SYOBJH_ID = Sql.GetFirst("SELECT SYOBJH.SAPCPQ_ATTRIBUTE_NAME AS REC_ID,SYOBJR.NAME AS NAME FROM SYOBJR (NOLOCK) INNER JOIN SYOBJH (NOLOCK) ON SYOBJR.OBJ_REC_ID = SYOBJH.RECORD_ID WHERE SYOBJR.SAPCPQ_ATTRIBUTE_NAME = '{syobjr_rec_id}'".format(syobjr_rec_id = btn.RELATED_LIST_RECORD_ID))
                    if len(dynamic_Button) > 1:
                        if str(btn.HTML_CONTENT) != "" and str(btn.RELATED_LIST_RECORD_ID) != "":
                            button_id = str(btn.RELATED_LIST_RECORD_ID).replace("-","_")+"_"+str(SYOBJH_ID.REC_ID).replace("-","_")
                            add_button = ""
                            if btn.RELATED_LIST_RECORD_ID:
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
                            Trace.Write("add_button"+str(add_button))
                            multi_buttons.append(add_button)
                            
                        else:
                            Trace.Write("Billing matrix 124--------")
                            add_button = btn.HTML_CONTENT
                            if btn.RELATED_LIST_RECORD_ID:
                                div_id = "div_CTR_"+str(SYOBJH_ID.NAME).replace(" ","_")
                                if "div_id" in str(btn.HTML_CONTENT):
                                    add_button = add_button.format(div_id = div_id)
                            multi_buttons.append(add_button)
                            
                    else:					
                        if str(btn.HTML_CONTENT) != "" and str(btn.RELATED_LIST_RECORD_ID) != "":
                            button_id = str(btn.RELATED_LIST_RECORD_ID).replace("-","_")+"_"+str(SYOBJH_ID.REC_ID).replace("-","_")						
                            
                            if btn.RELATED_LIST_RECORD_ID:
                                div_id = "div_CTR_"+str(SYOBJH_ID.NAME).replace(" ","_")
                                if "div_id" in str(btn.HTML_CONTENT):
                                    add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id), div_id= str(div_id))
                                else:
                                    add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id))
                            else:
                                add_button =  str(btn.HTML_CONTENT).format(button_id = str(button_id))
                            
                        else:
                            Trace.Write("Billing matrix 146-------")
                            add_button = btn.HTML_CONTENT
                            if btn.RELATED_LIST_RECORD_ID:
                                div_id = "div_CTR_"+str(SYOBJH_ID.NAME).replace(" ","_")
                                if "div_id" in add_button:
                                    add_button = add_button.format(div_id = div_id)
                else:
                    add_button = ""
        else:
            add_button = ""
    else:
        add_button = ""
    Trace.Write("ADD+BUT_J "+str(add_button))
    Trace.Write("Multi buttons--> "+str(multi_buttons))
    # Getting Dynamic buttons for secondary banner -  Ends
    
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
            if str(CurrentRecordId) == 'SYOBJR-98799' and str(ObjName) == 'SAQDOC':                
                PrimaryLable = "Documents"
                PrimaryValue = "All"
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
            elif TabName == "Quote" and str(TreeParentParam) == "Quote Information" and str(TreeParam) == "Approvals" :                
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
            
                    
            elif (
                CurrentRecordId.startswith("SYOBJR", 0) == True and str(TreeParentNodeRecId) != ""
            ) and TreeParam == 'Documents' and TabName == "Quote":
                PrimaryLable = str(TreeParam)
                PrimaryValue = "ALL"
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
                ip_equipment = Sql.GetFirst("SELECT QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID,SRCFBL_NAME,SRCFBL_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
                ThirdLable = "Source Fab Location ID"
                ThirdValue = "All"
                FourthLable = "Equipment ID"
                FourthValue = "ALL"
                
            elif str(CurrentRecordId) == 'SYOBJR-00028':
                PrimaryLable = "Source Account ID"
                PrimaryValue = str(Product.GetGlobal("stp_account_Id"))
                SecondLable = "Source Account Name"
                SecondValue = str(Product.GetGlobal("stp_account_name"))
                ip_equipment = Sql.GetFirst("SELECT QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID,SRCFBL_NAME,SRCFBL_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
                ThirdLable = "Source Fab Location ID"
                ThirdValue = "All" 
                FourthLable = "Equipment ID"
                FourthValue = "ALL"           
                
    
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
            else:
                ThirdQuery = Sql.GetFirst(
                "select * from SYOBJD (nolock) where OBJECT_NAME = '" + str(ObjName) + "' AND IS_KEY = 'True' "
            )
                
                
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

            elif subTabName == "Equipment" and (TreeParentParam == "Fab Locations" or TreeSuperParentParam == "Product Offerings" or TreeParentParam == "Add-On Products" and sec_rel_sub_bnr == "") and CurrentTab == 'Quotes':		
                sale_type = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id")))
                if sale_type == 'TOOL RELOCATION' or TreeParam.startswith('Z0007'):
                    sec_rel_sub_bnr += ''
                
                else:
                    Trace.Write("Inside Else"+str(sec_rel_sub_bnr))
                    sec_rel_sub_bnr += (str(add_button))
                    Trace.Write(str(sec_rel_sub_bnr))

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
            elif TreeParam == "Billing Matrix":
                ObjName = "SAQTBP"
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
            elif (TreeSuperParentParam == "Fab Locations" or TreeTopSuperParentParam == "Fab Locations") and (subTabName == 'Equipment' or subTabName == "Details" or subTabName == "Greenbook Fab Value Drivers"):	
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
            elif TreeParam == "Approvals" and TreeParentParam == "Quote Information":
                
                contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                getval = Sql.GetFirst(" select DISTINCT TOP 10 ACAPCH.APRCHN_ID, ACAPMA.APRCHN_RECORD_ID ,ACAPCH.APPROVAL_CHAIN_RECORD_ID, ACAPCH.APRCHN_NAME, ACAPCH.APPROVAL_METHOD FROM ACAPMA (nolock) inner join ACAPCH (nolock) on ACAPCH.APPROVAL_CHAIN_RECORD_ID = ACAPMA.APRCHN_RECORD_ID  where ACAPMA.APRTRXOBJ_RECORD_ID = '"+str(contract_quote_record_id)+"' AND ACAPCH.APRCHN_ID = '"+str(subTabName)+"'")
                getown = Sql.GetFirst(" select DISTINCT TOP 10 OWNER_NAME from SAQTMT(nolock) where MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' ")
                # acaptx_dat = Sql.GetFirst("SELECT * FROM ACAPCH (NOLOCK) WHERE APRCHN_ID = '{Subtab}'".format(Subtab=subTabName))
                PrimaryLable = "Approval Chain ID"
                if getval:
                    PrimaryValue = getval.APRCHN_ID
                    SecondLable = "Approval Chain Name"
                    SecondValue = getval.APRCHN_NAME
                    ThirdLable = "Approval Chain Method"
                    ThirdValue = getval.APPROVAL_METHOD
                    FourthLable = "Quote Owner"
                else:
                    PrimaryLable = "Approvals"
                    PrimaryValue = "All" 
                    SecondLable = ""
                    SecondValue = ""
                if getown:
                    FourthValue = getown.OWNER_NAME                   
            elif (TreeParam.startswith('Sending') or TreeParam.startswith('Receiving')):
                
                if subTabName == "Details" and TreeParam.startswith('Sending'):
                    account_name = Sql.GetFirst("SELECT PARTY_NAME FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' AND PARTY_ROLE LIKE '%SENDING%'")
                    PrimaryLable = "Sending Account ID"
                    PrimaryValue = str(TreeParam).split("-")[1].strip()
                    SecondLable = "Sending Account Name"
                    SecondValue = account_name.PARTY_NAME
                elif subTabName == "Details" and TreeParam.startswith('Receiving'):
                    account_name = Sql.GetFirst("SELECT PARTY_NAME FROM SAQTIP(NOLOCK) WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' AND PARTY_ROLE LIKE '%RECEIVING%'")
                    PrimaryLable = "Receiving Account ID"
                    PrimaryValue = str(TreeParam).split("-")[1].strip()
                    SecondLable = "Receiving Account Name"
                    SecondValue = account_name.PARTY_NAME
                elif (subTabName == "Sending Equipment" or subTabName == "Service Fab Value Drivers" or subTabName == "Service Cost and Value Drivers" or subTabName == "Entitlements") and TreeParam.startswith("Sending Equipment"):
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    account_id = Sql.GetFirst("SELECT ACCOUNT_ID FROM SAQSRA (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND RELOCATION_TYPE LIKE '%SENDING%'".format(contract_quote_record_id))
                    PrimaryLable = "Sending Account ID"
                    PrimaryValue = str(account_id.ACCOUNT_ID)
                    SecondLable = str(subTabName)
                    SecondValue = "ALL"
                elif (subTabName == "Receiving Equipment" or subTabName == "Service Fab Value Drivers" or subTabName == "Service Cost and Value Drivers" or subTabName == "Entitlements") and TreeParam.startswith("Receiving Equipment"):
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    account_id = Sql.GetFirst("SELECT ACCOUNT_ID FROM SAQSRA (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND RELOCATION_TYPE LIKE '%RECEIVING%'".format(contract_quote_record_id))
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
                
                if str(ObjName) == "SAQTBP":
                    contract_quote_record_id = Product.GetGlobal("contract_quote_record_id")
                    getbillid = Sql.GetFirst("select QUOTE_BILLING_PLAN_RECORD_ID from SAQTBP(nolock) where QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
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
                if ObjName == "SAQIGB":
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    itm_gb_node = Sql.GetFirst("SELECT QUOTE_ITEM_GREENBOOK_RECORD_ID FROM SAQIGB (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND GREENBOOK = '"+str(TreeParam)+"'")
                    if itm_gb_node:
                        CurrentRecordId = itm_gb_node.QUOTE_ITEM_GREENBOOK_RECORD_ID
                elif ObjName == "SAQTMT":
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    itm_gb_node = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
                    if itm_gb_node:
                        CurrentRecordId = itm_gb_node.MASTER_TABLE_QUOTE_RECORD_ID
                # elif ObjName == "SAQSTE":
                #     contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                #     ip_equipment = Sql.GetFirst("SELECT QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID FROM SAQSTE (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
                #     if ip_equipment:
                #         CurrentRecordId = ip_equipment.QUOTE_SOURCE_TARGET_FAB_LOC_EQUIP_RECORD_ID
                elif ObjName == "SAQIFL" and subTabName != 'Details':
                    ListKey[0] = ''
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
                elif ObjName == "SAQITM" and TreeParentParam == "Quote Items" and subTabName == "Line Item Details":
                    Trace.Write("663")
                    getname = Sql.GetFirst("select QUOTE_ITEM_RECORD_ID,LINE_ITEM_ID,SERVICE_ID,SERVICE_DESCRIPTION,PRICINGPROCEDURE_ID from SAQITM where QUOTE_ITEM_RECORD_ID ='"+str(CurrentRecordId)+"'")
                    TreeParam = TreeParam.split('-')
                    PrimaryLable = "Line"
                    PrimaryValue = TreeParam[0].strip()
                    SecondLable = "Product Offering ID"
                    SecondValue = TreeParam[1].strip()
                elif ObjName == "SAQIFL" and TreeSuperParentParam == "Quote Items" and subTabName == "Details":
                    Trace.Write("Quote Items")
                    get_fab = SqlHelper.GetList("select SERVICE_ID,SERVICE_DESCRIPTION,FABLOCATION_ID,FABLOCATION_NAME from SAQIFL where QUOTE_ITEM_FAB_LOCATION_RECORD_ID = '"+str(CurrentRecordId)+"'")
                    PrimaryLable = "Fab Location ID"
                    PrimaryValue = TreeParam
                elif ObjName == "SAQICO":
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    qte_fab_node = Sql.GetFirst("SELECT MASTER_TABLE_QUOTE_RECORD_ID FROM SAQTMT (NOLOCK) WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
                    if qte_fab_node:
                        CurrentRecordId = qte_fab_node.MASTER_TABLE_QUOTE_RECORD_ID
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
                    qte_fab_node = Sql.GetFirst("SELECT QUOTE_SERVICE_FAB_LOCATION_RECORD_ID FROM SAQSFB (NOLOCK) WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
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
                    if ObjName == "SAQTBP":
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
                        elif ObjName == "SAQTBP":
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
                        
                    CurrentTabName = TestProduct.CurrentTab
                    
                    if CurrentTabName == "Quote":
                        getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()
                        Trace.Write("734")
                        
                    elif CurrentTabName == "Contract":
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
                    FourthValue = get_val.FABLOCATION_ID
                    FifthLable = "Equipment"
                    FifthValue = "ALL" 
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
                if (TreeTopSuperParentParam == "Other Products" ) and (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Greenbook Fab Value Drivers" or subTabName == "Greenbook Cost and Value Drivers" or subTabName == "Equipment Fab Value Drivers" or subTabName =="Details" ):
                    Trace.Write("Fab2333")
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
                        if TreeParam == "Receiving Equipment":			
                            get_val = Sql.GetFirst("select FABLOCATION_ID from SAQSGB(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"' and FABLOCATION_ID = '"+str(TreeParam)+"'")
                        else:
                            get_val = Sql.GetFirst("select FABLOCATION_ID from SAQSGB(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"' and FABLOCATION_ID = '"+str(TreeParentParam)+"'")
                        PrimaryLable = "Product Offering ID"
                        PrimaryValue = str(TreeSuperParentParam)
                        SecondLable = "Fab Location ID"
                        SecondValue = str(TreeParentParam)
                        ThirdLable = "Greenbook"
                        ThirdValue = str(TreeParam)
                        # FourthLable = "Fab Location ID"
                        # FourthValue = get_val.FABLOCATION_ID
                        # FifthLable = "Equipment"
                        # FifthValue = "ALL" 			
                if str(ObjName) == 'SAQSFB':
                    if TreeParentParam == "Sending Equipment" or TreeParentParam == "Receiving Equipment":
                        get_val = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQSFB(nolock) where SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
                        ThirdLable = "Product Offering Description"
                        ThirdValue = get_val.SERVICE_DESCRIPTION
                        FourthLable = "Product Offering Type"
                        FourthValue = TreeTopSuperParentParam 
                        FifthLable = " Fab Location ID"
                        FifthValue = TreeParam
                    else:
                        get_val = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQSFB(nolock) where SERVICE_ID = '"+str(TreeParentParam)+"'")
                        ThirdLable = "Product Offering Description"
                        ThirdValue = get_val.SERVICE_DESCRIPTION
                        FourthLable = "Product Offering Type"
                        FourthValue = TreeSuperParentParam 
                        FifthLable = " Fab Location ID"
                        FifthValue = TreeParam	
                if (str(ObjName) == 'SAQSCO' and str(TreeTopSuperParentParam) == "COMPREHENSIVE SERVICES"):
                    Trace.Write("check")
                    get_val = Sql.GetFirst(" SELECT EQUIPMENT_ID,SERIAL_NO FROM SAQSCO WHERE GREENBOOK = '"+str(TreeParam)+"'")
                    FifthLable = "Equipment ID"
                    FifthValue = get_val.EQUIPMENT_ID
                    SixthLable = "Serial No"
                    SixthValue = get_val.SERIAL_NO
                if (str(ObjName) == 'SAQTSV'or str(ObjName) == 'SAQSCO' or str(ObjName == 'SAQSPT')) and TreeSuperParentParam == 'Product Offerings'and TabName == "Quotes":
                    Trace.Write('subb--')					
                    TreeParam = Quote.GetGlobal("TreeParam")
                    TreeParentParam = Quote.GetGlobal("TreeParentLevel0")
                    getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV(nolock) where SERVICE_ID = '"+str(TreeParam)+"'")
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
                    covered_obj = Sql.GetFirst("select EQUIPMENT_ID from SAQSCO(nolock) where QUOTE_RECORD_ID = '{contract_quote_record_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")))
                    if covered_obj is not None and (subTabName == "Equipment" or subTabName == 'Entitlements' or subTabName == 'Service Fab Value Drivers' or subTabName == 'Service Cost and Value Drivers'):
                        FourthLable = "Greenbooks"
                        FourthValue = "All"
                        FifthLable = "Equipment"
                        FifthValue = "All"
                    elif covered_obj is not None and (subTabName == "Sending Equipment" or subTabName == 'Entitlements' or subTabName == 'Service Fab Value Drivers' or subTabName == 'Service Cost and Value Drivers'):
                        FourthLable = "Sending Equipment"
                        FourthValue = "All"
                        FifthLable = ""
                        FifthValue = ""	
                    elif covered_obj is not None and (subTabName == "Receiving Equipment" or subTabName == 'Entitlements' or subTabName == 'Service Fab Value Drivers' or subTabName == 'Service Cost and Value Drivers'):
                        FourthLable = "Receiving Equipment"
                        FourthValue = "All"
                        FifthLable = ""
                        FifthValue = ""		
                elif (str(ObjName) == 'CTCTSV'or str(ObjName) == 'CTCSCO' or str(ObjName == 'CTCSPT')) and TreeSuperParentParam == 'Product Offerings'and CurrentTab == "Contracts":
                    Trace.Write('subb@@@@@@@--')					
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
                elif (TreeSuperParentParam == "Fab Locations" or TreeTopSuperParentParam == "Fab Locations") and (subTabName == 'Equipment' or subTabName == "Details" or subTabName == "Greenbook Fab Value Drivers" or subTabName == "Fab Value Drivers"):
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
    if TreeParam == "Approvals" and CurrentTabName == "My Approvals Queue":
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
    elif subTabName == "PM Events" or subTabName == "Assembly Entitlements" :
        PrimaryLable = "Greenbook"
        PrimaryValue = str(TreeParam)
        SecondLable = "Equipment ID"
        SecondValue = str(EquipmentId)
        ThirdLable = "Serial Number"
        ThirdValue = str(SerialNumber)
        FourthLable = "Assembly ID"
        FourthValue = str(AssemblyId)
        PreventiveMaintainenceobj = Sql.GetFirst("select EQUIPMENT_ID from SAQSAP(nolock) where QUOTE_RECORD_ID = '{contract_quote_record_id}' and EQUIPMENT_ID = '{Equipment_Id}' and ASSEMBLY_ID = '{Assembly_id}'".format(contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id"),Equipment_Id = EquipmentId,Assembly_id =AssemblyId ))
        if PreventiveMaintainenceobj is not None:
            FifthLable = "PM Events"
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
    elif TopSuperParentParam == "Product Offerings" and (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Fab Value Drivers" or subTabName == "Fab Cost and Value Drivers" or subTabName == "Service Fab Value Drivers" or subTabName == "Service Cost and Value Drivers") and current_prod !='SYSTEM ADMIN' and CurrentTab == 'Quotes':
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeParentParam)
        SecondLable = "Product Offering Description"
        SecondValue = getService.SERVICE_DESCRIPTION
        ThirdLable = "Fab Location ID"
        ThirdValue = str(TreeParam)
        FourthLable = "Greenbooks"
        FourthValue = "ALL"
        FifthLable = "Equipment"
        FifthValue = "ALL"
    elif TopSuperParentParam == "Product Offerings" and (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Fab Value Drivers" or subTabName == "Fab Cost and Value Drivers" or subTabName == "Service Fab Value Drivers" or subTabName == "Service Cost and Value Drivers") and current_prod !='SYSTEM ADMIN' and CurrentTab == 'Contracts':
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from CTCTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeParentParam)
        SecondLable = "Product Offering Description"
        SecondValue = getService.SERVICE_DESCRIPTION
        ThirdLable = "Fab Location ID"
        ThirdValue = str(TreeParam)
        FourthLable = "Greenbooks"
        FourthValue = "ALL"
        FifthLable = "Equipment"
        FifthValue = "ALL"	
        SixthLable = ""
        SixthValue = ""
    elif TreeParentParam == "Quote Items" and subTabName == "Entitlements" and getQuotetype == "ZWK1 - SPARES":
        PrimaryLable = ""
        PrimaryValue = ""
    elif TopSuperParentParam == "Quote Items" and (subTabName == "Equipment Entitlements" or subTabName == "Equipment Fab Value Drivers" or subTabName == "Equipment Cost and Value Drivers" or subTabName == "Equipment Details"):
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
    elif TreeSuperParentParam == 'Approvals' and CurrentTabName == 'Quote':
        getchain = Sql.GetFirst("SELECT APRCHN_NAME FROM ACAPCH WHERE APRCHN_ID = '{}'".format(str(TreeParentParam)))
        PrimaryLable = 'Approval Chain ID'
        PrimaryValue = str(TreeParentParam)
        SecondLable = 'Approval Chain Name'
        SecondValue = getchain.APRCHN_NAME
        ThirdLable = 'Approval Round'
        ThirdValue = str(TreeParam).split(' ')[1]
        FourthLable = ''
        FourthValue = ''
        # FourthLable = "GreenBook" 
        # FourthValue = str(TreeParam)
        # FifthLable = "Equipment ID"
        # FifthValue = "All"
        # if SerialNumber is not None:
        #     SixthLable = "Serial Number"
        #     SixthValue = str(SerialNumber)
        # else:
        #     SixthLable = ""
        #     SixthValue = ""
    #elif str(TreeParentParam) == "Other Products" or str(TreeParentParam) == "Comprehensive Services":
        #Trace.Write('-----------'+str(TreeParentParam)+str(TreeParam))
    elif TopSuperParentParam == "Comprehensive Services" or TopSuperParentParam == "Add-On Products":		
        getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeSuperParentParam)+"'")
        if (subTabName == "Equipment Details" or subTabName == "Equipment Assemblies" or subTabName == "Equipment Entitlements" or subTabName == "Equipment Fab Value Drivers" or subTabName == "Equipment Cost and Value Drivers"):
            PrimaryLable = "Product Offering ID"
            PrimaryValue = str(TreeSuperParentParam)
            SecondLable = "Product Offering Description"
            SecondValue = getService.SERVICE_DESCRIPTION
            ThirdLable = "Fab Location ID"
            ThirdValue = str(TreeParentParam)
            FourthLable = "Greenbook"
            FourthValue = str(TreeParam)
            FifthLable = "Equipment ID"
            FifthValue = str(EquipmentId)
            SixthLable = "Serial Number"
            SixthValue = str(SerialNumber)
        elif((subTabName == "Details" or subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Greenbook Fab Value Drivers" or subTabName == "Greenbook Cost and Value Drivers") and subTabName != "Assembly Details"):			
            PrimaryLable = "Product Offering ID"
            PrimaryValue = str(TreeSuperParentParam)
            SecondLable = "Product Offering Description"
            SecondValue = getService.SERVICE_DESCRIPTION
            ThirdLable = "Fab Location ID"
            ThirdValue = str(TreeParentParam)
            FourthLable = "Greenbook"
            FourthValue = str(TreeParam)
            if subTabName != "Details":
                FifthLable = "Equipment"
                FifthValue = "All"
        elif subTabName == "Details":			
            PrimaryLable = ListKey[0]
            PrimaryValue = PrimaryValue
    elif TreeSuperTopParentParam == "Product Offerings" and (subTabName == "Equipment Assemblies" or subTabName == "Equipment Entitlements" or subTabName == "Equipment Fab Value Drivers" or subTabName == "Equipment Cost and Value Drivers" or subTabName == "Equipment Details" ):		
        #getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        Trace.Write("1356")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeSuperParentParam)
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
    elif (TreeSuperParentParam == "Sending Equipment" and TreeSuperTopParentParam =="Other Products" and (subTabName == "Details")):		
        #getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        Trace.Write("1359")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeTopSuperParentParam)
        SecondLable = "Fab Location ID"
        SecondValue = str(TreeParentParam)
        ThirdLable = "Greenbook"
        ThirdValue = str(TreeParam)
    elif TreeTopSuperParentParam == "Other Products"  and (subTabName == "Details"):		
        #getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        Trace.Write("1359===========")
        PrimaryLable = "Product Offering ID"
        PrimaryValue = str(TreeSuperParentParam)
        SecondLable = "Fab Location ID"
        SecondValue = str(TreeParentParam)
        ThirdLable = "Greenbook"
        ThirdValue = str(TreeParam)	

    elif (TreeSuperParentParam == "Sending Equipment" or TreeSuperTopParentParam =="Other Products" and (subTabName == "Equipment Fab Value Drivers" or subTabName == "Equipment Entitlements" or subTabName == "Equipment Cost and Value Drivers" or subTabName == "Equipment Details" )):		
        #getService = Sql.GetFirst("select SERVICE_DESCRIPTION from SAQTSV where SERVICE_ID = '"+str(TreeParentParam)+"'")
        Trace.Write("1358")
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
    elif (TreeTopSuperParentParam == "Fab Locations" or TreeSuperParentParam == "Fab Locations" and (subTabName == 'Equipment' or subTabName == 'Equipment Details' or subTabName == 'Greenbook Fab Value Drivers' or subTabName == 'Details'  or subTabName == 'Equipment Fab Value Drivers')) and ("Sending" not in TreeParam or "Receiving" not in TreeParam):
        if ("Sending" not in TreeParam and "Receiving" not in TreeParam) and ("Sending" not in TreeParentParam and "Receiving" not in TreeParentParam):
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
                ThirdLable = "Greenbook"
                ThirdValue = str(TreeParam)
                FourthLable = "Equipment"
                FourthValue = "All"
            
            '''try:
                FifthLable = ListKey[2]
                FifthValue = ListVal[2]
            except:
                FifthLable = ""
                FifthValue = ""
            Trace.Write("4 th "+str(FourthLable) + "4 th val" +str(FourthValue) + " 5 th " +str(FifthLable) + "5 th val" +str(FifthValue))'''
        elif ("Sending" in TreeParam and "Receiving" in TreeParam) or ("Sending" in TreeParentParam and "Receiving" in TreeParentParam):			
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
                FourthLable = "Equipment"
                FourthValue = "All"
            
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
    elif (TreeParentParam == "Fab Locations" and (subTabName == 'Equipment' or subTabName == 'Details' or subTabName == 'Fab Value Drivers')) and ("Sending" not in TreeParam and "Receiving" not in TreeParam):
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
    if TreeParentParam == 'Quote Items' and ObjName == 'SAQITM' and subTabName == 'Details':	
        Trace.Write("1207")	
        PrimaryLable = ListKey[0]
        PrimaryValue = PrimaryValue
        SecondLable = ListKey[1]
        SecondValue = ListVal[1]
        ThirdLable = ListKey[2]
        ThirdValue = ListVal[2]
        FourthValue = ListKey[4]
        FourthValue = ListVal[4]
        getQuotetype = ""
        getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()		
        if str(getQuotetype) == "ZTBC - TOOL BASED":
            FourthLable = ""                        
            FourthValue = ""
        else:
            FourthLable = ListKey[3]
            FourthValue = "RVCEU1" if ListVal[3]=="" else ListVal[3]
    elif TreeParentParam == 'Quote Items' and ObjName == 'SAQITM' and subTabName == 'Spare Parts':
        PrimaryLable = ""
        PrimaryValue = ""       
    elif TreeParam == 'Quote Items':
        PrimaryLable = "Quote Items"
        PrimaryValue = "ALL"
        SecondLable = "Product Offering ID"
        SecondValue = "ALL"
        ThirdLable = ""
        ThirdValue = ""
    elif TreeParentParam == 'Quote Items' and (subTabName == 'Equipment' or subTabName == 'Quote Item Fab Value Drivers' or subTabName == 'Quote Item Cost and Value Drivers'):
        TreeParam = TreeParam.split('-')
        PrimaryLable = "Line"
        PrimaryValue = TreeParam[0].strip()
        SecondLable = "Product Offering ID"
        SecondValue = TreeParam[1].strip()
        FifthLable = "Greenbooks"
        FifthValue = "All"
        SixthLable = "Equipment"
        SixthValue = "All"
    elif TreeSuperParentParam == 'Quote Items' and ObjName == 'SAQICO':
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
    elif  TreeSuperParentParam == "Quote Items" and ObjName == "SAQICO" and TabName == "Quote" and str(TreeParam) != "":
        Trace("Check----123-->")
        PrimaryLable = ListKey[0]
        PrimaryValue = PrimaryValue		
        try:
            FifthLable = ListKey[4]
            FifthValue = ListVal[4]
        except:
            FifthLable = ""
            FifthValue = ""
        try:
            PrimaryLable = ListKey[0]
            PrimaryValue = PrimaryValue
        except:
            PrimaryLable = ""
            PrimaryValue = ""
        try:
            SecondLable = ListKey[1]
            SecondValue = ListVal[1]
        except:
            SecondLable = ""
            SecondValue = ""
        try:
            ThirdLable = ListKey[2]
            ThirdValue = ListVal[2]
        except:
            ThirdLable = ""
            ThirdValue = ""
        try:
            FourthLable = ListKey[3]
            FourthValue = ListVal[3]
        except:
            FourthLable = ListKey[3]
            FourthValue = ListVal[3]
        try:
            SixthLable =ListKey[5]
            SixthValue = ListVal[5]
        except:
            SixthLable =ListKey[5]
            SixthValue = ListVal[5]
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
                
    elif  TopSuperParentParam == "Quote Items" and TabName == "Quotes" and str(TreeParam) != "" and (subTabName == "Equipment" or subTabName == "Entitlements" or subTabName == "Greenbook Fab Value Drivers" or subTabName == "Greenbook Cost and Value Drivers" or subTabName == "Details"):
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
    if str(Image) != "":
        sec_rel_sub_bnr += (
            '<div class="product_tab_icon"><img style="height: 40px; margin-top: -1px; margin-left: -1px; float: left;" src="'
            + str(Image)
            + '"/></div>'
        )

    if str(PrimaryLable) != "" and str(PrimaryValue) != "":
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
    if str(SecondLable) != "" and str(SecondValue) != "":
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
    if str(ThirdLable) != "" and str(ThirdValue) != "":		
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
                + str(ThirdValue)
                + "'>"
                + str(ThirdValue)
                + "</abbr></div></div>"
            )
    if str(FourthLable) != "" and str(FourthValue) != "" and (ObjName != "SAQTMT") and str(TreeParam) != "Quote Preview":		
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
    if str(FifthLable) != "" and str(FifthValue) != "" and str(TreeParam) != "Quote Preview":		
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
    if str(SixthLable) != "" and str(SixthValue) != "" and (str(TreeParam) != "Quote Information" and str(TreeParam) != "Quote Preview"):		
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
    if str(SeventhLable) != "" and str(SeventhValue) != "" and (str(TreeParam) != "Quote Information" and str(TreeParam) != "Quote Preview"):		
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
        if CurrentRecordId == "SYOBJR-98799":
            get_quote_status = Sql.GetFirst("SELECT QUOTE_STATUS FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id")))
            if str(get_quote_status.QUOTE_STATUS).upper() in  ["APPROVED","BOOKING SUBMITTED"]:			
                sec_rel_sub_bnr += (
                    '<button class="btnconfig cust_def_btn" id="Generate_Documents" onclick="btn_banner_content(this)" style="display: block;">GENERATE DOCUMENTS</button>'
                )
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
                elif TreeParam == "Billing Matrix" and ObjName == "SAQTBP":
                    Trace.Write("Billing")
                    for btn in multi_buttons:
                        sec_rel_sub_bnr += (btn)		

                elif CurrentRecordId == "SYOBJR-98789" and TreeParentParam != "Fab Locations" and TreeParam != "Fab Locations":
                    contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                    FabList = Sql.GetList(
                        "SELECT FAB_LOCATION_RECORD_ID FROM MAFBLC (NOLOCK) JOIN SAQTMT (NOLOCK) ON MAFBLC.ACCOUNT_RECORD_ID = SAQTMT.ACCOUNT_RECORD_ID WHERE SAQTMT.MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND FAB_LOCATION_ID NOT IN (SELECT FABLOCATION_ID FROM SAQFBL (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' )".format(
                            contract_quote_record_id,contract_quote_record_id
                        )
                    )
                    if TreeParam == "Fab Locations" and subTabName == "Equipment":
                        Trace.Write("CHK_2")
                        Trace.Write("Fab node equipment add hide")
                        sec_rel_sub_bnr += ""
                    elif FabList is not None and len(FabList) >0:
                        Trace.Write("CHK_1")
                        #Product.Attributes.GetByName("BTN_SYACTI_QT_00011_ADDFAB").Allowed = True						
                        sec_rel_sub_bnr += (str(add_button))
                        # sec_rel_sub_bnr += (
                        #     '<button id="ADDNEW__' + str(buttonid) + '" onclick="cont_openaddnew(this,'
                        #     ')" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD FAB</button>'
                        # )

                    else:
                        Trace.Write("CHK_3")
                        if CurrentRecordId == "SYOBJR-98789" and TreeParam == "Fab Locations":
                            Trace.Write("No Button are required!!!")
                        else:	
                            sec_rel_sub_bnr += (str(add_button))
                        # sec_rel_sub_bnr += (
                        #     '<button id="ADDNEW__' + str(buttonid) + '" onclick="cont_openaddnew(this,'
                        #     ')" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal" disabled>ADD FAB</button>'
                        # )

                elif CurrentRecordId == "SYOBJR-98788":
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
                    sale_type = Sql.GetFirst("SELECT SALE_TYPE FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id")))
                    if sale_type == 'TOOL RELOCATION':
                        sec_rel_sub_bnr += ''
                    else:
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
                                   
                else:	
                    Trace.Write('elseeee')

                    
                    if TreeParam == "Fab Locations":
                        GetToolReloc = Sql.GetList("SELECT CpqTableEntryId FROM SAQTIP WHERE (PARTY_ROLE = 'RECEIVING ACCOUNT' OR PARTY_ROLE = 'SENDING ACCOUNT') AND QUOTE_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id")))
                        if len(GetToolReloc) == 0:
                            for btn in multi_buttons:
                                if "ADD FAB" in str(btn):
                                    sec_rel_sub_bnr += (str(btn))
                    if subTabName == 'Fab Locations':
                        if TreeParam.startswith("Sending"):
                            for btn in multi_buttons:
                                if "ADD SENDING FAB" in str(btn):
                                    sec_rel_sub_bnr += (str(btn))
                        elif TreeParam.startswith("Receiving"):
                            for btn in multi_buttons:
                                if "ADD RECEIVING FAB" in str(btn):
                                    sec_rel_sub_bnr += (str(btn))
                    elif TreeParam == "Fab Locations" and subTabName == "Equipment":
                        
                        sec_rel_sub_bnr += ""
                    elif TreeParam == "Customer Information":
                        send_receive =[]
                        ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
                        send_and_receive = Sql.GetList("SELECT PARTY_ROLE FROM SAQTIP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}'".format(str(ContractRecordId)))
                        for acnt in send_and_receive:
                            send_receive.append(acnt.PARTY_ROLE)
                        Trace.Write("send_receive_J"+str(send_receive))
                        if ("SENDING ACCOUNT" in send_receive and "RECEIVING ACCOUNT" in send_receive):
                            sec_rel_sub_bnr += ""
                        else:
                            sec_rel_sub_bnr += (str(add_button))
                    else:
                        Trace.Write('elseeee11')
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
                getsaletypeloc = Sql.GetFirst("select SALE_TYPE,QUOTE_TYPE from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(ContractRecordId))				
                if getsaletypeloc:
                    # dynamic_Button = Sql.GetList("SELECT HTML_CONTENT FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '{}'".format(page_details.RECORD_ID))
                    Trace.Write("multi_buttons"+str(len(multi_buttons)))
                    if len(multi_buttons) > 0:						
                        if TreeParam == "Quote Items" and getsaletypeloc.QUOTE_TYPE =="ZTBC - TOOL BASED" and getsaletypeloc.SALE_TYPE != "TOOL RELOCATION":
                            # Appending Price button in Quote Items Node
                            Trace.Write("inside---> quote item"+str(multi_buttons))
                            for btn in multi_buttons:
                                if "PRICE" in btn:
                                    sec_rel_sub_bnr += (btn)
                            # Appending Price button in Quote Items Node

                            sec_rel_sub_bnr += (
                                '<button id="CALCULATE_QItems" onclick="calculate_QItems(this)" class="btnconfig">PRICE</button>'
                            )    
                        if TreeParam == "Quote Items":
                            # Appending REFRESH button in Quote Items Node
                            for btn in multi_buttons:
                                if "REFRESH" in btn:
                                    sec_rel_sub_bnr += (btn)
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
                                        sec_rel_sub_bnr += ""





            '''if str(currecId.CAN_DELETE).upper() == "TRUE":
                del_btn_id = (
                    "DELETE_ADDNEW__"
                    + str(str(currecId.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_"))
                    + "_"
                    + str(SYOBJH_RECORD_ID)
                )
                Trace.Write("390--" + str(del_btn_id))

                Trace.Write("Else")
                NORECORDS = Product.GetGlobal("RELATEDLIST_NORECORDS")
                if str(NORECORDS) == "":
                    sec_rel_sub_bnr += (
                        '<button id="'
                        + str(del_btn_id)
                        + '" class="btnconfig" onclick="relateListBulkDelete(this)" data-target="#related_delete_POPUP" data-toggle="modal" disabled>DELETE</button>'
                    )'''
        elif TreeParam == "Billing Matrix":
            Trace.Write("BM 1740")
            for btn in multi_buttons:
                sec_rel_sub_bnr += (btn)
            Trace.Write(sec_rel_sub_bnr)
        

    ''' elif TreeParam == 'Approvals' and TabName == "Quote":
        quote_status = Sql.GetFirst("SELECT QUOTE_STATUS,QUOTE_ID FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id")))
        #Trace.Write("quote status------->"+str(quote_status.QUOTE_STATUS))
        Quote_Owner = Sql.GetFirst("SELECT CPQTABLEENTRYADDEDBY FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"'")
        Quote_item_obj = Sql.GetFirst("SELECT QUOTE_ITEM_RECORD_ID FROM SAQITM WHERE QUOTE_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id")))
        User_Name = User.UserName 
        
        Submit_approval = ''
        if Quote_Owner.CPQTABLEENTRYADDEDBY == User_Name:
            Submit_approval = "True"
        else:
            Submit_approval = "False"
        get_quote_status = Sql.GetList("SELECT CpqTableEntryId FROM ACAPTX (NOLOCK) WHERE APPROVAL_ID LIKE '%{}%'".format(quote_status.QUOTE_ID))
        if not get_quote_status and str(quote_status.QUOTE_STATUS) != 'APPROVED':
            sec_rel_sub_bnr += (
                    '<button class="btnconfig cust_def_btn" id="APPROVE" onclick="quote_approval(this.id)">APPROVE</button>'
                )
        Trace.Write("get_quote_status"+str(get_quote_status))
        Trace.Write("QUOTE_STATUS"+str(quote_status.QUOTE_STATUS))
        Trace.Write("Submit_approval"+str(Submit_approval))
        Trace.Write("Quote_item_obj"+str(Quote_item_obj))
        
        if get_quote_status and str(quote_status.QUOTE_STATUS) == 'IN-PROGRESS' and Submit_approval == "True" and Quote_item_obj is not None:
            Trace.Write("submit for approval")
            sec_rel_sub_bnr += (
                    '<button class="btnconfig cust_def_btn submitbutton" data-target="#submit_for_approval" data-toggle="modal" id="submit_for_approval_btn_primary" onclick="submit_comment()">SUBMIT FOR APPROVAL</button>'
                    ) '''
        # else:
        # 	Trace.Write("elseeee")
    Trace.Write("tabNameeee"+str(TabName))
    Trace.Write("sec_rel_sub_bnr---->"+str(sec_rel_sub_bnr))
    if subTabName == 'Subtotal by Offerings' and TreeParam == "Quote Items" and (str(TabName) == "Quotes" or str(TabName) == "Quote") and current_prod == "Sales":
        Trace.Write("Subtotal by Offering"+str(TabName))
        getQuotetype = ""
        #getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()
        ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
        getsaletypeloc = Sql.GetFirst("select SALE_TYPE,QUOTE_TYPE from SAQTMT where MASTER_TABLE_QUOTE_RECORD_ID = '{}'".format(ContractRecordId))				
        if getsaletypeloc:
            # dynamic_Button = Sql.GetList("SELECT HTML_CONTENT FROM SYPGAC (NOLOCK) WHERE PAGE_RECORD_ID = '{}'".format(page_details.RECORD_ID))
            Trace.Write("multi_buttons"+str(len(multi_buttons)))
            if len(multi_buttons) > 0:						
                if TreeParam == "Quote Items" and getsaletypeloc.QUOTE_TYPE =="ZTBC - TOOL BASED":
                    # Appending Price button in Quote Items Node
                    Trace.Write("inside---> quote item")
                    for btn in multi_buttons:
                        Trace.Write("btn---12"+str(btn))
                        # if "PRICE" in btn:
                        fts_scenario_check = Sql.GetList("SELECT CpqTableEntryId FROM SAQTIP (NOLOCK) WHERE PARTY_ROLE IN ('SENDING ACCOUNT','RECEIVING ACCOUNT') AND QUOTE_RECORD_ID = '"+str(ContractRecordId)+"'")
                        Trace.Write("len_CHK_J "+str(len(fts_scenario_check)))
                        if len(fts_scenario_check) == 2:
                            sec_rel_sub_bnr += (btn)
                        else:
                            Trace.Write("hide PRICING for fts")
                            if 'GENERATE LINE ITEMS' in btn:
                                sec_rel_sub_bnr += (btn)
                    # Appending Price button in Quote Items Node

                    # sec_rel_sub_bnr += (
                    # 	'<button id="CALCULATE_QItems" onclick="calculate_QItems(this)" class="btnconfig">PRICE</button>'
                    # )    
                if TreeParam == "Quote Items":
                    # Appending REFRESH button in Quote Items Node
                    for btn in multi_buttons:
                        if "REFRESH" in btn:
                            sec_rel_sub_bnr += (btn)
                # Appending REFRESH button in Quote Items Node

                # sec_rel_sub_bnr += (
                #         '<button id="REFRESH_MATRIX" onclick="refresh_billingmatrix(this)"  class="btnconfig">REFRESH</button>'
                #     )  


    if subTabName == 'Involved Parties' and TreeParam == "Quote Information":
        Trace.Write("Involved Parties button")
        sec_rel_sub_bnr += (add_button)
    if TreeParam == "Billing Matrix" and subTabName =="Details" and ObjName == "SAQTBP":
    # 	Trace.Write("button")
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
        if TabName == "Quote":            
            ContractRecordId = Quote.GetGlobal("contract_quote_record_id")
            Quote_Owner = Sql.GetFirst("SELECT CPQTABLEENTRYADDEDBY FROM SAQTMT WHERE MASTER_TABLE_QUOTE_RECORD_ID = '"+str(ContractRecordId)+"'")
            User_Name = User.UserName 
            
            recall_edit = ''
            if Quote_Owner.CPQTABLEENTRYADDEDBY == User_Name:
                recall_edit = "True"
            else:
                recall_edit = "False"
        
        elif str(TreeParam).upper() == "QUOTE INFORMATION" and subTabName == "Involved Parties" and TabName == "Quote":
            sec_rel_sub_bnr += (
                        '<button id="ADDNEW__SYOBJR_98798_7F4F4C8D_73C7_4779_9BE5_38C695" onclick="cont_openaddnew(this, \'div_CTR_Involved_Parties\')" class="btnconfig addNewRel HideAddNew">ADD NEW</button>'
                    )

        elif str(TreeParam).upper() == "QUOTE INFORMATION" and subTabName == "Source Fab Location" and TabName == "Quote":
            sec_rel_sub_bnr += (
                        '<button id="ADDNEW__SYOBJR_98857_SYOBJ_01033" onclick="cont_openaddnew(this, \'div_CTR_Source_Fab_Locations\')" class="btnconfig addNewRel HideAddNew">ADD NEW</button>'
                    )
        elif str(TreeParam).upper() == "QUOTE INFORMATION" and subTabName == "Equipment" and TabName == "Quote":
            sec_rel_sub_bnr += (
                        '<button id="ADDNEW__SYOBJR_98858_SYOBJ_01034" onclick="cont_openaddnew(this, \'div_CTR_Involved_Parties_Equipments\')" class="btnconfig addNewRel">ADD EQUIPMENT</button>'
                    )

        elif  str(TreeParentParam).upper() == "BRIDGE PRODUCTS" and TabName == "Quote":		
            sec_rel_sub_bnr += ('<button id="spare-parts-bulk-edit-btn" onclick="showSparePartsBulkEdit(this)" style="display: none;" class="btnconfig">BULK EDIT</button><button id="spare-parts-bulk-save-btn" onclick="showSparePartsBulksave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="spare-parts-bulk-cancel-btn" onclick="showSparePartsBulkcancel(this)" style="display: none;" class="btnconfig">CANCEL</button> '  ) 
        elif  (str(TreeParentParam).upper() == "FAB LOCATIONS" or str(TreeParam).upper() == "QUOTE INFORMATION" or str(TreeSuperParentParam).upper() == "FAB LOCATIONS" )  and TabName == "Quote":
            
            sec_rel_sub_bnr += ('<button id="fablocate_save" onclick="fablocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fablocate_cancel" onclick="fablocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>'  )
        if  (str(TreeSuperParentParam).upper() == "PRODUCT OFFERINGS")  and TabName == "Quote":
            
            sec_rel_sub_bnr += ('<button id="fabcostlocate_save" onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fabcostlocate_cancel" onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>'  )                                  
        elif  (str(TreeSuperParentParam).upper() == "COMPREHENSIVE SERVICES")  and TabName == "Quote":
            
            sec_rel_sub_bnr += ('<button id="fabcostlocate_save" onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fabcostlocate_cancel" onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>'  )
        elif  (str(TreeTopSuperParentParam).upper() == "COMPREHENSIVE SERVICES")  and TabName == "Quote":
            sec_rel_sub_bnr += ('<button id="fabcostlocate_save" onclick="fabcostlocatesave(this)" style="display: none;" class="btnconfig">SAVE</button><button id="fabcostlocate_cancel" onclick="fabcostlocatecancel(this)" style="display: none;" class="btnconfig">CANCEL</button>'  ) 

    return sec_rel_sub_bnr,recall_edit
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
    # if str(ObjName) == "SAQTBP":
    # 	CurrentRecordId = "8A70EAA9-094B-4D42-AB91-111DCE26DD52"
    # 	crnt_Qry = Sql.GetFirst("SELECT SAPCPQ_ATTRIBUTE_NAME FROM SYOBJR (NOLOCK) WHERE RECORD_ID = '" + str(CurrentRecordId) + "'")
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
    # 	if str(ObjName) != "SAQTBP":
    # 		CurrentRecordId = str(crnt_Qry.SAPCPQ_ATTRIBUTE_NAME)


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

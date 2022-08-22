# =========================================================================================================================================
#   __script_name : SYULODTREE.PY   UAT
#   __script_description : THIS SCRIPT IS USED TO LOAD THE LEFT SIDE TREE CONTROL IN ALL TABS. CURRENTLY WE CALL THE SCRIPT
#                           IN THE COMMISSIONS ADMIN AND ORDER MANAGEMENT APPS.
#   __primary_author__ : ASHA LYSANDAR
#   __create_date : 26/08/2020
#   Ã‚Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================

import Webcom.Configurator.Scripting.Test.TestProduct
from SYDATABASE import SQL
import re

Sql = SQL()
get_ohold_pricing_status = ""
# node visibility query based on sales employee
get_node_visibility = Sql.GetFirst(
    "SELECT CP.permission_id from  CPQ_PERMISSIONS (NOLOCK) CP  INNER JOIN USERS_PERMISSIONS (NOLOCK) UP ON CP.PERMISSION_ID = UP.PERMISSION_ID  where user_id ='{login_user}' and CP.permission_id = '319'".format(
        login_user=User.Id
    )
)
try:
    get_pricing_status = Sql.GetFirst(
        "SELECT REVISION_STATUS FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='{}' AND ACTIVE = 1".format(Quote.CompositeNumber)
    )
    if get_pricing_status:
        get_ohold_pricing_status = get_pricing_status.REVISION_STATUS
except:
    pass
# node visibility query based on sales employee end

try:
    GetActiveRevision = Sql.GetFirst(
        "SELECT QUOTE_REVISION_RECORD_ID,QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='{}' AND ACTIVE = 1".format(Quote.CompositeNumber)
    )
except:
    # Trace.Write("EXCEPT: GetActiveRevision")
    GetActiveRevision = ""
if GetActiveRevision:
    Quote.SetGlobal("quote_revision_record_id", str(GetActiveRevision.QUOTE_REVISION_RECORD_ID))


class TreeView:
    def __init__(self):
        """Use for initialization"""
        self.exceptMessage = ""
        self.contract_quote_record_id = ''
        self.quote_revision_record_id = ''
        self.check_count = 0
    def CommonDynamicLeftTreeView(self):
        try:
            current_prod = Product.Name
        except Exception:
            current_prod = "Sales"
        CurrentModuleObj = Sql.GetFirst("select APP_ID from SYAPPS (NOLOCK) where APP_LABEL = '" + str(current_prod) + "'")
        try:
            TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
            tab_name = TestProduct.CurrentTab
            TabName = str(tab_name)
            crnt_prd_val = str(CurrentModuleObj.APP_ID)
        except:
            TestProduct = "Sales"
            try:
                tab_name = Param.sales_current_tab
            except:
                tab_name = "Quote"

            if tab_name == "Contracts":
                tab_name = "Contract"
                TabName = "Contract"
            else:
                tab_name = "Quote"
                TabName = "Quote"
            crnt_prd_val = "QT"
        if tab_name == "Quote" and current_prod == "Sales":
            try:
                GetActiveRevision = Sql.GetFirst(
                    "SELECT QUOTE_REVISION_RECORD_ID,QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='{}' AND ACTIVE = 1".format(
                        Quote.CompositeNumber
                    )
                )
            except:
                GetActiveRevision = ""
            if GetActiveRevision:
                Quote.SetGlobal("quote_revision_record_id", str(GetActiveRevision.QUOTE_REVISION_RECORD_ID))
                Quote.SetGlobal("quote_rev_id", str(GetActiveRevision.QTEREV_ID))
            # 	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
            try:
                getQuote = Sql.GetFirst(
                    "SELECT MASTER_TABLE_QUOTE_RECORD_ID,QTEREV_RECORD_ID,QTEREV_ID FROM SAQTMT(NOLOCK) WHERE QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                        Quote.CompositeNumber, GetActiveRevision.QUOTE_REVISION_RECORD_ID
                    )
                )
                Quote.SetGlobal("contract_quote_record_id", getQuote.MASTER_TABLE_QUOTE_RECORD_ID)
            except:
                getQuote = ""

            try:
                self.contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                self.quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
            except Exception:
                self.contract_quote_record_id = ""
                self.quote_revision_record_id = ""
        returnList = []
        nodeId = 0

        AllObj = Sql.GetFirst(
            "SELECT SYSECT.PRIMARY_OBJECT_RECORD_ID, SYSEFL.SAPCPQ_ATTRIBUTE_NAME, SYSEFL.RECORD_ID, SYOBJD.OBJECT_NAME FROM SYTABS (nolock) INNER JOIN SYPAGE (nolock) on SYTABS.RECORD_ID = SYPAGE.TAB_RECORD_ID INNER JOIN SYSECT ON SYSECT.PAGE_RECORD_ID = SYPAGE.RECORD_ID INNER JOIN SYSEFL (nolock) on SYSEFL.SECTION_RECORD_ID = SYSECT.RECORD_ID INNER JOIN  SYOBJD (nolock) on  SYOBJD.API_NAME = SYSEFL.API_FIELD_NAME and  SYOBJD.OBJECT_NAME = SYSEFL.API_NAME WHERE SYTABS.SAPCPQ_ALTTAB_NAME='"
            + str(TabName).strip()
            + "' AND SYSECT.SECTION_NAME = 'BASIC INFORMATION' AND  SYOBJD.DATA_TYPE = 'AUTO NUMBER' AND SYSEFL.SAPCPQ_ATTRIBUTE_NAME like '%"
            + str(crnt_prd_val)
            + "%' "
        )
        if AllObj is not None:
            QuestionRecId = str(AllObj.SAPCPQ_ATTRIBUTE_NAME)
            ObjectRecId = str(AllObj.PRIMARY_OBJECT_RECORD_ID)
            ObjectName = str(AllObj.OBJECT_NAME)
            wh_Qstn_REC_ID = "QSTN_" + str(QuestionRecId).replace("-", "_")
            RecAttValue = ""
            try:
                RecAtt = Product.Attributes.GetByName(str(wh_Qstn_REC_ID))
                if RecAtt is not None:
                    RecAttValue = RecAtt.GetValue()
                else:  # Fix for cart item insert
                    if TabName == "Quote":
                        RecAttValue = self.contract_quote_record_id
            except Exception:
                if TabName == "Quote":
                    RecAttValue = self.contract_quote_record_id
                else:
                    RecAttValue = ""

            getParentObjQuery = Sql.GetList(
                "SELECT top 1000 * FROM SYTRND (nolock) where TREE_NAME = '"
                + str(TabName)
                + "' AND NODE_TYPE = 'STATIC' AND PARENT_NODE_RECORD_ID ='' ORDER BY abs(DISPLAY_ORDER)"
            )
            if getParentObjQuery is not None:
                for getParentObj in getParentObjQuery:
                    ##adding image along with tree params
                    # 12096 start-quote item visibility start
                    if (
                        get_node_visibility
                        and str(get_ohold_pricing_status).upper() == "ON HOLD - COSTING"
                        and str(getParentObj.NODE_NAME) == "Quote Items"
                    ):
                        continue
                    # 12096 start-quote item visibility end
                    try:
                        if str(TabName) == "Quote":
                            if (str(get_ohold_pricing_status).upper() in ("CBC-CBC COMPLETED","BOK-CONTRACT CREATED","BOK-CONTRACT BOOKED","LGL-LEGAL SOW ACCEPTED","LGL-LEGAL SOW REJECTED","LGL-PREPARING LEGAL SOW","CBC-PREPARING CBC")) or (str(get_ohold_pricing_status).upper() in ("CFG-ACQUIRING","PRR-ON HOLD PRICING","CFG-ON HOLD - COSTING","PRI-PRICING") and str(getParentObj.NODE_NAME).upper() not in ("QUOTE ITEMS","BILLING","APPROVALS","QUOTE DOCUMENTS")) or (str(get_ohold_pricing_status).upper() in ("APR-APPROVED","APR-REJECTED","APR-RECALLED","APR-APPROVAL PENDING","OPD-PREPARING QUOTE DOCUMENTS","OPD-CUSTOMER ACCEPTED","OPD-CUSTOMER REJECTED") and str(getParentObj.NODE_NAME).upper() not in ("APPROVALS","QUOTE DOCUMENTS")):
                                lock_icon = '<span class="icon fa fa-lock" aria-hidden="true"></span>'
                            else:
                                lock_icon = ""
                        else:
                            lock_icon = ""
                    except:
                        Trace.Write("error")
                        lock_icon = ""
                    if str(getParentObj.TREEIMAGE_URL):
                        image_url = str(getParentObj.TREEIMAGE_URL)
                        image_url = '<img class="leftside-bar-icons" src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/AMAT/Quoteimages/{image_url}"/>'.format(
                            image_url=image_url
                        )
                        active_image_url = str(getParentObj.ACTIVE_TREEIMAGE_URL)
                        active_image_url = '<img class="activeimage-leftside-bar-icons" src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/AMAT/Quoteimages/{image_url}"/>'.format(
                            image_url=active_image_url
                        )
                    else:
                        image_url = active_image_url = ""
                    ProductDict = {}
                    ChildListData = []
                    SubTabList = []
                    NewList = []

                    RecId = str(getParentObj.TREE_NODE_RECORD_ID)
                    NodeText = lock_icon + image_url + active_image_url + str(getParentObj.NODE_NAME)
                    ProductDict["text"] = NodeText
                    ProductDict["nodeId"] = int(getParentObj.NODE_ID)
                    PageRecId = str(getParentObj.NODE_PAGE_RECORD_ID)
                    pageDetails = Sql.GetFirst("select * from SYPAGE (nolock) where RECORD_ID = '" + str(PageRecId) + "'")
                    if pageDetails is not None:
                        ObjName = pageDetails.OBJECT_APINAME
                        ProductDict["objname"] = ObjName
                        ProductDict["id"] = pageDetails.OBJECT_RECORD_ID
                    getParentObjRightView = Sql.GetList(
                        "SELECT top 1000 * FROM SYSTAB (nolock) where TREE_NODE_RECORD_ID = '"
                        + str(RecId)
                        + "' ORDER BY abs(DISPLAY_ORDER) "
                    )					
                    if getParentObjRightView is not None and len(getParentObjRightView) > 0:
                        for getRightView in getParentObjRightView:
                            type = str(getRightView.SUBTAB_TYPE)
                            subTabName = str(getRightView.SUBTAB_NAME)
                            ObjRecId = getRightView.OBJECT_RECORD_ID
                            RelatedId = getRightView.RELATED_RECORD_ID
                            RelatedName = getRightView.RELATED_LIST_NAME
                            ProductDict["id"] = RelatedId
                            # contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
                            # quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

                            if subTabName:
                                if subTabName == "Spare Parts Line Item Details":
                                    subTabName = ""
                                    spare_parts_object = Sql.GetFirst(
                                        "SELECT count(CpqTableEntryId) as cnt FROM SAQIFP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                            self.contract_quote_record_id, self.quote_revision_record_id
                                        )
                                    )
                                    if spare_parts_object is not None:
                                        if spare_parts_object.cnt > 0:
                                            subTabName = str(getRightView.SUBTAB_NAME)
                                SubTabList.append(self.getSubtabRelatedDetails(subTabName, type, ObjRecId, RelatedId, RelatedName))
                        # Billing Matrix Dynamic Tabs - Start
                        if ProductDict.get("objname") == "SAQRIB" and ProductDict.get("text") == "Billing":
                            item_billing_plan_obj = Sql.GetFirst(
                                "SELECT count(CpqTableEntryId) as cnt FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' GROUP BY EQUIPMENT_ID,SERVICE_ID".format(
                                    self.contract_quote_record_id, self.quote_revision_record_id
                                )
                            )
                            if item_billing_plan_obj is not None:
                                quotient, remainder = divmod(item_billing_plan_obj.cnt, 12)
                                years = quotient + (1 if remainder > 0 else 0)
                                if not years:
                                    years = 1
                                ObjRecId = RelatedId = None
                                related_obj = Sql.GetFirst(
                                    """SELECT SYOBJR.OBJ_REC_ID, SYOBJR.SAPCPQ_ATTRIBUTE_NAME, SYOBJR.NAME FROM SYOBJH (NOLOCK)
                                                JOIN SYOBJR (NOLOCK) ON SYOBJR.OBJ_REC_ID = SYOBJH.RECORD_ID
                                                WHERE SYOBJH.OBJECT_NAME = 'SAQIBP'"""
                                )
                                if related_obj:
                                    ObjRecId = related_obj.OBJ_REC_ID
                                    RelatedId = related_obj.SAPCPQ_ATTRIBUTE_NAME
                                    RelatedName = related_obj.NAME
                                for index in range(1, years + 1):
                                    type = "OBJECT RELATED LAYOUT"
                                    subTabName = "Year {}".format(index)
                                    # Trace.Write('subTabName--'+str(subTabName))
                                    if ObjRecId and RelatedId:
                                        SubTabList.append(self.getSubtabRelatedDetails(subTabName, type, ObjRecId, RelatedId, RelatedName))
                        # Billing Matrix Dynamic Tabs - End
                    else:
                        if pageDetails is not None:
                            pageType = pageDetails.PAGE_TYPE
                            subTabName = "No SubTab"
                            objRecId = pageDetails.OBJECT_RECORD_ID
                            if NodeText == "Variable":
                                querystr = "AND NAME = '" + str(NodeText) + "'"
                            else:
                                querystr = ""
                            SubTabList.append(self.getPageRelatedDetails(subTabName, pageType, objRecId, ObjectRecId, querystr))
                            RelatedObj = Sql.GetFirst(
                                "SELECT RECORD_ID, SAPCPQ_ATTRIBUTE_NAME, NAME FROM SYOBJR(NOLOCK) WHERE PARENT_LOOKUP_REC_ID = '"
                                + str(ObjectRecId)
                                + "' AND OBJ_REC_ID = '"
                                + str(objRecId)
                                + "' AND VISIBLE = 'True'"
                            )
                            if RelatedObj is not None:
                                ProductDict["id"] = RelatedObj.SAPCPQ_ATTRIBUTE_NAME

                    ProductDict["SubTabs"] = SubTabList
                    # if TabName == "Quote":

                    findChildOneObj = Sql.GetList(
                        "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                        + str(RecId)
                        + "' AND DISPLAY_CRITERIA != 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                    )
                    try:
                        getZ0009 = Sql.GetFirst(
                            "SELECT CpqTableEntryId,SERVICE_ID FROM SAQTSV (NOLOCK) WHERE SERVICE_ID IN ('Z0009','Z0010','Z0128') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                self.contract_quote_record_id, self.quote_revision_record_id
                            )
                        )
                        if getZ0009 is not None:
                            is_pmsa = self.PMSATree(getZ0009.SERVICE_ID)
                        else:
                            is_pmsa = 0
                    except:
                        is_pmsa = 0
                    if is_pmsa:
                        if RecId in (
                            "1F47A350-4E38-41C9-A5C5-F53DC9BB3DB8",
                            "B7BC662B-91A4-42C0-A2D9-B1E713D59E18",
                            "1CE55561-F2DF-4A05-A21B-82AF08C23215",
                            "1D531821-21B2-4F5F-8579-9724F10F8911",
                            "5C5AA48D-6598-4B55-91BB-1D043575C3B7",
                            "72FC842D-99A8-430C-A689-6DBB093015B5",
                            "11C3DA16-72B3-49A8-8B80-23637D0D499E",
                            "EBC61A4C-18C8-4374-9BDD-17BB93172453",
                            "B9E7FF3A-CD32-4414-8036-A4310FB4A80E",
                        ):
                            findChildOneObj = Sql.GetList(
                                "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                                + str(RecId)
                                + "' AND DISPLAY_CRITERIA = 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                            )
                    if findChildOneObj is not None:
                        for findChildOne in findChildOneObj:
                            parobj = str(findChildOne.PARENTNODE_OBJECT)
                            NodeType = str(findChildOne.NODE_TYPE)
                            NodeApiName = str(findChildOne.NODE_DISPLAY_NAME)
                            DynamicQuery = str(findChildOne.DYNAMIC_NODEDATA_QUERY)
                            PageRecId = str(findChildOne.NODE_PAGE_RECORD_ID)
                            ordersBy = str(findChildOne.ORDERS_BY)
                            nodeId = str(findChildOne.NODE_ID)
                            where_string = " 1=1 "
                            if parobj == "True" and ACTION != "ADDNEW":
                                ChildListData = self.getChildFromParentObj(
                                    NodeText,
                                    NodeType,
                                    NodeName,
                                    RecAttValue,
                                    nodeId,
                                    ParRecId,
                                    DynamicQuery,
                                    ObjectName,
                                    RecId,
                                    where_string,
                                    PageRecId,
                                    ObjectRecId,
                                    NodeApiName,
                                    ordersBy,
                                    lock_icon,
                                )
                            else:
                                if ACTION != "ADDNEW":
                                    NodeName = str(findChildOne.NODE_DISPLAY_NAME)
                                    ParRecId = str(findChildOne.TREE_NODE_RECORD_ID)
                                    DynamicQuery = str(findChildOne.DYNAMIC_NODEDATA_QUERY)
                                    NodeType = str(findChildOne.NODE_TYPE)
                                    PageRecId = str(findChildOne.NODE_PAGE_RECORD_ID)
                                    nodeId = str(findChildOne.NODE_ID)
                                    where_string = " 1 = 1 "									
                                    if ACTION != "ADDNEW":
                                        ChildListData = self.getChildOne(
                                            NodeType,
                                            NodeName,
                                            RecAttValue,
                                            nodeId,
                                            NodeText,
                                            ParRecId,
                                            DynamicQuery,
                                            ObjectName,
                                            RecId,
                                            where_string,
                                            PageRecId,
                                            ObjectRecId,
                                            ordersBy,
                                            lock_icon,
                                        )
                            if len(ChildListData) > 0:
                                NewList.append(ChildListData)
                                list2 = []
                                for sublist in NewList:
                                    for item in sublist:
                                        list2.append(item)
                                ProductDict["nodes"] = list2
                        returnList.append(ProductDict)
        Product.SetGlobal("CommonTreeList", str(returnList))
        #Trace.Write("returnList----------------> " + str(returnList))
        cbc_subtab = ""
        try:
            user_id = ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERNAME")
            salesteam_obj = Sql.GetList(
                " SELECT MEMBER_ID FROM SAQDLT (NOLOCK) WHERE QUOTE_RECORD_ID = '{qte_rec_id}' AND QTEREV_RECORD_ID = '{revision_rec_id}' AND C4C_PARTNERFUNCTION_ID = 'CONTRACT MANAGER' AND MEMBER_ID = '{UserId}'".format(
                    qte_rec_id=self.contract_quote_record_id, revision_rec_id=self.quote_revision_record_id, UserId=user_id
                )
            )
            # A055S000P01-17166 start
            get_status = Sql.GetFirst(
                "SELECT WORKFLOW_STATUS from SAQTRV (NOLOCK) where QUOTE_RECORD_ID='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'".format(
                    contract_quote_rec_id=self.contract_quote_record_id, quote_revision_rec_id=self.quote_revision_record_id
                )
            )
            if get_status:
                if get_status.WORKFLOW_STATUS == "LEGAL-SOW":
                    update_rev_status = "UPDATE SAQTRV SET WORKFLOW_STATUS = 'CLEAN BOOKING CHECKLIST',REVISION_STATUS = 'CBC-PREPARING CBC' where QUOTE_RECORD_ID='{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_rec_id}'".format(
                        contract_quote_rec_id=self.contract_quote_record_id, quote_revision_rec_id=self.quote_revision_record_id
                    )
                    # A055S000P01-17166 end
                    Sql.RunQuery(update_rev_status)
            if salesteam_obj:
                cbc_subtab = "Yes"
            else:
                cbc_subtab = "No"
        except:
            Trace.Write("CBC_Subtab_Exception")
        Trace.Write(str(self.check_count)+"==============>>> "+str(returnList))
        return returnList, "", cbc_subtab

    def getChildOne(
        self,
        NodeType,
        NodeName,
        RecAttValue,
        nodeId,
        NodeText,
        ParRecId,
        DynamicQuery,
        ObjectName,
        RecId,
        where_string,
        PageRecId,
        ObjectRecId,
        ordersBy,
        lock_icon = "",
        result = []
    ):
        NodeValue = ""
        NodeText1 = ""
        NodeText_temp = ""
        ChildList = []
        NewList = []
        self.check_count += 1
        try:			
            getAccounts = Sql.GetFirst(
                "SELECT CpqTableEntryId FROM SAQTIP (NOLOCK) WHERE CPQ_PARTNER_FUNCTION = 'RECEIVING ACCOUNT' AND QUOTE_RECORD_ID = '{}'".format(
                    self.contract_quote_record_id
                )
            )
        except:			
            getAccounts = ""

        if str(NodeType) == "DYNAMIC":
            try:
                ContAtt = Product.Attributes.GetByName("QSTN_SYSEFL_QT_016909")
            except:
                ContAtt = ""
            try:
                ContAttValue = ContAtt.GetValue()
            except Exception:
                try:
                    ContAttValue = Quote.GetGlobal("contract_record_id")
                except:
                    ContAttValue = ""
            pageDetails = Sql.GetFirst("select * from SYPAGE (nolock) where RECORD_ID = '" + str(PageRecId) + "'")
            if pageDetails is not None:
                OBJECT_RECORD_ID = pageDetails.OBJECT_RECORD_ID
                ObjName = pageDetails.OBJECT_APINAME
                CurrentTabName = pageDetails.TAB_NAME
                if str(ObjName) == "USERS" and str(ObjectName) == "cpq_permissions":
                    objd_where_obj = Sql.GetFirst("select * from SYOBJD (nolock) where OBJECT_NAME = '" + str(ObjName) + "'")
                else:
                    if str(ObjName).strip() in ("SAQSFB","SAQFBL","SAQSSF") and str(NodeName).strip() in ("FABLOCATION_ID","SNDFBL_ID"):
                        ObjectName = "SAQTMT"
                    objd_where_obj = Sql.GetFirst(
                        "select * from SYOBJD (nolock) where OBJECT_NAME = '"
                        + str(ObjName)
                        + "' AND LOOKUP_OBJECT = '"
                        + str(ObjectName)
                        + "'"
                    )
                try:
                    CurrentTabName = TestProduct.CurrentTab
                except:
                    CurrentTabName = "Quotes"
                
                if objd_where_obj is not None:
                    if str(ObjName) == "USERS" and str(ObjectName) == "cpq_permissions":						
                        where_string = where_string
                    elif str(ObjName).strip() == "SAQSSF" and str(NodeName).strip() == "SNDFBL_ID":
                        where_string = " QUOTE_RECORD_ID = '{quote}' AND SERVICE_ID = '{service}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(
                            self.contract_quote_record_id, service=Product.GetGlobal("SERVICE"), quote_revision_record_id=self.quote_revision_record_id
                        )
                    elif str(ObjName).strip() == "SAQSFB" and str(NodeName).strip() == "FABLOCATION_ID":
                        where_string = " QUOTE_RECORD_ID = '{quote}' AND SERVICE_ID = '{service}' AND FABLOCATION_ID != '' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(
                            quote=self.contract_quote_record_id,
                            service=Product.GetGlobal("SERVICE"),
                            quote_revision_record_id=self.quote_revision_record_id,
                        )
                    if str(ObjName).strip() == "SAQSAO":
                        where_string = where_string
                        where_string += """ AND QUOTE_RECORD_ID = '{contract_quote_record_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'""".format(
                            contract_quote_record_id=self.contract_quote_record_id, quote_revision_record_id=self.quote_revision_record_id
                        )
                    elif str(ObjName).strip() == "SAQTIP" and str(NodeName).strip() == "PARTY_ID":
                        where_string += " AND QUOTE_RECORD_ID ='{}' AND (CPQ_PARTNER_FUNCTION LIKE '%SENDING%' OR CPQ_PARTNER_FUNCTION LIKE '%RECEIVING%')  AND QTEREV_RECORD_ID = '{}'".format(
                            self.contract_quote_record_id, self.quote_revision_record_id
                        )
                    elif str(ObjName).strip() == "SAQRGG" and str(NodeName).strip() == "GOT_CODE":
                        greenbook = Product.GetGlobal("Z0009_Greenbook")
                        where_string = "QUOTE_RECORD_ID ='{}' AND GREENBOOK = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                            self.contract_quote_record_id, greenbook, self.quote_revision_record_id
                        )
                    elif str(NodeName).strip() == "PM_ID":
                        greenbook = Product.GetGlobal("Z0009_Greenbook")
                        gotcode = Product.GetGlobal("Z0009_Gotcode")
                        where_string = "QUOTE_RECORD_ID ='{}' AND GREENBOOK = '{}' AND QTEREV_RECORD_ID = '{}' AND GOT_CODE = '{}'".format(
                            self.contract_quote_record_id, greenbook, self.quote_revision_record_id, gotcode
                        )
                    elif str(ObjName).strip() == "SAQFBL" and str(NodeName).strip() == "FABLOCATION_ID":
                        send_receive_node_text = Product.GetGlobal("setnodetextname")
                        if send_receive_node_text.startswith("Sending"):
                            where_string = (
                                " QUOTE_RECORD_ID ='{}' AND RELOCATION_FAB_TYPE = 'SENDING FAB' AND QTEREV_RECORD_ID = '{}'".format(
                                    self.contract_quote_record_id, self.quote_revision_record_id
                                )
                            )
                        elif send_receive_node_text.startswith("Receiving"):
                            where_string = (
                                " QUOTE_RECORD_ID ='{}' AND RELOCATION_FAB_TYPE = 'RECEIVING FAB' AND QTEREV_RECORD_ID = '{}'".format(
                                    self.contract_quote_record_id, self.quote_revision_record_id
                                )
                            )
                        else:
                            where_string = " QUOTE_RECORD_ID ='{}' AND QTEREV_RECORD_ID = '{}'".format(
                                self.contract_quote_record_id, self.quote_revision_record_id
                            )
                    else:
                        Wh_API_NAME = objd_where_obj.API_NAME
                        if RecAttValue and str(NodeName).strip() != "APRCHN_ID" and str(ObjName).strip() != "ACAPMA":
                            where_string = " " + str(where_string) + " AND " + str(Wh_API_NAME) + " = '" + str(RecAttValue) + "'"
                        else:
                            where_string = where_string

                    childRecName = Sql.GetFirst(
                        "select * from SYOBJD (nolock) where OBJECT_NAME = '" + str(ObjName) + "' AND DATA_TYPE = 'AUTO NUMBER'"
                    )
                    if CurrentTabName != "Approval Chain":
                        if (
                            "QTEREV_RECORD_ID" not in where_string
                            and "ACAPMA" not in where_string
                            and "ACACHR" not in where_string
                            and "ACAPTX" not in where_string
                        ):
                            where_string += " AND QTEREV_RECORD_ID = '" + str(self.quote_revision_record_id) + "' "
                    if DynamicQuery is not None and len(DynamicQuery) > 0:
                        Trace.Write("inside dynamic query.....")
                        DynamicQuery = (
                            DynamicQuery.replace("{", "")
                            .replace("}", "")
                            .replace("RecAttValue", RecAttValue)
                            .replace("ContAttValue", ContAttValue)
                            .replace("where_string", where_string)
                        )
                        # ("DynamicQueryCHK1"+str(DynamicQuery))
                        childQuery = Sql.GetList("" + str(DynamicQuery) + "")
                    else:
                        Trace.Write("inside else query.....")
                        if NodeName.find("-") == -1:
                            NodeValue = NodeName
                        else:
                            NodeValuesplit = NodeName.split("-")
                            if len(NodeValuesplit) > 1:
                                NodeValue = NodeValuesplit[1]
                        if ordersBy:
                            ordersByQuery = " ORDER BY " + str(ordersBy)
                            if NodeValue != ordersBy:
                                childQuery = Sql.GetList(
                                    "select distinct top 1000 "
                                    + str(NodeValue)
                                    + ", "
                                    + str(ordersBy)
                                    + " from "
                                    + str(ObjName)
                                    + " (nolock) where "
                                    + str(where_string)
                                    + " "
                                    + str(ordersByQuery)
                                    + ""
                                )
                            else:
                                childQuery = Sql.GetList(
                                    "select distinct top 1000 "
                                    + str(NodeValue)
                                    + " from "
                                    + str(ObjName)
                                    + " (nolock) where "
                                    + str(where_string)
                                    + " "
                                    + str(ordersByQuery)
                                    + ""
                                )
                        elif str(ObjName) == "USERS":
                            ordersByQuery = ""
                            childQuery = Sql.GetList(
                                "SELECT DISTINCT top 1000 UPPER(US.USERNAME) AS USERNAME,US.ID,US.NAME,US.ACTIVE FROM USERS US WITH (NOLOCK) inner join users_permissions up on us.id = up.user_id inner join cpq_permissions cp on cp.permission_id = up.permission_id where cp.permission_type= '0' and up.permission_id = '"
                                + str(RecAttValue)
                                + "' order by USERNAME"
                            )
                        elif str(ObjName) == "SAQRIB":
                            ordersByQuery = ""
                            childQuery = Sql.GetList(
                                "select * from "
                                + str(ObjName)
                                + " (nolock) where "
                                + str(where_string)
                                + " "
                                + str(ordersByQuery)
                                + ""
                            )
                        else:
                            ordersByQuery = ""
                            childQuery = Sql.GetList(
                                "select distinct "
                                + str(NodeName)
                                + " from "
                                + str(ObjName)
                                + " (nolock) where "
                                + str(where_string)
                                + " "
                                + str(ordersByQuery)
                                + ""
                            )
                    flag = 1
                    if str(ObjName).strip() == "SAQTIP" and str(NodeName).strip() == "PARTY_ID" and flag != 2:
                        flag = 1
                    if childQuery is not None:
                        for childdata in childQuery:
                            ChildDict = {}
                            SubChildData = []					
                            if (
                                str(ObjName).strip() == "SAQSFB"
                                and str(NodeName).strip() == "FABLOCATION_ID"
                                and str(ProductName).upper() == "SALES"
                            ):
                                NodeText = str(eval("childdata." + str(NodeName)))
                                # Quote.SetGlobal('fablocation_id_for_parts_list',str(NodeText))
                                childQueryObj = Sql.GetFirst(
                                    "select  SAQSCO.FABLOCATION_ID,SAQSFB.QUOTE_SERVICE_FAB_LOCATION_RECORD_ID from SAQSCO (nolock) INNER JOIN SAQSFB ON SAQSCO.QUOTE_RECORD_ID = SAQSFB.QUOTE_RECORD_ID AND SAQSFB.QTEREV_RECORD_ID = SAQSCO.QTEREV_RECORD_ID WHERE  SAQSFB.QUOTE_RECORD_ID = '{quote}' AND SAQSCO.SERVICE_ID = '{service}' AND SAQSCO.FABLOCATION_ID != '' AND SAQSFB.QTEREV_RECORD_ID = '{quote_revision_record_id}' and SAQSFB.FABLOCATION_ID = '{NodeText}'  ".format(
                                        quote=self.contract_quote_record_id,
                                        service=self.Product.GetGlobal("SERVICE"),
                                        quote_revision_record_id=self.quote_revision_record_id,
                                        NodeText=NodeText,
                                    )
                                )
                            elif NodeName.find(",") == -1 and NodeName.find("-") == -1:
                                Trace.Write("2005-----Node name--------1" + str(NodeName))
                                if str(NodeName) == "OBJECT_NAME" and TabName == "Profile":
                                    NodeText = str(eval("childdata." + str(NodeName)))
                                elif str(NodeName) == "PARTY_ID":
                                    if flag == 1:
                                        NodeText = "Sending Account - " + str(eval("childdata." + str(NodeName)))
                                        flag = 2
                                        Product.SetGlobal("setnodetextname", str(NodeText))
                                    else:
                                        NodeText = "Receiving Account - " + str(eval("childdata." + str(NodeName)))
                                        Product.SetGlobal("setnodetextname", str(NodeText))
                                else:
                                    NodeText = str(eval("childdata." + str(NodeName))).upper()
                                
                                if str(NodeName) == "SERVICE_ID":
                                    Product.SetGlobal("SERVICE", NodeText)
                                elif str(NodeName) in ["Sending Equipment", "Receiving Equipment"]:
                                    Product.SetGlobal("Equipment", NodeText)
                                elif str(NodeName) == "GREENBOOK":
                                    Product.SetGlobal("Z0009_Greenbook", NodeText)
                                elif str(NodeName) == "GOT_CODE":
                                    Product.SetGlobal("Z0009_Gotcode", NodeText)
                                
                                childQueryObj = Sql.GetFirst(
                                    "select * from "
                                    + str(ObjName)
                                    + " (nolock) where "
                                    + str(where_string)
                                    + " AND "
                                    + str(NodeName)
                                    + " = '"
                                    + str(NodeText)
                                    + "'"
                                )
                                if str(NodeName) == "TREE_NAME":
                                    Product.SetGlobal("TreeName", str(NodeText))
                            elif NodeName.find(",") > 0:
                                Trace.Write("2050-----Node name--------1" + str(NodeName))
                                Nodesplit = NodeName.split(",")
                                if len(Nodesplit) > 1:
                                    NodeName1 = Nodesplit[0]
                                    NodeText = str(eval("childdata." + str(NodeName1))).title()
                                    childQueryObj = Sql.GetFirst(
                                        "select * from "
                                        + str(ObjName)
                                        + " (nolock) where "
                                        + str(where_string)
                                        + " AND "
                                        + str(NodeName1)
                                        + " = '"
                                        + (NodeText)
                                        + "'"
                                    )
                                    NodeText += " - "
                                    NodeName1 = Nodesplit[1]
                                    NodeText += str(eval("childdata." + str(NodeName1)))
                                    childQueryObj = Sql.GetFirst(
                                        "select * from "
                                        + str(ObjName)
                                        + " (nolock) where "
                                        + str(where_string)
                                        + " AND "
                                        + str(NodeName1)
                                        + " = '"
                                        + str(eval("childdata." + str(NodeName1)))
                                        + "'"
                                    )
                            elif NodeName.find("-") > 0:
                                Trace.Write("2081-----Node name--------1" + str(NodeName))
                                Nodesplit = NodeName.split("-")
                                if len(Nodesplit) > 1:
                                    NodeName1 = Nodesplit[0]
                                    NodeName2 = Nodesplit[1]
                                    NodeText1 = str(eval("childdata." + str(NodeName2))).title()
                                    NodeText = NodeName1 + "-" + NodeText1
                                    childQueryObj = Sql.GetFirst(
                                        "select * from "
                                        + str(ObjName)
                                        + " (nolock) where "
                                        + str(where_string)
                                        + " AND "
                                        + str(NodeName2)
                                        + " = '"
                                        + str(NodeText1)
                                        + "'"
                                    )
                            if childQueryObj is not None:
                                NodeRecId = str(eval("childQueryObj." + str(childRecName.API_NAME)))
                                ChildDict["id"] = str(NodeRecId)
                                # if str(NodeName) == "SECTION_NAME" and TabName == "App":
                                # 	Product.SetGlobal("NodeRecIdS", NodeRecId)
                                # elif str(NodeName) == "SECTION_ID" and TabName == "Profile":
                                # 	Product.SetGlobal("NodeSecRecIdS", NodeRecId)
                            if NodeText == "True":
                                NodeRecId = ""
                                ChildDict["text"] = "Active"
                            elif NodeText == "False":
                                NodeRecId = ""
                                ChildDict["text"] = "Inactive"
                            else:
                                NodeRecId = ""								
                                ##showing config status along with offering
                                if str(ObjName).strip() == "SAQTSV" and str(NodeName) == "SERVICE_ID":
                                    service_id = NodeText
                                    image_url = ""
                                    try:
                                        get_status = Sql.GetFirst(
                                            "SELECT CONFIGURATION_STATUS FROM SAQTSE(NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID ='{}'".format(
                                                self.contract_quote_record_id, self.quote_revision_record_id, NodeText
                                            )
                                        )
                                        if get_status:
                                            if get_status.CONFIGURATION_STATUS == "COMPLETE":
                                                image_url = "config_status_icon.png"
                                            elif get_status.CONFIGURATION_STATUS == "INCOMPLETE":
                                                image_url = "config_pend_status_icon.png"
                                            elif get_status.CONFIGURATION_STATUS == "ERROR":
                                                image_url = "config_incomp_status_icon.png"
                                    except:
                                        image_url = ""
                                    if image_url:
                                        image_url = '<img class="leftside-bar-status_icon" src="/mt/APPLIEDMATERIALS_UAT/Additionalfiles/AMAT/Quoteimages/{image_url}"/>'.format(
                                            image_url=image_url
                                        )
                                        NodeText = image_url + NodeText
                                ##concatenate name with ID
                                if (str(ObjName).strip() == "SAQFBL" or str(ObjName).strip() == "SAQSFB") and str(
                                    NodeName
                                ) == "FABLOCATION_ID":
                                    get_fab_name = Sql.GetFirst(
                                        "SELECT * FROM {} (NOLOCK) WHERE {} AND FABLOCATION_ID = '{}'".format(
                                            ObjName, where_string, NodeText
                                        )
                                    )
                                    if get_fab_name:
                                        NodeText_temp = NodeText + " - " + get_fab_name.FABLOCATION_NAME
                                elif str(ObjName).strip() == "SAQRIB" and str(NodeName) == "PRDOFR_ID":
                                    NodeRecIdVal = str(eval("childdata.QUOTE_BILLING_PLAN_RECORD_ID"))
                                    
                                    get_service_name_bill = Sql.GetFirst(
                                        "SELECT * FROM SAQTSV (NOLOCK) WHERE {} AND SERVICE_ID = '{}' ".format(where_string, NodeText)
                                    )
                                    if get_service_name_bill:
                                        NodeText_temp = NodeText + " - " + get_service_name_bill.SERVICE_DESCRIPTION										
                                    ChildDict["id"] = str(NodeRecIdVal)
                                if NodeText_temp:
                                    ChildDict["text"] = lock_icon + NodeText_temp
                                else:
                                    ChildDict["text"] = lock_icon + NodeText
                            ChildDict["nodeId"] = int(nodeId)
                            objQuery = Sql.GetFirst(
                                "SELECT OBJECT_NAME FROM SYOBJH (NOLOCK) WHERE RECORD_ID = '" + str(OBJECT_RECORD_ID) + "'"
                            )
                            if objQuery is not None:
                                ChildDict["objname"] = objQuery.OBJECT_NAME
                                parObjName = objQuery.OBJECT_NAME
                            SubTabList = []
                            getParentObjRightView = Sql.GetList(
                                "SELECT top 1000 * FROM SYSTAB (nolock) where TREE_NODE_RECORD_ID = '"
                                + str(ParRecId)
                                + "' ORDER BY abs(DISPLAY_ORDER) "
                            )
                            if getParentObjRightView is not None and len(getParentObjRightView) > 0:
                                for getRightView in getParentObjRightView:
                                    type = str(getRightView.SUBTAB_TYPE)
                                    subTabName = str(getRightView.SUBTAB_NAME)
                                    ObjRecId = getRightView.OBJECT_RECORD_ID
                                    if (
                                        str(ObjRecId) == "354C16C4-BDCA-4045-BC4A-40F1A6600AFD"
                                        and str(getRightView.SUBTAB_TYPE) == "OBJECT SECTION LAYOUT"
                                    ):
                                        subTabName = str(NodeText) + " : " + str(subTabName)
                                    elif (
                                        str(ObjRecId) == "354C16C4-BDCA-4045-BC4A-40F1A6600AFD"
                                        and str(getRightView.SUBTAB_TYPE) == "OBJECT RELATED LAYOUT"
                                    ):
                                        subTabName = str(NodeText) + " : " + str(subTabName)
                                    elif getAccounts is None and (
                                        subTabName == "Sending Equipment" or subTabName == "Receiving Equipment"
                                    ):
                                        subTabName = ""
                                    # A055S000P01-14557 - New Parts, Inclusion , Exclusion Subtabs starts
                                    elif subTabName in (
                                        "Events",
                                        "Service New Parts",
                                        "Service Parts List",
                                        "Service Inclusions",
                                        "Greenbook Inclusions",
                                        "Green Parts List",
                                        "Green New Parts",
                                    ):
                                        ent_table_list = ["SAQTSE"]
                                        subtab_temp_variable = subTabName
                                        whr_str_greenbook = ""
                                        ent_table = ""
                                        subTabName = ""
                                        ent_value_dict = {}
                                        service_id = Product.GetGlobal("SERVICE")
                                        if subtab_temp_variable in ("Greenbook Inclusions", "Green Parts List", "Green New Parts"):
                                            whr_str_greenbook = " AND GREENBOOK = '{}'".format(NodeText)
                                            ent_table_list.append("SAQSGE")
                                        ent_value_dict["SAQSGE"] = ""
                                        ent_value_dict["SAQTSE"] = ""
                                        for ent_table in ent_table_list:
                                            get_entitlement_xml = Sql.GetFirst(
                                                """select ENTITLEMENT_XML from {ent_table} (NOLOCK) WHERE QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' AND SERVICE_ID = '{service_id}' {whr_str_greenbook}""".format(
                                                    QuoteRecordId=self.contract_quote_record_id,
                                                    RevisionRecordId=self.quote_revision_record_id,
                                                    service_id=service_id,
                                                    ent_table=ent_table,
                                                    whr_str_greenbook=whr_str_greenbook if ent_table == "SAQSGE" else "",
                                                )
                                            )
                                            if get_entitlement_xml:
                                                pattern_tag = re.compile(r"(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)")
                                                pattern_id = ""
                                                pattern_name = ""
                                                subtab_temp = ""
                                                if subtab_temp_variable == "Events" and ent_table == "SAQTSE" and service_id != "Z0010":
                                                    pattern_id = re.compile(r"<ENTITLEMENT_ID>AGS_[^>]*?_NET_PRMALB</ENTITLEMENT_ID>")
                                                    pattern_name = re.compile(
                                                        r"<ENTITLEMENT_DISPLAY_VALUE>(?:Included - All PM|Included - Monthly and Above|Included - Quarterly and Above|Included - All PM (PDC/MPS)|Included - Qtrly and Above|Included - &lt; Quarterly)</ENTITLEMENT_DISPLAY_VALUE>"
                                                    )
                                                    subtab_temp = "Events"
                                                elif subtab_temp_variable == "Events" and service_id in ("Z0010", "Z0128"):
                                                    subtab_temp = "Events"
                                                elif subtab_temp_variable in ("Service Inclusions", "Greenbook Inclusions"):
                                                    pattern_id = re.compile(
                                                        r"<ENTITLEMENT_ID>(?:AGS_"
                                                        + str(service_id)
                                                        + "_TSC_NONCNS|AGS_"
                                                        + str(service_id)
                                                        + "_TSC_CONADD|AGS_"
                                                        + str(service_id)
                                                        + "_TSC_CONSUM|AGS_"
                                                        + str(service_id)
                                                        + "_NON_CONSUMABLE)</ENTITLEMENT_ID>"
                                                    )
                                                    pattern_name = re.compile(
                                                        r"<ENTITLEMENT_DISPLAY_VALUE>Some Inclusions</ENTITLEMENT_DISPLAY_VALUE>"
                                                    )
                                                    subtab_temp = "Inclusions"
                                                elif subtab_temp_variable in ("Service New Parts", "Green New Parts"):
                                                    pattern_id = re.compile(r"<ENTITLEMENT_ID>AGS_[^>]*?_TSC_RPPNNW</ENTITLEMENT_ID>")
                                                    pattern_name = re.compile(
                                                        r"<ENTITLEMENT_DISPLAY_VALUE>Yes</ENTITLEMENT_DISPLAY_VALUE>"
                                                    )
                                                    subtab_temp = "New Parts"
                                                elif subtab_temp_variable in ("Service Parts List", "Green Parts List"):
                                                    pattern_id = re.compile(
                                                        r"<ENTITLEMENT_ID>(?:AGS_"
                                                        + str(service_id)
                                                        + "_TSC_NONCNS|AGS_"
                                                        + str(service_id)
                                                        + "_TSC_CONADD|AGS_"
                                                        + str(service_id)
                                                        + "_TSC_CONSUM|AGS_"
                                                        + str(service_id)
                                                        + "_NON_CONSUMABLE)</ENTITLEMENT_ID>"
                                                    )
                                                    pattern_name = re.compile(
                                                        r"<ENTITLEMENT_DISPLAY_VALUE>Some Exclusions</ENTITLEMENT_DISPLAY_VALUE>"
                                                    )
                                                    subtab_temp = "Exclusions"
                                                if pattern_id and pattern_name:
                                                    updateentXML = get_entitlement_xml.ENTITLEMENT_XML
                                                    flag_excluse = 0
                                                    for m in re.finditer(pattern_tag, updateentXML):
                                                        sub_string = m.group(1)
                                                        get_ent_id = re.findall(pattern_id, sub_string)
                                                        get_ent_name = re.findall(pattern_name, sub_string)
                                                        if get_ent_id and get_ent_name:
                                                            flag_excluse = 1
                                                            break
                                                    if flag_excluse == 1 and subtab_temp:
                                                        ent_value_dict[ent_table] = subtab_temp
                                        if (
                                            subtab_temp_variable in ("Events", "Service Parts List", "Service New Parts")
                                            and service_id != "Z0010"
                                        ):
                                            subTabName = ent_value_dict["SAQTSE"]
                                        if subtab_temp_variable in ("Events") and service_id in ("Z0010", "Z0128"):
                                            subTabName = "Events"

                                        if entitlement_level_flag and (
                                            subtab_temp_variable in ("Green Parts List", "Green New Parts", "Greenbook Inclusions")
                                        ):
                                            if entitlement_level_flag == "SAQTSE":
                                                subTabName = ent_value_dict["SAQTSE"]
                                            elif entitlement_level_flag == "SAQSGE":
                                                subTabName = ent_value_dict["SAQSGE"]
                                        else:
                                            if (
                                                subtab_temp_variable in ("Green Parts List", "Green New Parts", "Greenbook Inclusions")
                                            ) and "SAQSGE" in ent_value_dict.keys():
                                                subTabName = ent_value_dict["SAQSGE"]
                                    # A055S000P01-14557 - New Parts, Inclusion , Exclusion Subtabs ends
                                    elif subTabName == "Equipment" and str(ObjName).strip() == "SAQITM" and "BASE" in NodeText:
                                        subTabName = ""
                                        service_id = NodeText.split("-")[1].strip()
                                        spare_parts_object = Sql.GetFirst(
                                            "SELECT count(CpqTableEntryId) as cnt FROM SAQICO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}'".format(
                                                self.contract_quote_record_id, self.quote_revision_record_id, service_id
                                            )
                                        )
                                        if spare_parts_object is not None:
                                            if spare_parts_object.cnt > 0:
                                                subTabName = str(getRightView.SUBTAB_NAME)
                                    ##A055S000P01-14790 code starts..
                                    elif subTabName == "Applied Events":
                                        subTabName = "Events"
                                    ##A055S000P01-14790 code ends...
                                    elif (subTabName == "Spare Parts") and str(NodeName) == "SERVICE_ID" and str(ObjName) == "SAQTSV":
                                        doc_type = Sql.GetFirst(
                                            "SELECT DOCTYP_ID FROM SAQTRV (NOLOCk) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                                self.contract_quote_record_id, self.quote_revision_record_id
                                            )
                                        )
                                        subTabName = str(getRightView.SUBTAB_NAME) if str(doc_type.DOCTYP_ID) == "ZWK1" else ""
                                    elif (subTabName == "Periods") and str(NodeName) == "SERVICE_ID" and str(ObjName) == "SAQTSV":
                                        doc_type = Sql.GetFirst(
                                            "SELECT DOCTYP_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                                self.contract_quote_record_id, self.quote_revision_record_id
                                            )
                                        )
                                        subTabName = (
                                            str(getRightView.SUBTAB_NAME)
                                            if str(doc_type.DOCTYP_ID) == "ZWK1" and Product.GetGlobal("SERVICE") == "Z0108"
                                            else ""
                                        )
                                    elif subTabName == "Equipment" and Product.GetGlobal("ParentNodeLevel") == "Complementary Products":
                                        doc_type = Sql.GetFirst(
                                            "SELECT DOCTYP_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                                self.contract_quote_record_id, self.quote_revision_record_id
                                            )
                                        )
                                        subTabName = "" if str(doc_type.DOCTYP_ID) == "ZWK1" else str(getRightView.SUBTAB_NAME)
                                        Product.SetGlobal("ParentNodeLevel", "")
                                    else:
                                        subTabName = str(getRightView.SUBTAB_NAME)
                                    RelatedId = getRightView.RELATED_RECORD_ID
                                    RelatedName = getRightView.RELATED_LIST_NAME
                                    if subTabName:
                                        # Trace.Write("Events subtab-----"+str(subTabName)+"NodeText--->"+str(NodeText)+" ===> Service"+Product.GetGlobal("SERVICE"))
                                        if subTabName == "Events" and Product.GetGlobal("SERVICE") == "Z0009":
                                            service_entitlement_object = Sql.GetFirst(
                                                """select ENTITLEMENT_XML from SAQTSE (nolock) where QUOTE_RECORD_ID = '{QuoteRecordId}' AND QTEREV_RECORD_ID = '{RevisionRecordId}' and SERVICE_ID = '{service_id}' """.format(
                                                    QuoteRecordId=self.contract_quote_record_id,
                                                    RevisionRecordId=self.quote_revision_record_id,
                                                    service_id=Product.GetGlobal("SERVICE"),
                                                )
                                            )
                                            if service_entitlement_object is not None:
                                                pattern_tag = re.compile(r"(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)")
                                                quote_type_attribute = re.compile(
                                                    r"<ENTITLEMENT_ID>AGS_[^>]*?_PQB_QTETYP</ENTITLEMENT_ID>"
                                                )
                                                quote_type_attribute_value = re.compile(
                                                    r"<ENTITLEMENT_DISPLAY_VALUE>([^>]*?)</ENTITLEMENT_DISPLAY_VALUE>"
                                                )
                                                XML = service_entitlement_object.ENTITLEMENT_XML
                                                for values in re.finditer(pattern_tag, XML):
                                                    sub_string = values.group(1)
                                                    quotetype_id = re.findall(quote_type_attribute, sub_string)
                                                    if quotetype_id:
                                                        quotetype_value = re.findall(quote_type_attribute_value, sub_string)
                                                        if quotetype_value != ["Tool based"]:
                                                            ObjRecId = "0975E1E2-9D30-4928-AB0A-4DA54537A67A"
                                                            RelatedId = "SYOBJR-95556"
                                                            RelatedName = "Events"
                                                            break
                                                        else:
                                                            ObjRecId = "271F55CA-C844-43C5-99AB-806A72152F25"
                                                            RelatedId = "SYOBJR-00011"
                                                            RelatedName = "Events"
                                                            break
                                        elif subTabName == "Events" and (Product.GetGlobal("SERVICE") == "Z0010" or Product.GetGlobal("SERVICE") == "Z0128"):##added the code to show the events nested grid for Z0128 product offerings...
                                            ObjRecId = "0975E1E2-9D30-4928-AB0A-4DA54537A67A"
                                            RelatedId = "SYOBJR-95556"
                                            RelatedName = "Events"

                                        SubTabList.append(self.getSubtabRelatedDetails(subTabName, type, ObjRecId, RelatedId, RelatedName))
                                        # Trace.Write("SubTabList --->"+str(SubTabList))
                                    if str(ObjRecId) == "01C264E8-9B64-4F99-B05C-D61ECD2C4D27":
                                        
                                        item_billing_plans_obj = Sql.GetList(
                                            "SELECT DISTINCT top 100 BILLING_YEAR  FROM SAQIBP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}' order by BILLING_YEAR".format(self.contract_quote_record_id, str(NodeText), self.quote_revision_record_id)
                                        )
                                            
                                        if item_billing_plans_obj is not None:
                                            
                                            ObjRecId = RelatedId = None
                                            related_obj = Sql.GetFirst(
                                                """SELECT SYOBJR.OBJ_REC_ID, SYOBJR.SAPCPQ_ATTRIBUTE_NAME, SYOBJR.NAME FROM SYOBJH (NOLOCK)
                                                            JOIN SYOBJR (NOLOCK) ON SYOBJR.OBJ_REC_ID = SYOBJH.RECORD_ID
                                                            WHERE SYOBJH.OBJECT_NAME = 'SAQIBP'"""
                                            )
                                            if related_obj:
                                                ObjRecId = related_obj.OBJ_REC_ID
                                                RelatedId = related_obj.SAPCPQ_ATTRIBUTE_NAME
                                                RelatedName = related_obj.NAME
                                            for item_billing_plan_obj in item_billing_plans_obj:
                                                type = "OBJECT RELATED LAYOUT"
                                                subTabName = str(item_billing_plan_obj.BILLING_YEAR).title()
                                                if ObjRecId and RelatedId:
                                                    SubTabList.append(
                                                        self.getSubtabRelatedDetails(subTabName, type, ObjRecId, RelatedId, RelatedName)
                                                    )
                                    # Trace.Write("SUBTAB_LIST_J "+str(SubTabList))
                            else:
                                if pageDetails is not None:
                                    pageType = pageDetails.PAGE_TYPE
                                    subTabName = "No SubTab"
                                    objRecId = pageDetails.OBJECT_RECORD_ID
                                    querystr = ""
                                    SubTabList.append(self.getPageRelatedDetails(subTabName, pageType, objRecId, ObjectRecId, querystr))
                            ChildDict["SubTabs"] = SubTabList

                            findSubChildAvailable = Sql.GetList(
                                "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                                + str(ParRecId)
                                + "' AND DISPLAY_CRITERIA != 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                            )
                            try:
                                getZ0009 = Sql.GetFirst(
                                    "SELECT CpqTableEntryId,SERVICE_ID FROM SAQTSV (NOLOCK) WHERE SERVICE_ID IN ('Z0009','Z0010','Z0128') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                        self.contract_quote_record_id, self.quote_revision_record_id
                                    )
                                )
                                if getZ0009 is not None:
                                    is_pmsa = self.PMSATree(getZ0009.SERVICE_ID)
                                else:
                                    is_pmsa = 0
                            except:
                                is_pmsa = ""
                            Product.SetGlobal("PMSA_TREE", str(is_pmsa))
                            if is_pmsa:
                                if ParRecId in (
                                    "1F47A350-4E38-41C9-A5C5-F53DC9BB3DB8",
                                    "B7BC662B-91A4-42C0-A2D9-B1E713D59E18",
                                    "1CE55561-F2DF-4A05-A21B-82AF08C23215",
                                    "1D531821-21B2-4F5F-8579-9724F10F8911",
                                    "5C5AA48D-6598-4B55-91BB-1D043575C3B7",
                                    "72FC842D-99A8-430C-A689-6DBB093015B5",
                                    "11C3DA16-72B3-49A8-8B80-23637D0D499E",
                                    "EBC61A4C-18C8-4374-9BDD-17BB93172453",
                                    "B9E7FF3A-CD32-4414-8036-A4310FB4A80E",
                                ):
                                    findSubChildAvailable = Sql.GetList(
                                        "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                                        + str(ParRecId)
                                        + "' AND DISPLAY_CRITERIA = 'DYNAMIC'  ORDER BY abs(DISPLAY_ORDER) "
                                    )
                            # Getting parent node for Add-On Products
                            if NodeText in (
                                "Z0091",
                                "Z0009",
                                "Z0006",
                                "Z0092",
                                "Z0035",
                                "Z0004",
                                "Z0100",
                                "Z0110",
                                "Z0006",
                                "Z0007",
                                "Z0010",
                                "Z0016",
                                "Z0128"
                            ):
                                Product.SetGlobal("SERVICE", NodeText)
                            # PROFILE EXPLORER
                            if NodeText in ("APPROVAL CENTER", "SALES", "MATERIALS", "PRICE MODELS", "PRICE MODELS", "SYSTEM ADMIN"):
                                Product.SetGlobal("APPS", NodeText)

                            pages_tab = Sql.GetList("SELECT TAB_LABEL,PRIMARY_OBJECT_NAME FROM SYTABS (NOLOCK)")
                            tab_list = [(tab.TAB_LABEL).upper() for tab in pages_tab]
                            object_list = [tab.PRIMARY_OBJECT_NAME for tab in pages_tab]
                            tab_obj_dict = {tab_list[i]: object_list[i] for i in range(len(tab_list))}
                            if NodeText in tab_list:
                                Product.SetGlobal("page_tab", NodeText)
                                Product.SetGlobal("object_name", tab_obj_dict[NodeText])

                            if findSubChildAvailable is not None:
                                for findSubChildOne in findSubChildAvailable:
                                    parobj = str(findSubChildOne.PARENTNODE_OBJECT)
                                    NodeType = str(findSubChildOne.NODE_TYPE)
                                    NodeApiName = str(findSubChildOne.NODE_DISPLAY_NAME)
                                    DynamicQuery = str(findSubChildOne.DYNAMIC_NODEDATA_QUERY)
                                    PageRecId = str(findSubChildOne.NODE_PAGE_RECORD_ID)
                                    ordersBy = str(findSubChildOne.ORDERS_BY)
                                    if parobj == "True":
                                        if NodeValue != "":
                                            Node_name = NodeValue
                                        else:
                                            Node_name = NodeName
                                        if NodeText1 != "":
                                            NodeText = NodeText1
                                        childwhere_string = (
                                            " " + str(where_string) + " AND " + str(Node_name) + " = '" + str(NodeText) + "'"
                                        )
                                        NodeText = lock_icon + str(NodeText)
                                        SubChildData = self.getChildFromParentObj(
                                            NodeText,
                                            NodeType,
                                            Node_name,
                                            RecAttValue,
                                            nodeId,
                                            ParRecId,
                                            DynamicQuery,
                                            ObjectName,
                                            RecId,
                                            childwhere_string,
                                            PageRecId,
                                            ObjectRecId,
                                            NodeApiName,
                                            ordersBy,
                                            lock_icon,
                                        )
                                    else:
                                        SubNodeName = str(findSubChildOne.NODE_DISPLAY_NAME)
                                        SubParRecId = str(findSubChildOne.TREE_NODE_RECORD_ID)
                                        SubChildDynamicQuery = str(findSubChildOne.DYNAMIC_NODEDATA_QUERY)
                                        SubNodeType = str(findSubChildOne.NODE_TYPE)
                                        nodeId = str(findSubChildOne.NODE_ID)
                                        PageRecId = str(findSubChildOne.NODE_PAGE_RECORD_ID)
                                        RecAttValue = NodeRecId
                                        ObjectName = parObjName
                                        Subwhere_string = "" + str(where_string) + ""
                                        # Trace.Write('Subwhere_string---'+str(Subwhere_string))
                                        # Trace.Write('SubNodeName---'+str(SubNodeName))
                                        addon_obj = None
                                        if NodeText.startswith("Z"):
                                            addon_obj = Sql.GetFirst(
                                                "SELECT * FROM SAQSAO (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND ADNPRD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                                    self.contract_quote_record_id, NodeText, self.quote_revision_record_id
                                                )
                                            )
                                        if SubNodeName == "GREENBOOK":
                                            if ">" in NodeText:
                                                serviceid = NodeText.split(">")[1]
                                            else:
                                                serviceid = NodeText
                                            Subwhere_string += " AND SERVICE_ID = '{}' ".format(serviceid)
                                            Product.SetGlobal("SERVICE", serviceid)
                                        if NodeText in ("Z0091", "Z0009","Z0006", "Z0092", "Z0035", "Z0016", "Z0007", "Z0016_AG", "Z0007_AG","Z0128"):
                                            Subwhere_string += " AND SERVICE_ID = '{}' ".format(NodeText)
                                            Product.SetGlobal("SERVICE", NodeText)
                                        elif addon_obj:
                                            if "SERVICE_ID" in Subwhere_string:
                                                Subwhere_string = Subwhere_string.replace("SERVICE_ID", "PAR_SERVICE_ID")
                                                Subwhere_string += " AND SERVICE_ID = '{}'".format(NodeText)
                                        
                                        if (" - ") in NodeText:
                                            temp_node = []
                                            if "-" in NodeText:
                                                temp_node = NodeText.split("-")
                                                if str(len(temp_node)) == "4":
                                                    Subwhere_string += (
                                                        " AND QUOTE_RECORD_ID = '"
                                                        + str(self.contract_quote_record_id)
                                                        + "' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(
                                                            self.quote_revision_record_id, temp_node[-2].strip()
                                                        )
                                                    )
                                                else:
                                                    Subwhere_string += (
                                                        " AND QUOTE_RECORD_ID = '"
                                                        + str(self.contract_quote_record_id)
                                                        + "'  AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND SERVICE_ID != 'Z0101'".format(
                                                            self.quote_revision_record_id, temp_node[1].strip()
                                                        )
                                                        + " AND LINE_ITEM_ID = '{}'".format(temp_node[0].strip())
                                                    )
                                        if NodeName == "PAGE_NAME" and CurrentTabName == "Tab":
                                            Subwhere_string += " AND  PAGE_NAME = '" + str(NodeText) + "'"
                                        elif NodeName == "Actions" and CurrentTabName == "Tab":
                                            Subwhere_string = Subwhere_string
                                        if ACTION != "ADDNEW":
                                            SubChildData = self.getChildOne(
                                                SubNodeType,
                                                SubNodeName,
                                                RecAttValue,
                                                nodeId,
                                                NodeText,
                                                SubParRecId,
                                                SubChildDynamicQuery,
                                                ObjectName,
                                                ParRecId,
                                                Subwhere_string,
                                                PageRecId,
                                                ObjectRecId,
                                                ordersBy,
                                                lock_icon,
                                                result
                                            )
                                    #Trace.Write("====SubChildData===>>>>>>>>>>> "+str(SubChildData))
                                    if len(SubChildData) > 0:
                                        NewList.append(SubChildData)
                                        list2 = []
                                        for sublist in NewList:
                                            for item in sublist:
                                                #Trace.Write("====item===>>>>>>>>>>>"+str(item))
                                                list2.append(item)
                                        ChildDict["nodes"] = list2
                                        #Trace.Write("====ChildDict===>>>>>>>>>>> "+str(ChildDict))
                                NewList = []
                                ChildList.append(ChildDict)
                                #Trace.Write("ChildList ====> "+str(ChildList))
        else:
            findChildOneObj = Sql.GetList(
                "SELECT top 1000 * FROM SYTRND (nolock) where TREE_NODE_RECORD_ID = '"
                + str(ParRecId)
                + "' AND DISPLAY_CRITERIA != 'DYNAMIC' AND NODE_TYPE = 'STATIC'"
            )
            if Product.GetGlobal("PMSA_TREE") == "1" and ParRecId in (
                "4237BF62-7934-4CFF-811A-7A64282CE693",
                "FE46CADE-B72F-46FF-9E01-1699D2955E6B",
            ):
                findChildOneObj = Sql.GetList(
                    "SELECT top 1000 * FROM SYTRND (nolock) where TREE_NODE_RECORD_ID = '"
                    + str(ParRecId)
                    + "' AND DISPLAY_CRITERIA = 'DYNAMIC' AND NODE_TYPE = 'STATIC'"
                )
            try:
                getZ0009 = Sql.GetFirst(
                    "SELECT CpqTableEntryId,SERVICE_ID FROM SAQTSV (NOLOCK) WHERE SERVICE_ID IN ('Z0009','Z0010','Z0128') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                        self.contract_quote_record_id, self.quote_revision_record_id
                    )
                )
                if getZ0009 is not None:
                    is_pmsa = self.PMSATree(getZ0009.SERVICE_ID)
                else:
                    is_pmsa = 0
            except:
                is_pmsa = 0
            if is_pmsa:
                if ParRecId in (
                    "1F47A350-4E38-41C9-A5C5-F53DC9BB3DB8",
                    "B7BC662B-91A4-42C0-A2D9-B1E713D59E18",
                    "1CE55561-F2DF-4A05-A21B-82AF08C23215",
                    "1D531821-21B2-4F5F-8579-9724F10F8911",
                    "5C5AA48D-6598-4B55-91BB-1D043575C3B7",
                    "72FC842D-99A8-430C-A689-6DBB093015B5",
                    "11C3DA16-72B3-49A8-8B80-23637D0D499E",
                    "EBC61A4C-18C8-4374-9BDD-17BB93172453",
                    "B9E7FF3A-CD32-4414-8036-A4310FB4A80E",
                ):
                    findSubChildAvailable = Sql.GetList(
                        "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                        + str(ParRecId)
                        + "' AND DISPLAY_CRITERIA = 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                    )
            if findChildOneObj is not None and len(findChildOneObj) > 0:
                for findChildOne in findChildOneObj:
                    if DynamicQuery is not None and len(DynamicQuery) > 0:
                        DynamicQuery = (
                            DynamicQuery.replace("{", "")
                            .replace("}", "")
                            .replace("RecAttValue", RecAttValue)
                            .replace("where_string", where_string)
                        )
                        childQuery = Sql.GetList("" + str(DynamicQuery) + "")
                    ChildDict = {}
                    SubChildData = []
                    ParRecId = str(findChildOne.TREE_NODE_RECORD_ID)
                    try:
                        if str(TabName) == "Quote":
                            if (str(get_ohold_pricing_status).upper() in ("CBC-CBC COMPLETED","BOK-CONTRACT CREATED","BOK-CONTRACT BOOKED","LGL-LEGAL SOW ACCEPTED","LGL-LEGAL SOW REJECTED","LGL-PREPARING LEGAL SOW","CBC-PREPARING CBC")) or (str(get_ohold_pricing_status).upper() in ("CFG-ACQUIRING","PRR-ON HOLD PRICING","CFG-ON HOLD - COSTING","PRI-PRICING") and str(findChildOne.NODE_NAME).upper() not in ("QUOTE ITEMS","BILLING","APPROVALS","QUOTE DOCUMENTS")) or (str(get_ohold_pricing_status).upper() in ("APR-APPROVED","APR-REJECTED","APR-RECALLED","APR-APPROVAL PENDING","OPD-PREPARING QUOTE DOCUMENTS","OPD-CUSTOMER ACCEPTED","OPD-CUSTOMER REJECTED") and str(findChildOne.NODE_NAME).upper() not in ("APPROVALS","QUOTE DOCUMENTS")):
                                lock_icon = '<span class="icon fa fa-lock" aria-hidden="true"></span>'
                            else:
                                lock_icon = ""
                            if str(get_ohold_pricing_status).upper() not in ("BOK-CONTRACT BOOKED","BOK-CONTRACT CREATED","CBC-CBC COMPLETED"):
                                if str(findChildOne.NODE_DISPLAY_NAME).upper() == "REVISIONS":
                                    lock_icon = ""
                                else:
                                    pass
                            else:
                                pass
                        else:
                            lock_icon = ""
                    except Exception as e:
                        Trace.Write("error" +str(e))
                        lock_icon = ""
                    NodeText = lock_icon + str(findChildOne.NODE_DISPLAY_NAME)
                    ChildDict["text"] =  NodeText
                    ChildDict["id"] = str(ParRecId)
                    ChildDict["nodeId"] = str(findChildOne.NODE_ID)
                    ParpageRecId = str(findChildOne.NODE_PAGE_RECORD_ID)
                    pageDetails = Sql.GetFirst("select * from SYPAGE (nolock) where RECORD_ID = '" + str(ParpageRecId) + "'")
                    if pageDetails is not None:
                        objRecId = pageDetails.OBJECT_RECORD_ID
                        objQuery = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH(NOLOCK) WHERE RECORD_ID = '" + str(objRecId) + "'")
                        if objQuery is not None:
                            ChildDict["objname"] = objQuery.OBJECT_NAME
                    SubTabList = []
                    getParentObjRightView = Sql.GetList(
                        "SELECT top 1000 * FROM SYSTAB (nolock) where TREE_NODE_RECORD_ID = '"
                        + str(ParRecId)
                        + "' ORDER BY abs(DISPLAY_ORDER) "
                    )
                    if getParentObjRightView is not None and len(getParentObjRightView) > 0:
                        for getRightView in getParentObjRightView:
                            type = str(getRightView.SUBTAB_TYPE)
                            subTabName = str(getRightView.SUBTAB_NAME)
                            ObjRecId = getRightView.OBJECT_RECORD_ID
                            RelatedId = getRightView.RELATED_RECORD_ID
                            RelatedName = getRightView.RELATED_LIST_NAME
                            ChildDict["id"] = RelatedId
                            if subTabName:
                                if getAccounts is None and (subTabName == "Sending Equipment" or subTabName == "Receiving Equipment"):
                                    subTabName = ""
                                elif subTabName == "Spare Parts Line Item Details":
                                    subTabName = ""
                                    spare_parts_object = Sql.GetFirst(
                                        "SELECT count(CpqTableEntryId) as cnt FROM SAQIFP (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                            self.contract_quote_record_id, self.quote_revision_record_id
                                        )
                                    )
                                    if spare_parts_object is not None:
                                        if spare_parts_object.cnt > 0:
                                            subTabName = str(getRightView.SUBTAB_NAME)
                                SubTabList.append(self.getSubtabRelatedDetails(subTabName, type, ObjRecId, RelatedId, RelatedName))
                    else:
                        if pageDetails is not None:
                            pageType = pageDetails.PAGE_TYPE
                            subTabName = "No SubTab"
                            objRecId = pageDetails.OBJECT_RECORD_ID
                            if NodeText == "Variable":
                                querystr = "AND NAME = '" + str(NodeText) + "'"
                            else:
                                querystr = ""
                            SubTabList.append(self.getPageRelatedDetails(subTabName, pageType, objRecId, ObjectRecId, querystr))
                            RelatedObj = Sql.GetFirst(
                                "SELECT RECORD_ID, SAPCPQ_ATTRIBUTE_NAME, NAME FROM SYOBJR (NOLOCK) WHERE PARENT_LOOKUP_REC_ID = '"
                                + str(ObjectRecId)
                                + "' AND OBJ_REC_ID = '"
                                + str(objRecId)
                                + "' AND VISIBLE = 'True'"
                            )
                            if RelatedObj is not None:
                                ChildDict["id"] = RelatedObj.SAPCPQ_ATTRIBUTE_NAME
                    ChildDict["SubTabs"] = SubTabList

                    findSubChildAvailable = Sql.GetList(
                        "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                        + str(ParRecId)
                        + "' AND DISPLAY_CRITERIA != 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                    )
                    try:
                        getZ0009 = Sql.GetFirst(
                            "SELECT CpqTableEntryId,SERVICE_ID FROM SAQTSV (NOLOCK) WHERE SERVICE_ID IN ('Z0009','Z0010','Z0128') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                self.contract_quote_record_id, self.quote_revision_record_id
                            )
                        )
                        if getZ0009 is not None:
                            is_pmsa = self.PMSATree(getZ0009.SERVICE_ID)
                        else:
                            is_pmsa = 0
                    except:
                        is_pmsa = 0
                    if is_pmsa is not None :
                        if ParRecId in (
                            "1F47A350-4E38-41C9-A5C5-F53DC9BB3DB8",
                            "B7BC662B-91A4-42C0-A2D9-B1E713D59E18",
                            "1CE55561-F2DF-4A05-A21B-82AF08C23215",
                            "1D531821-21B2-4F5F-8579-9724F10F8911",
                            "5C5AA48D-6598-4B55-91BB-1D043575C3B7",
                            "72FC842D-99A8-430C-A689-6DBB093015B5",
                            "11C3DA16-72B3-49A8-8B80-23637D0D499E",
                            "EBC61A4C-18C8-4374-9BDD-17BB93172453",
                            "B9E7FF3A-CD32-4414-8036-A4310FB4A80E",
                        ):
                            findSubChildAvailable = Sql.GetList(
                                "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                                + str(ParRecId)
                                + "' AND DISPLAY_CRITERIA = 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                            )
                    if findSubChildAvailable is not None and len(findSubChildAvailable) > 0:
                        for findSubChildOne in findSubChildAvailable:
                            if str(findSubChildOne.TREEIMAGE_URL):
                                image_url = str(findSubChildOne.TREEIMAGE_URL)
                            parobj = str(findSubChildOne.PARENTNODE_OBJECT)
                            NodeType = str(findSubChildOne.NODE_TYPE)
                            NodeApiName = str(findSubChildOne.NODE_DISPLAY_NAME)
                            DynamicQuery = str(findSubChildOne.DYNAMIC_NODEDATA_QUERY)
                            PageRecId = str(findSubChildOne.NODE_PAGE_RECORD_ID)
                            ordersBy = str(findSubChildOne.ORDERS_BY)
                            ParRecId = str(findSubChildOne.TREE_NODE_RECORD_ID)
                            if parobj == "True":
                                childwhere_string = " " + str(where_string) + ""
                                SubChildData = self.getChildFromParentObj(
                                    NodeText,
                                    NodeType,
                                    NodeName,
                                    RecAttValue,
                                    nodeId,
                                    ParRecId,
                                    DynamicQuery,
                                    ObjectName,
                                    RecId,
                                    childwhere_string,
                                    PageRecId,
                                    ObjectRecId,
                                    NodeApiName,
                                    ordersBy,
                                    lock_icon,
                                )
                            else:
                                SubNodeName = str(findSubChildOne.NODE_DISPLAY_NAME)
                                SubParRecId = str(findSubChildOne.TREE_NODE_RECORD_ID)
                                subDynamicQuery = str(findSubChildOne.DYNAMIC_NODEDATA_QUERY)
                                SubNodeType = str(findSubChildOne.NODE_TYPE)
                                nodeId = str(findSubChildOne.NODE_ID)
                                where_string = " 1=1"
                                Subwhere_string = str(where_string)
                                # Filter based on service type - Services Node - Start
                                try:
                                    CurrentTabName = TestProduct.CurrentTab
                                except:
                                    CurrentTabName = "Quotes"
                                if NodeText.replace(lock_icon,"") in (
                                    "Actions",
                                    "Tabs",
                                    "Add-On Products",
                                    "Comprehensive Services",
                                    "Complementary Products",
                                    "Other Products",
                                    "Billing",
                                ):
                                    # if Currenttab == "Contracts":
                                    # 	Subwhere_string += " AND PRODUCT_TYPE = '{}'".format(NodeText)
                                    if NodeText.replace(lock_icon,"") == "Add-On Products":
                                        service_id = Product.GetGlobal("SERVICE")
                                        Subwhere_string += " AND SERVICE_ID = '{}'".format(str(service_id))									
                                    else:
                                        Product.SetGlobal("ParentNodeLevel", NodeText.replace(lock_icon,""))
                                        # A055S000P01-9646 CODE STARTS..
                                        Trace.Write("2840--" + str(NodeText.replace(lock_icon,"")))

                                        Subwhere_string += " AND SERVICE_TYPE = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID != 'Z0046' AND SERVICE_ID != 'Z0101'".format(
                                            NodeText.replace(lock_icon,""), self.quote_revision_record_id
                                        )
                                        # A055S000P01-9646 CODE ENDS..
                                # elif NodeText in ("Pages"):
                                # 	# Trace.Write("NodeText"+str(NodeText)+"---")
                                # 	if NodeText == "Pages":
                                # 		page_tab = Quote.GetGlobal("page_tab")
                                # 		# Trace.Write("page_tab"+str(page_tab)+"---")
                                # 		Subwhere_string += " AND TAB_LABEL = '{}'".format(page_tab)

                                # elif NodeText in ("Tree Node"):
                                # 	RecAttValue = Product.Attributes.GetByName("QSTN_SYSEFL_SY_01110").GetValue()
                                # 	getpagename = Sql.GetList(
                                # 		"select TREE_RECORD_ID from SYTREE (NOLOCK) where PAGE_RECORD_ID = '"
                                # 		+ str(RecAttValue)
                                # 		+ "' and TREE_NAME = '"
                                # 		+ str(Quote.GetGlobal("TreeName"))
                                # 		+ "'"
                                # 	)
                                # 	if getpagename:
                                # 		for tree in getpagename:
                                # 			# where_string =  where_string
                                # 			Tree_Node = str(tree.TREE_RECORD_ID)
                                # 		Subwhere_string += " AND TREE_RECORD_ID = '" + str(Tree_Node) + "'"
                                elif str(NodeText.replace(lock_icon,"")) in ["Sending Equipment", "Receiving Equipment"]:
                                    Product.SetGlobal("Equipment", NodeText.replace(lock_icon,""))
                                PageRecId = str(findSubChildOne.NODE_PAGE_RECORD_ID)
                                # Filter based on service type - Services Node - End
                                # Trace.Write("check----"+str(NodeText))
                                # try:
                                # 	CurrentTabName = TestProduct.CurrentTab
                                # except:
                                # 	CurrentTabName = ""
                                
                                if ACTION != "ADDNEW":
                                    SubChildData = self.getChildOne(
                                        SubNodeType,
                                        SubNodeName,
                                        RecAttValue,
                                        nodeId,
                                        NodeText,
                                        SubParRecId,
                                        subDynamicQuery,
                                        ObjectName,
                                        RecId,
                                        Subwhere_string,
                                        PageRecId,
                                        ObjectRecId,
                                        ordersBy,
                                        lock_icon,
                                    )

                            # Trace.Write("SubChildData---1940"+str(SubChildData))
                            # Trace.Write("NewList---1940"+str(NewList))
                            if len(SubChildData) > 0:
                                NewList.append(SubChildData)
                                list2 = []
                                for sublist in NewList:
                                    for item in sublist:
                                        list2.append(item)
                                ChildDict["nodes"] = list2
                    NewList = []
                    ChildList.append(ChildDict)
        # Trace.Write("ChildList"+str(ChildList))
        
        return ChildList

    def getChildFromParentObj(
        self,
        NodeText,
        NodeType,
        NodeName,
        RecAttValue,
        nodeId,
        ParRecId,
        DynamicQuery,
        ObjectName,
        RecId,
        where_string,
        PageRecId,
        ObjectRecId,
        NodeApiName,
        ordersBy,
        lock_icon = ""
    ):
        try:
            getAccounts = Sql.GetFirst(
                "SELECT CpqTableEntryId FROM SAQTIP (NOLOCK) WHERE CPQ_PARTNER_FUNCTION = 'RECEIVING ACCOUNT' AND QUOTE_RECORD_ID = '{}'".format(
                    self.contract_quote_record_id
                )
            )
        except:
            getAccounts = ""

        # NewList = []
        NodeNameValue = ""
        NodeTextValue = ""
        #contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
        #quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
        if str(NodeType) == "DYNAMIC":
            pageDetails = Sql.GetFirst("select * from SYPAGE (nolock) where RECORD_ID = '" + str(PageRecId) + "'")
            if pageDetails is not None:
                OBJECT_RECORD_ID = pageDetails.OBJECT_RECORD_ID
                ObjName = pageDetails.OBJECT_APINAME
                childRecName = Sql.GetFirst(
                    "select * from SYOBJD (nolock) where OBJECT_NAME = '" + str(ObjName) + "' AND DATA_TYPE = 'AUTO NUMBER'"
                )
                if DynamicQuery is not None and len(DynamicQuery) > 0:

                    DynamicQuery = (
                        DynamicQuery.replace("{", "")
                        .replace("}", "")
                        .replace("RecAttValue", RecAttValue)
                        .replace("NodeText", str(NodeText))
                        .replace("where_string", where_string)
                    )
                    childQuery = Sql.GetList("" + str(DynamicQuery) + "")
                    # Trace.Write("@2449----------->" + str(DynamicQuery) + "")
                else:
                    # Trace.Write("@2442---")
                    if (str(ObjName).strip() != "SAQSGB" and str(NodeApiName) != "FABLOCATION_ID") or (
                        str(ObjName).strip() != "SAQFGB" and str(NodeApiName) != "GREENBOOK"
                    ):
                        # Trace.Write("@2444---")
                        childQuery = Sql.GetList("select * from " + str(ObjName) + " (nolock) where " + str(where_string) + "")
                    if str(ObjName).strip() != "CTCSGB" and str(NodeApiName) != "FABLOCATION_ID":
                        childQuery = Sql.GetList("select * from " + str(ObjName) + " (nolock) where " + str(where_string) + "")
                    else:
                        if str(ObjName).strip() == "SAQFGB":
                            childQuery = Sql.GetList(
                                "select  GREENBOOK from " + str(ObjName) + " (nolock) where " + str(where_string) + " GROUP BY GREENBOOK"
                            )
                # getAccounts = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQTIP WHERE CPQ_PARTNER_FUNCTION = 'RECEIVING ACCOUNT' AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                # if getAccounts is None:
                findSubChildAvailable = Sql.GetList(
                    "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                    + str(ParRecId)
                    + "' AND DISPLAY_CRITERIA != 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                )
                try:
                    getZ0009 = Sql.GetFirst(
                        "SELECT CpqTableEntryId,SERVICE_ID FROM SAQTSV (NOLOCK) WHERE SERVICE_ID IN ('Z0009','Z0010','Z0128') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                            self.contract_quote_record_id, self.quote_revision_record_id
                        )
                    )
                    if getZ0009 is not None:
                        is_pmsa = self.PMSATree(getZ0009.SERVICE_ID)
                    else:
                        is_pmsa = 0
                except:
                    is_pmsa = 0
                if is_pmsa:
                    if ParRecId in (
                        "1F47A350-4E38-41C9-A5C5-F53DC9BB3DB8",
                        "B7BC662B-91A4-42C0-A2D9-B1E713D59E18",
                        "1CE55561-F2DF-4A05-A21B-82AF08C23215",
                        "1D531821-21B2-4F5F-8579-9724F10F8911",
                        "5C5AA48D-6598-4B55-91BB-1D043575C3B7",
                        "72FC842D-99A8-430C-A689-6DBB093015B5",
                        "11C3DA16-72B3-49A8-8B80-23637D0D499E",
                        "EBC61A4C-18C8-4374-9BDD-17BB93172453",
                        "B9E7FF3A-CD32-4414-8036-A4310FB4A80E",
                    ):
                        findSubChildAvailable = Sql.GetList(
                            "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                            + str(ParRecId)
                            + "' AND DISPLAY_CRITERIA = 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                        )
                if childQuery is not None:
                    ChildList = []
                    for childdata in childQuery:
                        ChildDict = {}
                        SubChildData = []
                        if NodeApiName.find(",") == -1 and NodeApiName.find("-") == -1:
                            NodeText = str(eval("childdata." + str(NodeApiName)))
                        elif NodeApiName.find("-") > 0:
                            Nodesplit = NodeApiName.split("-")
                            if len(Nodesplit) > 1:
                                NodeName1 = Nodesplit[0]
                                NodeNameValue = Nodesplit[1]
                                NodeTextValue = str(eval("childdata." + str(NodeNameValue))).title()
                                NodeText = NodeName1 + "-" + NodeTextValue
                        NodeText = lock_icon + str(NodeText)
                        try:
                            NodeRecId = str(eval("childdata." + str(childRecName.API_NAME)))
                        except Exception:
                            if str(ObjName).strip() == "SAQSGB":
                                if NodeApiName == "FABLOCATION_ID":
                                    NodeRecId = str(eval("childdata.FABLOCATION_ID"))
                                    nodeId = 32
                                elif NodeApiName == "GREENBOOK":
                                    try:
                                        NodeRecId = str(eval("childdata.GREENBOOK"))
                                    except:
                                        NodeRecId = "-"
                            elif str(ObjName).strip() == "SAQFGB":
                                NodeRecId = str(eval("childdata.GREENBOOK"))
                            elif str(ObjName).strip() == "ACAPTF":
                                if NodeApiName == "TRKOBJ_TRACKEDFIELD_LABEL":
                                    NodeRecId = str(eval("childdata.TRKOBJ_TRACKEDFIELD_LABEL"))
                            else:
                                NodeRecId = str(eval("childdata.REC_ID"))

                        ChildDict["text"] = str(NodeText)
                        ChildDict["id"] = str(NodeRecId)
                        ChildDict["nodeId"] = int(nodeId)
                        ChildDict["id"] = str(NodeRecId)
                        oldNodeApiName = NodeApiName
                        objQuery = Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH(NOLOCK) WHERE RECORD_ID = '" + str(OBJECT_RECORD_ID) + "'")
                        if objQuery is not None:
                            ChildDict["objname"] = objQuery.OBJECT_NAME
                            parObjName = objQuery.OBJECT_NAME

                        SubTabList = []
                        getParentObjRightView = Sql.GetList(
                            "SELECT top 1000 * FROM SYSTAB (nolock) where TREE_NODE_RECORD_ID = '"
                            + str(ParRecId)
                            + "' ORDER BY abs(DISPLAY_ORDER) "
                        )
                        if getParentObjRightView is not None and len(getParentObjRightView) > 0:
                            for getRightView in getParentObjRightView:
                                type = str(getRightView.SUBTAB_TYPE)
                                subTabName = str(getRightView.SUBTAB_NAME)
                                ObjRecId = getRightView.OBJECT_RECORD_ID
                                RelatedId = getRightView.RELATED_RECORD_ID
                                RelatedName = getRightView.RELATED_LIST_NAME
                                # ChildDict["id"] = RelatedId
                                if subTabName == "Green Parts List":
                                    subTabName = ""
                                    # service_id = Quote.GetGlobal("SERVICE")
                                    greenbook_entitlement_object = Sql.GetFirst(
                                        """select ENTITLEMENT_XML from SAQSGE (nolock) where QUOTE_RECORD_ID = '{quote_id}' AND QTEREV_RECORD_ID = '{quote_rev_id}' and SERVICE_ID = '{service_id}' and GREENBOOK = '{NodeText}' """.format(
                                            quote_id=self.contract_quote_record_id,
                                            quote_rev_id=self.quote_revision_record_id,
                                            service_id=Product.GetGlobal("SERVICE"),
                                            NodeText=NodeText,
                                        )
                                    )
                                    if greenbook_entitlement_object is not None:
                                        updateentXML = greenbook_entitlement_object.ENTITLEMENT_XML
                                        flag_excluse = 0
                                        pattern_tag = re.compile(r"(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)")
                                        pattern_id = re.compile(
                                            r"<ENTITLEMENT_ID>(?:AGS_[^>]*?_TSC_NONCNS|AGS_[^>]*?_TSC_CONSUM|AGS_[^>]*?_NON_CONSUMABLE|AGS_[^>]*?_TSC_RPPNNW|AGS_[^>]*?_TSC_CONADD)</ENTITLEMENT_ID>"
                                        )
                                        pattern_name = re.compile(
                                            r"<ENTITLEMENT_DISPLAY_VALUE>(?:Some Exclusions|Some Inclusions|Yes)</ENTITLEMENT_DISPLAY_VALUE>"
                                        )
                                        for m in re.finditer(pattern_tag, updateentXML):
                                            sub_string = m.group(1)
                                            get_ent_id = re.findall(pattern_id, sub_string)
                                            get_ent_name = re.findall(pattern_name, sub_string)
                                            if get_ent_id and get_ent_name:
                                                flag_excluse = 1
                                                break
                                        if flag_excluse == 1:
                                            subTabName = "Parts List"
                                if subTabName:
                                    if getAccounts is None and (subTabName == "Sending Equipment" or subTabName == "Receiving Equipment"):
                                        subTabName = ""
                                    SubTabList.append(self.getSubtabRelatedDetails(subTabName, type, ObjRecId, RelatedId, RelatedName))
                        else:
                            if pageDetails is not None:
                                pageType = pageDetails.PAGE_TYPE
                                subTabName = "No SubTab"
                                objRecId = pageDetails.OBJECT_RECORD_ID
                                querystr = ""
                                SubTabList.append(self.getPageRelatedDetails(subTabName, pageType, objRecId, ObjectRecId, querystr))

                        ChildDict["SubTabs"] = SubTabList
                        # getAccounts = Sql.GetFirst("SELECT CpqTableEntryId FROM SAQTIP WHERE CPQ_PARTNER_FUNCTION = 'RECEIVING ACCOUNT' AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
                        # if getAccounts is None:
                        findSubChildAvailable = Sql.GetList(
                            "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                            + str(ParRecId)
                            + "' AND DISPLAY_CRITERIA != 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                        )
                        try:
                            getZ0009 = Sql.GetFirst(
                                "SELECT CpqTableEntryId,SERVICE_ID FROM SAQTSV (NOLOCK) WHERE SERVICE_ID IN ('Z0009','Z0010','Z0128') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                    self.contract_quote_record_id, self.quote_revision_record_id
                                )
                            )
                            if getZ0009 is not None:
                                is_pmsa = self.PMSATree(getZ0009.SERVICE_ID)
                            else:
                                is_pmsa = 0
                        except:
                            is_pmsa = 0
                        if is_pmsa:
                            if ParRecId in (
                                "1F47A350-4E38-41C9-A5C5-F53DC9BB3DB8",
                                "B7BC662B-91A4-42C0-A2D9-B1E713D59E18",
                                "1CE55561-F2DF-4A05-A21B-82AF08C23215",
                                "1D531821-21B2-4F5F-8579-9724F10F8911",
                                "5C5AA48D-6598-4B55-91BB-1D043575C3B7",
                                "72FC842D-99A8-430C-A689-6DBB093015B5",
                                "11C3DA16-72B3-49A8-8B80-23637D0D499E",
                                "EBC61A4C-18C8-4374-9BDD-17BB93172453",
                                "B9E7FF3A-CD32-4414-8036-A4310FB4A80E",
                            ):
                                findSubChildAvailable = Sql.GetList(
                                    "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                                    + str(ParRecId)
                                    + "' AND DISPLAY_CRITERIA = 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                                )
                        if findSubChildAvailable is not None:
                            for findSubChildOne in findSubChildAvailable:
                                NewList = []
                                ParRecId = str(findSubChildOne.TREE_NODE_RECORD_ID)
                                # if getAccounts is None:
                                findSubChildAvailable1 = Sql.GetList(
                                    "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                                    + str(ParRecId)
                                    + "' AND DISPLAY_CRITERIA != 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                                )
                                try:
                                    getZ0009 = Sql.GetFirst(
                                        "SELECT CpqTableEntryId,SERVICE_ID FROM SAQTSV (NOLOCK) WHERE SERVICE_ID IN ('Z0009','Z0010','Z0128') AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(
                                            self.contract_quote_record_id, self.quote_revision_record_id
                                        )
                                    )
                                    if getZ0009 is not None:
                                        is_pmsa = self.PMSATree(getZ0009.SERVICE_ID)
                                    else:
                                        is_pmsa = 0
                                except:
                                    is_pmsa = 0
                                if is_pmsa:
                                    if ParRecId in (
                                        "1F47A350-4E38-41C9-A5C5-F53DC9BB3DB8",
                                        "B7BC662B-91A4-42C0-A2D9-B1E713D59E18",
                                        "1CE55561-F2DF-4A05-A21B-82AF08C23215",
                                        "1D531821-21B2-4F5F-8579-9724F10F8911",
                                        "5C5AA48D-6598-4B55-91BB-1D043575C3B7",
                                        "72FC842D-99A8-430C-A689-6DBB093015B5",
                                        "11C3DA16-72B3-49A8-8B80-23637D0D499E",
                                        "EBC61A4C-18C8-4374-9BDD-17BB93172453",
                                        "B9E7FF3A-CD32-4414-8036-A4310FB4A80E",
                                    ):
                                        findSubChildAvailable = Sql.GetList(
                                            "SELECT TOP 1000 * FROM SYTRND (nolock) WHERE PARENT_NODE_RECORD_ID='"
                                            + str(ParRecId)
                                            + "' AND DISPLAY_CRITERIA = 'DYNAMIC' ORDER BY abs(DISPLAY_ORDER) "
                                        )
                                if findSubChildAvailable1 is not None:
                                    for findSubChildOne in findSubChildAvailable1:
                                        parobj = str(findSubChildOne.PARENTNODE_OBJECT)
                                        NodeType = str(findSubChildOne.NODE_TYPE)
                                        NodeApiName = str(findSubChildOne.NODE_DISPLAY_NAME)
                                        DynamicQuery = str(findSubChildOne.DYNAMIC_NODEDATA_QUERY)
                                        PageRecId = str(findSubChildOne.NODE_PAGE_RECORD_ID)
                                        ordersBy = str(findSubChildOne.ORDERS_BY)
                                        ParRecId = str(findSubChildOne.TREE_NODE_RECORD_ID)
                                        if parobj == "True":
                                            where_string = (
                                                " " + str(where_string) + " AND " + str(oldNodeApiName) + " = '" + str(NodeText) + "'"
                                            )
                                            SubChildData = self.getChildFromParentObj(
                                                NodeText,
                                                NodeType,
                                                NodeName,
                                                RecAttValue,
                                                nodeId,
                                                ParRecId,
                                                DynamicQuery,
                                                ObjectName,
                                                RecId,
                                                where_string,
                                                PageRecId,
                                                ObjectRecId,
                                                NodeApiName,
                                                ordersBy,
                                                lock_icon,
                                            )
                                        else:
                                            if NodeNameValue != "":
                                                Node_name = NodeNameValue
                                            else:
                                                Node_name = oldNodeApiName
                                            if NodeTextValue != "":
                                                NodeText = NodeTextValue
                                            SubNodeName = str(findSubChildOne.NODE_DISPLAY_NAME)
                                            SubNodeName = str(findSubChildOne.NODE_DISPLAY_NAME)
                                            SubParRecId = str(findSubChildOne.TREE_NODE_RECORD_ID)
                                            subDynamicQuery = str(findSubChildOne.DYNAMIC_NODEDATA_QUERY)
                                            SubNodeType = str(findSubChildOne.NODE_TYPE)
                                            nodeId = str(findSubChildOne.NODE_ID)
                                            where_string = (
                                                " " + str(where_string) + " AND " + str(Node_name) + " = '" + str(NodeText) + "'"
                                            )
                                            Subwhere_string = str(where_string)
                                            PageRecId = str(findSubChildOne.NODE_PAGE_RECORD_ID)
                                            if ACTION != "ADDNEW":
                                                SubChildData = self.getChildOne(
                                                    SubNodeType,
                                                    SubNodeName,
                                                    RecAttValue,
                                                    nodeId,
                                                    NodeText,
                                                    SubParRecId,
                                                    subDynamicQuery,
                                                    ObjectName,
                                                    RecId,
                                                    Subwhere_string,
                                                    PageRecId,
                                                    ObjectRecId,
                                                    ordersBy,
                                                    lock_icon,
                                                )
                                        if len(SubChildData) > 0:
                                            NewList.append(SubChildData)
                                            list2 = []
                                            for sublist in NewList:
                                                for item in sublist:
                                                    list2.append(item)
                                            ChildDict["nodes"] = list2

                            ChildList.append(ChildDict)

                    return ChildList

    def getSubtabRelatedDetails(self, subTabName, type, ObjRecId, RelatedId, RelatedName):
        SubTabDict = {}
        DetailList = []
        DetailDict = {}
        if type == "OBJECT SECTION LAYOUT":
            sectObj = Sql.GetList(
                "SELECT DISTINCT SYSECT.RECORD_ID FROM SYSECT (NOLOCK) WHERE SYSECT.PRIMARY_OBJECT_RECORD_ID = '"
                + str(ObjRecId)
                + "' AND SYSECT.PAGE_RECORD_ID = ''"
            )
            if sectObj is not None:
                for section in sectObj:
                    DetailList.append(section.RECORD_ID)
                DetailDict.update({"Detail": DetailList})
                # syojhObj=Sql.GetFirst("SELECT OBJECT_NAME FROM SYOBJH (NOLOCK) WHERE RECORD_ID='"+str(ObjRecId) +"'")
                # if syojhObj is not None:
                # DetailDict.update({"ObjectName": syojhObj.OBJECT_NAME})
                SubTabDict.update({subTabName: DetailDict})

        if type == "OBJECT RELATED LAYOUT":
            RelatedDict = {}
            RelatedDict.update({str(RelatedId): str(RelatedName)})
            SubTabDict = {}
            RelatedList = []
            RelatedList.append(RelatedDict)
            RelDict = {}
            RelDict.update({"Related": RelatedList})
            SubTabDict.update({subTabName: RelDict})
        Trace.Write("SubTabDict------>"+str(SubTabDict))
        return SubTabDict

    def getPageRelatedDetails(self, subTabName, pageType, objRecId, ObjectRecId, querystr):
        SubTabDict = {}
        DetailList = []
        DetailDict = {}
        if pageType == "OBJECT PAGE LISTGRID":
            RelatedObj = Sql.GetList(
                "SELECT RECORD_ID, SAPCPQ_ATTRIBUTE_NAME, NAME FROM SYOBJR (NOLOCK) WHERE PARENT_LOOKUP_REC_ID = '"
                + str(ObjectRecId)
                + "' AND OBJ_REC_ID = '"
                + str(objRecId)
                + "' AND VISIBLE = 'True' "
                + str(querystr)
                + ""
            )
            if RelatedObj is not None:
                RelatedDict = {}
                for rel in RelatedObj:
                    RelatedDict = {}
                    RelatedDict.update({rel.SAPCPQ_ATTRIBUTE_NAME: rel.NAME})
                SubTabDict = {}
                RelatedList = []
                RelatedList.append(RelatedDict)
                RelDict = {}
                RelDict.update({"Related": RelatedList})
                SubTabDict.update({subTabName: RelDict})

        if pageType == "OBJECT PAGE LAYOUT":
            sectObj = Sql.GetList(
                "SELECT DISTINCT SYSECT.RECORD_ID FROM SYSECT (NOLOCK) WHERE SYSECT.PRIMARY_OBJECT_RECORD_ID = '"
                + str(objRecId)
                + "' AND SYSECT.PAGE_RECORD_ID = ''"
            )
            if sectObj is not None:
                for section in sectObj:
                    DetailList.append(section.RECORD_ID)
                DetailDict.update({"Detail": DetailList})
                SubTabDict.update({subTabName: DetailDict})
        # Trace.Write("=====================> SubTabDict"+str(SubTabDict))
        return SubTabDict

    # A055S000P01-4578 starts
    def pricing_picklist(self):
        if ACTION == "VIEW":
            try:
                picklist = Quote.GetCustomField("PRICING_PICKLIST").Content
            except:
                picklist = ""
            return picklist
        elif ACTION == "ONCHANGE":
            try:
                picklist_value = Param.picklist_value
            except:
                picklist_value = ""
            Quote.GetCustomField("PRICING_PICKLIST").Content = picklist_value
            return True

    # A055S000P01-4578 ends

    def PMSATree(self, TreeParam):
        flag = 0
        if str(Product.GetGlobal("SERVICE")) == "Z0009" or str(Product.GetGlobal("SERVICE")) == "Z0010" or str(Product.GetGlobal("SERVICE")) == "Z0128":
            TableName = "SAQTSE"			
            entitlement_obj = SqlHelper.GetFirst(
                "select replace(ENTITLEMENT_XML,'&',';#38') as ENTITLEMENT_XML from {} (nolock) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' and SERVICE_ID = '{}' ".format(
                    TableName, self.contract_quote_record_id, self.quote_revision_record_id, TreeParam
                )
            )

            quote_item_tag = re.compile(r"(<QUOTE_ITEM_ENTITLEMENT>[\w\W]*?</QUOTE_ITEM_ENTITLEMENT>)")
            pattern_consumable = re.compile(r"<ENTITLEMENT_ID>AGS_[^>]*?_PQB_QTETYP</ENTITLEMENT_ID>")
            pattern_new_parts_only_yes = re.compile(r"<ENTITLEMENT_DISPLAY_VALUE>Flex Event Based</ENTITLEMENT_DISPLAY_VALUE>")
            pattern_new_parts_only = re.compile(r"<ENTITLEMENT_DISPLAY_VALUE>Event Based</ENTITLEMENT_DISPLAY_VALUE>")
            pattern_new_parts_Z0010 = re.compile(r"<ENTITLEMENT_DISPLAY_VALUE>Event based</ENTITLEMENT_DISPLAY_VALUE>")
            # Trace.Write("PMSA----->"+str(pattern_new_parts_only_yes))
            entitlement_xml = entitlement_obj.ENTITLEMENT_XML
            for m in re.finditer(quote_item_tag, entitlement_xml):
                sub_string = m.group(1)
                # Trace.Write("substring----->"+str(sub_string))
                attribute_id = re.findall(pattern_consumable, sub_string)
                attribute = re.findall(pattern_new_parts_only, sub_string)
                attribute_value = re.findall(pattern_new_parts_only_yes, sub_string)
                attribute_Z0010 = re.findall(pattern_new_parts_Z0010, sub_string)
                # Trace.Write("attrvalue----->"+str(attribute_value))
                if len(attribute_id) != 0 and (len(attribute_value) != 0 or len(attribute) != 0 or len(attribute_Z0010) != 0):
                    Trace.Write("YES 3440")
                    flag = 1
                    break
        if flag == 1:
            return 1
        else:
            return 0

tree = TreeView()
try:
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
    try:
        GetActiveRevision = Sql.GetFirst(
            "SELECT QUOTE_REVISION_RECORD_ID,QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='{}' AND ACTIVE = 1".format(
                Quote.CompositeNumber
            )
        )
        if GetActiveRevision:
            Quote.SetGlobal("quote_revision_record_id", GetActiveRevision.QUOTE_REVISION_RECORD_ID)
            Quote.SetGlobal("quote_rev_id", str(GetActiveRevision.QTEREV_ID))
            quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
    except Exception as e:
        Trace.Write("error------" + str(e))
        quote_revision_record_id = ""
if not quote_revision_record_id and quote_revision_record_id != "":
    try:
        GetActiveRevision = Sql.GetFirst(
            "SELECT QUOTE_REVISION_RECORD_ID,QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='{}' AND ACTIVE = 1".format(
                Quote.CompositeNumber
            )
        )
    except:
        GetActiveRevision = ""
    if GetActiveRevision:
        Quote.SetGlobal("quote_revision_record_id", GetActiveRevision.QUOTE_REVISION_RECORD_ID)
        Quote.SetGlobal("quote_rev_id", str(GetActiveRevision.QTEREV_ID))
        quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")

LOAD = Param.LOAD
try:
    ACTION = Param.ACTION
except:
    ACTION = ""
try:
    Currenttab = Param.Currenttab
except:
    Currenttab = ""
try:
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    TabName = str(TestProduct.CurrentTab)
    ProductName = str(TestProduct.Name)
except Exception:
    TabName = "Quote"
    ProductName = "Sales"

    variable_type_selectval = childQuery = ""
try:
    entitlement_level_flag = Param.entitlement_level_flag
except:
    entitlement_level_flag = ""

if LOAD == "Treeload":
    ApiResponse = ApiResponseFactory.JsonResponse(tree.CommonDynamicLeftTreeView())	
elif LOAD == "CommonGlobalSet":
    AllTreeParamsValue = {
        "TreeParam": "",
        "TreeParentLevel0": "",
        "TreeParentLevel1": "",
        "TreeParentLevel2": "",
        "TreeParentLevel3": "",
        "TreeParentLevel4": "",
        "TreeParentLevel5": "",
        "TreeParentLevel6": "",
        "TreeParentLevel7": "",
        "TreeParentLevel8": "",
    }
    # SAP Performance improvement fix -start
    try:
        for key, value in AllTreeParamsValue.items():
            Product.SetGlobal(str(key), "")
    except Exception:
        pass
    # SAP Performance improvement fix -end
    AllTreeParams = Param.AllTreeParams
    AllTreeParamsValue = eval(AllTreeParams)
    #Trace.Write("GetTreeParamValues" + str(AllTreeParams))
    
    for key, value in AllTreeParamsValue.items():
        #Trace.Write("check12345"+str(value))
        Product.SetGlobal(str(key), str(value))
elif LOAD == "GlobalSet":
    try:
        TreeParam = Param.TreeParam
    except Exception:
        TreeParam = ""
    try:
        TreeParentParam = Param.TreeParentParam
    except Exception:
        TreeParentParam = ""
    try:
        TreeSuperParentParam = Param.TreeSuperParentParam
    except Exception:
        TreeSuperParentParam = ""
    try:
        TreeTopSuperParentParam = Param.TreeTopSuperParentParam
    except Exception:
        TreeTopSuperParentParam = ""
    try:
        TreeSuperTopParentParam = Param.TreeSuperTopParentParam
    except Exception:
        TreeSuperTopParentParam = ""

    try:
        TreeFirstSuperTopParentParam = Param.TreeFirstSuperTopParentParam
    except Exception:
        TreeFirstSuperTopParentParam = ""

    Product.SetGlobal("CommonTreeParam", str(TreeParam))
    Product.SetGlobal("CommonTreeParentParam", str(TreeParentParam))
    Product.SetGlobal("CommonTreeSuperParentParam", str(TreeSuperParentParam))
    Product.SetGlobal("CommonTreeTopSuperParentParam", str(TreeTopSuperParentParam))
    Product.SetGlobal("CommonTopTreeSuperParentParam", str(TreeSuperTopParentParam))
    Product.SetGlobal("CommonTreeFirstSuperTopParentParam", str(TreeFirstSuperTopParentParam))

# A055S000P01-4578 starts
elif LOAD == "PRICING PICKLIST":
    ApiResponse = ApiResponseFactory.JsonResponse(tree.pricing_picklist())
##A055S000P01-4578 ends
##else:
##Trace.Write("elsee")
# ApiResponse = ApiResponseFactory.JsonResponse(tree.CommonLeftTreeView())

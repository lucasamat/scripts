# =========================================================================================================================================
#   __script_name : SYLDRLADBN.PY
#   __script_description : THIS SCRIPT IS USED TO SHOW AND HIDE ACTION BUTTONS AND RELATED LISTS ON A PAGE BASED ON THE MODES SUCH AS VIEW,
#                          EDIT, CLONE.  THE SCRIPT IS USED ACROSS ALL MODULES.
#   __primary_author__ : JOE EBENEZER
#   Â© BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom
import Webcom.Configurator.Scripting.Test.TestProduct

Webcom = Webcom  # pylint: disable=E0602
Trace = Trace  # pylint: disable=E0602
User = User  # pylint: disable=E0602
Product = Product  # pylint: disable=E0602
ScriptExecutor = ScriptExecutor  # pylint: disable=E0602
AttributeAccess = AttributeAccess  # pylint: disable=E0602
Session = Session  # pylint: disable=E0602
# pylint: disable = no-name-in-module, import-error, multiple-imports, pointless-string-statement, wrong-import-order

from datetime import date, datetime
from SYDATABASE import SQL  # pylint: disable=F0401
import math

Sql = SQL()


get_user_id = Session["USERID"]

# GET TEST PRODUCT AND PRODUCT NAME
TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
Product.SetGlobal("LoggedUserId", str(User.Id))
Product.SetGlobal("LoggedUserName", str(User.UserName))
productName, priceModelFlag = Product.Name, Product.GetGlobal("Pricemodel")

productAttributesGetByName = lambda productAttribute: Product.Attributes.GetByName(productAttribute)
get_user_id = User.Id
Current_sec_Recid = Product.GetGlobal("SEC_REC_ID")
#Trace.Write('SEC_REC_ID-Current_sec_Recid------'+str(Current_sec_Recid))
class ButtonAction:
    def __init__(self):
        """Use for initialization"""
        self.exceptMessage = ""

    def setAllowedAttribute(self, productAttribute, value):
        #Trace.Write("setAllowedAttributesetAllowedAttribute--->"+str(value))
        if isinstance(productAttribute, str):
            productAttribute = productAttributesGetByName(productAttribute)
        if productAttribute is not None:
            productAttribute.Allowed = value

    def productsAttributesPermission(self):
        if productName != "":
            if TestProduct != "":
                # GET THE CURRENT TAB NAME
                TabName = str(TestProduct.CurrentTab)
                # GET THE RELATED TAB NAME
                getTabDetails = Sql.GetFirst(
                    "SELECT TOP 1000 TAB_LABEL FROM SYTABS (NOLOCK) WHERE SAPCPQ_ALTTAB_NAME = '"
                    + str(TabName)
                    + "' AND RTRIM(LTRIM(APP_LABEL))='"
                    + str(productName)
                    + "' ORDER BY DISPLAY_ORDER "
                )

                if getTabDetails is not None:
                    found = (getTabDetails.TAB_LABEL).strip()
                    if found != TabName:
                        TabName = getTabDetails.TAB_LABEL

                # GET ADDNEW BUTTON NAME
                Addnew = "BTN_" + str(TabName).replace(" ", "_").upper() + "_ADDNEW"
                #Trace.Write("Addnew---68----"+str(Addnew))

            if str(TabName).strip() != "":
                # GET RECORD ID FOR CURRENT TAB
                SYTABS_OBJNAME = Sql.GetFirst(
                    "select top 1 RECORD_ID from SYTABS (nolock) where  RTRIM(LTRIM(TAB_LABEL)) ='"
                    + str(TabName).strip()
                    + "' and RTRIM(LTRIM(APP_LABEL))='"
                    + str(productName)
                    + "' order by DISPLAY_ORDER"
                )

                # RESTRICT BUTTON ACTIONS FOR SET TYPE IN SET TAB
                flag, myAttribute = True, productAttributesGetByName("QSTN_SYSEFL_MA_00077")
                if myAttribute and str(TabName).strip().upper() == "SETS":
                    Value = myAttribute.GetValue()
                    if Value != "VARIANT SET" and Value != "ZMAT SET":
                        flag = False

                if SYTABS_OBJNAME is not None:
                    Question_Rec_Id, TABLE_RECORDID, TAB_RECID = "", "", str(SYTABS_OBJNAME.RECORD_ID).strip()
                    '''SYSECT_OBJNAME_OBJ = Sql.GetFirst(
                        "SELECT TOP 1000 SYSECT.RECORD_ID,SYSECT.SAPCPQ_ATTRIBUTE_NAME,SYSECT.PRIMARY_OBJECT_NAME,SYSECT.PRIMARY_OBJECT_RECORD_ID FROM SYSECT (NOLOCK) "
                        + " INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID WHERE SYPAGE.TAB_RECORD_ID ='"
                        + TAB_RECID
                        + "' ORDER BY SYSECT.DISPLAY_ORDER "
                    )'''
                    SYSECT_OBJNAME_OBJ = Sql.GetFirst(
                        "SELECT TOP 1000 SYSECT.RECORD_ID,SYSECT.SAPCPQ_ATTRIBUTE_NAME,SYSECT.PRIMARY_OBJECT_NAME,SYSECT.PRIMARY_OBJECT_RECORD_ID FROM SYSECT (NOLOCK)  INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID AND SYPAGE.OBJECT_RECORD_ID = SYSECT.PRIMARY_OBJECT_RECORD_ID  inner join SYPRSN (NOLOCK) on SYPRSN.SECTION_RECORD_ID = SYSECT.RECORD_ID INNER JOIN USERS_PERMISSIONS (NOLOCK)  ON USERS_PERMISSIONS.PERMISSION_ID = SYPRSN.PROFILE_RECORD_ID WHERE SYPAGE.TAB_RECORD_ID ='"
                        + TAB_RECID
                        + "'  AND SYPRSN.VISIBLE = 1 and USERS_PERMISSIONS.USER_ID = '"
                        + str(get_user_id)
                        + "' ORDER BY SYSECT.DISPLAY_ORDER "
                    )

                    if SYSECT_OBJNAME_OBJ is not None:
                        # CURRENT TABLE NAME AND RECORD ID
                        TABLE_NAME, TABLE_RECORDID = (
                            (SYSECT_OBJNAME_OBJ.PRIMARY_OBJECT_NAME).strip(),
                            (SYSECT_OBJNAME_OBJ.PRIMARY_OBJECT_RECORD_ID).strip(),
                        )
                    #A055S000P01-3428 start
                    '''SYSECT_OBJNAME = Sql.GetList(
                        "SELECT TOP 1000 SYSECT.RECORD_ID,SYSECT.PRIMARY_OBJECT_NAME,SYSECT.PRIMARY_OBJECT_RECORD_ID,SYSECT.SAPCPQ_ATTRIBUTE_NAME,SYSECT.SUPPRESS_BANNER FROM SYSECT (NOLOCK) "
                        + " INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID WHERE SYPAGE.TAB_RECORD_ID ='"
                        + TAB_RECID
                        + "' ORDER BY SYSECT.DISPLAY_ORDER "
                    )'''
                    SYSECT_OBJNAME = Sql.GetList(
                        "SELECT TOP 1000 SYSECT.RECORD_ID,SYSECT.PRIMARY_OBJECT_NAME,SYSECT.PRIMARY_OBJECT_RECORD_ID,SYSECT.SAPCPQ_ATTRIBUTE_NAME,SYSECT.SUPPRESS_BANNER FROM SYSECT (NOLOCK) INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID inner join SYPRSN on SYPRSN.SECTION_RECORD_ID = SYSECT.RECORD_ID INNER JOIN USERS_PERMISSIONS (NOLOCK)  ON USERS_PERMISSIONS.PERMISSION_ID = SYPRSN.PROFILE_RECORD_ID WHERE SYPAGE.TAB_RECORD_ID ='"
                        + TAB_RECID
                        + "' and SYPRSN.VISIBLE = 1 AND USERS_PERMISSIONS.USER_ID = '"
                        + str(get_user_id)
                        + "' ORDER BY SYSECT.DISPLAY_ORDER "
                    )
                    #A055S000P01-3428 end
                    if SYSECT_OBJNAME is not None:
                        for SYSECT_DETAILS in SYSECT_OBJNAME:
                            # GET AUTO NUMBER COLUMN NAME FROM SYOBJH TABLE
                            SYOBJH_OBJ = Sql.GetFirst(
                                "SELECT RECORD_ID,RECORD_NAME FROM SYOBJH (NOLOCK) WHERE OBJECT_NAME='"
                                + str(TABLE_NAME).strip()
                                + "'"
                            )

                            if SYOBJH_OBJ is not None:
                                # GET THE AUTO NUMBER ATTRIBUTE NAME FROM SYSEFL TABLE
                                if str(SYSECT_DETAILS.RECORD_ID) is not None:
                                    QUE_OBJ = Sql.GetFirst(
                                        "Select RECORD_ID, SAPCPQ_ATTRIBUTE_NAME from SYSEFL (NOLOCK) where RTRIM(LTRIM(API_FIELD_NAME))='"
                                        + str(SYOBJH_OBJ.RECORD_NAME).strip()
                                        + "' and RTRIM(LTRIM(API_NAME))='"
                                        + str(TABLE_NAME).strip()
                                        + "' and SECTION_RECORD_ID='"
                                        + str(SYSECT_DETAILS.RECORD_ID)
                                        + "' "
                                    )

                                    if QUE_OBJ is not None:
                                        QUE_REC = str(QUE_OBJ.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
                                        QUE_REC_NAME = (QUE_REC).upper()
                                        Question_Rec_Id = "QSTN_" + str(QUE_REC_NAME)
                            all_lookuplist = []  # A043S001P01-15458
                            sec_loouplist = []
                            SYOBJD_OBJ = Sql.GetList(
                                "Select API_NAME, OBJECT_NAME,IS_KEY from  SYOBJD (NOLOCK) where  DATA_TYPE='FORMULA' and OBJECT_NAME='"
                                + str(TABLE_NAME)
                                + "' "
                            )
                            if SYOBJD_OBJ is not None:
                                for SYOBJD_Details in SYOBJD_OBJ:
                                    QUE_OBJ = Sql.GetFirst(
                                        "Select RECORD_ID,SAPCPQ_ATTRIBUTE_NAME,API_NAME, SECTION_NAME, FIELD_LABEL from SYSEFL (NOLOCK) where API_FIELD_NAME='"
                                        + str(SYOBJD_Details.API_NAME).strip()
                                        + "' and API_NAME='"
                                        + str(TABLE_NAME).strip()
                                        + "' and SECTION_RECORD_ID='"
                                        + str(SYSECT_DETAILS.RECORD_ID)
                                        + "' "
                                    )
                                    #Trace.Write(
                                    #    "====Select RECORD_ID,SAPCPQ_ATTRIBUTE_NAME,API_NAME, SECTION_NAME, FIELD_LABEL from SYSEFL (NOLOCK) where API_FIELD_NAME='"
                                    #    + str(SYOBJD_Details.API_NAME).strip()
                                    #    + "' and API_NAME='"
                                    #    + str(TABLE_NAME).strip()
                                    #    + "' and SECTION_RECORD_ID='"
                                    #    + str(SYSECT_DETAILS.RECORD_ID)
                                    #    + "'"
                                    #)
                                    LKP_OBJ = Sql.GetFirst(
                                        "Select RECORD_ID,SAPCPQ_ATTRIBUTE_NAME,API_NAME, SECTION_NAME, FIELD_LABEL from SYSEFL (NOLOCK) where API_FIELD_NAME='"
                                        + str(SYOBJD_Details.API_NAME).strip()
                                        + "' and API_NAME='"
                                        + str(TABLE_NAME).strip()
                                        + "' and SECTION_RECORD_ID='"
                                        + str(Current_sec_Recid)
                                        + "' "
                                    )
                                    Trace.Write("lookup query")
                                    if LKP_OBJ is not None:
                                        sec_loouplist.append(
                                            str(LKP_OBJ.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
                                        )
                                        #Trace.Write("sec_loouplist" + str(sec_loouplist))
                                    if QUE_OBJ :
                                        #Trace.Write("SAPCPQ_ATTRIBUTE_NAME--195--->"+str(QUE_OBJ.SAPCPQ_ATTRIBUTE_NAME))
                                        
                                        LKP_ATTR = str(QUE_OBJ.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
                                        #Trace.Write("RECORD_ID-----198---->"+str(LKP_ATTR))
                                        LKP_NAME = (LKP_ATTR).upper()
                                        Attr_Id = "QSTN_" + str(LKP_NAME)
                                        RECORD_ID = "QSTN_LKP_" + str(LKP_NAME)
                                        #Trace.Write("RECORD_ID--------->"+str(RECORD_ID))
                                        recIdAttributes, attributeIdAttributes = (
                                            productAttributesGetByName(str(RECORD_ID).strip()),
                                            productAttributesGetByName(str(Attr_Id).strip()),
                                        )
                                        all_lookuplist.append(LKP_ATTR)  # A043S001P01-15458
                                        #Trace.Write("all_lookuplist" + str(all_lookuplist))
                                        #Trace.Write("QSTN----" + str(Attr_Id) + "--QSTN_LKP--" + str(RECORD_ID))
                                        SEC_SUP_BANNER = str(SYSECT_DETAILS.SUPPRESS_BANNER)
                                        SEC_ATTR = (
                                            str(SYSECT_DETAILS.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
                                        )
                                        Sec_id = "SEC_" + str(SEC_ATTR)
                                        

                                        #Trace.Write("TESTZ_CHK--value----"+str(value))
                                         
                                        if Sec_id is not None:
                                            if str(SEC_SUP_BANNER).upper() == "TRUE":
                                                Product.Attributes.GetByName(Sec_id).Allowed = False
                                                
                                            if value == "ADDNEW":
                                                if str(QUE_OBJ.SECTION_NAME) == "AUDIT INFORMATION":
                                                    Product.Attributes.GetByName(Sec_id).Allowed = False
                                                   
                                            elif value == "VIEW":
                                                if str(QUE_OBJ.SECTION_NAME) == "AUDIT INFORMATION":
                                                    Product.Attributes.GetByName(Sec_id).Allowed = True
                                            


                                                       
                                        
                                        if recIdAttributes is not None:
                                            if value == "ADDNEW":
                                                #Trace.Write("standardreportingcurrencyyyyyyyyyy2222222")
                                                """if Product.Attributes.GetByName("QSTN_SYSEFL_SE_03346") is not None:
                                                    #Product.Attributes.GetByName(str("QSTN_SYSEFL_SE_03346")).Allowed=False
                                                    #Product.Attributes.GetByName(str("QSTN_SYSEFL_SE_03346")).Access = AttributeAccess.ReadOnly"""

                                                recIdAttributes.Allowed = True
                                                Trace.Write("Audit information")
                                                if attributeIdAttributes is not None and TABLE_NAME != "PRLPBS":
                                                    attributeIdAttributes.Access = AttributeAccess.ReadOnly
                                                if str(QUE_OBJ.FIELD_LABEL) in [
                                                    "Added Date",
                                                    "Added By",
                                                    "Last Modified By",
                                                    "Last Modified Date",
                                                ]:
                                                    attributeIdAttributes.Access.Allowed = False
                                                    
                                            elif value == "VIEW":
                                                #Product.Attributes.GetByName('QSTN_SYSEFL_PR_00022').Access = AttributeAccess.ReadOnly 
                                                #Product.Attributes.GetByName('QSTN_SYSEFL_PR_00017').Access = AttributeAccess.ReadOnly
                                                if recIdAttributes is not None:
                                                    recIdAttributes.Allowed = False
                                            elif value == "EDIT":
                                                #Trace.Write("RECORD_IDRECORD_IDRECORD_ID--->"+str(RECORD_ID))
                                                recIdAttributes.Allowed = True
                                                if str(SYOBJD_Details.OBJECT_NAME) == "PASGMT":
                                                    productAttributesGetByName(
                                                        "QSTN_SYSEFL_SE_00158"
                                                    ).Access = AttributeAccess.ReadOnly
                                                    productAttributesGetByName("QSTN_LKP_SYSEFL_SE_00158").HintFormula = ""
                                                if str(SYOBJD_Details.OBJECT_NAME) == "MACATG":
                                                    Flag_val = str(SYOBJD_Details.IS_KEY)
                                                    if Flag_val != "" and Flag_val is not None:
                                                        if Flag_val.upper() == "TRUE":
                                                            ATTR_Id = (
                                                                str(QUE_OBJ.SAPCPQ_ATTRIBUTE_NAME)
                                                                .replace("-", "_")
                                                                .replace(" ", "")
                                                            )
                                                            ATTR_NAME = (ATTR_Id).upper()
                                                            Attr_Id = "QSTN_" + str(ATTR_NAME)
                                                            if attributeIdAttributes is not None:
                                                                attributeIdAttributes.Access = AttributeAccess.ReadOnly
                                                if str(SYOBJD_Details.OBJECT_NAME) == "SVPGTY":
                                                    Product.Attributes.GetByName(
                                                        "QSTN_SYSEFL_SV_00095"
                                                    ).Access = AttributeAccess.Editable
                                        if value == "SEG_EDIT":
                                            #Trace.Write('188-------------------'+str(value))
                                            if len(all_lookuplist) > 0:
                                                if len(sec_loouplist) >= 0:
                                                    for LKP_VAL in all_lookuplist:
                                                        #Trace.Write("LKP_VAL1-294----> " + str(LKP_VAL))
                                                        if LKP_VAL not in sec_loouplist:
                                                            LKP_RECORD = "QSTN_LKP_" + str(LKP_VAL)
                                                            if Product.Attributes.GetByName(str(LKP_RECORD)):
                                                                Trace.Write(
                                                                    "Lookup Before->"
                                                                    + str(
                                                                        Product.Attributes.GetByName(str(LKP_RECORD)).Allowed
                                                                    )
                                                                )
                                                                Product.Attributes.GetByName(str(LKP_RECORD)).Allowed = False
                                                                Trace.Write(
                                                                    "Lookup After->"
                                                                    + str(
                                                                        Product.Attributes.GetByName(str(LKP_RECORD)).Allowed
                                                                    )
                                                                )
                                                        else:
                                                            #Trace.Write('311-----' + str(LKP_VAL))
                                                            LKP_RECORD = "QSTN_LKP_" + str(LKP_VAL)
                                                            #Trace.Write('311---LKP_RECORD--' + str(LKP_RECORD))
                                                            if Product.Attributes.GetByName(str(LKP_RECORD)):
                                                                Product.Attributes.GetByName(str(LKP_RECORD)).Allowed = True

                        """SYOBJROBJ = Sql.GetList(
                            " SELECT TOP 1000 RECORD_ID,SAPCPQ_ATTRIBUTE_NAME FROM SYOBJR (NOLOCK) MR JOIN SYPRJR (NOLOCK) SR ON"
                            + " MR.RECORD_ID = SR.RELATED_LIST_RECORD_ID JOIN SYPRUS (NOLOCK) SS ON SS.PROFILE_RECORD_ID = SR.PROFILE_RECORD_ID"
                            + " WHERE MR.PARENT_LOOKUP_REC_ID ='"
                            + str(TABLE_RECORDID).strip()
                            + "' AND SR.VISIBLE = 1 AND SS.USER_RECORD_ID = '"
                            + str(get_user_id)
                            + "'"
                        )"""
                        SYOBJROBJ = Sql.GetList(
                            " SELECT TOP 1000 RECORD_ID,SAPCPQ_ATTRIBUTE_NAME FROM SYOBJR (NOLOCK)  WHERE PARENT_LOOKUP_REC_ID ='"
                            + str(TABLE_RECORDID).strip()
                            + "' AND VISIBLE = 1"
                        )
                        if SYOBJROBJ is not None:
                            for attr in SYOBJROBJ:
                                CTR_ATTR = str(attr.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")
                                CTR_Name = "QSTN_R_" + str(CTR_ATTR)
                                ctrAttributes = Product.Attributes.GetByName(str(CTR_Name))
                                if ctrAttributes is not None:
                                    if value in ["CLONE", "EDIT", "ADDNEW"]:
                                        ctrAttributes.Allowed = False
                                    if value == "VIEW":
                                        ctrAttributes.Allowed = True

                        ADD = EDIT = DELETE = ""
                        # GET NEED ACTION BUTTON NAMES FROM SYOBJS TABLE
                        SYOBJS_OBJNAME = Sql.GetFirst(
                            "SELECT NAME,CAN_ADD,CAN_EDIT,CAN_DELETE,COLUMNS,CONTAINER_NAME,OBJ_REC_ID FROM SYOBJS (NOLOCK) WHERE OBJ_REC_ID ='"
                            + str(TABLE_RECORDID)
                            + "' AND UPPER(NAME)='TAB LIST'"
                        )
                        if SYOBJS_OBJNAME is not None:
                            ADD, EDIT, DELETE = (
                                str(SYOBJS_OBJNAME.CAN_ADD).strip(),
                                str(SYOBJS_OBJNAME.CAN_EDIT).strip(),
                                str(SYOBJS_OBJNAME.CAN_DELETE).strip(),
                            )

                        # GET ACTION BUTTON RECORD ID AND NAME FORM SYPSAC TABLE
                        SYACTI_OBJNAME = Sql.GetList(
                            "SELECT PAGEACTION_RECORD_ID,SAPCPQ_ATTRIBUTE_NAME,ACTION_NAME, TAB_NAME FROM SYPGAC (NOLOCK) WHERE TAB_RECORD_ID='"
                            + TAB_RECID
                            + "' "
                        )
                        
                        all_lookuplist = []  # A043S001P01-15458
                        sec_loouplist = []
                        if SYACTI_OBJNAME is not None:
                            Trace.Write("Value_Test222")
                            attributeDictionary = {}
                            for ACTItem in SYACTI_OBJNAME:
                                Trace.Write("Value_Test111")
                                # GET ACTION BUTTON ATTRIBUTE NAME
                                ACTIONRECORDID = str(ACTItem.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_")
                                ACTIONNAME = str(ACTItem.ACTION_NAME).replace(" ", "")
                                actRawAttributeName = "BTN_" + (ACTIONRECORDID + "_" + ACTIONNAME).upper()
                                Trace.Write("Button ID--actRawAttributeName----" + str(actRawAttributeName))
                                Trace.Write("Value_Test" + str(value))
                                actAttributeName = productAttributesGetByName(str(actRawAttributeName))
                                #Trace.Write("Button attr ID--" + str(actAttributeName))
                                #attr_list = ['BTN_SYACTI_QT_00011_ADDFAB']
                                # if Product.Attributes.GetByName("BTN_SYACTI_QT_00011_ADDFAB"):                               
                                #     Product.Attributes.GetByName("BTN_SYACTI_QT_00011_ADDFAB").Allowed = False

                                if value == "INFO":
                                    if str(ACTItem.ACTION_NAME).upper() == "ADDNEW":
                                        addNewAttribute = productAttributesGetByName(str(Addnew))
                                        if ADD.upper() == "TRUE" and addNewAttribute is not None:
                                            addNewAttribute.Allowed = True
                                        elif addNewAttribute is not None:
                                            addNewAttribute.Allowed = False                                                                                 

                                if value == "EDIT":
                                    if (
                                        str(ACTItem.ACTION_NAME).upper() == "SAVE"
                                        or str(ACTItem.ACTION_NAME).upper() == "CANCEL"
                                    ) and actAttributeName:
                                        actAttributeName.Allowed = True
                                        actAttributeName.Allowed = True
                                    notAllowedActionsList = ["BACK TO LIST", "EDIT", "DELETE", "CLONE"]
                                    if str(ACTItem.ACTION_NAME).upper() in notAllowedActionsList:
                                        if actAttributeName is not None:
                                            btnactn.setAllowedAttribute(actAttributeName, False)
                                    for attributes in attributeDictionary:
                                        btnactn.setAllowedAttribute(attributeDictionary[attributes], True)

                                if value == "CLONE":
                                    allowedActionsList, notAllowedActionsList = (
                                        ["BACK TO LIST", "SAVE"],
                                        ["CANCEL", "EDIT", "DELETE", "CLONE"],
                                    )
                                    if str(ACTItem.ACTION_NAME).upper() in allowedActionsList:
                                        btnactn.setAllowedAttribute(actAttributeName, True)
                                        if str(ACTItem.ACTION_NAME).upper() == "BACK TO LIST":
                                            actAttributeName.HintFormula = "CANCEL"
                                    if str(ACTItem.ACTION_NAME).upper() in notAllowedActionsList:
                                        btnactn.setAllowedAttribute(actAttributeName, False)

                                if value == "VIEW" or value == "SEG_EDIT":
                                    Trace.Write(str(flag)+'------424---------------'+str(value))
                                    Trace.Write("value------" + str(value))
                                    if str(ACTItem.ACTION_NAME) == "DELETE" and actAttributeName is not None:
                                        actAttributeName.Allowed = (
                                            True if DELETE.upper() == "TRUE" and flag == "True" else False
                                        )
                                    for attributes in attributeDictionary:
                                        btnactn.setAllowedAttribute(attributeDictionary[attributes], True)
                                    if str(ACTItem.ACTION_NAME) == "EDIT" and actAttributeName is not None:
                                        if EDIT:
                                            actAttributeName.Allowed = (
                                                True if EDIT.upper() == "TRUE" and flag == "True" else False
                                            )
                                    allowedActionsList, notAllowedActionsList = ["BACK TO LIST", "CLONE"], ["CANCEL", "SAVE"]
                                    if str(ACTItem.ACTION_NAME) in allowedActionsList:
                                        btnactn.setAllowedAttribute(actAttributeName, True)
                                        if str(ACTItem.ACTION_NAME) == "BACK TO LIST":
                                            if actAttributeName is not None:
                                                actAttributeName.HintFormula = "BACK TO LIST"
                                    if str(ACTItem.ACTION_NAME) in notAllowedActionsList:
                                        btnactn.setAllowedAttribute(actAttributeName, False)

                                if value == "ADDNEW":
                                    if (
                                        str(ACTItem.ACTION_NAME) == "SAVE"
                                        and actAttributeName is not None
                                        and str(ACTItem.SAPCPQ_ATTRIBUTE_NAME) != "SYPSAC-PB-00018"
                                    ):
                                        
                                        actAttributeName.Allowed = True
                                    elif str(ACTItem.SAPCPQ_ATTRIBUTE_NAME) == "SYPSAC-SY-00056":
                                        actAttributeName.Allowed = False
                                    elif str(ACTItem.SAPCPQ_ATTRIBUTE_NAME) == "SYPSAC-PB-00018":
                                        actAttributeName.Allowed = False

                                    for attributes in attributeDictionary:
                                        btnactn.setAllowedAttribute(attributeDictionary[attributes], True)
                                    if str(ACTItem.ACTION_NAME) == "BACK TO LIST" and actAttributeName is not None:
                                        actAttributeName.Allowed, actAttributeName.HintFormula = True, "CANCEL"
                                    notAllowedActionsList = ["EDIT", "CANCEL", "DELETE", "CLONE"]
                                    if str(ACTItem.ACTION_NAME) in notAllowedActionsList:
                                        btnactn.setAllowedAttribute(actAttributeName, False)
                    QuestionRecId = productAttributesGetByName(Question_Rec_Id)
                    if QuestionRecId is not None:
                        QuestionRecId.DisplayType, QuestionRecId.Access = "FreeInputNoMatching", AttributeAccess.ReadOnly
                        if value in ["VIEW", "EDIT"]:
                            QuestionRecId.Allowed = True
                        elif value in ["CLONE", "ADDNEW"]:
                            QuestionRecId.Allowed = False
                    if value == "ADDNEW":                        
                        if myAttribute is not None:
                            Select_Date = myAttribute.GetValue()
                            if Select_Date != "":
                                selected_date = datetime.datetime.strptime(Select_Date, "%m/%d/%Y").date()
                                if selected_date < date.today():
                                    myAttribute.AssignValue("")


btnactn = ButtonAction()


# BY DEFAULT NOTIFICATION BANNER SETS TO FALSE
myAttribute = productAttributesGetByName("SEC_N_TAB_PAGE_ALERT")
if myAttribute  and myAttribute.HintFormula == "TAB PAGE ALERT":
    #myAttribute.HintFormula, myAttribute.Allowed = "", False
    myAttribute.Allowed = True     
# DECLARE LOCAL VARIABLES
QuestionRecId, val, TabName, TABLE_RECORDID = "", "Tab list", "", ""
# GET CURRENT ACTION
value = productAttributesGetByName("MA_MTR_TAB_ACTION").GetValue()
Trace.Write('')

if myAttribute is not None:
    Trace.Write("check inside else")
    if (str(TestProduct.CurrentTab) == 'Approval Chain' and str(TestProduct.Name) == 'APPROVAL CENTER') or str(TestProduct.Name) == 'SYSTEM ADMIN':
        #Trace.Write("check allowed view"+ str(myAttribute.Allowed)+str(myAttribute.HintFormula)+str(value))
        if value == "VIEW":
            myAttribute.Allowed = False
            myAttribute.HintFormula = ""
            #Trace.Write("check allowed view"+ str(myAttribute.Allowed))
        elif value == "EDIT":
            if (
                len(str(myAttribute.HintFormula)) == "0"
                or str(myAttribute.HintFormula) == "TAB PAGE ALERT"
                or str(myAttribute.HintFormula) == "NOTIFICATION"
            ):
                myAttribute.Allowed = False
                myAttribute.HintFormula = ""
 
    else:                     
               
        if value == "ADDNEW" or value == "VIEW":
            #Trace.Write('val00==='+str(value))
            # if myAttribute.HintFormula == "TAB PAGE ALERT":
            myAttribute.Allowed = False
            myAttribute.HintFormula = ""
            #Trace.Write("check allowed else"+ str(myAttribute.Allowed))
         
        elif value == "EDIT":
            if (
                len(str(myAttribute.HintFormula)) == "0"
                or str(myAttribute.HintFormula) == "TAB PAGE ALERT"
                or str(myAttribute.HintFormula) == "NOTIFICATION"
            ):
                myAttribute.Allowed = False
                myAttribute.HintFormula = ""


if str(value) != "" and value is not None:
    btnactn.productsAttributesPermission()


'''if TestProduct.CurrentTab == "Object":
    TableName = Product.Attributes.GetByName("QSTN_SYSEFL_SY_00517").GetValue()
    constraint_obj = Sql.GetFirst(
        "SELECT  HAS_CONSTRAINTS FROM SYOBJH (nolock) WHERE OBJECT_NAME='" + str(TableName) + "' AND HAS_CONSTRAINTS = 0"
    )
    Trace.Write(
        "SELECT  HAS_CONSTRAINTS FROM SYOBJH (nolock) WHERE OBJECT_NAME='" + str(TableName) + "' AND HAS_CONSTRAINTS = 0"
    )
    if constraint_obj is not None:
        Product.Attributes.GetByName("BTN_SYACTI_SY_00139_DROPCONSTRAINT").Allowed = False
        Product.Attributes.GetByName("BTN_SYACTI_SY_00140_RECREATECONSTRAINT").Allowed = True
    else:
        Product.Attributes.GetByName("BTN_SYACTI_SY_00139_DROPCONSTRAINT").Allowed = True
        Product.Attributes.GetByName("BTN_SYACTI_SY_00140_RECREATECONSTRAINT").Allowed = False'''

disable_section_list, disable_question_dict = [], {}
tab_name = TestProduct.CurrentTab

section_actn_visble_obj = Sql.GetList(
    """
                        SELECT 
                            SYPGAC.SAPCPQ_ATTRIBUTE_NAME,SYPGAC.ACTION_NAME
                        FROM 
                            SYPGAC (NOLOCK) 
                        JOIN SYTABS (NOLOCK) ON SYTABS.RECORD_ID = SYPGAC.TAB_RECORD_ID    
                        JOIN 
                            SYPAGE (NOLOCK) ON SYPAGE.TAB_RECORD_ID = SYTABS.RECORD_ID AND SYPAGE.TAB_NAME = SYTABS.TAB_LABEL
                        JOIN 
                            SYPRAC (NOLOCK) ON  SYPGAC.ACTION_NAME = SYPRAC.ACTION_TEXT     
                         
                        JOIN 
                            USERS_PERMISSIONS (NOLOCK)  ON USERS_PERMISSIONS.PERMISSION_ID = SYPRAC.PROFILE_RECORD_ID
                          
                        WHERE 
                            LTRIM(RTRIM(SYTABS.SAPCPQ_ALTTAB_NAME)) = '{Tab_Text}' AND 
                            LTRIM(RTRIM(SYTABS.APP_LABEL)) ='{APP_LABEL}' AND                           
                            USERS_PERMISSIONS.USER_ID = '{User_Record_Id}' AND SYPRAC.VISIBLE = 0
                        """.format(
        Tab_Text=tab_name, APP_LABEL=productName, User_Record_Id=get_user_id
    )
)
section_qstns_visble_obj = Sql.GetList(
    """
                        SELECT 
                                SYSECT.RECORD_ID as SECTION_REC_ID,SYSECT.SAPCPQ_ATTRIBUTE_NAME, SYSEFL.RECORD_ID , SYOBJD.DATA_TYPE
                        FROM 
                            SYTABS (NOLOCK) 
                        JOIN 
                            SYPAGE (NOLOCK) ON SYPAGE.TAB_RECORD_ID = SYTABS.RECORD_ID AND SYPAGE.TAB_NAME = SYTABS.TAB_LABEL                     
                        JOIN
                            SYSECT (NOLOCK) ON SYSECT.PAGE_RECORD_ID = SYTABS.PAGE_RECORD_ID AND SYSECT.PAGE_NAME = SYTABS.PAGE_NAME
                        JOIN 
                            SYSEFL (NOLOCK) ON SYSEFL.SECTION_RECORD_ID=SYSECT.RECORD_ID 
                        JOIN 
                            SYOBJD (NOLOCK)  ON SYOBJD.API_NAME = SYSEFL.API_FIELD_NAME  AND  SYOBJD.OBJECT_NAME = SYSEFL.API_NAME 
                        JOIN
                            SYPRSN (NOLOCK)  ON SYPRSN.SECTION_RECORD_ID = SYSECT.RECORD_ID 
                        JOIN 
                            USERS_PERMISSIONS (NOLOCK)  ON USERS_PERMISSIONS.PERMISSION_ID = SYPRSN.PROFILE_RECORD_ID
                        WHERE 
                            LTRIM(RTRIM(SYTABS.SAPCPQ_ALTTAB_NAME)) = '{Tab_Text}' AND 
                            LTRIM(RTRIM(SYTABS.APP_LABEL)) ='{APP_LABEL}' AND
                            ISNULL(SYSECT.SECTION_NAME,'') != '' AND
                            ISNULL(SYSECT.PRIMARY_OBJECT_NAME,'') != '' AND 
                            USERS_PERMISSIONS.USER_ID = '{User_Record_Id}' AND 
                            SYPRSN.VISIBLE = 0
                        """.format(
        Tab_Text=tab_name, APP_LABEL=productName, User_Record_Id=get_user_id
    )
)

question_visible_obj = Sql.GetList(
    """
                        SELECT TOP 1000 QN.SECTIONFIELD_RECORD_ID, MQ.SAPCPQ_ATTRIBUTE_NAME,MO.DATA_TYPE
                        FROM SYTABS (NOLOCK) MT
                        JOIN SYPAGE (NOLOCK) SP ON SP.TAB_RECORD_ID = MT.RECORD_ID
                        JOIN SYSECT (NOLOCK) MS ON MS.PAGE_RECORD_ID = SP.RECORD_ID
                        JOIN SYPRSN (NOLOCK) SN ON SN.SECTION_RECORD_ID = MS.RECORD_ID
                        JOIN SYSEFL (NOLOCK) MQ ON MQ.SECTION_RECORD_ID = MS.RECORD_ID
                        JOIN SYPRSF(NOLOCK) QN ON QN.SECTIONFIELD_RECORD_ID = MQ.RECORD_ID
                        JOIN USERS_PERMISSIONS (NOLOCK) US ON US.PERMISSION_ID = QN.PROFILE_RECORD_ID
                        JOIN SYOBJD (NOLOCK) MO ON MO.API_NAME = MQ.API_FIELD_NAME
                        AND MO.OBJECT_NAME = MQ.API_NAME
                        AND US.USER_ID = '{User_Record_Id}'
                        AND QN.VISIBLE = 0
                        AND ISNULL(MQ.FIELD_LABEL,'') != ''
                        AND LTRIM(RTRIM(MT.SAPCPQ_ALTTAB_NAME)) = '{Tab_Text}'
                        AND LTRIM(RTRIM(MT.APP_LABEL)) ='{APP_LABEL}'
                        AND ISNULL(MS.SECTION_NAME,'') != ''
                        ORDER BY ABS(MQ.DISPLAY_ORDER)
                        """.format(
        Tab_Text=tab_name, APP_LABEL=productName, User_Record_Id=get_user_id
    )
)

question_editable_obj = Sql.GetList(
    """
                                SELECT TOP 1000 SECTIONFIELD_RECORD_ID, DATA_TYPE, PERMISSION FROM (
                                SELECT TOP 1000 QN.SECTIONFIELD_RECORD_ID, QN.SECTION_FIELD_ID , SD.DATA_TYPE, SD.PERMISSION FROM SYPRSF (nolock) QN
                                JOIN SYOBJD (nolock) SD ON QN.OBJECT_NAME = SD.OBJECT_NAME AND QN.OBJECTFIELD_API_NAME = SD.API_NAME 
                                JOIN SYPROD (nolock) SP ON SP.OBJECTFIELD_RECORD_ID = SD.RECORD_ID
                                JOIN SYPRSN (nolock) SN ON SN.SECTION_RECORD_ID = QN.SECTION_RECORD_ID
                                JOIN SYTABS (nolock) MT ON MT.RECORD_ID = SN.TAB_RECORD_ID
                                JOIN USERS_PERMISSIONS (NOLOCK) US ON US.PERMISSION_ID = SN.PROFILE_RECORD_ID
                                AND SP.VISIBLE = 1
                                AND QN.VISIBLE = 1
                                AND ISNULL(SN.TAB_RECORD_ID, '') != ''
                                AND US.USER_ID = '{User_Record_Id}'
                                AND ISNULL(QN.SECTION_FIELD_ID ,'') != ''
                                AND LTRIM(RTRIM(MT.SAPCPQ_ALTTAB_NAME)) = '{Tab_Text}'
                                AND LTRIM(RTRIM(MT.APP_LABEL)) ='{APP_LABEL}'
                                AND ISNULL(SN.SECTION_ID,'') != ''
                                GROUP BY QN.SECTIONFIELD_RECORD_ID, QN.SECTION_FIELD_ID ,  SD.DATA_TYPE, SD.PERMISSION ) TAB1 WHERE TAB1.PERMISSION = 'READ ONLY'
                                """.format(
        Tab_Text=tab_name, APP_LABEL=productName, User_Record_Id=get_user_id
    )
)
if section_actn_visble_obj:    
    for section_actn in section_actn_visble_obj:
        if section_actn.SAPCPQ_ATTRIBUTE_NAME:               
            secactn_id = (str(section_actn.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")).upper()            
            sec_attr_name = "BTN_{}_".format(secactn_id)
            if section_actn.ACTION_NAME == 'BACK TO LIST':
                action_name = 'BACKTOLIST'
                att_name = sec_attr_name + (str(action_name))                      
                Product.Attributes.GetByName(att_name).Access = AttributeAccess.Hidden
            else: 
                att_name = sec_attr_name + (str(section_actn.ACTION_NAME))                      
                Product.Attributes.GetByName(att_name).Access = AttributeAccess.Hidden   
if section_qstns_visble_obj is not None:
    for section_obj in section_qstns_visble_obj:
        if section_obj.SAPCPQ_ATTRIBUTE_NAME not in disable_section_list:
            secrec_id = (str(section_obj.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")).upper()
            sec_attr_name = "SEC_{}".format(secrec_id)
            #Trace.Write("sec_attr_name----709--576-----" + str(sec_attr_name))
            disable_section_list.append(section_obj.SAPCPQ_ATTRIBUTE_NAME)
            Product.Attributes.GetByName(sec_attr_name).Access = AttributeAccess.Hidden
        disable_question_dict[section_obj.RECORD_ID] = section_obj.DATA_TYPE

for question_rec_id, data_type in disable_question_dict.items():
    qstn_rec_id = (str(question_rec_id).replace("-", "_").replace(" ", "")).upper()
    data_type = str(data_type)
    app_attr_name = "QSTN_{}_LONG".format(qstn_rec_id) if data_type == "LONG TEXT AREA" else "QSTN_{}".format(qstn_rec_id)
    #Trace.Write("app_attr_name ====????? " + str(app_attr_name))
    if Product.Attributes.GetByName(app_attr_name):
        Product.Attributes.GetByName(app_attr_name).Access = AttributeAccess.Hidden

if question_editable_obj is not None:
    for question_edit_obj in question_editable_obj:
        qstn_rec_id = (str(question_edit_obj.SECTIONFIELD_RECORD_ID).replace("-", "_").replace(" ", "")).upper()
        data_type = str(question_edit_obj.DATA_TYPE)
        qstn_edit_attr_name = (
            "QSTN_{}_LONG".format(qstn_rec_id) if data_type == "LONG TEXT AREA" else "QSTN_{}".format(qstn_rec_id)
        )
        if Product.Attributes.GetByName(qstn_edit_attr_name):
            Product.Attributes.GetByName(qstn_edit_attr_name).Access = AttributeAccess.Editable

if question_visible_obj is not None:
    for question_obj in question_visible_obj:
        qstn_rec_id = (str(question_obj.SAPCPQ_ATTRIBUTE_NAME).replace("-", "_").replace(" ", "")).upper()
        data_type = str(question_obj.DATA_TYPE)
        qstn_attr_name = (
            "QSTN_{}_LONG".format(qstn_rec_id) if data_type == "LONG TEXT AREA" else "QSTN_{}".format(qstn_rec_id)
        )
        if Product.Attributes.GetByName(qstn_attr_name):
            Product.Attributes.GetByName(qstn_attr_name).Access = AttributeAccess.Hidden
if value == "ADDNEW":
    sql_obj = Sql.GetFirst(
    "select SAPCPQ_ALTTAB_NAME,PRIMARY_OBJECT_NAME,APP_LABEL from SYTABS (NOLOCK) where SAPCPQ_ALTTAB_NAME = '"
    + str(tab_name)
    + "' AND APP_LABEL ='"
    + str(TestProduct.Name)
    + "' "
)
    #Trace.Write("Objname-->"+str(sql_obj.PRIMARY_OBJECT_NAME))
    if sql_obj:
        sqlqstn_obj = Sql.GetList(
            "select a.SAPCPQ_ATTRIBUTE_NAME AS SEC_ATTR,c.SAPCPQ_ATTRIBUTE_NAME AS QSTN_ATTR,a.PRIMARY_OBJECT_NAME as obj_name from SYSECT (NOLOCK) a join sypage b (nolock) on a.page_record_id = b.RECORD_ID join SYSEFL (NOLOCK) c ON a.RECORD_ID = c.SECTION_RECORD_ID AND a.PRIMARY_OBJECT_NAME = '"
            + str(sql_obj.PRIMARY_OBJECT_NAME)
            + "' and a.SECTION_NAME = 'AUDIT INFORMATION' and b.TAB_APP ='"
            + str(sql_obj.APP_LABEL)
            + "' "
        )
        if sqlqstn_obj:
            for qstn in sqlqstn_obj:
                qstn_attr = "QSTN_" + str(qstn.QSTN_ATTR).replace("-", "_")
                #Trace.Write("----FIELD_LABEL---"+str(qstn_attr)+"----before---" + str(Product.Attributes.GetByName(str(qstn_attr)).Allowed))
                if Product.Attributes.GetByName(str(qstn_attr)) is not None:
                    Product.Attributes.GetByName(str(qstn_attr)).Allowed = False
        
#fields_hide = ["QSTN_SYSEFL_AC_01140","QSTN_SYSEFL_AC_04282"]
if value == "VIEW":    
    attr_name = "QSTN_SYSEFL_AC_01140"
    if Product.Attributes.GetByName(str(attr_name)):
        Product.Attributes.GetByName(str(attr_name)).Allowed = False
        
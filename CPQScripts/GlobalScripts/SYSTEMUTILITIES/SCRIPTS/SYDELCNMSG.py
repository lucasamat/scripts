# =========================================================================================================================================
#   __script_name : SYDELCNMSG.PY
#   __script_description : THIS SCRIPT IS USED TO DISPLAY THE DELETE CONFORMATION MESSAGE.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
import SYCNGEGUID as CPQID
import Webcom.Configurator.Scripting.Test.TestProduct
Sql = SQL()
#Product_name = Product.Name

import clr

clr.AddReference("System.Net")
import System.Net
from System.Text.Encoding import UTF8
from System import Convert
from System.Net import *


def nativeProfileDelete(RecordId):
    LOGIN_CREDENTIALS = SqlHelper.GetFirst("SELECT USER_NAME, PASSWORD, DOMAIN, URL FROM SYCONF (nolock) WHERE USER_NAME = 'X0117669'")
    if LOGIN_CREDENTIALS is not None:
        Login_Username = str(LOGIN_CREDENTIALS.USER_NAME)
        Login_Password = str(LOGIN_CREDENTIALS.Password)
        Login_Domain = str(LOGIN_CREDENTIALS.Domain)
    #Trace.Write("29---------" + str(Login_Username))
    sandboxBaseURL = "https://sandbox.webcomcpq.com"
    authenticationUrl = (
        sandboxBaseURL
        + "/api/rd/v1/Core/Login?username="
        + Login_Username
        + "&password="
        + Login_Password
        + "&domain="
        + Login_Domain
    )
    authRequest = WebRequest.Create(str(authenticationUrl))
    authRequest.Method = "POST"
    authRequest.CookieContainer = CookieContainer()
    authRequest.ContentLength = 0
    authResponse = authRequest.GetResponse()
    cookies = authResponse.Cookies
    authResponseData = StreamReader(authResponse.GetResponseStream()).ReadToEnd()
    xcrf = str(authResponseData).replace('"', "")

    # cookies
    coookies = ""
    if cookies is not None:
        for cookie in cookies:
            coookies = coookies + str(cookie) + ";"

    data = "grant_type=password&username=" + Login_Username + "&password=" + Login_Password + "&domain=" + Login_Domain + ""
    # authentication api token creation start
    authenticationapitokenUrl = "https://sandbox.webcomcpq.com/basic/api/token"
    authRequesttoken = WebRequest.Create(str(authenticationapitokenUrl))
    authRequesttoken.Method = "DELETE"
    webclienttoken = System.Net.WebClient()
    webclienttoken.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
    webclienttoken.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
    webclienttoken.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
    webclienttoken.Headers.Add("X-CSRF-Token", xcrf)
    response = webclienttoken.UploadString(str(authenticationapitokenUrl), data)
    accessToken = "Bearer " + str(response).split(":")[1].split(",")[0].replace('"', "")

    datasave = """{
        "Id":%s
        
    }""" % (
        RecordId
    )
    #Trace.Write("188-------------datasave----" + str(datasave))
    setPermissionURL = sandboxBaseURL + "/setup/api/v1/admin/permissionGroups/" + str(int(RecordId))
    webclient = System.Net.WebClient()
    webclient.Headers[System.Net.HttpRequestHeader.Host] = "sandbox.webcomcpq.com"
    webclient.Headers[System.Net.HttpRequestHeader.ContentType] = "application/json; charset=utf-8"
    webclient.Headers[System.Net.HttpRequestHeader.Cookie] = coookies
    webclient.Headers.Add("X-CSRF-Token", xcrf)
    webclient.Headers.Add("Authorization", accessToken)
    response = webclient.UploadString(str(setPermissionURL), "DELETE", "")
    #Trace.Write("PERMISSIONS : " + str(response.encode("ascii", "ignore")))
    return "response"


class DeleteConfirmPopup:
    def __init__(self):
        self.UserId = str(User.Id)
        self.UserName = str(User.Name)

    def DELETECONFIRMATION(self, LABLE, GridID):
        try:
            TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
            TabName = str(TestProduct.CurrentTab)
            Trace.Write("TabName--" + str(TabName))
        except Exception:
            TabName = "Quote"
        #Trace.Write("222222222222222222222")
        GridName = ""
        sql_obj = Sql.GetFirst(
            "select RECORD_ID,NAME,RELATED_LIST_SINGULAR_NAME from SYOBJR where SAPCPQ_ATTRIBUTE_NAME = '"
            + str(GridID)
            + "' "
        )
        # Trace.Write(
        #     "select RECORD_ID,NAME,RELATED_LIST_SINGULAR_NAME from SYOBJR where SAPCPQ_ATTRIBUTE_NAME = '"
        #     + str(GridID)
        #     + "' "
        # )
        if sql_obj is not None:
            GridName = str(sql_obj.RELATED_LIST_SINGULAR_NAME).strip()
        ban_str = ""
        sec_str = ""
        ban_str += "<div>"
        ban_str += "CONFIRMATION : DELETE " + str(LABLE)
        # ban_str += '<button type="button" class="close" data-dismiss="modal">X</button>'
        ban_str += "</div>"
        Trace.Write('GridName----'+str(GridName))
        Trace.Write('LABLE----'+str(LABLE))
        sec_str += (
            "<div> Are you sure you would like to delete this " + str(GridName).title() + " " + str(LABLE) + " ?</div>"
        )
        return ban_str, sec_str

    def DynamicButton(self, dBtnFun):
        btnStr = ""
        try:
            for key, value in dBtnFun.items():
                BtnName = str(key)
                onClick = "onclick='" + str(value) + "'"
                btnStr += "<button type='button' {onClick} data-dismiss='modal'>{BtnName}</button>".format(
                    onClick=onClick, BtnName=BtnName
                )
        except Exception, e:
            Trace.Write("ERROR IN DYNAMIC BUTTON GENERATION")
        return btnStr

    def CommonDeleteConfirmation(self, RecordId, ObjName, Message, RecordValue):
        sec_str = ""
        try:
            Trace.Write("entering @140")
            # Trace.Write("TESTZ1" + str(RecordId))
            # Trace.Write("TESTZ2" + str(ObjName))
            # Trace.Write("TESTZ3" + str(Message))
            # Trace.Write("TESTZ4" + str(RecordValue))
            if str(Message) == "WARNING":
                InfoIcon = "/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg"
                InfoMsg = "CONFIRMATION : DELETE"
                if ObjName.startswith("SAQFEA"):
                    details = RecordValue.split('#')
                    deleteFunction = 'CommonDeleteRecord("{RecordId}", "{ObjName}")'.format(
                        RecordId=RecordValue, ObjName=ObjName
                    )
                    Buttons = self.DynamicButton({"DELETE": str(deleteFunction), "Cancel": ""})
                    ErrorMsg = "Are you sure you would like to delete {RecordValue} record?".format(RecordValue=str(RecordValue.split("#")[0]))
                elif ObjName.startswith("SAQSCO"):
                    details = RecordValue.split('#')
                    deleteFunction = 'CommonDeleteRecord("{RecordId}", "{ObjName}")'.format(
                        RecordId=RecordValue, ObjName=ObjName
                    )
                    Buttons = self.DynamicButton({"DELETE": str(deleteFunction), "Cancel": ""})
                    ErrorMsg = "Are you sure you would like to delete {RecordValue} record?".format(
                        RecordValue=str(details[1])
                    )
                elif ObjName.startswith("SYOBJX"):
                    deleteFunction = 'CommonDeleteRecord("{RecordId}", "{ObjName}")'.format(
                        RecordId=RecordId, ObjName=ObjName
                    )
                    Buttons = self.DynamicButton({"DELETE": str(deleteFunction), "Cancel": ""})
                    ErrorMsg = "Are you sure you would like to delete {RecordValue} record?".format(RecordValue=RecordValue.split('#')[0])
                # elif ObjName.startswith("SYSCRP"):
                #     Trace.Write("Check")
                #     details = RecordValue.split('#')
                #     deleteFunction = 'CommonDeleteRecord("{RecordID}","{ObjName}")'.format(
                #         RecordId=RecordValue, ObjName=ObjName
                #     )
                #     Trace.Wrtie("check1")
                #     Buttons = self.DynamicButton({"DELETE":  str(deleteFunction), "Cancel": ""})
                #     ErrorMsg = "Are you sure you want to delete these records ?".format(
                #         RecordValue=str(RecordValue.split("#")[0])
                #     )

                else:
                    deleteFunction = 'CommonDeleteRecord("{RecordId}", "{ObjName}")'.format(
                        RecordId=RecordId, ObjName=ObjName
                    )
                    Buttons = self.DynamicButton({"DELETE": str(deleteFunction), "Cancel": ""})
                    ErrorMsg = "Are you sure you would like to delete {RecordValue} record?".format(RecordValue=RecordValue)
                    #ErrorMsg = "Are you sure you would like to delete these records?"
                    Trace.Write('REcordValue--->'+str(RecordValue))
            elif str(Message) == "INFO":
                InfoIcon = "mt/APPLIEDMATERIALS_TST/Additionalfiles/infocircle1.svg"
                InfoMsg = "CONFIRMATION : INFO"
                Buttons = self.DynamicButton({"Ok": ""})
                ErrorMsg = "We can't able to delete this record Association exist."
            elif str(Message) == "ERROR":
                InfoIcon = "mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg"
                InfoMsg = "CONFIRMATION : ERROR"
                Buttons = self.DynamicButton({"DELETE": "cont_modalDelete()", "Cancel": ""})
                ErrorMsg = "Are you sure you would like to delete this record?"

            sec_str += """<div class="modulesecbnr brdr mrgbt0"><span id="relatedDelete">{InfoMsg}</span>
                            <button type="button" class="close" data-dismiss="modal">X</button>
                        </div>
                        <div class="row pad10">
                            <div class="col-xs-1">
                                <img src="{InfoIcon}">
                            </div>
                            <div class="col-xs-11" id="CommonDEL">{ErrorMsg}</div>
                        </div>
                        <div class="modal-footer txt_center">
                            {Buttons}
                        </div>""".format(
                InfoMsg=InfoMsg, InfoIcon=InfoIcon, Buttons=Buttons, ErrorMsg=ErrorMsg
            )
        except Exception, e:
            Trace.Write("ERROR IN COMMON DELETE POPUP")
        return sec_str

    def Constdel(self, LABLE, GridID):
        try:
            TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
            TabName = str(TestProduct.CurrentTab)
            Trace.Write("CONST_TabName--" + str(TabName))
        except Exception:
            TabName = ""
        Trace.Write("CONSTRAINT DROP==213===" + str(LABLE))

        

        InfoIcon = "mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg"
        InfoMsg = "CONFIRMATION : ERROR"
        Buttons = self.DynamicButton({"DELETE": "cont_modalDelete()", "Cancel": ""})
        ErrorMsg = "Are you sure you want to drop these constraints ?"
        dicti = {}
        dict_list = []
        obj = []
        obj_API = []
        sec_str = ""
        sec_str += """<div class="modulesecbnr brdr mrgbt0"><span id="relatedDelete">{InfoMsg}</span>
                        <button type="button" class="close" data-dismiss="modal">X</button>
                    </div>
                    <div class="row pad10">
                        <div class="col-xs-1">
                            <img src="{InfoIcon}">
                        </div>
                        <div class="col-xs-11" id="CommonDEL">{ErrorMsg}</div>
                    </div>
                    <div class="modal-footer txt_center">
                        {Buttons}
                    </div>""".format(
            InfoMsg=InfoMsg, InfoIcon=InfoIcon, Buttons=Buttons, ErrorMsg=ErrorMsg
        )
        #drop index for single record in schema- start
        if GridID == "SYOBJX":
            getindexname = Sql.GetFirst("SELECT INDEX_NAME,OBJECT_APINAME from SYOBJX where RECORD_ID = '"+str(LABLE)+"'")
            if getindexname:
                try:
                    QueryStatement = "DROP INDEX {Index_Name} on {Obj_Name}".format(
                        Index_Name=getindexname.INDEX_NAME, Obj_Name=getindexname.OBJECT_APINAME
                    )
                    a = Sql.RunQuery(QueryStatement)
                    Trace.Write("Dropped index successfully----")
                except:
                    Trace.Write("not dropped index")
        #drop index for single record in schema - End
        #in table level start
        delete_query_string = """DELETE FROM SYOBJX WHERE RECORD_ID ='{rec_id}'""".format(rec_id = LABLE)
        Sql.RunQuery(delete_query_string)
        #in table level end
        Trace.Write("---sec_str--" + str(sec_str))
       

        return dict_list, sec_str

    # A055S000P01-1170 Start-Om Shanker
    def DelEquipmentTrace(self, RecordId, ObjName):
        # Trace.Write("OM.........> CAME TO DelEquipmentTrace")
        Trace.Write("OM...RecordId-----> " + str(RecordId))
        Trace.Write("OM...ObjName-----> " + str(ObjName))

        if ObjName.startswith("SAQFEA"):
            Trace.Write("Check")
            OBJS_TO_DELETE = {
                "SAQFEA": "IGNORE_CHECK",
                "SAQFEQ": "SERIAL_NUMBER",
                "SAQSCA": "SERIAL_NUMBER",
                "SAQSCO": "SERIAL_NO",
                "SAQICO": "SERIAL_NO",
                "SAQICA": "SERIAL_NUMBER"
            }
        if ObjName.startswith("SAQSCO"):
            OBJS_TO_DELETE = {
                "SAQSCA": "SERIAL_NUMBER",
                "SAQSCO": "SERIAL_NO",
                "SAQICO": "SERIAL_NO",
                "SAQICA": "SERIAL_NUMBER",
            }

        # GET EQUIPMENT_ID AND SERIAL_NO FROM RECORD_ID
        if ObjName.startswith("SAQFEA"):
            EQUIP_ID = RecordId
            OBJNAME = ObjName.split('#')[0]
            RECORD_ID = ObjName.split("#")[1]
            
        else:
            EQUIP_ID = RecordId.split("#")[0]
            SERIAL_NO = RecordId.split("#")[1]
            Trace.Write("Del "+str(SERIAL_NO))
            OBJNAME = RecordId.split('#')[2]
            RECORD_ID = RecordId.split('#')[3]
        # GET QUOTE_ID
        if OBJNAME == 'SAQFEA':
            QUOTE_ID = Sql.GetFirst("SELECT QUOTE_ID from  SAQFEQ (nolock) where QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = '" + str(RECORD_ID) +"' AND EQUIPMENT_ID ='" + str(EQUIP_ID) + "';")
        elif OBJNAME == 'SAQSCO':
            QUOTE_ID = Sql.GetFirst("SELECT QUOTE_ID from  SAQSCO (nolock) where EQUIPMENTCATEGORY_ID ='" + str(EQUIP_ID) + "' AND SERIAL_NO = '"+ str(SERIAL_NO) +"' AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '"+ str(RECORD_ID) +"';")
        
        #GET SERVICE ID
        if OBJNAME != 'SAQFEA':
            SERVICE_ID = Sql.GetFirst("SELECT SERVICE_ID FROM SAQSCO (nolock) WHERE QUOTE_ID = '{QUOTE_ID}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND EQUIPMENTCATEGORY_ID = '{EQUIPMENT_ID}' AND SERIAL_NO = '{SERIAL_NO}'".format(QUOTE_ID= QUOTE_ID.QUOTE_ID, EQUIPMENT_ID=EQUIP_ID, SERIAL_NO=SERIAL_NO,quote_revision_record_id=quote_revision_record_id))
        
        all_sql_statement = ""
        Trace.Write("TableName "+str(OBJS_TO_DELETE))
        for tablename in OBJS_TO_DELETE:
            Trace.Write("Check1")
            if str(OBJS_TO_DELETE[tablename]) == "IGNORE_CHECK":
                all_sql_statement += "DELETE FROM {} WHERE EQUIPMENT_ID = '{}' AND QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'; ".format(tablename, EQUIP_ID, QUOTE_ID.QUOTE_ID,quote_revision_record_id)              
            else:                
                all_sql_statement += "DELETE FROM {} WHERE EQUIPMENTCATEGORY_ID = '{}' AND {} = '{}' AND QUOTE_ID = '{}' AND QTEREV_RECORD_ID = '{}'; ".format(
                    tablename, EQUIP_ID, OBJS_TO_DELETE[tablename], SERIAL_NO, QUOTE_ID.QUOTE_ID,quote_revision_record_id
                )
        #Trace.Write("OM...SQL_TO_DELETE: " + all_sql_statement)
        Sql.RunQuery(all_sql_statement)

        # All Records deleted now correct the line item id order in
        # SAQICO, SAQITM Table
        # PSEUDO CODE
        # STEP 1: SELECT ITEM_LINE_ID, EQUIPMENT_ID, QUOTE_ID, WHERE QUOTE_ID = 'CURRENT_QUOTE_ID'
        # STEP 2: START FROM 10 AND UPDATE ALL LINE ITEM IDS IN SAQICO ABOVE SET BY INCREMENT OF 10
        # STEP 3: START FROM 10 AND UPDATE ALL LINE ITEM IDS IN SAQITM ABOVE SET BY INCREMENT OF 10
        
        all_equip_of_quote = Sql.GetList("SELECT QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, LINE_ITEM_ID FROM SAQICO (nolock) WHERE QUOTE_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(QUOTE_ID.QUOTE_ID, SERVICE_ID.SERVICE_ID,quote_revision_record_id))
        count_of_existing_equipment = Sql.GetFirst("SELECT ISNULL(COUNT(ISNULL(QUOTE_ITEM_COVERED_OBJECT_RECORD_ID,0)),0) AS COUNT_OF_EQUIP FROM SAQICO (nolock) WHERE QUOTE_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(QUOTE_ID.QUOTE_ID, SERVICE_ID.SERVICE_ID,quote_revision_record_id))
        if all_equip_of_quote is not None:
            start_line_item_id = 0
            sql_to_upd_SAQICO_SAQITM_li_item = ""
            for l_item in all_equip_of_quote:
                start_line_item_id += 10
                sql_to_upd_SAQICO_SAQITM_li_item += "UPDATE SAQICO SET EQUIPMENT_LINE_ID = '{}' WHERE QUOTE_ITEM_COVERED_OBJECT_RECORD_ID = '{}' AND QUOTE_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'; ".format(
                    start_line_item_id, str(l_item.LINE_ITEM_ID) + " - " + str(start_line_item_id), l_item.QUOTE_ITEM_COVERED_OBJECT_RECORD_ID, QUOTE_ID.QUOTE_ID, SERVICE_ID.SERVICE_ID,quote_revision_record_id
                )
            # UPDATE SAQITM
            # if count_of_existing_equipment:
            #     if int(count_of_existing_equipment.COUNT_OF_EQUIP) > 0:
            #         sql_to_upd_SAQICO_SAQITM_li_item += "UPDATE SAQITM SET OBJECT_QUANTITY = '{}' WHERE QUOTE_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'; ".format(
            #             count_of_existing_equipment.COUNT_OF_EQUIP,
            #             QUOTE_ID.QUOTE_ID,
            #             SERVICE_ID.SERVICE_ID,
            #             quote_revision_record_id
            #         )
            #     else:
            #         sql_to_upd_SAQICO_SAQITM_li_item += "DELETE FROM SAQITM WHERE QUOTE_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(QUOTE_ID.QUOTE_ID, SERVICE_ID.SERVICE_ID,quote_revision_record_id)
            # Sql.RunQuery(sql_to_upd_SAQICO_SAQITM_li_item)
        # else:
            # all_equip_of_quote is None that means Delete the record in SAQITM
            # Sql.RunQuery("DELETE FROM SAQITM WHERE QUOTE_ID = '{}' AND SERVICE_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(QUOTE_ID.QUOTE_ID, SERVICE_ID.SERVICE_ID,quote_revision_record_id))
        return True

    def CommonDelete(self, RecordId, ObjName):
        try:
            contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
        except:
            contract_quote_record_id = ''    
        # Trace.Write("Delete came here.....353....")
        # Trace.Write("RecordId-----> " + str(RecordId))
        # Trace.Write("ObjName-----> " + str(ObjName))
        # Trace.Write("Quote recordid----------------->"+str(contract_quote_record_id))
        # A043S001P01-11792 Start-Dhurga
        if str(ObjName) == "cpq_permissions":
            nativeProfileDelete(RecordId)
        # A043S001P01-11792 end-Dhurga

        # A055S000P01-1170 Start-Om Shanker
        if ObjName.startswith("SAQFEA"):
            Trace.Write("Rec ID "+str(RecordId))
            self.DelEquipmentTrace(str(RecordId), str(ObjName))
        elif ObjName.startswith("SAQSCO"):
            self.EquipmentDelete(str(RecordId), str(ObjName))   
        # A055S000P01-1170 End-Om Shanker
        elif ObjName == "SAQTSV":
            Serviceobject = Sql.GetFirst("select * from SAQTSV (NOLOCK) where QUOTE_SERVICE_RECORD_ID = '" + str(RecordId) + "' AND QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) +"'")
            getQuotetype = ""
            quote_obj = Sql.GetFirst("select QUOTE_TYPE from SAQTMT (NOLOCK) where MASTER_TABLE_QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
            if quote_obj:
                #getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()
                Log.Info("SYDELCNMSG - SAQSGB")
                if quote_obj.QUOTE_TYPE == "ZTBC - TOOL BASED":
                    TOOLDELETELIST = ["SAQTSV","SAQSCA","SAQICO","SAQSCE","SAQSGE","SAQICO","SAQIEN","SAQSFB","SAQSGB","SAQSCO","SAQTSE","SAQSFE","SAQSGE"]
                    for Table in TOOLDELETELIST:
                        QueryStatement = "DELETE FROM "+str(Table)+" WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' and SERVICE_ID = '{Service_id}' and SERVICE_DESCRIPTION = '{Service_Description}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(ObjectName = Table,Service_id = Serviceobject.SERVICE_ID,Service_Description = Serviceobject.SERVICE_DESCRIPTION,quote_revision_record_id=quote_revision_record_id)
                        Sql.RunQuery(QueryStatement)
                elif quote_obj.QUOTE_TYPE == "ZWK1 - SPARES":
                    TOOLDELETELIST = ["SAQTSV","SAQSPT","SAQSGE","SAQTSE","SAQIFP","SAQIEN","SAQSFE","SAQSCE","SAQSCO","SAQSCA"]
                    for Table in TOOLDELETELIST:
                        QueryStatement = "DELETE FROM "+str(Table)+" WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' and SERVICE_ID = '{Service_id}' and SERVICE_DESCRIPTION = '{Service_Description}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(ObjectName = Table,Service_id = Serviceobject.SERVICE_ID,Service_Description = Serviceobject.SERVICE_DESCRIPTION,quote_revision_record_id=quote_revision_record_id)
                        Sql.RunQuery(QueryStatement)
        elif ObjName == "SAQFBL":
            Trace.Write("SAQFBL======")
            fab_location = Sql.GetFirst("SELECT * FROM SAQFBL (NOLOCK) WHERE QUOTE_FABLOCATION_RECORD_ID = '"+str(RecordId)+"' AND QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) +"'")
            if fab_location:
                TOOLDELETELIST = ["SAQFBL","SAQTSV","SAQSGB","SAQSCO","SAQFEQ","SAQTSE","SAQSAP"]
                for Table in TOOLDELETELIST:
                    if Table == "SAQFBL":
                        QueryStatement = "DELETE FROM "+str(Table)+" WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' and FABLOCATION_ID = '{fab_id}' and QUOTE_FABLOCATION_RECORD_ID = '{fab_location_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(ObjectName = Table,fab_id = fab_location.FABLOCATION_ID,fab_location_rec_id = fab_location.QUOTE_FABLOCATION_RECORD_ID,quote_revision_record_id=quote_revision_record_id)
                        Sql.RunQuery(QueryStatement)
                    if Table in ("SAQTSV","SAQTSE","SAQSGB","SAQSAP"):
                        QueryStatement = "DELETE FROM "+str(Table)+" WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"'  AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(ObjectName = Table,quote_revision_record_id=quote_revision_record_id)
                        Sql.RunQuery(QueryStatement)
                    else:
                        QueryStatement = "DELETE FROM "+str(Table)+" WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' and FABLOCATION_ID = '{fab_id}' and FABLOCATION_RECORD_ID = '{fab_location_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(ObjectName = Table,fab_id = fab_location.FABLOCATION_ID,fab_location_rec_id = fab_location.FABLOCATION_RECORD_ID,quote_revision_record_id=quote_revision_record_id)
                        Sql.RunQuery(QueryStatement)
                    
                    update_saqtrv = ("UPDATE SAQTRV SET PRICING_DIRTY_FLAG = 'TRUE', REVISION_STATUS = 'PREPARING REVISION', WORKFLOW_STATUS = 'CONFIGURE' WHERE QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) +"'")
                    Sql.RunQuery(update_saqtrv)
        else:
            tableInfo = Sql.GetTable(ObjName)
            ColumnName = Sql.GetFirst(
                "select API_NAME from  SYOBJD where OBJECT_NAME ='" + str(ObjName) + "' and DATA_TYPE ='AUTO NUMBER'"
            )
            sqlobjs = Sql.GetList(
                "select OBJECT_NAME,API_NAME from  SYOBJD where LOOKUP_OBJECT ='" + str(ObjName) + "' and DATA_TYPE ='LOOKUP'"
            )
            if sqlobjs is not None:
                for sqlobj in sqlobjs:
                    if ObjName == "SAQTSV":
                        GetSAQTSV = Sql.GetFirst(
                            "SELECT * FROM SAQTSV (NOLOCK) WHERE QUOTE_SERVICE_RECORD_ID = '" + str(RecordId) + "'"
                        )
                        # if GetSAQTSV is not None:
                        #     serv_rec_id = str(GetSAQTSV.SERVICE_RECORD_ID)
                        #     if serv_rec_id != "":
                        #         tableInfoSAQITM = Sql.GetTable("SAQITM")
                        #         SqlObj = Sql.GetList(
                        #             "SELECT * FROM SAQITM (NOLOCK) WHERE SERVICE_RECORD_ID = '"
                        #             + str(serv_rec_id)
                        #             + "' AND QUOTE_RECORD_ID = '"
                        #             + str(GetSAQTSV.QUOTE_RECORD_ID)
                        #             + "' AND QTEREV_RECORD_ID = '"
                        #             + str(quote_revision_record_id)
                        #             + "'"
                        #         )
                        #         if SqlObj is not None:
                        #             for val in SqlObj:
                        #                 tableInfoSAQITM.AddRow(val)
                        #                 Sql.Delete(tableInfoSAQITM)
                        # Rearrange Item Line Id start
                        # all_item_of_quote = Sql.GetList(
                        #     "SELECT LINE_ITEM_ID FROM SAQITM WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(GetSAQTSV.QUOTE_RECORD_ID,quote_revision_record_id)
                        # )
                        # start_line_item_id = 0
                        # sql_to_upd_SAQICO_SAQITM_li_item = ""
                        # for l_item in all_item_of_quote:
                        #     start_line_item_id += 10
                        #     sql_to_upd_SAQICO_SAQITM_li_item += "UPDATE SAQITM SET LINE_ITEM_ID = {} WHERE LINE_ITEM_ID = {} AND QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'; ".format(
                        #         start_line_item_id, l_item.LINE_ITEM_ID, GetSAQTSV.QUOTE_RECORD_ID,quote_revision_record_id
                        #     )
                        # Sql.RunQuery(sql_to_upd_SAQICO_SAQITM_li_item)
                        # Rearrange Item Line Id end
                    
                    if RecordId:
                        
                        QueryStatement = (
                            "delete from "
                            + str(sqlobj.OBJECT_NAME)
                            + " where "
                            + str(sqlobj.API_NAME)
                            + " ='"
                            + str(RecordId)
                            + "'"
                        )
                        Sql.RunQuery(QueryStatement)
                if RecordId != "":
                    GetQuery = Sql.GetList(
                        "select CpqTableEntryId from "
                        + str(ObjName)
                        + " where "
                        + str(ColumnName.API_NAME)
                        + "='"
                        + str(RecordId)
                        + "'"
                    )
                    if str(ObjName) == 'ACACST':
                        GetAprchnRecId = Sql.GetList(
                            "select APRCHN_RECORD_ID from "
                            + str(ObjName)
                            + " where "
                            + str(ColumnName.API_NAME)
                            + "='"
                            + str(RecordId)
                            + "'")
                    if ObjName == "SAQRSP":
                        getpart = Sql.GetFirst("SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_REV_PO_PRODUCT_LIST_ID = '{}'".format(RecordId))
                        part = getpart.PART_NUMBER
                        Sql.RunQuery("DELETE FROM SAQRIP WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SERVICE_ID = 'Z0101' AND PART_NUMBER = '{}'".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),part))
                    if GetQuery is not None:
                        for tablerow in GetQuery:
                            
                            tableInfo.AddRow(tablerow)
                            Sql.Delete(tableInfo)
                        if str(ObjName) == 'ACACST' and GetAprchnRecId is not None:
                            for step_id in GetAprchnRecId:
                                Trace.Write('APRCHN_RECORD_ID-- ' + str(step_id.APRCHN_RECORD_ID))
                                all_existing_steps = SqlHelper.GetList("SELECT APPROVAL_CHAIN_STEP_RECORD_ID FROM ACACST (nolock) WHERE APRCHN_RECORD_ID = '{}'".format(step_id.APRCHN_RECORD_ID))
                                count_of_existing_step = SqlHelper.GetList("SELECT ISNULL(COUNT(ISNULL(APRCHNSTP_NUMBER,0)),0) AS COUNT_OF_STEP FROM ACACST (nolock) WHERE APRCHN_RECORD_ID = '{}'".format(step_id.APRCHN_RECORD_ID))
                                #Trace.Write("count_of_existing_step" + str(count_of_existing_step[0].COUNT_OF_STEP))
                                if count_of_existing_step[0].COUNT_OF_STEP > 0 and all_existing_steps is not None:
                                    start_step_id = 1
                                    sql_to_upd_acacst_step_number = ""
                                    for l_step in all_existing_steps:
                                        sql_to_upd_acacst_step_number += "UPDATE ACACST SET APRCHNSTP_NUMBER = '{}' WHERE APPROVAL_CHAIN_STEP_RECORD_ID = '{}' ".format(start_step_id, str(l_step.APPROVAL_CHAIN_STEP_RECORD_ID))
                                        start_step_id += 1

                                    Sql.RunQuery(sql_to_upd_acacst_step_number)

        return True

    def EquipmentDelete(self,RecordId, ObjName):
        if TreeParentParam == 'Comprehensive Services':
            ServiceId = TreeParam
        if TreeSuperParentParam == 'Comprehensive Services':
            ServiceId = TreeParentParam
        if TreeTopSuperParentParam =='Comprehensive Services':
            ServiceId = TreeSuperParentParam
        GetCount = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as cnt FROM SAQSCO WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(Quote.GetGlobal("contract_quote_record_id"),quote_revision_record_id))
        if GetCount.cnt >1:
            Trace.Write("More than one equipment")
            GetEquipment = Sql.GetFirst("SELECT EQUIPMENT_ID FROM SAQSCO WHERE QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '{}'".format(RecordId.split("#")[4]))
            Objects = ["SAQSCO","SAQSCA","SAQSAP","SAQSKP","SAQICO","SAQSCE","SAQSAE"]
            for obj in Objects:
                a = Sql.RunQuery("DELETE FROM {Obj} WHERE QUOTE_RECORD_ID = '{QuoteId}' AND EQUIPMENT_ID = '{Eq}' AND SERVICE_ID = '{ServiceId}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(Obj=obj,QuoteId=Quote.GetGlobal("contract_quote_record_id"),Eq=GetEquipment.EQUIPMENT_ID,ServiceId=ServiceId,quote_revision_record_id=quote_revision_record_id))
        else:
            if GetCount.cnt == 1:
                Trace.Write("Only one equipment")
                Objects = ["SAQSCO","SAQSCA","SAQSAP","SAQSKP","SAQICO","SAQSFB","SAQSCE","SAQSAE","SAQSGE","SAQSFE","SAQIEN"]
                for obj in Objects:
                    a = Sql.RunQuery("DELETE FROM {Obj} WHERE QUOTE_RECORD_ID = '{QuoteId}' AND SERVICE_ID LIKE '%{ServiceId}%' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(Obj=obj,QuoteId=Quote.GetGlobal("contract_quote_record_id"),ServiceId=ServiceId,quote_revision_record_id=quote_revision_record_id))


delconp = DeleteConfirmPopup()

Action = Param.Action
LABLE = Param.Record_Id
GridID = Param.Grid_Id
Trace.Write("ACT---" + str(Action))
Trace.Write("LAB---" + str(LABLE))
Trace.Write("DRID=====" + str(GridID))
TreeParentParam = Product.GetGlobal("TreeParentLevel0")
TreeSuperParentParam = Product.GetGlobal("TreeParentLevel1")
TreeTopSuperParentParam = Product.GetGlobal("TreeParentLevel2")
TreeParam = Product.GetGlobal("TreeParam")
try:
    if LABLE.startswith(str(GridID)):
        LABLE = CPQID.KeyCPQId.GetKEYId(str(GridID), str(LABLE))
except Exception:
    Trace.Write("Container level Delete......")
try:
	quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
	quote_revision_record_id = ""


if str(Action) == "old" and str(GridID) != "SYOBJC":
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.DELETECONFIRMATION(LABLE, GridID))
elif str(Action) == "delete" and str(GridID) != "SYOBJX":
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.CommonDelete(LABLE,GridID))
elif str(Action) == "new" and str(GridID) == "SYOBJC":
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.Constdel(LABLE, GridID))
elif str(Action) == "delete" and str(GridID) == "SYOBJX":
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.Constdel(LABLE, GridID))
else:
    Message = Param.Message
    RecordValue = Param.RecordValue
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.CommonDeleteConfirmation(LABLE, GridID, Message, RecordValue))
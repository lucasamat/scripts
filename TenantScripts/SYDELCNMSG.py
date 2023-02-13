# =========================================================================================================================================
#   __script_name : SYDELCNMSG.PY
#   __script_description : THIS SCRIPT IS USED TO DISPLAY THE DELETE CONFORMATION MESSAGE.
#   __primary_author__ : JOE EBENEZER
#   __create_date :
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
        GridName = ""
        sql_obj = Sql.GetFirst(
            "select RECORD_ID,NAME,RELATED_LIST_SINGULAR_NAME from SYOBJR where SAPCPQ_ATTRIBUTE_NAME = '"
            + str(GridID)
            + "' "
        )
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
        except Exception as e:
            Trace.Write("ERROR IN DYNAMIC BUTTON GENERATION")
        return btnStr

    def CommonDeleteConfirmation(self, RecordId, ObjName, Message, RecordValue):
        sec_str = ""
        try:
            if str(Message) == "WARNING":
                InfoIcon = "/mt/APPLIEDMATERIALS_PRD/Additionalfiles/warning1.svg"
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
                        RecordValue=str(CPQID.KeyCPQId.GetCPQId("SAQSCO", str(details[4])))
                    )
                elif ObjName.startswith("SYOBJX"):
                    deleteFunction = 'CommonDeleteRecord("{RecordId}", "{ObjName}")'.format(
                        RecordId=RecordId, ObjName=ObjName
                    )
                    Buttons = self.DynamicButton({"DELETE": str(deleteFunction), "Cancel": ""})
                    ErrorMsg = "Are you sure you would like to delete {RecordValue} record?".format(RecordValue=RecordValue.split('#')[0])
                elif ObjName.startswith("SAQSGB"):
                    #details = RecordValue.split('#')
                    deleteFunction = 'CommonDeleteRecord("{RecordId}", "{ObjName}")'.format(
                        RecordId=RecordId, ObjName=ObjName
                    )
                    Buttons = self.DynamicButton({"DELETE": str(deleteFunction), "Cancel": ""})
                    ErrorMsg = "Are you sure you would like to delete {RecordValue} record?".format(RecordValue=RecordId)
                else:
                    deleteFunction = 'CommonDeleteRecord("{RecordId}", "{ObjName}")'.format(
                        RecordId=RecordId, ObjName=ObjName
                    )
                    Buttons = self.DynamicButton({"DELETE": str(deleteFunction), "Cancel": ""})
                    ErrorMsg = "Are you sure you would like to delete {RecordValue} record?".format(RecordValue=RecordValue)
                    #ErrorMsg = "Are you sure you would like to delete these records?"
                    Trace.Write('REcordValue--->'+str(RecordValue))
            elif str(Message) == "INFO":
                InfoIcon = "mt/APPLIEDMATERIALS_PRD/Additionalfiles/infocircle1.svg"
                InfoMsg = "CONFIRMATION : INFO"
                Buttons = self.DynamicButton({"Ok": ""})
                ErrorMsg = "We can't able to delete this record Association exist."
            elif str(Message) == "ERROR":
                InfoIcon = "mt/APPLIEDMATERIALS_PRD/Additionalfiles/stopicon1.svg"
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
        except Exception as e:
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
        InfoIcon = "mt/APPLIEDMATERIALS_PRD/Additionalfiles/stopicon1.svg"
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

    #A055S000P01-20970 Starts
    def BulkDeleteConfirm(self, RecordId, ObjName, Message):
        sec_str = ""
        try:
            Trace.Write("BulkDeleteConfirm Function")
            if str(Message) == "WARNING":
                Trace.Write("entering @282")
                InfoIcon = "/mt/"+str(Sql.getDomainDetails())+"/Additionalfiles/warning1.svg"
                InfoMsg = "CONFIRMATION : DELETE"
                deleteFunction = 'bulkDeleteConfirm("{RecordId}")'.format(RecordId=RecordId)
                Buttons = self.DynamicButton({"DELETE": str(deleteFunction), "CANCEL": ""})
                ErrorMsg = "Are you sure you would like to delete record?"
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
        except Exception as e:
            Trace.Write("ERROR IN Confirm Delete POPUP")
        Trace.Write("sec"+str(sec_str))
        return sec_str
    #A055S000P01-20970 Ends

    # A055S000P01-1170 Start-Om Shanker
    def DelEquipmentTrace(self, RecordId, ObjName):
        Trace.Write("CAME TO DelEquipmentTrace")
        Trace.Write("OM...RecordId-----> " + str(RecordId))
        Trace.Write("OM...ObjName-----> " + str(ObjName))
        #contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
        #Trace.Write("OM.....contract_quote_rec_id2---->"+str(contract_quote_rec_id))
        refresh_flag = False
        if ObjName.find('#') == -1:
            Trace.Write("No")
        else:
            ObjName=ObjName.split("#")[1]
            Trace.Write("Yes")
        # INC08928004 A
        getGreenbook = Sql.GetFirst("SELECT GREENBOOK,FABLOCATION_ID FROM SAQFEQ (NOLOCK) WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id,RecordId))
        # INC08928004 A
        if TreeParentParam == 'Fab Locations':
            fab_loc_id = getGreenbook.FABLOCATION_ID
            #INC08621345#INC08696637 - Start -M
            #CR BULK DELETE STARTS
            equipment_key_ids = RecordId
            #SAQGPA
            saqgpa_del = "DELETE A FROM SAQGPA A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqgpa_del)
            #SAQGPM
            saqgpm_del = "DELETE FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID NOT IN (SELECT  QTEREVPME_RECORD_ID FROM SAQGPA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id)
            Sql.RunQuery(saqgpm_del)
            #SAQRGG
            saqrgg_del = "DELETE FROM SAQRGG WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID NOT IN (SELECT QTEREVGOT_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id)
            Sql.RunQuery(saqrgg_del)
            #SAQGPE
            saqgpe_del = "DELETE FROM SAQGPE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEGGTPME_RECORD_ID NOT IN (SELECT  QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id)
            Sql.RunQuery(saqgpe_del)        
            #SAQSAP
            saqsap_del = "DELETE A FROM SAQSAP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids =equipment_key_ids)
            Sql.RunQuery(saqsap_del)
            #SAQSKP
            saqskp_del = "DELETE A FROM SAQSKP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVMASY_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqskp_del)
            #SAQSKP2
            saqskp_del_2 = "DELETE FROM SAQSKP WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}' AND ISNULL(QTEGBKPME_RECORD_ID,'') != ''".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqskp_del_2)
            #SAQSAE
            saqsae_del = "DELETE A FROM SAQSAE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsae_del)
            #SAQSCE
            saqsae_del = "DELETE A FROM SAQSCE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsae_del)
            #SAQSCA
            saqsca_del ="DELETE FROM SAQSCA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsca_del)
            #SAQSCO
            saqsco_del = "DELETE FROM SAQSCO WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsco_del)
            #SAQSGB
            get_saqsgb = Sql.GetList("Select DISTINCT GREENBOOK FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND GREENBOOK NOT IN (SELECT DISTINCT GREENBOOK FROM SAQSCO WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id))
            for delete in get_saqsgb:
                Saqsgb_del = "DELETE FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND GREENBOOK = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,greenbook =str(delete.GREENBOOK))
                Sql.RunQuery(Saqsgb_del)
            #SAQSGE
            get_saqsge = Sql.GetList("SELECT QTESRVGBK_RECORD_ID FROM SAQSGE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTESRVGBK_RECORD_ID NOT IN (SELECT QUOTE_SERVICE_GREENBOOK_RECORD_ID FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id))
            for delete in get_saqsge:
                Saqsge_del = "DELETE FROM SAQSGE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTESRVGBK_RECORD_ID = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,greenbook =str(delete.QTESRVGBK_RECORD_ID))
                Sql.RunQuery(Saqsge_del)
            #SAQFEA
            Saqfea_del = "DELETE FROM SAQFEA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(Saqfea_del)
            #SAQFEQ
            Saqfeq_del = "DELETE FROM SAQFEQ WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(Saqfeq_del)
            #SAQFGB
            get_saqfgb = Sql.GetList("Select DISTINCT GREENBOOK FROM SAQFGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID ='{fab_loc_id}' AND GREENBOOK NOT IN (SELECT DISTINCT GREENBOOK FROM SAQFEQ WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID ='{fab_loc_id}' )".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,fab_loc_id = fab_loc_id))
            for delete in get_saqfgb:
                Saqfgb_del = "DELETE FROM SAQFGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID ='{fab_loc_id}' AND GREENBOOK = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,fab_loc_id = fab_loc_id,greenbook =str(delete.GREENBOOK))
                Sql.RunQuery(Saqfgb_del)
                refresh_flag = True
            #INC08696637 - End -M
            #CR BULK DELETE ENDS
        elif TreeParam == 'Fab Locations':
            fab_loc_id = getGreenbook.FABLOCATION_ID
            #INC08621345#INC08696637 - Start -M
            #CR BULK DELETE STARTS
            equipment_key_ids = RecordId
            #SAQGPA
            saqgpa_del = "DELETE A FROM SAQGPA A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqgpa_del)
            #SAQGPM
            saqgpm_del = "DELETE FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID NOT IN (SELECT  QTEREVPME_RECORD_ID FROM SAQGPA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id)
            Sql.RunQuery(saqgpm_del)
            #SAQRGG
            saqrgg_del = "DELETE FROM SAQRGG WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID NOT IN (SELECT QTEREVGOT_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id)
            Sql.RunQuery(saqrgg_del)
            #SAQGPE
            saqgpe_del = "DELETE FROM SAQGPE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEGGTPME_RECORD_ID NOT IN (SELECT  QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id)
            Sql.RunQuery(saqgpe_del)        
            #SAQSAP
            saqsap_del = "DELETE A FROM SAQSAP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids =equipment_key_ids)
            Sql.RunQuery(saqsap_del)
            #SAQSKP
            saqskp_del = "DELETE A FROM SAQSKP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVMASY_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqskp_del)
            #SAQSKP2
            saqskp_del_2 = "DELETE FROM SAQSKP WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}' AND ISNULL(QTEGBKPME_RECORD_ID,'') != ''".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqskp_del_2)
            #SAQSAE
            saqsae_del = "DELETE A FROM SAQSAE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsae_del)
            #SAQSCE
            saqsae_del = "DELETE A FROM SAQSCE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsae_del)
            #SAQSCA
            saqsca_del ="DELETE FROM SAQSCA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsca_del)
            #SAQSCO
            saqsco_del = "DELETE FROM SAQSCO WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsco_del)
            #SAQSGB
            get_saqsgb = Sql.GetList("Select DISTINCT GREENBOOK FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND GREENBOOK NOT IN (SELECT DISTINCT GREENBOOK FROM SAQSCO WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id))
            for delete in get_saqsgb:
                Saqsgb_del = "DELETE FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND GREENBOOK = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,greenbook =str(delete.GREENBOOK))
                Sql.RunQuery(Saqsgb_del)
            #SAQSGE
            get_saqsge = Sql.GetList("SELECT QTESRVGBK_RECORD_ID FROM SAQSGE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTESRVGBK_RECORD_ID NOT IN (SELECT QUOTE_SERVICE_GREENBOOK_RECORD_ID FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id))
            for delete in get_saqsge:
                Saqsge_del = "DELETE FROM SAQSGE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTESRVGBK_RECORD_ID = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,greenbook =str(delete.QTESRVGBK_RECORD_ID))
                Sql.RunQuery(Saqsge_del)
            #SAQFEA
            Saqfea_del = "DELETE FROM SAQFEA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(Saqfea_del)
            #SAQFEQ
            Saqfeq_del = "DELETE FROM SAQFEQ WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(Saqfeq_del)
            #SAQFGB
            get_saqfgb = Sql.GetList("Select DISTINCT GREENBOOK FROM SAQFGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID ='{fab_loc_id}' AND GREENBOOK NOT IN (SELECT DISTINCT GREENBOOK FROM SAQFEQ WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID ='{fab_loc_id}' )".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,fab_loc_id = fab_loc_id))
            for delete in get_saqfgb:
                Saqfgb_del = "DELETE FROM SAQFGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID ='{fab_loc_id}' AND GREENBOOK = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,fab_loc_id = fab_loc_id,greenbook =str(delete.GREENBOOK))
                Sql.RunQuery(Saqfgb_del) 
                refresh_flag = True  
            #INC08696637 - End -M
            #CR BULK DELETE ENDS
        elif TreeSuperParentParam == 'Fab Locations':
            fab_loc_id = getGreenbook.FABLOCATION_ID
            #INC08621345#INC08696637 - Start -M
            #CR BULK DELETE STARTS
            equipment_key_ids = RecordId
            #SAQGPA
            saqgpa_del = "DELETE A FROM SAQGPA A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqgpa_del)
            #SAQGPM
            saqgpm_del = "DELETE FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID NOT IN (SELECT  QTEREVPME_RECORD_ID FROM SAQGPA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id)
            Sql.RunQuery(saqgpm_del)
            #SAQRGG
            saqrgg_del = "DELETE FROM SAQRGG WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID NOT IN (SELECT QTEREVGOT_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id)
            Sql.RunQuery(saqrgg_del)
            #SAQGPE
            saqgpe_del = "DELETE FROM SAQGPE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEGGTPME_RECORD_ID NOT IN (SELECT  QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id)
            Sql.RunQuery(saqgpe_del)        
            #SAQSAP
            saqsap_del = "DELETE A FROM SAQSAP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids =equipment_key_ids)
            Sql.RunQuery(saqsap_del)
            #SAQSKP
            saqskp_del = "DELETE A FROM SAQSKP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVMASY_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqskp_del)
            #SAQSKP2
            saqskp_del_2 = "DELETE FROM SAQSKP WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}' AND ISNULL(QTEGBKPME_RECORD_ID,'') != ''".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqskp_del_2)
            #SAQSAE
            saqsae_del = "DELETE A FROM SAQSAE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsae_del)
            #SAQSCE
            saqsae_del = "DELETE A FROM SAQSCE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsae_del)
            #SAQSCA
            saqsca_del ="DELETE FROM SAQSCA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsca_del)
            #SAQSCO
            saqsco_del = "DELETE FROM SAQSCO WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(saqsco_del)
            #SAQSGB
            get_saqsgb = Sql.GetList("Select DISTINCT GREENBOOK FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND GREENBOOK NOT IN (SELECT DISTINCT GREENBOOK FROM SAQSCO WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id))
            for delete in get_saqsgb:
                Saqsgb_del = "DELETE FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND GREENBOOK = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,greenbook =str(delete.GREENBOOK))
                Sql.RunQuery(Saqsgb_del)
            #SAQSGE
            get_saqsge = Sql.GetList("SELECT QTESRVGBK_RECORD_ID FROM SAQSGE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTESRVGBK_RECORD_ID NOT IN (SELECT QUOTE_SERVICE_GREENBOOK_RECORD_ID FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id))
            for delete in get_saqsge:
                Saqsge_del = "DELETE FROM SAQSGE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTESRVGBK_RECORD_ID = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,greenbook =str(delete.QTESRVGBK_RECORD_ID))
                Sql.RunQuery(Saqsge_del)
            #SAQFEA
            Saqfea_del = "DELETE FROM SAQFEA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(Saqfea_del)
            #SAQFEQ
            Saqfeq_del = "DELETE FROM SAQFEQ WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
            Sql.RunQuery(Saqfeq_del)
            #SAQFGB
            get_saqfgb = Sql.GetList("Select DISTINCT GREENBOOK FROM SAQFGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID ='{fab_loc_id}' AND GREENBOOK NOT IN (SELECT DISTINCT GREENBOOK FROM SAQFEQ WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID ='{fab_loc_id}' )".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,fab_loc_id = fab_loc_id))
            for delete in get_saqfgb:
                Saqfgb_del = "DELETE FROM SAQFGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID ='{fab_loc_id}' AND GREENBOOK = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,fab_loc_id = fab_loc_id,greenbook =str(delete.GREENBOOK))
                Sql.RunQuery(Saqfgb_del) 
                refresh_flag = True  
            #INC08696637 - End -M
            #CR BULK DELETE ENDS

        #A055S000P01-20807 - M
        getIdlingVal = Sql.GetFirst("select CpqTableEntryId from saqsce where QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID ='{}' AND ISNULL(IDLING_ALLOWED,'No') = 'Yes'".format(quote_revision_record_id,contract_quote_rec_id))
        if not getIdlingVal:
            Sql.RunQuery("DELETE FROM SAQTDA WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID ='{}'".format(quote_revision_record_id,contract_quote_rec_id))
        #A055S000P01-20807 - M


        return True,refresh_flag

#INC08737172 Start - A
    def CommonDelete(self, RecordId, ObjName, subtab):
#INC08737172 End - A
        try:
            contract_quote_record_id = Quote.GetGlobal("contract_quote_record_id")
        except:
            contract_quote_record_id = ''
        refresh_flag = False
        if ObjName.startswith("SAQFEA") or ObjName =='SAQFEQ': #INC08621345
            Trace.Write("Rec ID "+str(RecordId))
            response,refresh_flag = self.DelEquipmentTrace(str(RecordId), str(ObjName))
        elif ObjName.startswith("SAQSCO"):
            refresh_flag = self.EquipmentDelete(str(RecordId), str(ObjName))
        elif ObjName == "SAQTSV":
            Serviceobject = Sql.GetFirst("select * from SAQTSV (NOLOCK) where QUOTE_SERVICE_RECORD_ID = '" + str(RecordId) + "' AND QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) +"'")
            getQuotetype = ""
            quote_obj = Sql.GetFirst("select DOCTYP_ID from SAQTRV (NOLOCK) where QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}'".format(contract_quote_record_id,quote_revision_record_id))
            if quote_obj:
                #getQuotetype = Product.Attributes.GetByName("QSTN_SYSEFL_QT_00723").GetValue()
                #Log.Info("SYDELCNMSG - SAQSGB")
                if Serviceobject.SERVICE_ID not in ["Z0108", "Z0110"]:
                    #A055S000P01-20807 - M
                    getCount = Sql.GetFirst("SELECT COUNT(SERVICE_ID) as cnt FROM SAQTSV(NOLOCK) WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID ='{}' AND SERVICE_ID != '{}'".format(quote_revision_record_id,contract_quote_record_id,Serviceobject.SERVICE_ID))
                    getServices = Sql.GetList("SELECT SERVICE_ID FROM SAQTSV(NOLOCK) WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID ='{}' AND SERVICE_ID != '{}'".format(quote_revision_record_id,contract_quote_record_id,Serviceobject.SERVICE_ID))
                    idling_flag = 0
                    if getServices:
                        for service in getServices:
                            getIdlingVal = Sql.GetFirst("select CpqTableEntryId from saqsce where QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID ='{}' AND SERVICE_ID = '{}' AND ISNULL(IDLING_ALLOWED,'No') = 'No'".format(quote_revision_record_id,contract_quote_record_id,service.SERVICE_ID))
                            if getIdlingVal:
                                idling_flag += 1
                    if idling_flag == getCount.cnt:
                        Sql.RunQuery("DELETE FROM SAQTDA WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID ='{}'".format(quote_revision_record_id,contract_quote_record_id))
                    #A055S000P01-20807 - M
                    TOOLDELETELIST = ["SAQTSV","SAQSCA","SAQICO","SAQSCE","SAQSGE","SAQICO","SAQIEN","SAQSFB","SAQSGB","SAQSCO","SAQTSE","SAQSFE","SAQSGE","SAQGPA","SAQGPM","SAQRGG","SAQGPE","SAQSAP","SAQSKP","SAQSAE","SAQSAO"]#1934 ,#INC08709720
                    for Table in TOOLDELETELIST:
                        QueryStatement = "DELETE FROM "+str(Table)+" WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' and SERVICE_ID = '{Service_id}'  AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(ObjectName = Table,Service_id = Serviceobject.SERVICE_ID,quote_revision_record_id=quote_revision_record_id)
                        Sql.RunQuery(QueryStatement)
                        #INC08739271 - Start - A
                        QueryStatement = "DELETE FROM "+str(Table)+" WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' and PAR_SERVICE_ID = '{Service_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(ObjectName = Table,Service_id = Serviceobject.SERVICE_ID,quote_revision_record_id=quote_revision_record_id)
                        Sql.RunQuery(QueryStatement)
                        #INC08739271 - End - A
                else:
                    #INC08696637 - M
                    TOOLDELETELIST = ["SAQTSV","SAQSPT","SAQSGE","SAQTSE","SAQIFP","SAQIEN","SAQSFE","SAQSCE","SAQSCO","SAQSCA","SAQGPA","SAQGPM","SAQRGG","SAQGPE","SAQSAE","SAQSAO"]#1934 
                    for Table in TOOLDELETELIST:
                        QueryStatement = "DELETE FROM "+str(Table)+" WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' and SERVICE_ID = '{Service_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(ObjectName = Table,Service_id = Serviceobject.SERVICE_ID,quote_revision_record_id=quote_revision_record_id)
                        Sql.RunQuery(QueryStatement)
                        #INC08739271 - Start - A
                        QueryStatement = "DELETE FROM "+str(Table)+" WHERE QUOTE_RECORD_ID ='"+str(contract_quote_record_id)+"' and PAR_SERVICE_ID = '{Service_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}'".format(ObjectName = Table,Service_id = Serviceobject.SERVICE_ID,quote_revision_record_id=quote_revision_record_id)
                        Sql.RunQuery(QueryStatement)
                        #INC08739271 - End - A
        elif ObjName == "SAQFBL":
            #CR BULK DELETE STARTS
            fab_location = Sql.GetFirst("SELECT * FROM SAQFBL (NOLOCK) WHERE QUOTE_FABLOCATION_RECORD_ID = '"+str(RecordId)+"' AND QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) +"'")
            fab_rec_id = fab_location.FABLOCATION_RECORD_ID
            fab_id = fab_location.FABLOCATION_ID
            if fab_location:
                #INC08696637 - M
                equp_count = Sql.GetFirst("SELECT COUNT(*) as count FROM SAQFEQ(NOLOCK) WHERE FABLOCATION_ID = '"+str(fab_id)+"' AND QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) +"'")
                if equp_count.count == 0:
                   #SAQFBL
                   fab_del = "DELETE FROM SAQFBL WHERE QUOTE_RECORD_ID ='{contract_quote_record_id}' AND  QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID = '{fab_id}'".format(contract_quote_record_id = contract_quote_record_id, quote_revision_record_id = quote_revision_record_id, fab_id = fab_id)
                   Sql.RunQuery(fab_del) 
                elif equp_count.count >1:
                   Trace.Write("equipment_key_iaaads")
                   equip_rec_ids = Sql.GetList("SELECT QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQFEQ(NOLOCK) WHERE FABLOCATION_ID = '"+str(fab_id)+"' AND QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) +"'")
                   equipment_key_ids = "','".join([equip_rec_id.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID for equip_rec_id in equip_rec_ids])
                else:
                    equip_rec_ids = Sql.GetFirst("SELECT QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID FROM SAQFEQ(NOLOCK) WHERE FABLOCATION_ID = '"+str(fab_id)+"' AND QUOTE_RECORD_ID = '"+str(contract_quote_record_id)+"' AND QTEREV_RECORD_ID = '" + str(quote_revision_record_id) +"'")
                    equipment_key_ids = equip_rec_ids.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID
                if equipment_key_ids:
                    #SAQGPA
                    saqgpa_del = "DELETE A FROM SAQGPA A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,equipment_key_ids = equipment_key_ids)
                    Sql.RunQuery(saqgpa_del)
                    #SAQGPM
                    saqgpm_del = "DELETE FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID NOT IN (SELECT  QTEREVPME_RECORD_ID FROM SAQGPA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id)
                    Sql.RunQuery(saqgpm_del)
                    #SAQRGG
                    saqrgg_del = "DELETE FROM SAQRGG WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID NOT IN (SELECT QTEREVGOT_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id)
                    Sql.RunQuery(saqrgg_del)
                    #SAQGPE
                    saqgpe_del = "DELETE FROM SAQGPE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEGGTPME_RECORD_ID NOT IN (SELECT  QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id)
                    Sql.RunQuery(saqgpe_del)
                    #SAQSAP
                    saqsap_del = "DELETE A FROM SAQSAP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,equipment_key_ids =equipment_key_ids)
                    Sql.RunQuery(saqsap_del)
                    #SAQSKP
                    saqskp_del = "DELETE A FROM SAQSKP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVMASY_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,equipment_key_ids = equipment_key_ids)
                    Sql.RunQuery(saqskp_del)
                    #SAQSKP2
                    saqskp_del_2 = "DELETE FROM SAQSKP WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}') AND ISNULL(QTEGBKPME_RECORD_ID,'') != ''".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
                    Sql.RunQuery(saqskp_del_2)
                    #SAQSAE
                    saqsae_del = "DELETE A FROM SAQSAE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,equipment_key_ids = equipment_key_ids)
                    Sql.RunQuery(saqsae_del)
                    #SAQSCE
                    saqsae_del = "DELETE A FROM SAQSCE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,equipment_key_ids = equipment_key_ids)
                    Sql.RunQuery(saqsae_del)
                    #SAQSCA
                    saqsca_del ="DELETE FROM SAQSCA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,equipment_key_ids = equipment_key_ids)
                    Sql.RunQuery(saqsca_del)
                    #SAQSCO
                    saqsco_del = "DELETE FROM SAQSCO WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,equipment_key_ids = equipment_key_ids)
                    Sql.RunQuery(saqsco_del)
                    #SAQSGB
                    get_saqsgb = Sql.GetList("Select DISTINCT GREENBOOK FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND GREENBOOK NOT IN (SELECT DISTINCT GREENBOOK FROM SAQSCO WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,fab_id = fab_id))
                    for delete in get_saqsgb:
                        Saqsgb_del = "DELETE FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND GREENBOOK = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,greenbook =str(delete.GREENBOOK))
                        Sql.RunQuery(Saqsgb_del)
                    #SAQSGE
                    get_saqsge = Sql.GetList("SELECT QTESRVGBK_RECORD_ID FROM SAQSGE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTESRVGBK_RECORD_ID NOT IN (SELECT QUOTE_SERVICE_GREENBOOK_RECORD_ID FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id))
                    for delete in get_saqsge:
                        Saqsge_del = "DELETE FROM SAQSGE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTESRVGBK_RECORD_ID = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,greenbook =str(delete.QTESRVGBK_RECORD_ID))
                        Sql.RunQuery(Saqsge_del)
                    #SAQFGB
                    saqfgb_del = "DELETE FROM SAQFGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID ='{fab_loc_id}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,fab_loc_id = fab_id)
                    Sql.RunQuery(saqfgb_del)
                    #SAQFBL
                    fab_del = "DELETE FROM SAQFBL WHERE QUOTE_RECORD_ID ='{contract_quote_record_id}' AND  QTEREV_RECORD_ID = '{quote_revision_record_id}' AND FABLOCATION_ID = '{fab_id}'".format(contract_quote_record_id = contract_quote_record_id, quote_revision_record_id = quote_revision_record_id, fab_id = fab_id)
                    Sql.RunQuery(fab_del)
                    #SAQFEA
                    saqfea_del = "DELETE FROM SAQFEA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_record_id,equipment_key_ids = equipment_key_ids)
                    Sql.RunQuery(saqfea_del)
                    #SAQFEQ
                    saqfeq_del = "DELETE FROM SAQFEQ WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID IN ('{equipment_key_ids}')".format(quote_revision_record_id = quote_revision_record_id, contract_quote_rec_id = contract_quote_record_id, equipment_key_ids = equipment_key_ids)
                    Sql.RunQuery(saqfeq_del)
                    #Add on products
                    Saqscn_del = "DELETE FROM SAQSCN WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID IN ('{equipment_key_ids}') ".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids)
                    Sql.RunQuery(Saqscn_del)
            #CR BULK DELETE STARTS
        elif ObjName == "SAQRCV":
            deleted_rec_query = Sql.GetFirst("SELECT CREDIT_APPLIED_INGL_CURR,CREDITVOUCHER_RECORD_ID FROM SAQRCV (NOLOCK) WHERE QUOTE_REV_CREDIT_VOUCHER_RECORD_ID = '"+str(RecordId)+"'")
            sacrcv_rec_query = Sql.GetFirst("SELECT CRTAPP_INGL_CURR,UNBL_INGL_CURR FROM SACRVC (NOLOCK) WHERE CREDITVOUCHER_RECORD_ID = '"+str(deleted_rec_query.CREDITVOUCHER_RECORD_ID)+"'")
            try:
                if sacrcv_rec_query.CRTAPP_INGL_CURR != "" and deleted_rec_query.CREDIT_APPLIED_INGL_CURR != "":
                    credit_applied = sacrcv_rec_query.CRTAPP_INGL_CURR - deleted_rec_query.CREDIT_APPLIED_INGL_CURR
                    unapplied_balance = sacrcv_rec_query.UNBL_INGL_CURR + deleted_rec_query.CREDIT_APPLIED_INGL_CURR
                    update_SAQRCV = "UPDATE SACRVC SET CRTAPP_INGL_CURR = '"+str(credit_applied)+"',UNBL_INGL_CURR = '"+str(unapplied_balance)+"' WHERE CREDITVOUCHER_RECORD_ID = '"+str(deleted_rec_query.CREDITVOUCHER_RECORD_ID)+"'"
                    Sql.RunQuery(update_SAQRCV)
            except:
                Trace.Write("EXCEPTION Occured")
            QueryStatement = "DELETE FROM SAQRCV WHERE QUOTE_REV_CREDIT_VOUCHER_RECORD_ID ='"+str(RecordId)+"'"
            Sql.RunQuery(QueryStatement)
        elif ObjName == "SAQSGB":
        #INC08696998 -A
            objects = ['SAQSGB','SAQSCO','SAQSCN','SAQSGE']
        #START-A055S000P01-20961-M
            if RecordId == "Z0123":
                objects.append("SAQSCN")
            elif RecordId == "Z0116":
                objects.append("SAQRCV")
        #END-A055S000P01-20961-M
            for obj in objects:
                saqsgb_delete = "DELETE FROM {obj} WHERE SERVICE_ID = '{RecordId}' AND QUOTE_RECORD_ID = '{qte_rec_id}' AND QTEREV_RECORD_ID = '{qtr_rev_rec_id}' AND GREENBOOK = '{TreeParentParam}' AND PAR_SERVICE_ID = '{TreeSuperParentParam}' ".format(obj=obj, RecordId = RecordId,qte_rec_id = contract_quote_record_id,qtr_rev_rec_id = quote_revision_record_id,TreeParentParam=TreeParentParam,TreeSuperParentParam=TreeSuperParentParam)
                Sql.RunQuery(saqsgb_delete)
            get_parent_delete =Sql.GetFirst("SELECT COUNT(*) as cnt From SAQSGB WHERE  SERVICE_ID = '{RecordId}' AND QUOTE_RECORD_ID = '{qte_rec_id}' AND QTEREV_RECORD_ID = '{qtr_rev_rec_id}' AND PAR_SERVICE_ID = '{TreeSuperParentParam}'".format(RecordId = RecordId,qte_rec_id = contract_quote_record_id,qtr_rev_rec_id = quote_revision_record_id,TreeSuperParentParam=TreeSuperParentParam))
            if get_parent_delete.cnt == 0: # Query result will be interger not string.
                objects2 = ['SAQTSV','SAQTSE']
                for obj2 in objects2:
                    saqtsv_delete = "DELETE FROM {obj2} WHERE SERVICE_ID = '{RecordId}' AND QUOTE_RECORD_ID = '{qte_rec_id}' AND QTEREV_RECORD_ID = '{qtr_rev_rec_id}' AND PAR_SERVICE_ID = '{TreeSuperParentParam}' ".format(obj2=obj2, RecordId = RecordId,qte_rec_id = contract_quote_record_id,qtr_rev_rec_id = quote_revision_record_id,TreeSuperParentParam=TreeSuperParentParam)
                    Sql.RunQuery(saqtsv_delete)
        #INC08696998 -A
        #INC08632845-A STARTS
        elif ObjName == "SAQSAF":
            get_send_fab =Sql.GetFirst("SELECT SNDFBL_ID FROM SAQSAF(NOLOCK) WHERE QUOTE_REV_SENDING_ACC_FAB_LOCATION_RECORD_ID ='{RecordId}' AND QUOTE_RECORD_ID = '{qte_rec_id}' AND QTEREV_RECORD_ID = '{qtr_rev_rec_id}'".format(RecordId = RecordId,qte_rec_id = contract_quote_record_id,qtr_rev_rec_id = quote_revision_record_id))
            saqsaf_del = "DELETE FROM SAQSAF WHERE SNDFBL_ID = '{fab_id}' AND QUOTE_RECORD_ID = '{qte_rec_id}' AND QTEREV_RECORD_ID = '{qtr_rev_rec_id}'".format(fab_id=get_send_fab.SNDFBL_ID,qte_rec_id = contract_quote_record_id,qtr_rev_rec_id = quote_revision_record_id)
            Sql.RunQuery(saqsaf_del)
            saqase_del = "DELETE FROM SAQASE WHERE SNDFBL_ID = '{fab_id}' AND QUOTE_RECORD_ID = '{qte_rec_id}' AND QTEREV_RECORD_ID = '{qtr_rev_rec_id}'".format(fab_id=get_send_fab.SNDFBL_ID,qte_rec_id = contract_quote_record_id,qtr_rev_rec_id = quote_revision_record_id)
            Sql.RunQuery(saqase_del)
        #INC08632845-A STARTS

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
                        GetSAQTSV = Sql.GetFirst("SELECT * FROM SAQTSV (NOLOCK) WHERE QUOTE_SERVICE_RECORD_ID = '" + str(RecordId) + "'")
                    if RecordId:
                        QueryStatement = ("delete from " + str(sqlobj.OBJECT_NAME) + " where " + str(sqlobj.API_NAME) + " ='" + str(RecordId) + "'")
                        Sql.RunQuery(QueryStatement)
                if RecordId != "":
                    GetQuery = Sql.GetList("select CpqTableEntryId from " + str(ObjName) + " where " + str(ColumnName.API_NAME) + "='" + str(RecordId) + "'")
                    if ObjName == "SAQRSP":
                        getpart = Sql.GetFirst("SELECT PART_NUMBER FROM SAQRSP (NOLOCK) WHERE QUOTE_REV_PO_PRODUCT_LIST_ID = '{}'".format(RecordId))
                        part = getpart.PART_NUMBER
                        Sql.RunQuery("DELETE FROM SAQRIP WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SERVICE_ID = 'Z0101' AND PART_NUMBER = '{}'".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),part))
                        #INC08737172 Start - A
                        if subtab == 'Inclusions':
                            Sql.RunQuery("DELETE FROM SAQRSP WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SERVICE_ID = 'Z0101' AND INCLUDED='True' AND NEW_PART='False' AND PART_NUMBER = '{}' AND GREENBOOK = '{}' AND PAR_SERVICE_ID = '{}'".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),part, TreeParam, TreeParentParam))
                        #INC08737172 End - A
                    if ObjName == "SAQSPT":
                        getpart = Sql.GetFirst("SELECT PART_NUMBER FROM SAQSPT (NOLOCK) WHERE QUOTE_SERVICE_PART_RECORD_ID = '{}'".format(RecordId))
                        part = getpart.PART_NUMBER
                        Sql.RunQuery("DELETE FROM SAQSPT WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID = '{}' AND SERVICE_ID IN( 'Z0110','Z0108') AND PAR_PART_NUMBER = '{}'".format(Quote.GetGlobal("quote_revision_record_id"),Quote.GetGlobal("contract_quote_record_id"),part))
                    if GetQuery is not None:
                        for tablerow in GetQuery:
                            tableInfo.AddRow(tablerow)
                            Sql.Delete(tableInfo)
        return True,refresh_flag

    def EquipmentDelete(self,RecordId, ObjName):
        if TreeParentParam == 'Comprehensive Services' or TreeParentParam == 'Complementary Products':
            ServiceId = TreeParam
            Get_refresh = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as cnt FROM SAQSCO WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' ".format(contract_quote_rec_id,quote_revision_record_id,ServiceId))
        if TreeSuperParentParam == 'Comprehensive Services' or TreeSuperParentParam == 'Complementary Products':
            ServiceId = TreeParentParam
            Get_refresh = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as cnt FROM SAQSCO WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}' AND GREENBOOK = '{}' ".format(contract_quote_rec_id,quote_revision_record_id,ServiceId,TreeParam))
        if TreeTopSuperParentParam =='Comprehensive Services':
            ServiceId = TreeSuperParentParam
        if TreeParam == "Add-On Products":
            ServiceId = Product.GetGlobal('addon_service_id')
            Get_refresh = Sql.GetFirst("SELECT COUNT(CpqTableEntryId) as cnt FROM SAQSCO WHERE QUOTE_RECORD_ID = '{}' AND QTEREV_RECORD_ID = '{}' AND SERVICE_ID = '{}'".format(contract_quote_rec_id,quote_revision_record_id,ServiceId))
        refresh_flag = True if Get_refresh.cnt == 1 else False
        GetEquipment = Sql.GetFirst("SELECT EQUIPMENT_ID, PAR_SERVICE_ID,QTEREVFEQ_RECORD_ID,SERVICE_ID,QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID FROM SAQSCO (nolock) WHERE QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '{}'".format(RecordId.split("#")[4]))
        equipment_key_ids = GetEquipment.QTEREVFEQ_RECORD_ID
        service_id = GetEquipment.SERVICE_ID
        key = GetEquipment.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID
        if TreeParam != "Add-On Products":
            #SAQGPA
            saqgpa_del = "DELETE A FROM SAQGPA A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}' AND B.QTESRVCOB_RECORD_ID ='{key}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids,service_id = service_id,key =key)
            Sql.RunQuery(saqgpa_del)
            #SAQGPM
            saqgpm_del = "DELETE FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' AND QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID NOT IN (SELECT  QTEREVPME_RECORD_ID FROM SAQGPA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,service_id = service_id)
            Sql.RunQuery(saqgpm_del)
            #SAQRGG
            saqrgg_del = "DELETE FROM SAQRGG WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' AND QUOTE_REV_PO_GREENBOOK_GOT_CODES_RECORD_ID NOT IN (SELECT QTEREVGOT_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' )".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,service_id = service_id)
            Sql.RunQuery(saqrgg_del)
            #SAQGPE
            saqgpe_del = "DELETE FROM SAQGPE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' AND QTEGGTPME_RECORD_ID NOT IN (SELECT  QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID FROM SAQGPM WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,service_id = service_id)
            Sql.RunQuery(saqgpe_del)
            #SAQSAP
            saqsap_del = "DELETE A FROM SAQSAP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND A.SERVICE_ID = '{service_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids =equipment_key_ids,service_id = service_id)
            Sql.RunQuery(saqsap_del)
            #SAQSKP
            saqskp_del = "DELETE A FROM SAQSKP A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVMASY_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND A.SERVICE_ID = '{service_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids,service_id = service_id)
            Sql.RunQuery(saqskp_del)
            #SAQSKP2
            saqskp_del_2 = "DELETE FROM SAQSKP WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}' AND SERVICE_ID = '{service_id}' AND ISNULL(QTEGBKPME_RECORD_ID,'') != ''".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids, service_id=service_id)
            Sql.RunQuery(saqskp_del_2)
            #SAQSAE
            saqsae_del = "DELETE A FROM SAQSAE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOA_RECORD_ID = B.QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND A.SERVICE_ID = '{service_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids,service_id = service_id)
            Sql.RunQuery(saqsae_del)
            #SAQSCE
            saqsae_del = "DELETE A FROM SAQSCE A JOIN SAQSCA B ON A.QUOTE_RECORD_ID = B.QUOTE_RECORD_ID AND A.QTEREV_RECORD_ID = B.QTEREV_RECORD_ID AND A.QTESRVCOB_RECORD_ID = B.QTESRVCOB_RECORD_ID AND A.SERVICE_ID = B.SERVICE_ID WHERE A.QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND A.QTEREV_RECORD_ID = '{quote_revision_record_id}' AND A.SERVICE_ID = '{service_id}' AND B.QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids,service_id= service_id)
            Sql.RunQuery(saqsae_del)
            #SAQSCA
            saqsca_del ="DELETE FROM SAQSCA WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids,service_id = service_id)
            Sql.RunQuery(saqsca_del)
            #SAQSCO
            saqsco_del = "DELETE FROM SAQSCO WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' AND QTEREVFEQ_RECORD_ID = '{equipment_key_ids}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,equipment_key_ids = equipment_key_ids,service_id=service_id)
            Sql.RunQuery(saqsco_del)
            #SAQSGB
            get_saqsgb = Sql.GetList("Select DISTINCT GREENBOOK FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK NOT IN (SELECT DISTINCT GREENBOOK FROM SAQSCO WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,service_id = service_id))
            for delete in get_saqsgb:
                Saqsgb_del = "DELETE FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' AND GREENBOOK = '{greenbook}' ".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,greenbook =str(delete.GREENBOOK),service_id = service_id)
                Sql.RunQuery(Saqsgb_del)
                refresh_flag = True
            #SAQSGE
            get_saqsge = Sql.GetList("SELECT QTESRVGBK_RECORD_ID FROM SAQSGE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' AND QTESRVGBK_RECORD_ID NOT IN (SELECT QUOTE_SERVICE_GREENBOOK_RECORD_ID FROM SAQSGB WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}')".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,service_id = service_id))
            for delete in get_saqsge:
                Saqsge_del = "DELETE FROM SAQSGE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND QTESRVGBK_RECORD_ID = '{greenbook}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,greenbook =str(delete.QTESRVGBK_RECORD_ID))
                Sql.RunQuery(Saqsge_del)
        else:
            #SAQSCE
            saqsae_del = "DELETE FROM SAQSCE WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' AND QTESRVCOB_RECORD_ID = '{key}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,key = key,service_id = service_id)
            Sql.RunQuery(saqsae_del)
            #SAQSCO
            saqsco_del = "DELETE FROM SAQSCO WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' AND QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID = '{key}'".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,key = key,service_id=service_id)
            Sql.RunQuery(saqsco_del)
            #SAQSCN
            Saqscn_del = "DELETE FROM SAQSCN WHERE QUOTE_RECORD_ID = '{contract_quote_rec_id}' AND QTEREV_RECORD_ID = '{quote_revision_record_id}' AND SERVICE_ID = '{service_id}' AND QTESRVCOB_RECORD_ID = '{key}' ".format(quote_revision_record_id = quote_revision_record_id,contract_quote_rec_id = contract_quote_rec_id,key =key,service_id = service_id)
            Sql.RunQuery(Saqscn_del)
            
        Trace.Write("refresh_flagrefresh_flagrefresh_flag"+str(refresh_flag))
        #A055S000P01-20807 - M
        getIdlingVal = Sql.GetFirst("select CpqTableEntryId from saqsce where QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID ='{}' AND ISNULL(IDLING_ALLOWED,'No') = 'Yes'".format(quote_revision_record_id,contract_quote_rec_id))
        if not getIdlingVal:
            Sql.RunQuery("DELETE FROM SAQTDA WHERE QTEREV_RECORD_ID = '{}' AND QUOTE_RECORD_ID ='{}'".format(quote_revision_record_id,contract_quote_rec_id))
        #A055S000P01-20807 - M
        return refresh_flag


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
    contract_quote_rec_id = Quote.GetGlobal("contract_quote_record_id")
except:
    contract_quote_rec_id = ""
try:
    quote_revision_record_id = Quote.GetGlobal("quote_revision_record_id")
except:
    quote_revision_record_id = ""


#INC08737172 Start - A
try:
    subtab = Param.SUBTAB
except:
    subtab = ''
#INC08737172 End - A

if str(Action) == "old" and (str(GridID) != "SYOBJC" and str(GridID) != "SAQTSV"):
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.DELETECONFIRMATION(LABLE, GridID))
elif str(Action) == "old" and str(GridID) == "SAQTSV":
    Trace.Write("checking del cond")
    #INC08737172 Start - A
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.CommonDelete(LABLE,GridID, subtab))
elif str(Action) == "delete" and str(GridID) != "SYOBJX":
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.CommonDelete(LABLE,GridID, subtab))
    #INC08737172 End - A
elif str(Action) == "new" and str(GridID) == "SYOBJC":
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.Constdel(LABLE, GridID))
elif str(Action) == "delete" and str(GridID) == "SYOBJX":
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.Constdel(LABLE, GridID))
#A055S000P01-20970 Starts
elif str(Action) == "confirm_bulk_delete":
    Message = Param.Message
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.BulkDeleteConfirm(LABLE, GridID, Message))
#A055S000P01-20970 Ends
else:
    Message = Param.Message
    RecordValue = Param.RecordValue
    ApiResponse = ApiResponseFactory.JsonResponse(delconp.CommonDeleteConfirmation(LABLE, GridID, Message, RecordValue))

# =========================================================================================================================================
#   __script_name : Module/SYERRMSGVL.PY
#   __script_description : THIS SCRIPT IS USED TO DISPLAY AND SAVE THE ERROR MESSAGE
#   __primary_author__ : JOE EBENEZER
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import Webcom.Configurator.Scripting.Test.TestProduct
#Webcom = Webcom  # pylint: disable=E0602
Trace = Trace  # pylint: disable=E0602
Log = Log  # pylint: disable=E0602
ScriptExecutor = ScriptExecutor  # pylint: disable=E0602
# Product = Product   # pylint: disable=E0602
# Param = Param   # pylint: disable=E0602
# ApiResponseFactory = ApiResponseFactory   # pylint: disable=E0602
import SYCNGEGUID as CPQID
from SYDATABASE import SQL
#from datetime import timedelta
from datetime import datetime as date
import datetime

Sql = SQL()

TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
current_tab = str(TestProduct.CurrentTab)


def GetTablevelErrorMessage(TabRecordId, API_Name, RecordId, ErrorType):
    ErrorMsgList = []    
    ###8199, 8127, 8911,8990 starts....

    ErrorMessageObjQry = Sql.GetList(
        "SELECT TOP 1000 SYMSGS.RECORD_ID , SYMSGS.MESSAGE_TEXT, SYMSGS.MESSAGE_TYPE, SYMSGS.MESSAGE_CODE, SYMSGS.MESSAGE_LEVEL, SYMSGS.CTX_CALCULATION_LOGIC FROM SYMSGS (nolock) INNER JOIN SYELOG (NOLOCK) ON SYELOG.ERRORMESSAGE_RECORD_ID = SYMSGS.RECORD_ID WHERE SYMSGS.TAB_RECORD_ID = '"
        + str(TabRecordId)
        + "'AND SYMSGS.MESSAGE_LEVEL = '"
        + str(ErrorType)
        + "' AND SYELOG.OBJECT_VALUE_REC_ID = '"
        + str(RecordId)
        + "' and SYMSGS.MESSAGE_TYPE='TAB LEVEL' ORDER BY abs(SYMSGS.MESSAGE_CODE)"
    )    
    if ErrorMessageObjQry is not None:
        for ErrorMessageObj in ErrorMessageObjQry:
            FORMULA = str(ErrorMessageObj.CTX_CALCULATION_LOGIC)
            FORMULA = FORMULA.replace("{" + API_Name + "}", RecordId)
            Trace.Write("Formula:" + str(FORMULA))
            if FORMULA is not None and FORMULA != "":
                FORMULA_RESULT = Sql.GetFirst(str(FORMULA))

                if FORMULA_RESULT is not None:
                    Trace.Write("FORMULA_RESULT_MESSAGE" + str(FORMULA_RESULT.MESSAGE))
                    if str(FORMULA_RESULT.MESSAGE).upper() == "TRUE":
                        ErrorMessage = {}
                        ErrorMessage["MESSAGE_LEVEL"] = str(ErrorMessageObj.MESSAGE_LEVEL)
                        ErrorMessage["MESSAGE_TEXT"] = str(ErrorMessageObj.MESSAGE_TEXT)
                        ErrorMessage["MESSAGE_CODE"] = str(ErrorMessageObj.MESSAGE_CODE)
                        ErrorMessage["MESSAGE_TYPE"] = str(ErrorMessageObj.MESSAGE_TYPE)
                        ErrorMessage["RECORD_ID"] = str(ErrorMessageObj.RECORD_ID)
                        ErrorMsgList.append(ErrorMessage)	
	return ErrorMsgList

def GetTablevelMessage(TabRecordId, API_Name, RecordId):
    Message = []
    msg_txt = []
    Message = GetTablevelErrorMessage(TabRecordId, API_Name, RecordId, "ERROR")    
    if len(Message) == 0:
        Message = GetTablevelErrorMessage(TabRecordId, API_Name, RecordId, "WARNING")
    if Message is not None:
        for mlist in Message:
            if str(mlist["MESSAGE_LEVEL"]) == "ERROR":
                ErrorIcon = '<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error">'
            elif str(mlist["MESSAGE_LEVEL"]) == "WARNING":
                ErrorIcon = '<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Warning">'
            else:
                ErrorIcon = '<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infocircle1.svg" alt="Info">'
            msg_txt.append(
                "<label> "
                + str(ErrorIcon)
                + str(mlist["MESSAGE_LEVEL"])
                + " : "
                + str(mlist["MESSAGE_CODE"])
                + " : "
                + str(mlist["MESSAGE_TEXT"])
                + "</label>"
            )  ###9783 ends...
    return msg_txt

def GetObjlevelErrorMessage(ObjectRecordId, RecordId, ErrorType):
    ErrorMsgList = []
    
    ErrorMessageObjQry = Sql.GetList(
        "SELECT TOP 1000 SYMSGS.RECORD_ID , SYMSGS.MESSAGE_TEXT, SYMSGS.MESSAGE_TYPE, SYMSGS.MESSAGE_CODE, SYMSGS.MESSAGE_LEVEL FROM SYMSGS (nolock) INNER JOIN SYELOG (NOLOCK) ON SYELOG.ERRORMESSAGE_RECORD_ID = SYMSGS.RECORD_ID WHERE SYMSGS.OBJECT_RECORD_ID = '"
        + str(ObjectRecordId)
        + "'AND SYMSGS.MESSAGE_LEVEL = '"
        + str(ErrorType)
        + "' AND SYELOG.OBJECT_VALUE_REC_ID = '"
        + str(RecordId)
        + "' ORDER BY abs(SYMSGS.MESSAGE_CODE)"
    )
    
    if ErrorMessageObjQry is not None:
        for ErrorMessageObj in ErrorMessageObjQry:
            ErrorMessage = {}
            ErrorMessage["MESSAGE_LEVEL"] = str(ErrorMessageObj.MESSAGE_LEVEL)
            ErrorMessage["MESSAGE_TEXT"] = str(ErrorMessageObj.MESSAGE_TEXT)
            ErrorMessage["MESSAGE_CODE"] = str(ErrorMessageObj.MESSAGE_CODE)
            ErrorMessage["MESSAGE_TYPE"] = str(ErrorMessageObj.MESSAGE_TYPE)
            ErrorMessage["RECORD_ID"] = str(ErrorMessageObj.RECORD_ID)
            ErrorMsgList.append(ErrorMessage)    
    return ErrorMsgList

# def GetEntObjlevelErrorMessage(ObjectRecordId, RecordId, ErrorType):
#     ErrorMsgList = []
    
#     ErrorMessageObjQry = Sql.GetList(
#         "SELECT TOP 1000 SYMSGS.RECORD_ID , SYMSGS.MESSAGE_TEXT, SYMSGS.MESSAGE_TYPE, SYMSGS.MESSAGE_CODE, SYMSGS.MESSAGE_LEVEL FROM SYMSGS (nolock) INNER JOIN SYELOG (NOLOCK) ON SYELOG.ERRORMESSAGE_RECORD_ID = SYMSGS.RECORD_ID WHERE SYMSGS.OBJECT_RECORD_ID = '"
#         + str(ObjectRecordId)
#         + "'AND SYMSGS.MESSAGE_LEVEL = '"
#         + str(ErrorType)
#         + "' AND SYELOG.OBJECT_VALUE_REC_ID = '"
#         + str(RecordId)
#         + "' ORDER BY abs(SYMSGS.MESSAGE_CODE)"
#     )
    
#     if ErrorMessageObjQry is not None:
#         for ErrorMessageObj in ErrorMessageObjQry:
#             ErrorMessage = {}
#             ErrorMessage["MESSAGE_LEVEL"] = str(ErrorMessageObj.MESSAGE_LEVEL)
#             ErrorMessage["MESSAGE_TEXT"] = str(ErrorMessageObj.MESSAGE_TEXT)
#             ErrorMessage["MESSAGE_CODE"] = str(ErrorMessageObj.MESSAGE_CODE)
#             ErrorMessage["MESSAGE_TYPE"] = str(ErrorMessageObj.MESSAGE_TYPE)
#             ErrorMessage["RECORD_ID"] = str(ErrorMessageObj.RECORD_ID)
#             ErrorMsgList.append(ErrorMessage)    
#     return ErrorMsgList

def GetObjlevelMessage(ObjectRecordId, RecordId):
    Message = []
    msg_txt = ""
    Message = GetObjlevelErrorMessage(ObjectRecordId, RecordId, "ERROR")
    if len(Message) == 0:
        Message = GetObjlevelErrorMessage(ObjectRecordId, RecordId, "WARNING")
    if Message is not None:
        for mlist in Message:
            if str(mlist["MESSAGE_LEVEL"]) == "ERROR":
                ErrorIcon = '<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error">'
            elif str(mlist["MESSAGE_LEVEL"]) == "WARNING":
                ErrorIcon = '<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Warning">'
            else:
                ErrorIcon = '<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infocircle1.svg" alt="Info">'
            msg_txt += (
                "<label> "
                + str(ErrorIcon)
                + str(mlist["MESSAGE_LEVEL"])
                + " : "
                + str(mlist["MESSAGE_CODE"])
                + " : "
                + str(mlist["MESSAGE_TEXT"])
                + "</label>"
            )
    return msg_txt

def GetQuestionlevelMessage(TABLE_NAME, DictData, SEC_REC_ID, Seg=None):
    Trace.Write("Question Level Error Updated")
    ConvertDictData = DictData
    requiredDict = []
    TestProduct = Webcom.Configurator.Scripting.Test.TestProduct()
    tabName = str(TestProduct.CurrentTab)    
    prodName = TestProduct.Name
    SqlQuery = (
        "select d.API_NAME,d.FIELD_LABEL,d.REQUIRED,c.RECORD_ID,c.SECTION_RECORD_ID from SYTABS (nolock) a inner join SYSECT (nolock) b on a.PAGE_RECORD_ID = b.PAGE_RECORD_ID inner join SYSEFL (nolock) c on c.SECTION_RECORD_ID = b. RECORD_ID inner join  SYOBJD (nolock) d on d.OBJECT_NAME = c.API_NAME and d.API_NAME = c.API_FIELD_NAME where a.SAPCPQ_ALTTAB_NAME = '"
        + str(tabName).upper()
        + "' and a.APP_LABEL ='"
        + str(prodName)
        + "' and b.RECORD_ID = '"
        + str(SEC_REC_ID)
        + "' and d.REQUIRED = 'TRUE'"
    )    
    Required_obj = Sql.GetList(SqlQuery)
    if Required_obj is not None:
        for x in Required_obj:
            RequiredApiName = str(x.API_NAME)            
            if RequiredApiName in ConvertDictData:
                RequiredApiVal = ConvertDictData[RequiredApiName]
                if RequiredApiVal == "":
                    Err_msg = str(x.FIELD_LABEL) + " is a required field"
                    cur_val = "QSTN_" + str(x.RECORD_ID.replace("-", "_"))
                    cur_val = cur_val + "|" + str(Err_msg)
                    requiredDict.append(str(cur_val))    
    return requiredDict

def GetIflowlevelWarningMessage(OBJRECID, SegmentId, versionId):
    msg_txt = ""
    ErrorMessageObjQry = Sql.GetFirst(
        "SELECT TOP 1000 SYMSGS.RECORD_ID , SYMSGS.MESSAGE_TEXT, SYMSGS.MESSAGE_TYPE, SYMSGS.MESSAGE_CODE, SYMSGS.MESSAGE_LEVEL, SYMSGS.CTX_CALCULATION_LOGIC FROM SYMSGS (nolock) INNER JOIN SYELOG (NOLOCK) ON SYELOG.ERRORMESSAGE_RECORD_ID = SYMSGS.RECORD_ID WHERE SYMSGS.OBJECT_RECORD_ID != '' AND SYMSGS.MESSAGE_LEVEL = 'INFORMATION' AND SYMSGS.RECORD_ID = 'SYMSGS-SE-00008' AND SYELOG.OBJECT_VALUE = '"
        + str(SegmentId)
        + "' AND SYELOG.OBJECT_VALUE_REC_ID = '"
        + str(versionId)
        + "' ORDER BY abs(SYMSGS.MESSAGE_CODE)"
    )
    if ErrorMessageObjQry is not None:
        msg_txt = (
            '<label> <i class="fa fa-info" aria-hidden="true"></i> '
            + str(ErrorMessageObjQry.MESSAGE_LEVEL)
            + " : "
            + str(ErrorMessageObjQry.MESSAGE_CODE)
            + " : "
            + str(ErrorMessageObjQry.MESSAGE_TEXT)
            + "</label>"
        )
    return msg_txt

# A043S001P01-9994 - Start
def GetQBlevelinfoMessage(OBJRECID, SegmentId, versionId):
    msg_txt = ""
    ErrorMessageObjQry = Sql.GetFirst(
        "SELECT TOP 10 SYMSGS.RECORD_ID, SYMSGS.MESSAGE_TEXT, SYMSGS.MESSAGE_TYPE, SYMSGS.MESSAGE_CODE, SYMSGS.MESSAGE_LEVEL, SYMSGS.CTX_CALCULATION_LOGIC FROM SYMSGS (nolock) INNER JOIN SYELOG (NOLOCK) ON SYELOG.ERRORMESSAGE_RECORD_ID = SYMSGS.RECORD_ID WHERE SYMSGS.OBJECT_RECORD_ID = '"
        + str(OBJRECID)
        + "'AND SYMSGS.MESSAGE_LEVEL = 'INFORMATION' AND SYELOG.OBJECT_VALUE = '"
        + str(SegmentId)
        + "' AND SYELOG.OBJECT_VALUE_REC_ID = '"
        + str(versionId)
        + "' AND SYMSGS.MESSAGE_CODE = '100088' ORDER BY abs(SYMSGS.MESSAGE_CODE)"
    )
    if ErrorMessageObjQry is not None:
        msg_txt = (
            '<label> <i class="fa fa-info" aria-hidden="true"></i> '
            + str(ErrorMessageObjQry.MESSAGE_LEVEL)
            + " : "
            + str(ErrorMessageObjQry.MESSAGE_CODE)
            + " : "
            + str(ErrorMessageObjQry.MESSAGE_TEXT)
            + "</label>"
        )
    else:
        try:
            insertErrLogWarnQuery = """INSERT SYELOG (ERROR_LOGS_RECORD_ID, ERRORMESSAGE_RECORD_ID, ERRORMESSAGE_DESCRIPTION, OBJECT_NAME, OBJECT_TYPE, OBJECT_RECORD_ID, OBJECT_VALUE_REC_ID, OBJECT_VALUE, ACTIVE, CPQTABLEENTRYADDEDBY, CPQTABLEENTRYDATEADDED, CpqTableEntryModifiedBy, CpqTableEntryDateModified)
				select
				CONVERT(VARCHAR(4000),NEWID()) as ERROR_LOGS_RECORD_ID, 
				RECORD_ID as ERRORMESSAGE_RECORD_ID,
				MESSAGE_TEXT as ERRORMESSAGE_DESCRIPTION,
				OBJECT_APINAME as OBJECT_NAME,
				MESSAGE_TYPE as OBJECT_TYPE,
				OBJECT_RECORD_ID as OBJECT_RECORD_ID,
				'{versionId}' as OBJECT_VALUE_REC_ID,
				'{segmentId}' as OBJECT_VALUE,
				1 as ACTIVE,
				'{Get_UserID}' as CPQTABLEENTRYADDEDBY, 
				convert(varchar(10), '{datetime_value}', 101) as CPQTABLEENTRYDATEADDED, 
				'{Get_UserID}' as CpqTableEntryModifiedBy, 
				convert(varchar(10), '{datetime_value}', 101) as CpqTableEntryDateModified
				from SYMSGS (nolock)
				where OBJECT_APINAME = 'PACAFL' and OBJECT_RECORD_ID = 'SYOBJ-00155' and MESSAGE_LEVEL = 'INFORMATION' and RECORD_ID = 'SYMSGS-SE-000012'
			""".format(
                segmentId=str(Product.GetGlobal("segment_rec_id")),
                versionId=str(Product.GetGlobal("segmentRevisionId")),
                Get_UserID=ScriptExecutor.ExecuteGlobal("SYUSDETAIL", "USERID"),
                datetime_value=datetime.datetime.now(),
            )            
            Sql.RunQuery(insertErrLogWarnQuery)
        except:
            Log.Info("error in insertErrLogWarnQueryStatement")
        ErrorMessageObjQryQB = Sql.GetFirst(
            "SELECT TOP 10 SYMSGS.RECORD_ID , SYMSGS.MESSAGE_TEXT, SYMSGS.MESSAGE_TYPE, SYMSGS.MESSAGE_CODE, SYMSGS.MESSAGE_LEVEL, SYMSGS.CTX_CALCULATION_LOGIC FROM SYMSGS (nolock) INNER JOIN SYELOG (NOLOCK) ON SYELOG.ERRORMESSAGE_RECORD_ID = SYMSGS.RECORD_ID WHERE SYMSGS.OBJECT_RECORD_ID = '"
            + str(OBJRECID)
            + "'AND SYMSGS.MESSAGE_LEVEL = 'INFORMATION' AND SYELOG.OBJECT_VALUE = '"
            + str(SegmentId)
            + "' AND SYELOG.OBJECT_VALUE_REC_ID = '"
            + str(versionId)
            + "' AND SYMSGS.RECORD_ID = 'SYMSGS-SE-000012' ORDER BY abs(SYMSGS.MESSAGE_CODE)"
        )
        if ErrorMessageObjQryQB is not None:
            msg_txt = (
                '<label> <img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infocircle1.svg" alt="Info"> '
                + str(ErrorMessageObjQryQB.MESSAGE_LEVEL)
                + " : "
                + str(ErrorMessageObjQryQB.MESSAGE_CODE)
                + " : "
                + str(ErrorMessageObjQryQB.MESSAGE_TEXT)
                + "</label>"
            )
    return msg_txt

def GetErrorMessage(TabRecordId, API_Name, RecordId, ErrorType):
    ErrorMsgList = []
    msg_txt = []
    ErrorMessageObjQry = Sql.GetList(
        "SELECT TOP 1000 SYMSGS.RECORD_ID , SYMSGS.MESSAGE_TEXT, SYMSGS.MESSAGE_TYPE, SYMSGS.MESSAGE_CODE, SYMSGS.MESSAGE_LEVEL, SYMSGS.CTX_CALCULATION_LOGIC FROM SYMSGS (nolock) WHERE SYMSGS.TAB_RECORD_ID = '"
        + str(TabRecordId)
        + "'AND SYMSGS.MESSAGE_LEVEL = '"
        + str(ErrorType)
        + "' and SYMSGS.MESSAGE_TYPE='TAB LEVEL' ORDER BY abs(SYMSGS.MESSAGE_CODE)"
    )
    if ErrorMessageObjQry is not None:
        for ErrorMessageObj in ErrorMessageObjQry:
            FORMULA = str(ErrorMessageObj.CTX_CALCULATION_LOGIC)
            FORMULA = FORMULA.replace("{" + API_Name + "}", RecordId)
            #Trace.Write("Formula:" + str(FORMULA))
            if FORMULA is not None and FORMULA != "":
                FORMULA_RESULT = Sql.GetFirst(str(FORMULA))

                if FORMULA_RESULT is not None:
                    Trace.Write("FORMULA_RESULT_MESSAGE" + str(FORMULA_RESULT.MESSAGE))
                    if str(FORMULA_RESULT.MESSAGE).upper() == "TRUE":
                        ErrorMessage = {}
                        ErrorMessage["MESSAGE_LEVEL"] = str(ErrorMessageObj.MESSAGE_LEVEL)
                        ErrorMessage["MESSAGE_TEXT"] = str(ErrorMessageObj.MESSAGE_TEXT)
                        ErrorMessage["MESSAGE_CODE"] = str(ErrorMessageObj.MESSAGE_CODE)
                        ErrorMessage["MESSAGE_TYPE"] = str(ErrorMessageObj.MESSAGE_TYPE)
                        ErrorMessage["RECORD_ID"] = str(ErrorMessageObj.RECORD_ID)
                        ErrorMsgList.append(ErrorMessage)

    if ErrorMsgList is not None:
        for mlist in ErrorMsgList:
            if str(mlist["MESSAGE_LEVEL"]) == "ERROR":
                ErrorIcon = '<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/stopicon1.svg" alt="Error">'
            elif str(mlist["MESSAGE_LEVEL"]) == "WARNING":
                ErrorIcon = '<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/warning1.svg" alt="Warning">'
            else:
                ErrorIcon = '<img src="/mt/APPLIEDMATERIALS_TST/Additionalfiles/infocircle1.svg" alt="Info">'
            msg_txt.append(
                "<label> "
                + str(ErrorIcon)
                + str(mlist["MESSAGE_LEVEL"])
                + " : "
                + str(mlist["MESSAGE_CODE"])
                + " : "
                + str(mlist["MESSAGE_TEXT"])
                + "</label>"
            )
    return msg_txt

try:
    Action = Param.Action
except:
    Action = ""
if Action == "VIEW":
    Level = Param.Level
    if str(Level) == "TAB":
        RecordId = Param.RecordId
        TabName = Param.TabName
        API_Name = ""
        TabRecordId = ""
        ApiNameQuery = Sql.GetFirst(
            "select SYOBJH.RECORD_NAME, SYPAGE.TAB_RECORD_ID, SYOBJH.OBJECT_NAME from SYSECT (nolock) inner join SYOBJH (nolock) on SYOBJH.OBJECT_NAME = SYSECT.PRIMARY_OBJECT_NAME INNER JOIN SYPAGE (NOLOCK) ON SYPAGE.RECORD_ID = SYSECT.PAGE_RECORD_ID where SYPAGE.TAB_NAME = '"
            + str(TabName)
            + "' and SYSECT.SECTION_NAME = 'BASIC INFORMATION'"
        )
        if ApiNameQuery is not None:
            API_Name = str(ApiNameQuery.RECORD_NAME)
            TabRecordId = str(ApiNameQuery.TAB_RECORD_ID)
            ObjuctName = str(ApiNameQuery.OBJECT_NAME)
            if str(ObjuctName) == "PRLPBE":
                RecordId = CPQID.KeyCPQId.GetKEYId(str(ObjuctName), str(RecordId))                
        ApiResponse = ApiResponseFactory.JsonResponse(GetTablevelMessage(TabRecordId, API_Name, RecordId))
    if str(Level) == "OBJECT":
        OBJRECID = Param.OBJRECID
        objrecs = OBJRECID.split("_")
        try:
            ObjectRecId = objrecs[2] + "-" + objrecs[3] + "-" + objrecs[4] + "-" + objrecs[5] + "-" + objrecs[6]
        except:
            ObjectRecId = ""       
        try:
            RECORDID = Param.RECORDID
        except:
            RECORDID = ""
        if ObjectRecId is not None or ObjectRecId != "":
            ApiNameQuery = Sql.GetFirst(
                "select RECORD_NAME from SYOBJH (nolock) where RECORD_ID = '" + str(ObjectRecId) + "'"
            )
            if ApiNameQuery is not None:
                API_Name = str(ApiNameQuery.RECORD_NAME)
            ApiResponse = ApiResponseFactory.JsonResponse(GetObjlevelMessage(ObjectRecId, RECORDID))
elif Action == "Question":
    SEC_REC_ID = ""
    TableName = Param.TableName
    dictData = Param.dictData
    SEC_REC_ID = Param.SEC_REC_ID
    Result = GetQuestionlevelMessage(TableName, dictData, SEC_REC_ID)
# Added by VETRI for A043S001P01-8923 - Start
elif Action == "IFLOWWARNING":
    OBJRECID = Param.OBJRECID
    SegmentId = str(Product.GetGlobal("segment_rec_id"))
    versionId = str(Product.GetGlobal("segmentRevisionId"))
    ApiResponse = ApiResponseFactory.JsonResponse(GetIflowlevelWarningMessage(OBJRECID, SegmentId, versionId))
# Added by VETRI for A043S001P01-8923 - End
# A043S001P01-9610 - Start
elif Action == "QBINFO":
    OBJRECID = Param.OBJRECID
    SegmentId = str(Product.GetGlobal("segment_rec_id"))
    versionId = str(Product.GetGlobal("segmentRevisionId"))
    ApiResponse = ApiResponseFactory.JsonResponse(GetQBlevelinfoMessage(OBJRECID, SegmentId, versionId))
# A043S001P01-9610 - End

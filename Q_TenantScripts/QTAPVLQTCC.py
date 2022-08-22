# __script_name         : QTAPVLQTCC .PY
# __script_description  : THIS SCRIPT IS used to Self approval
# __primary_author__    : Venkatesh Korrapati
# __create_date         : 10.01.2021
# © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from SYDATABASE import SQL
Sql = SQL()
import datetime
try:
    apprRefVal = str(Param.FieldVal).strip()
except: 
    apprRefVal = ''
try:
    comp=str(Param.COMPETITOR)
except: 
    comp = ''
try:
    comm=str(Param.JUSTIFICATION_COMMENTS)
except: 
    comm = ''

try:
    apprule=str(Param.APPROVAL_RULE)
except:
    apprule=''

def App_upd(COMPETITOR,JUSTIFICATION_COMMENTS,APPROVAL_RULE):
    #CartId = TagParserProduct.ParseString('<*CTX( Quote.CartId )*>')
    #OwnerId = TagParserProduct.ParseString('<*CTX( Quote.OwnerId )*>')
    QuoteId = TagParserProduct.ParseString("<*CTX( Quote.CartCompositeNumber )*>")
    Query =Sql.GetFirst("SELECT ACTIVE,QTEREV_ID,CART_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='"+str(QuoteId)+"' and ACTIVE = 1 ")
    UserData =Sql.GetFirst("SELECT OWNER_NAME,OWNER_ID,ADDUSR_RECORD_ID FROM SAQTMT (NOLOCK) WHERE QUOTE_ID ='"+str(QuoteId)+"' ")
    submittedApprvr = str(UserData.OWNER_NAME)
    OwnerId = str(UserData.ADDUSR_RECORD_ID)
    CartId = str(Query.CART_ID)
    QTEREVID = Query.QTEREV_ID
    upsertQuoteTable = ""
    Appstatus=""
    Trace.Write("Action---------->"+str(APPROVAL_RULE))
    if APPROVAL_RULE=="Self Approval":
        Appstatus="Approved"
        Trace.Write("seffffAction---------->")
    elif comm != '':
        Appstatus="ApproveReject"
    else:
        Appstatus="Approval Requested"
    #APPROVAL_RULE = "Self Approval"
    #Appstatus="Approved"
    monQuoteTablQuery = SqlHelper.GetFirst("SELECT TOP 1 Id,COMPETITOR from QT__SAQAPP (NOLOCK) where cartId ='"+str(CartId)+"' and ownerId='"+str(OwnerId)+"' AND APPROVAL_RULE='"+str(APPROVAL_RULE)+"'  AND Revision_Number = '"+str(QTEREVID)+"' order by Id")
    if monQuoteTablQuery is not None :
        Trace.Write("insideAction---------->")
        if APPROVAL_RULE=="Self Approval":
            upsertQuoteTable = "UPDATE QT__SAQAPP SET STATUS = '"+str(Appstatus)+"', COMPETITOR='"+str(comp)+"' ,JUSTIFICATION_COMMENTS='"+str(comm)+"' WHERE ownerId = '"+str(OwnerId)+"' AND cartId = '"+str(CartId)+"' AND Id='"+str(monQuoteTablQuery.Id)+"' AND APPROVAL_RULE='"+str(APPROVAL_RULE)+"'  AND Revision_Number = '"+str(QTEREVID)+"'" 
            Trace.Write(str(upsertQuoteTable))
            Sql.RunQuery(upsertQuoteTable)
            updSaqtrvRevisionStatus = "UPDATE SAQTRV SET REVISION_STATUS ='APR-APPROVED',WORKFLOW_STATUS= 'APPROVALS',CPQTABLEENTRYDATEMODIFIED = '"+str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))+"'  WHERE QUOTE_ID = '"+str(QuoteId)+"' AND QTEREV_ID = '"+str(QTEREVID)+"'"
            try:
                SQLupdate = SqlHelper.GetFirst("sp_executesql @n=N'"+updSaqtrvRevisionStatus.replace("'","''")+"'")
            except Exception as e:
                Trace.Write("Query " + str(e))
            if Quote is not None and APPROVAL_RULE=="Self Approval":
                Quote.ChangeQuoteStatus('Approved')
                Quote.Save()
        elif Appstatus == "ApproveReject":
            upsertQuoteTable = "UPDATE QT__SAQAPP SET JUSTIFICATION_COMMENTS='"+str(comm)+"',CPQTABLEENTRYDATEMODIFIED = '"+str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))+"',SUBMIITED_APPROVER ='"+str(User.Name)+"' WHERE CURRENT_APPROVER  = '"+str(User.Name)+"' AND cartId = '"+str(CartId)+"'  AND Revision_Number = '"+str(QTEREVID)+"'" 
            Trace.Write(str(upsertQuoteTable))
            Sql.RunQuery(upsertQuoteTable)
        else:
            RequestorComment = str(monQuoteTablQuery.COMPETITOR)
            if str(COMPETITOR) == "":
                COMPETITOR = str(RequestorComment) 
            upsertQuoteTable = "UPDATE QT__SAQAPP SET COMPETITOR='"+str(COMPETITOR)+"'  WHERE ownerId = '"+str(OwnerId)+"' AND cartId = '"+str(CartId)+"'  AND Revision_Number = '"+str(QTEREVID)+"'" 
            Trace.Write(str(upsertQuoteTable))
            Sql.RunQuery(upsertQuoteTable)
            
    return True


try:
    Action = str(Param.Action)
except:
    Action = ""
Trace.Write("Action---------->"+str(Action))
if str(Action) == "saveApprRefVal":
    ApiResponse = ApiResponseFactory.JsonResponse(approval_ref(apprRefVal))
else:
    ApiResponse = ApiResponseFactory.JsonResponse(App_upd(comp,comm,apprule))
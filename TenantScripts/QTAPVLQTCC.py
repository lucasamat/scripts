# __script_name         : QTAPVLQTCC .PY
# __script_description  : THIS SCRIPT IS used to Self approval
# __primary_author__    : Venkatesh Korrapati
# __create_date         : 10.01.2021
# ==========================================================================================================================================
from SYDATABASE import SQL
Sql = SQL()
import datetime
import sys
import re
# INC08641181 - Start - A
import CQCPQC4CWB
# INC08641181 - End - A
try:
    apprRefVal = str(Param.FieldVal).strip()
except: 
    apprRefVal = ''
try:
    comp=Param.COMPETITOR
except: 
    comp = ''
try:
    comm=Param.JUSTIFICATION_COMMENTS
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
                # INC08641181 - Start - A
                Query2 =SqlHelper.GetFirst("SELECT REVISION_STATUS,QUOTE_RECORD_ID,QUOTE_REVISION_RECORD_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='"+str(QuoteId)+"' and ACTIVE = 1 ")
                REVISION_STATUS = Query2.REVISION_STATUS
                QUOTE_RECORD_ID = Query2.QUOTE_RECORD_ID
                QUOTE_REVISION_RECORD_ID = Query2.QUOTE_REVISION_RECORD_ID
                if REVISION_STATUS == 'APR-APPROVED':
                    CQCPQC4CWB.writeback_to_c4c("quote_header",QUOTE_RECORD_ID,QUOTE_REVISION_RECORD_ID)
                    CQCPQC4CWB.writeback_to_c4c("opportunity_header",QUOTE_RECORD_ID,QUOTE_REVISION_RECORD_ID)
                # INC08641181 - End - A
                Quote.Save()
        elif Appstatus == "ApproveReject":
            # INC08820269 - Start - A
            #A055S000P01-20960
            comment=comm.replace("'","''")
            comment = comment.encode('ascii', 'ignore').decode('ascii')
            comment = re.sub(r"[^a-zA-Z0-9 \n\.><&_-~,?]", '', comment)
            comment = comment.strip()
            #A055S000P01-20960
            # INC08820269 - End - A
            upsertQuoteTable = "UPDATE QT__SAQAPP SET JUSTIFICATION_COMMENTS='"+str(comm)+"',CPQTABLEENTRYDATEMODIFIED = '"+str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))+"',SUBMIITED_APPROVER ='"+str(User.Name)+"' WHERE CURRENT_APPROVER  = '"+str(User.Name)+"' AND cartId = '"+str(CartId)+"'  AND Revision_Number = '"+str(QTEREVID)+"'" 
            Trace.Write(str(upsertQuoteTable))
            Sql.RunQuery(upsertQuoteTable)
            #A055S000P01-20960
            GetTopId = Sql.GetFirst("SELECT TOP 1 id from current_cart_responsibility where cart_id = {} and owner_id = {}".format(CartId,OwnerId))
            if GetTopId:
                
                Sql.RunQuery("UPDATE current_cart_responsibility SET Comment = '{}' where cart_id = {} and owner_id = {} and id = '{}'".format(COMPETITOR,CartId,OwnerId,GetTopId.id))
            #A055S000P01-20960
        else:
            RequestorComment = str(monQuoteTablQuery.COMPETITOR)
            #A055S000P01-20960
            COMPETITOR = str(comp).replace("'","''")
            COMPETITOR = COMPETITOR.encode('ascii', 'ignore').decode('ascii')
            COMPETITOR = re.sub(r"[^a-zA-Z0-9 \n\.><&_-~,?]", '', COMPETITOR)
            COMPETITOR = COMPETITOR.strip()
            #A055S000P01-20960
            upsertQuoteTable = "UPDATE QT__SAQAPP SET COMPETITOR='"+str(COMPETITOR)+"'  WHERE ownerId = '"+str(OwnerId)+"' AND cartId = '"+str(CartId)+"'  AND Revision_Number = '"+str(QTEREVID)+"'" 
            Trace.Write(str(upsertQuoteTable))
            Sql.RunQuery(upsertQuoteTable)
            #A055S000P01-20960
            GetTopId = Sql.GetFirst("SELECT TOP 1 id from current_cart_responsibility where cart_id = {} and owner_id = {}".format(CartId,OwnerId))
            if GetTopId:
                
                Sql.RunQuery("UPDATE current_cart_responsibility SET Comment = '{}' where cart_id = {} and owner_id = {} and id = '{}'".format(COMPETITOR,CartId,OwnerId,GetTopId.id))
            #A055S000P01-20960
            
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
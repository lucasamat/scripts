from SYDATABASE import SQL
import datetime
Sql = SQL()
# visitor = TagParserProduct.ParseString("<*CTX( Visitor.Name )*>")
# if visitor != "Admin CPQ":
Quote_status = Quote.OrderStatus.Name
if Quote is not None:
    Ownrid1 = TagParserProduct.ParseString("<*CTX( Quote.OwnerId )*>")
    CrtId1 = TagParserProduct.ParseString("<*CTX( Quote.CartId )*>")
    QuoteId = TagParserProduct.ParseString("<*CTX( Quote.CartCompositeNumber )*>")
    RevisionId = TagParserProduct.ParseString("<*CTX( Quote.Revision.RevisionNumber )*>")
else:
    Ownrid1 = ""
    CrtId1 = ""
    QuoteId = ""
    RevisionId = ""

def InsertApprovals(QTRevId):     
    Sql.RunQuery("DELETE from QT__SAQAPP WHERE cartId ='"+str(CrtId)+"' and ownerId='"+str(Ownrid)+"'")
     
    Query=""
    curApproverName=""
       
    submittedApprvr1=TagParserProduct.ParseString('<*CTX( Quote.Owner.Name )*>')
    status ="Approval Submission Pending"
    Query =Sql.GetList("""SELECT TOP 10000 * FROM APPRUL (NOLOCK) ORDER BY APPROVAL_SEQUENCE""")
    try:
        region = Quote.GetCustomField('Region').Content
    except:
        region =""
   
    for appRule in Query:
        curApproverName = ""
        approverName = ""
        condition = appRule.APPROVAL_CONDITION
        apprName = appRule.APPROVAL_NAME
        apprDesc = appRule.APPROVAL_DESCRIPTION
        apprOrd = appRule.APPROVAL_SEQUENCE
        aapprRuleViolated = TagParserProduct.ParseString("" + condition + "")
        Trace.Write("APPROVAL NAME---------"+str(apprName))
       
        
        Trace.Write("aapprRuleViolated Value--------"+str(aapprRuleViolated))
        constat = TagParserQuote.ParseString("[IF]([NEQ](<*CTX( Quote.CustomField(CONFIG_STATUS) )*>,TRUE)){1}{0}[ENDIF]")
        Trace.Write("Config Status Value--------"+str(constat))
        if str(aapprRuleViolated) == "1":
            Trace.Write("====================DDDD")
            if apprName !="":
                splitApprName = apprName.split(" : ")
                finalAppName = splitApprName[0]
                Level = 0
                approverQuery = Sql.GetList("select top 1000 EMAIL,BUSINESS_GROUP,APPROVAL_CHAIN_NAME,MEMBER_NAME,APAPVR.APPROVAL_LEVEL,MEMBER_ID from SAQDLT(NOLOCK) JOIN APAPVR(NOLOCK) on trim(APAPVR.BUSINESS_GROUP) = trim(SAQDLT.C4C_PARTNERFUNCTION_ID)  WHERE QUOTE_ID ='"+str(QuoteId)+"' AND QTEREV_ID = '"+str(QTRevId)+"' AND APPROVAL_CHAIN_NAME like '%"+str(finalAppName)+"%' AND [PRIMARY] = 1  order by APAPVR.APPROVAL_LEVEL")
                Trace.Write(approverQuery)
                if approverQuery:
                    for getAppData in approverQuery:
                        Level = Level + 1
                        apprMail = getAppData.EMAIL
                        apprRulName = getAppData.APPROVAL_CHAIN_NAME
                        curApproverName = getAppData.MEMBER_NAME
                        curUserName = getAppData.MEMBER_ID
                        curBG = getAppData.BUSINESS_GROUP
                        upsertQuoteTable = "INSERT INTO QT__SAQAPP (APPROVAL_RULE,DESCRIPTION,LEVEL,SUBMIITED_APPROVER,CURRENT_APPROVER,CURRENT_APPROVER_EMAIL,STATUS,REGION,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEMODIFIED,ownerId,cartId,Current_User_Name, Business_Group, Revision_Number, CPQTABLEENTRYDATEADDED) VALUES( '"+str(apprRulName)+"', '"+str(apprDesc)+"','"+str(Level)+"' , '"+str(submittedApprvr)+"', '"+str(curApproverName)+"' , '"+str(apprMail)+"' , '"+str(status)+"' , '"+str(region)+"','"+str(User.Name)+"' , '"+str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))+"' , '"+Ownrid+"' , '"+CrtId+"','"+str(curUserName)+"','"+str(curBG)+"','"+str(QTRevId)+"','"+str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))+"')"
                        Trace.Write(upsertQuoteTable)
                        try:SQLupdate = SqlHelper.GetFirst("sp_executesql @n=N'"+upsertQuoteTable.replace("'","''")+"'")
                        except Exception as e:
                            Trace.Write("Query " + str(e))
        else:
            Trace.Write("====================DDDD")
            
    QuoteCount = Sql.GetFirst("SELECT count(*) as CNT from QT__SAQAPP WHERE cartId ='"+str(CrtId)+"' and ownerId='"+str(Ownrid)+"'  and Revision_Number = '"+str(QTRevId)+"'")
    finalCount = QuoteCount.CNT
    approverQuery = Sql.GetFirst("select * from SAQTRV (NOLOCK) WHERE QUOTE_ID ='"+str(QuoteId)+"' and QTEREV_ID = '"+str(QTEREVID)+"'")
    appcount=0
    if str(approverQuery.QT_PAYMENTTERM_DAYS) is not None and str(approverQuery.QT_PAYMENTTERM_DAYS) != "":
        if int(approverQuery.QT_PAYMENTTERM_DAYS)<=int(approverQuery.PAYMENTTERM_DAYS):
            appcount=1
        else:
            appcount=0
    if  int(finalCount) == 0 and appcount == 1:
        Level = 1
        apprRulName = "Self Approval"
        apprDesc = "Quote Owner must directly approve. Once approved, the quote will be locked for editing."
        status = "Approval Submission Pending"
        curBG = "Quote Owner"
        upsertQuoteTable = "INSERT INTO QT__SAQAPP (APPROVAL_RULE,DESCRIPTION,LEVEL,SUBMIITED_APPROVER,CURRENT_APPROVER,CURRENT_APPROVER_EMAIL,STATUS,REGION,CPQTABLEENTRYADDEDBY,CPQTABLEENTRYDATEMODIFIED,ownerId,cartId,Current_User_Name,Business_Group,Revision_Number,CPQTABLEENTRYDATEADDED) VALUES( '"+str(apprRulName)+"', '"+str(apprDesc)+"','"+str(Level)+"' , '"+str(submittedApprvr)+"', '"+str(submittedApprvr)+"' , '"+str(User.Email)+"' , '"+str(status)+"' , '"+str(region)+"','"+str(User.Name)+"' , '"+str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))+"' , '"+Ownrid+"' , '"+CrtId+"','"+str(submittedApprvr)+"','"+str(curBG)+"','"+str(QTRevId)+"','"+str(datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S %p"))+"')"
        Trace.Write(upsertQuoteTable)
        try:SQLupdate = SqlHelper.GetFirst("sp_executesql @n=N'"+upsertQuoteTable.replace("'","''")+"'")
        except Exception as e:
            Trace.Write("Query " + str(e))
    else:
        Trace.Write("====================DDDD")
Query =Sql.GetFirst("SELECT REVISION_STATUS,ACTIVE,QTEREV_ID, ADDUSR_RECORD_ID,CART_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='"+str(QuoteId)+"' and ACTIVE = 1 ")

try:
    Revision_Status = str(Query.REVISION_STATUS)
    CrtId = str(Query.CART_ID)
    QTEREVID = Query.QTEREV_ID
except:
     Revision_Status = ''
     CrtId = ''
     QTEREVID = ''

UserData =Sql.GetFirst("SELECT OWNER_NAME,OWNER_ID,ADDUSR_RECORD_ID FROM SAQTMT (NOLOCK) WHERE QUOTE_ID ='"+str(QuoteId)+"' ")
try:
	submittedApprvr = str(UserData.OWNER_NAME)
	Ownrid = str(UserData.ADDUSR_RECORD_ID)
except:
    submittedApprvr = ''
    Ownrid = ''
Trace.Write('RevisionSTATUS0000' + str(Revision_Status))
QueryCnt = SqlHelper.GetFirst("SELECT count(*) as CNT from QT__SAQAPP where cartId ='"+str(CrtId)+"' and ownerId='"+str(Ownrid)+"' AND STATUS IN ('Approval Requested','Approved','Rejected','Recalled') AND Revision_Number = '"+str(QTEREVID)+"'")
if  str(Revision_Status) != '' and str(Quote_status) == "Preparing" and (str(Revision_Status) != "APR-APPROVED" and str(Revision_Status) != "APR-REJECTED" and str(Revision_Status) != "APR-RECALLED"):
    Trace.Write("RevisionId0000INSIDE")
    if QueryCnt.CNT == 0 and str(CrtId) !='' : 
        InsertApprovals(QTEREVID)
# =========================================================================================================================================
# __script_name : QTAPRVLHST.PY
# __script_description : THIS SCRIPT IS USED TO SHOW APPROVAL HISTORY TABLE
# __primary_author__ : VENKATESH KORRAPATI
# __create_date :
# ==========================================================================================================================================
from SYDATABASE import SQL
Sql = SQL()

def SeqNonAgiApprvlHistry():
	NoRules = ""
	Tbody = ''
	Histry = ""
	monQuoteTablQuery = ""
	table = '''<div><table class='table configuration_table fiori3-table items-table car_lt_itm monapprhistry'><thead><tr class='conta_tbl_hd'>'''
	thead = ['Quote Revision','Action Date','Approval Chain Name','Approval Rule','Status','Approver Business Group','Approver Name','Performer','Requestor Comments','Approver Comments']
	for i in thead:
		table = table+"<th style='text-align: left !important;'><div class='conta_line_head'><abbr title='"+str(i)+"'>"+str(i)+"</abbr></div></div></th>"
	table = table+'''</tr></thead><tbody>'''

	composite = Quote.CompositeNumber
	QuoteId = TagParserProduct.ParseString("<*CTX( Quote.CartCompositeNumber )*>")
	#CartId = TagParserProduct.ParseString('<*CTX( Quote.CartId )*>')
	#OwnerId = TagParserProduct.ParseString('<*CTX( Quote.OwnerId )*>')
	Query =Sql.GetFirst("SELECT ACTIVE,QTEREV_ID,ADDUSR_RECORD_ID,CART_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='"+str(QuoteId)+"' and ACTIVE = 1 ")
	UserData =Sql.GetFirst("SELECT OWNER_RECORD_ID,OWNER_NAME,OWNER_ID,ADDUSR_RECORD_ID FROM SAQTMT (NOLOCK) WHERE QUOTE_ID ='"+str(QuoteId)+"' ")
	#submittedApprvr = UserData.OWNER_NAME
	OwnerId = UserData.ADDUSR_RECORD_ID
	CartId = Query.CART_ID
	QTEREVID = Query.QTEREV_ID
	monQuoteTablQuery = SqlHelper.GetList("select top 10000 APAPVR.BUSINESS_GROUP,QT__SAQAPP.APPROVAL_RULE,QT__SAQAPP.CURRENT_APPROVER,QT__SAQAPP.SUBMIITED_APPROVER,QT__SAQAPP.STATUS,DESCRIPTION,QT__SAQAPP.CPQTABLEENTRYDATEMODIFIED,COMPETITOR,JUSTIFICATION_COMMENTS from QT__SAQAPP(NOLOCK) join APAPVR(NOLOCK) on QT__SAQAPP.APPROVAL_RULE=APAPVR.APPROVAL_CHAIN_NAME and QT__SAQAPP.Business_Group=APAPVR.BUSINESS_GROUP where cartId ='"+str(CartId)+"' and ownerId='"+str(OwnerId)+"' AND Revision_Number = '"+str(QTEREVID)+"'  order by QT__SAQAPP.LEVEL,QT__SAQAPP.CURRENT_APPROVER")
	Trace.Write("select top 10000 APAPVR.BUSINESS_GROUP,QT__SAQAPP.APPROVAL_RULE,QT__SAQAPP.CURRENT_APPROVER,QT__SAQAPP.SUBMIITED_APPROVER,QT__SAQAPP.STATUS,DESCRIPTION,QT__SAQAPP.CPQTABLEENTRYDATEMODIFIED,COMPETITOR,JUSTIFICATION_COMMENTS from QT__SAQAPP(NOLOCK) join APAPVR(NOLOCK) on QT__SAQAPP.APPROVAL_RULE=APAPVR.APPROVAL_CHAIN_NAME and QT__SAQAPP.Business_Group=APAPVR.BUSINESS_GROUP where cartId ='"+str(CartId)+"' and ownerId='"+str(OwnerId)+"' AND Revision_Number = '"+str(QTEREVID)+"'  order by QT__SAQAPP.LEVEL,QT__SAQAPP.CURRENT_APPROVER")
	if len(monQuoteTablQuery) > 0:
		for row in monQuoteTablQuery:
			Comment = ""
			apprName=""
			appr=""
			delAppr=""
			apprId=""
			atttype = ""
			commentsQuery=""
			if str(row.CURRENT_APPROVER)!="":
				# If delegate approver does not exists (Other Approval chains and not deal health)
				apprName = str(row.CURRENT_APPROVER).split(" ")
				Trace.Write("Approver Name----->"+str(apprName))
				apprId = SqlHelper.GetFirst("SELECT ID from users(NOLOCK) where first_name='"+str(apprName[0])+"' and last_name='"+str(apprName[1])+"'")
				if apprId is not None:
					Trace.Write("pass")
					#commentsQuery = SqlHelper.GetFirst("SELECT current_cart_responsibility.Comment from current_cart_responsibility(NOLOCK) INNER JOIN QT__SAQAPP(NOLOCK) AS qt ON qt.cartId = current_cart_responsibility.cart_id AND qt.ownerId = current_cart_responsibility.owner_id where current_cart_responsibility.IsWaitingForApprove=0 and current_cart_responsibility.owner_id='"+str(OwnerId)+"' and current_cart_responsibility.cart_id='"+str(CartId)+"' and current_cart_responsibility.responsible_approver_id ='"+str(apprId.ID)+"' and qt.APPROVAL_RULE='"+str(row.APPROVAL_RULE)+"'")
					#if commentsQuery is not None:
					#Comment = commentsQuery.Comment
			Tbody = Tbody +"<tr><td title='"+str(Quote.CompositeNumber)+"-"+str(QTEREVID)+"'>"+str(Quote.CompositeNumber)+"-"+str(QTEREVID)+"</td><td title='"+str(row.CPQTABLEENTRYDATEMODIFIED)+"'>"+str(row.CPQTABLEENTRYDATEMODIFIED)+"</td><td title='"+str(row.APPROVAL_RULE)+"'>"+str(row.APPROVAL_RULE)+"</td><td title='"+str(row.DESCRIPTION)+"'>"+str(row.DESCRIPTION)+"</td><td title='"+str(row.STATUS)+"'>"+str(row.STATUS)+"</td><td title='"+str(row.BUSINESS_GROUP)+"'>"+str(row.BUSINESS_GROUP)+"</td><td title='"+str(row.CURRENT_APPROVER)+"'>"+str(row.CURRENT_APPROVER)+"</td><td title='"+str(row.SUBMIITED_APPROVER)+"'>"+str(row.SUBMIITED_APPROVER)+"</td><td title='"+str(row.COMPETITOR)+"'>"+str(row.COMPETITOR)+"</td><td style='text-align: left !important;' ><abbr title='"+str(row.JUSTIFICATION_COMMENTS).replace("'","&apos;")+"'>"+str(row.JUSTIFICATION_COMMENTS)+"</abbr></td></tr>"
			# performer = str(row.CURRENT_APPROVER)
	else:
		Tbody = Tbody +""
		NoRules = "No Approval Rules have been triggered."
	Tbody =Tbody+'</tbody></table></div>'
	Histry =  table + Tbody
	#Trace.Write("Histry"+str(Tbody));
	Trace.Write(Histry);
	#Log.Info("Histry"+str(Tbody))
	QuoteId = TagParserProduct.ParseString("<*CTX( Quote.CartCompositeNumber )*>")
	Query =Sql.GetFirst("SELECT ACTIVE,QTEREV_ID FROM SAQTRV (NOLOCK) WHERE QUOTE_ID ='"+str(QuoteId)+"' and ACTIVE = 1 ")
	QTEREVID = Query.QTEREV_ID
	visitor = TagParserProduct.ParseString("<*CTX( Visitor.Name )*>")
	owner = TagParserProduct.ParseString("<*CTX( Quote.Owner.Name )*>")
	Trace.Write("Approver Name----->"+str(visitor))
	Trace.Write("Approver Name----->"+str(owner))
	GetOwnerId =Sql.GetFirst("SELECT EMPLOYEE_ID FROM SAEMPL (NOLOCK) WHERE EMPLOYEE_RECORD_ID ='"+str(UserData.OWNER_RECORD_ID)+"' ")
	if(visitor.upper() == owner.upper()):
		selfapproveval=1
	else:
		if GetOwnerId is not None:
			if str(GetOwnerId.EMPLOYEE_ID) == str(User.UserName):
				selfapproveval=1
			else:
				selfapproveval=0
		else:
			selfapproveval=0
	RevStatus = SqlHelper.GetFirst("SELECT REVISION_STATUS from SAQTRV(NOLOCK) where QUOTE_ID = '"+str(QuoteId)+"' AND QTEREV_ID = '"+str(QTEREVID)+"'")
	SubmitBtnStatus = SqlHelper.GetFirst("SELECT count(*) as CNT from QT__SAQAPP(NOLOCK) where cartId ='"+str(CartId)+"' and ownerId='"+str(OwnerId)+"' and Revision_Number = '"+str(QTEREVID)+"' and STATUS='Approval Requested' and Current_User_Name='"+str(User.UserName)+"' ")
	CurrentStatus = SqlHelper.GetFirst("SELECT count(*) as CNT from QT__SAQAPP(NOLOCK) where cartId ='"+str(CartId)+"' and ownerId='"+str(OwnerId)+"' and Revision_Number = '"+str(QTEREVID)+"' and STATUS='Approval Requested' and SUBMIITED_APPROVER='"+str(User.Name)+"' ")
	FinalStatus = SqlHelper.GetFirst("SELECT count(*) as CNT from QT__SAQAPP(NOLOCK) where cartId ='"+str(CartId)+"' and ownerId='"+str(OwnerId)+"' and Revision_Number = '"+str(QTEREVID)+"' and STATUS='Approval Submission Pending'")
	StatusApproved = SqlHelper.GetFirst("SELECT count(*) as CNT from QT__SAQAPP(NOLOCK) where cartId ='"+str(CartId)+"' and ownerId='"+str(OwnerId)+"' and STATUS='Approved' and Revision_Number = '"+str(QTEREVID)+"' and Current_User_Name='"+str(User.UserName)+"' ")
	OneApproved = SqlHelper.GetFirst("SELECT count(*) as CNT from QT__SAQAPP(NOLOCK) where cartId ='"+str(CartId)+"' and ownerId='"+str(OwnerId)+"' and STATUS='Approved' and Revision_Number = '"+str(QTEREVID)+"'  ")
	newStatus = str(RevStatus.REVISION_STATUS)
	SubmitStatus = SubmitBtnStatus.CNT
	CurrentStatus = CurrentStatus.CNT
	finalStatus = FinalStatus.CNT
	statusApproved = StatusApproved.CNT
	oneApproved = OneApproved.CNT
	return Histry,newStatus,SubmitStatus,CurrentStatus,finalStatus,statusApproved,oneApproved,NoRules,selfapproveval
ApiResponse = ApiResponseFactory.JsonResponse(SeqNonAgiApprvlHistry())
Quote.Calculate()
if Quote is not None:
	Quote.Save()
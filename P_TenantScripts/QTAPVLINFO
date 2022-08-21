# =========================================================================================================================================
# __script_name : QTAPVLINFO.PY
# __script_description : THIS SCRIPT IS USED FOR SIMPLE MATERIAL POPUP
# __primary_author__ :
# __create_date :
# © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
from datetime import datetime
from SYDATABASE import SQL
Sql = SQL()
def Approvals_upd(CartId,OwnerId):
	Log.Info("QTAPVLINFO Approvals_upd hitting")
	lists =[]
	cartcomp = SqlHelper.GetFirst("SELECT CartCompositeNumber  from cart2 (NOLOCK) where CartId = '{CartId}' and OwnerId = '{OwnerId}' ".format(CartId=CartId,OwnerId=OwnerId))
	Quote = QuoteHelper.Edit(str(cartcomp.CartCompositeNumber))
	RevisnNum = str(Quote.CompositeNumber) +"-"+str(Quote.RevisionNumber)
	QuoteOwnr = TagParserQuote.ParseString('<*CTX( Quote.Owner.Name)*>')
	AccountName = Quote.GetCustomField('AccountName').Content
	QuoteStatus = Quote.GetCustomField('Revision_Status').Content
	QuoteTtl = Quote.GetCustomField('TOTAL_COST').Content
	QTNUM=TagParserProduct.ParseString('<*CTX( Quote.QuoteNumber )*>')
	QTREV=TagParserProduct.ParseString('<*CTX( Quote.Revision.RevisionNumber )*>')
	#QUOTE PROPERTIES	
	OPPORTUNITYID=TagParserProduct.ParseString('<*CTX( Quote.CustomField(OpportunityId) )*>')
	REGION=TagParserProduct.ParseString("<* TABLE ( SELECT REGION from SAQTMT where QUOTE_ID ='<*CTX( Quote.CartCompositeNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>') *>")
	ACCOUNTID=TagParserProduct.ParseString("<* TABLE ( SELECT ACCOUNT_ID from SAQTMT where QUOTE_ID ='<*CTX( Quote.CartCompositeNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>') *>")
	ACCOUNTNAME=TagParserProduct.ParseString("<* TABLE ( SELECT ACCOUNT_NAME from SAQTMT where QUOTE_ID ='<*CTX( Quote.CartCompositeNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>') *>")
	QUOTEREVISIONDESCRIPTION=TagParserProduct.ParseString("<* TABLE ( SELECT REVISION_DESCRIPTION from SAQTRV where QUOTE_ID ='<*CTX( Quote.CartCompositeNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>') *>")
	CONTRACTSTARTDATE=TagParserProduct.ParseString("<* TABLE ( SELECT CONVERT(VARCHAR(10),CONTRACT_VALID_FROM,101) from SAQRIS where Quote_ID='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>")
	CONTRACTENDDATE=TagParserProduct.ParseString("<* TABLE ( SELECT CONVERT(VARCHAR(10),CONTRACT_VALID_TO,101) from SAQRIS where Quote_ID='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>")
	QUOTEREVISION=TagParserProduct.ParseString('<*CTX( Quote.CartCompositeNumber )*>-<*CTX( Quote.Revision.RevisionNumber )*>')
	QUOTEOWNER=TagParserProduct.ParseString('<*CTX( Quote.Owner.Name )*>')
	#QUOTE SUMMARY
	TOTALEXCLUDINGTAX=TagParserProduct.ParseString("<* TABLE ( SELECT Convert(decimal(18,2),NET_VALUE_INGL_CURR) from SAQTRV where QUOTE_ID ='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>  <* TABLE ( SELECT DOC_CURRENCY from SAQTRV where QUOTE_ID ='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>")
	TOTALTAX=TagParserProduct.ParseString(" <* TABLE ( SELECT DOC_CURRENCY from SAQTRV where QUOTE_ID ='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>")
	TOTALESTNETVAL=TagParserProduct.ParseString("<* TABLE ( SELECT DOC_CURRENCY from SAQTRV where QUOTE_ID ='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>")
	TOTALNETVAL=TagParserProduct.ParseString("<* TABLE ( SELECT DOC_CURRENCY from SAQTRV where QUOTE_ID ='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>")
	TOTALAMT=TagParserProduct.ParseString("<* TABLE ( SELECT Convert(decimal(18,2),TOTAL_AMOUNT_INGL_CURR) from SAQTRV where QUOTE_ID ='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>  <* TABLE ( SELECT DOC_CURRENCY from SAQTRV where QUOTE_ID ='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>")
	TOTALMARGIN=TagParserProduct.ParseString("<* TABLE ( SELECT Convert (decimal(18,2),CNTMRG_INGL_CURR) from SAQTRV where QUOTE_ID ='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>  <* TABLE ( SELECT DOC_CURRENCY from SAQTRV where QUOTE_ID ='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>")
	TOTALMARGINPCT=TagParserProduct.ParseString("<* TABLE ( SELECT Convert(decimal(18,2),TOTAL_MARGIN_PERCENT) from SAQTRV where QUOTE_ID ='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>  <* TABLE ( SELECT DOC_CURRENCY from SAQTRV where QUOTE_ID ='<*CTX( Quote.QuoteNumber )*>' and QTEREV_ID='<*CTX( Quote.Revision.RevisionNumber )*>' ) *>")
	Commts=TagParserQuote.ParseString("<* TABLE ( SELECT TOP 1 COMPETITOR from QT__SAQAPP where cartId=<*CTX( Quote.CartId )*> and ownerId=<*CTX( Quote.OwnerId )*> order by LEVEL) *>")
	AddcmtFrmReq=str(Commts)
	Tb = ""
	Tb = "<div class='approval_top_col_sec'><span class='approval_php_lbl' title='Quote Number'>Quote Number</span><span id='RevNum' class='approval_php_val' title="+str(RevisnNum)+">"+str(RevisnNum)+"</span></div><div class='approval_top_col_sec'><span class='approval_php_lbl' title='Quote Owner'>Quote Owner</span><span class='approval_php_val' title="+str(QuoteOwnr)+">"+str(QuoteOwnr)+"</span></div><div class='approval_top_col_sec'><span class='approval_php_lbl' title='Account Name'>Account Name</span><span class='approval_php_val' title="+AccountName+">"+AccountName+"</span></div><div class='approval_top_col_sec'><span class='approval_php_lbl' title='Revision Status'>Revision Status</span><span class='approval_php_val' title="+str(QuoteStatus)+">"+str(QuoteStatus)+"</span></div><div class='approval_top_col_sec'><span class='approval_php_lbl' title='Quote Total'>Quote Total</span><span class='approval_php_val' title="+str(QuoteTtl)+">"+str(QuoteTtl)+"</span></div></div>"
	div = Tb+"</div>"
	lists.append(div)	
	Tb = ""
	Tb = "<div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='OPPORTUNITY ID'>OPPORTUNITY ID</div><div class='contTbl_value'>"+str(OPPORTUNITYID)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Region'>Region</div><div class='contTbl_value'>"+str(REGION)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Account ID'>Account ID</div><div class='contTbl_value'>"+str(ACCOUNTID)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Account Name'>Account Name</div><div class='contTbl_value'>"+str(ACCOUNTNAME)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Quote Revision'>Quote Revision</div><div class='contTbl_value'>"+str(QUOTEREVISION)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Quote Revision Description'>Quote Revision Description</div><div class='contTbl_value'>"+str(QUOTEREVISIONDESCRIPTION)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Contract Start Date'>Contract Start Date</div><div class='contTbl_value'>"+str(CONTRACTSTARTDATE)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Contract End Date'>Contract End Date</div><div class='contTbl_value'>"+str(CONTRACTENDDATE)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Quote Owner'>Quote Owner</div><div class='contTbl_value'>"+str(QUOTEOWNER)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='ADDITIONAL COMMENTS FROM REQUESTOR'>ADDITIONAL COMMENTS FROM REQUESTOR</div><div class='contTbl_value'>"+str(AddcmtFrmReq)+"</div></div>"
	div="<div class='appContainer' style='display:block'><div class='tableMainHeader' data-toggle='collapse' data-target='.quoteproperties' onclick='colPopupIcon(this)'><span>QUOTE PROPERTIES</span><span class='more-less glyphicon pointer glyphicon-chevron-down' style='float: right;'></span></div><div class='contTblWrap quoteInfoTbl collapse in quoteproperties'>"+Tb+"</div>"
	Tb = ""
	Tb = "<div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Total Excluding Tax'>Total Excluding Tax/VAT/GST</div><div class='contTbl_value'>"+str(TOTALEXCLUDINGTAX)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Total Tax'>Total Tax/VAT/GST</div><div class='contTbl_value'>"+str(TOTALTAX)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Total Est Net Val'>Total Est Net Val</div><div class='contTbl_value'>"+str(TOTALESTNETVAL)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Total Net Val'>Total Net Val</div><div class='contTbl_value'>"+str(TOTALNETVAL)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Total Amt'>Total Amt</div><div class='contTbl_value'>"+str(TOTALAMT)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Total Margin'>Total Margin</div><div class='contTbl_value'>"+str(TOTALMARGIN)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Total Margin Pct'>Total Margin Pct</div><div class='contTbl_value'>"+str(TOTALMARGINPCT)+"</div></div>"
	div+= "<div class='appContainer' style='display:block'><div class='tableMainHeader' data-toggle='collapse' data-target='.quotesummary' onclick='colPopupIcon(this)'><span>QUOTE SUMMARY</span><span class='more-less glyphicon pointer glyphicon-chevron-down' style='float: right;'></span></div><div class='contTblWrap quoteInfoTbl collapse in quotesummary'>"+Tb+"</div>"
	get = SqlHelper.GetList("SELECT SAQRIS.SERVICE_ID,SAQRIS.SERVICE_DESCRIPTION,SAQTSV.SERVICE_TYPE,SAQTRV.DOCTYP_ID,SAQRIS.CONTRACT_VALID_FROM,SAQRIS.CONTRACT_VALID_TO from SAQRIS (NOLOCK) join SAQTRV (NOLOCK) on SAQTRV.QUOTE_ID=SAQRIS.QUOTE_ID and SAQTRV.QTEREV_ID =SAQRIS.QTEREV_ID join SAQTSV (NOLOCK) on SAQTSV.QUOTE_ID=SAQRIS.QUOTE_ID and SAQTSV.QTEREV_ID =SAQRIS.QTEREV_ID and SAQTSV.SERVICE_ID=SAQRIS.SERVICE_ID  where SAQRIS.QUOTE_ID='{x}' and SAQRIS.QTEREV_ID='{y}'".format(x=QTNUM,y=QTREV))
	Tb=""
	for row in get:
		PRODUCTOFFERINGID=str(row.SERVICE_ID)
		PRODUCTOFFERINGDESCRIPTION=str(row.SERVICE_DESCRIPTION)
		POAPRODUCTTYPE=str(row.SERVICE_TYPE)
		DOCUMENTTYPE=str(row.DOCTYP_ID)		
		Tb = "<div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Product Offering ID'>Offering ID</div><div class='contTbl_value'>"+str(PRODUCTOFFERINGID)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Product Offering Description'>Product Offering Description</div><div class='contTbl_value'>"+str(PRODUCTOFFERINGDESCRIPTION)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='POA Product Type'>POA Product Type</div><div class='contTbl_value'>"+str(POAPRODUCTTYPE)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Document Type'>Document Type</div><div class='contTbl_value'>"+str(DOCUMENTTYPE)+"</div></div></div>"
	div+= "<div class='appContainer' style='display:block'><div class='tableMainHeader' data-toggle='collapse' data-target='.productofferings' onclick='colPopupIcon(this)'><span>PRODUCTS OFFERINGS</span><span class='more-less glyphicon pointer glyphicon-chevron-down' style='float: right;'></span></div><div class='contTblWrap quoteInfoTbl collapse in productofferings'>"+Tb+"</div></div>"
	QuoteTabquery =SqlHelper.GetList("SELECT SAQAPP.STATUS,SAQAPP.APPROVAL_RULE,SAQAPP.DESCRIPTION,SAQAPP.CPQTABLEENTRYDATEMODIFIED,SAQAPP.CURRENT_APPROVER FROM current_cart_responsibility (NOLOCK) AS CCT INNER JOIN QT__SAQAPP (NOLOCK) AS SAQAPP ON CCT.cart_id = SAQAPP.cartId and CCT.owner_id = SAQAPP.ownerid and SAQAPP.CURRENT_APPROVER='<* ResponsibleApprovers *>' and CCT.responsible_approver_id =SAQAPP.ownerid where CCT.cart_id='{CartId}' and CCT.owner_id='{OwnerId}' and SAQAPP.STATUS='Approval Requested'".format(CartId=CartId,OwnerId=OwnerId))
	Tb = ""
	for row in QuoteTabquery:
		Tb= Tb +"<div class='contTbl'style='width: 100%;'><div><div class='contTbl_label' title='Approval Rule'>Approval Rule</div><div class='contTbl_value'>"+str(row.APPROVAL_RULE)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Approval Rule Description'>Approval Rule Description</div><div class='contTbl_value'>"+str(row.DESCRIPTION)+"</div></div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Current Approver'>Current Approver</div><div class='contTbl_value'>"+str(row.CURRENT_APPROVER)+"</div><div class='contTbl' style='width: 100%;'><div class='contTbl_label' title='Status'>Status</div><div class='contTbl_value'>"+str(row.STATUS)+"</div></div></div>"
	div+= "<div class='appContainer' style='display:block'><div class='tableMainHeader' data-toggle='collapse' data-target='.itemsreqapprl' onclick='colPopupIcon(this)'><span>ITEMS REQURING APPROVAL</span><span class='more-less glyphicon pointer glyphicon-chevron-down' style='float: right;'></span></div><div class='contTblWrap quoteInfoTbl collapse in itemsreqapprl'>"+Tb+"</div></div>"
	div+= "</div>"
	lists.append(div)	
	Log.Info("QTAPVLINFO div tag hitting")
	return lists

def commentupd(CartId,OwnerId,Quote_txt):
	Log.Info("QTAPVLINFO Approvals_cmnt commentupd hitting")
	Log.info("Cmt"+str(Quote_txt))
	CartId=TagParserProduct.ParseString('<*CTX( Quote.CartId )*>')
	OwnerId=TagParserProduct.ParseString('<*CTX( Quote.OwnerId )*>')
	commesntQry = SqlHelper.GetFirst("select top 1 a.*, a.comment as app_cm,b.id as app_id from current_cart_Responsibility (NOLOCK) a join QT__SAQAPP (NOLOCK) b on b.Description = a.violation_reason  and b.ownerid = a.owner_id and  b.cartid = a.cart_id where Cart_Id ='"+CartId+"' and Owner_Id ='"+OwnerId+"' and (a.status in (1,-1) or (a.status=9 and date_resolved != ''))  order by submit_counter desc")
	count  = commesntQry.comment if commesntQry else 'empty'
	if commesntQry is not None:
		commesntQryss = SqlHelper.GetFirst("sp_executesql @Statement=N'update a set a.comment = ''"+Quote_txt+"'' from current_cart_Responsibility (NOLOCK) a join QT__SAQAPH (NOLOCK) b on b.Description = a.violation_reason  and b.ownerid = a.owner_id and  b.cartid = a.cart_id join (select top 1 a.id from current_cart_Responsibility (NOLOCK) a join QT__SAQAPH (NOLOCK) b on b.Description = a.violation_reason  and b.ownerid = a.owner_id and  b.cartid = a.cart_id where Cart_Id =''"+CartId+"'' and Owner_Id =''"+OwnerId+"'' and (a.status in (1,-1) or a.status=9 and date_resolved != '''')  order by submit_counter desc) f on f.id = a.id where Cart_Id =''"+CartId+"'' and Owner_Id =''"+OwnerId+"'' and (a.status in (1,-1) or (a.status=9 and date_resolved != '''')) '")
		Trace.Write(str(Quote_txt)+'-LOg----->'+str(commesntQry.date_resolved))
		Log.Info("QTAPVLINFO Approvals_cmnt cmnt saved hitting")
	else:
		Log.Info("QTAPVLINFO Approvals_cmnt cmnt notsaved hitting")

try:
	CartId = Param.CartId
	OwnerId = Param.OwnerId
except:
	CartId = ''
	OwnerId = ''
ACTION = Param.ACTION
if( ACTION == "Comment"):
	ApiResponse = ApiResponseFactory.JsonResponse(Approvals_upd(CartId,OwnerId))
	if hasattr(Param, "QuoteCmt"):
		Quote_txt = Param.QuoteCmt
		ApiResponse = ApiResponseFactory.JsonResponse(commentupd(CartId,OwnerId ,Quote_txt))
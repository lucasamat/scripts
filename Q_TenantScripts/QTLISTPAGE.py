# ==========================================================================================================================================
#   __script_name : QTLISTPAGE.PY
#   __script_description : THIS SCRIPT IS USED TO LOAD MAIN LISTS FOR A GIVEN QUOTES.
#   __primary_author__ : VENKATESH KORRAPATI
#   __create_date :
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================
import System
import math
from SYDATABASE import SQL
import datetime


today = datetime.datetime.now()
Modified_date = today.strftime("%m/%d/%Y %H:%M:%S %p")
Sql = SQL()
userid=User.Id
#!/usr/bin/python 
# -*- coding: utf-8 -*-
Trace.Write("Calling QTquotelistpage123")

try:
	StartandEnd = Param.StartandEnd
except:
	StartandEnd = "1_10"
	Trace.Write("b"+str(StartandEnd))
try:
	SORT = Param.SORT
	Trace.Write("sort-->"+SORT)
except :
	SORT= '' 
try:
	COLUMN=Param.COLUMN
	Trace.Write("column-->"+COLUMN)
except :
	COLUMN= ''   
try:
	Fetch_Count = Param.Fetch_Count
	Trace.Write("c"+str(Fetch_Count))
except:
	Fetch_Count = "10"
	Trace.Write("d"+str(Fetch_Count))
try:
	quoterev = Param.quoterev.strip()
except:
	quoterev = ''
try:
	
	activrev = Param.activrev.strip()
except:
	activrev = ''
try:
	stpaccountname=Param.stpaccountname.strip()
except:
	stpaccountname=''
try:
	opportname=Param.opportname.strip()
except:
	opportname=''
try:
	quotelistappStatus=Param.quotelistappStatus.strip()
except:
	quotelistappStatus=''
try:
	Primarycontname=Param.Primarycontname.strip()
except:
	Primarycontname=''
try:
	Qteowner=Param.Qteowner.strip()
except:
	Qteowner=''
try:
	Employeeresponsible=Param.Employeeresponsible.strip()
except:
	Employeeresponsible=''
try:
	Totalqte=Param.Totalqte.strip()
except:
	Totalqte=''
try:
	StartandEnd=Param.StartandEnd    
except:
	StartandEnd= "1_10"
try:
	Fetch_Count=Param.Fetch_Count
except:
	Fetch_Count="10"
try: 
	SearchValue =Param.SearchValue.strip()
except:
	SearchValue= ""
try:
	primaryqte = Param.primaryqte.strip()
except:
	primaryqte= ""
try:
	Qstatus = Param.Qstatus.strip()
except:
	Qstatus =""
try:
	quotetype = Param.quotetype.strip()
except:
	quotetype = ""
try:
	cntryacc= param.cntryacc.strip()
except:
	cntryacc= ""

if(SORT!="" and COLUMN != ""):
	sortingorder= COLUMN+" "+SORT
else:
	sortingorder= "cc.date_created DESC"
Companyname=User.Company.Name
if 'SFEnvironment' in globals():
	Session_id = SFEnvironment.SfSessionId
	Trace.Write("Sessid--"+str(Session_id))
else:
	Session_id = ""
	Trace.Write("Sessionid--"+str(Session_id))
try:
	if Session_id != "":
		Environment ="and c.r18 ='SFEnvironment' and c.order_status not in  ('44','45','47','49','50','51','52','53'))"
		Environment1 ="and c.r18 ='SFEnvironment'"
		Statusshown = "(13,36,40,35,41,12,42,32,14)"
		Trace.Write("if"+str(Environment))
		
	else:
		Environment ="and ((c.r18 = 'SFEnvironment'and c.order_status in ('13','35')) or (c.r18 !='SFEnvironment' and c.order_status not in  ('44','45','47','49','50','51','52','53'))))"
		Environment1 ="and c.r18 !='SFEnvironment'"
		Statusshown = "(13,35,48,32,14)"
		Trace.Write("else--"+str(Environment))
except:
	Environment ="and c.r18 !=''"

def loadapprovalpage(ACTION,quoterev,activrev,stpaccountname,opportname,quotelistappStatus,Primarycontname,Qteowner,Employeeresponsible,Totalqte,SearchValue,Qstatus,primaryqte,StartandEnd,Fetch_Count):       
	pagination = ""
	startcnt = 0
	StartandEnd = StartandEnd.split('_')
	startcnt = int(StartandEnd[0]) - 1
	startcount = StartandEnd[0]
	endcnt = StartandEnd[1]
	Offset_Skip_Count  = 1
	offset_skip_count = Offset_Skip_Count
	fetch_count = Fetch_Count
	#VisitorId = str(TagParserProduct.ParseString('<*CTX( Visitor.Id )*>'))

	if offset_skip_count == 1:
		offset_skip_count = 0
		pagination_condition = "OFFSET {Offset_Skip_Count} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY".format(Offset_Skip_Count=offset_skip_count, Fetch_Count=fetch_count)
		
	Pagination_M = Sql.GetFirst("""select COUNT(*) as Count from (select c.cart_id, c.userid, c.date_created, c.date_modified, c.order_status, IsNull(c.customer_id,0) as customer_id, c.isBlocked, c.revision1, c.quoteNumber2,isnull(c.revision2,'') as revision3, c.r3, c.r4, c.r5, c.r6, c.r7, c.r8, c.r9,c.r10,c.r11 from (select c.cart_id, c.userid, c.date_created, c.order_status, c.date_modified, IsNull(c.customer_id,0) as customer_id, c2col.BlockedFromDeletion as isBlocked, revCol.Name as revision1,revCol.REVISION_ID as revision2, c2Col.CartCompositeNumber as quoteNumber2, ci.customer_company as r3, u.name as r4,c.DATE_CREATED as r5, c2Col.MRC_TotalAmount as r8, IsNull(c.MarketTotalAmount, 0) as r9,  (select content from scparams with (nolock) where userid=c.userid and cart_id=c.cart_id and PARAMID=33) as r10,(select content from scparams with (nolock) where userid=c.userid and cart_id=c.cart_id and PARAMID=216) as r11,(select content from scparams with (nolock) where userid=c.userid and cart_id=c.cart_id and PARAMID=5) as r6 ,  try_cast((select content from scparams with (nolock) where userid=c.userid and cart_id=c.cart_id and PARAMID=27) as date) as r7  from cart c with (nolock)  left outer join cart2 c2Col with (nolock) on c.CART_ID = c2Col.cartid and c.USERID = c2Col.ownerid  left outer join customer_info ci with (nolock) on c.customer_id=ci.id left outer join cart_revisions revCol with (nolock) on c.CART_ID = revCol.cart_id and c.USERID = revCol.visitor_id  left outer join users u with (nolock) on c.userid=u.id  where (c.record_status=0 or c.record_status is null) and c.active_rev=1 and (c2Col.MarkedForDeletion is null or c2Col.MarkedForDeletion <> 1)  and c.ApprovalStatus = 9 ) c inner join (select responsible_approver_id, owner_id, cart_id, status from current_cart_responsibility ccr with (nolock) where isWaitingForApprove = 1 group by responsible_approver_id, owner_id, cart_id, status) ccr on c.cart_id=ccr.cart_id and c.userid=ccr.owner_id where 0 = 0  and ccr.responsible_approver_id='"""+str(userid)+"""' ) cc, (select distinct c.userid,c.cart_id from cart c with (nolock)  where 0=0 ) dd where cc.cart_id=dd.cart_id and cc.userid=dd.userid""")
	QueryCount = Pagination_M.Count
	pagination_total_count = QueryCount
	if Pagination_M is not None:
		records_end = endcnt
		if int(pagination_total_count) < int(records_end):
				records_end = pagination_total_count
		records_start_and_end = "{} - {} of ".format(startcount, records_end)
		Trace.Write("122"+str(records_start_and_end))
		disable_next_and_last = ""
		disable_previous_and_first = ""
		if records_end == pagination_total_count:
			disable_next_and_last = "class='btn-is-disabled'"
		if offset_skip_count == 0:
			disable_previous_and_first = "class='btn-is-disabled'"
			current_page = int(math.ceil(int(endcnt) / int(fetch_count)))
			Trace.Write("current page"+str(current_page))
			Product.SetGlobal("QueryCount", str(QueryCount))
			pagination += """<div id = "ApprovalPagination" class="col-md-12 brdr listContStyle padbthgt30">
				<div class="col-md-4 pager-numberofitem  clear-padding">
					<span class="pager-number-of-items-item flt_lt_pad2_mar2022 pull-left" id="NumberofItem">{Records_Start_And_End}</span>
					<span class="pager-number-of-items-item flt_lt_pad2_mar pull-left" id="totalItemCount">{Pagination_Total_Count}</span>
						<div class="clear-padding fltltmrgtp3">
							<div class="pull-left pull-left-10">
								<select onchange="PageFunctest(this)" class="cat-load-border-none" id="PageCountValue" >""".format(
			Records_Start_And_End="1 - 10 of ",
			Pagination_Total_Count=pagination_total_count,
			Selected_10="selected" if fetch_count == 10 else "",
			Selected_20="selected" if fetch_count == 20 else "",
			Selected_50="selected" if fetch_count == 50 else "",
			Selected_100="selected" if fetch_count == 100 else "",
			Selected_200="selected" if fetch_count == 200 else "",
			Disable_First=disable_previous_and_first,
			Disable_Previous=disable_previous_and_first,
			Disable_Next=disable_next_and_last,
			Disable_Last=disable_next_and_last,
			Current_Page=current_page
		)
			for i in [10,20,50,100,200]:
				if str(fetch_count) == str(i):
					pagination += "<option value="+str(i)+" selected>"+str(i)+"</option>"
				else:
					pagination += "<option value="+str(i)+">"+str(i)+"</option>"
			pagination +=  """</select>
							</div>
						</div>
				</div>
					<div class="col-xs-8 col-md-4 clear-padding inpadtex" data-bind="visible: totalItemCount">
						<div class="clear-padding col-xs-12 col-sm-6 col-md-12 brd0">
							<ul class="pagination pagination">
								<li><a class="cat-load-border-none" id="PageFirst" onclick="FirstPageLoad_pagination()" ><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a></li>
								<li><a class="cat-load-border-none" id="PagePrev" onclick="Previous12334()" ><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li>
								<li><a class="cat-load-border-none" id="PageNext" onclick="Next12334()">NEXT<i class="fa fa-caret-right fnt14"></i></a></li>
								<li><a class="cat-load-border-none" id="PageLast" onclick="LastPageLoad_pagination()"><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li>
							</ul>
						</div>
					</div>
					<div class="col-md-4 pad3 page-cnt-right pge-cnt-align-right">
					<span id="page_count" class="currentPage page_right_content">{Current_Page}</span>
					<span class="page_right_content padrt2">Page </span>
					</div>
			</div></div>""".format(
			Records_Start_And_End=records_start_and_end,
			Pagination_Total_Count=pagination_total_count,
			Selected_10="selected" if fetch_count == 10 else "",
			Selected_20="selected" if fetch_count == 20 else "",
			Selected_50="selected" if fetch_count == 50 else "",
			Selected_100="selected" if fetch_count == 100 else "",
			Selected_200="selected" if fetch_count == 200 else "",
			Disable_First=disable_previous_and_first,
			Disable_Previous=disable_previous_and_first,
			Disable_Next=disable_next_and_last,
			Disable_Last=disable_next_and_last,
			Current_Page=current_page
		) 	
	table = ''

	table = '''<div class ='qthtmltable'><table id= 'Quote_tableapp'><thead><tr>'''
	
	thead = ['ACTIONS','QUOTE','REVISION','STP ACC NAME','OPPORTUNITY NAME','OPPORTUNITY STATUS','PRIMARY CONTACT NAME','QUOTE OWNER','EMP RESPONSIBLE','REV CREATION DATE','REV EXPIRATION DATE','TOTAL QUOTE','PRIMARY QUOTE','STATUS']
	for i in thead:
		if str(i) == "ACTIONS":
			table = table+'''<th style="width: 70px;"><div class='Col_name'>'''+str(i)+'''</div><div class="search_button"><button class="searched_button" onclick="quote_list_sear_approval()">Search</button></th>'''
		elif str(i) == "QUOTE":
			table = table+'''<th id= "qterevapp"><div title="QUOTE" class='Col_name' id="sort_quoteNumber1" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div><div style='text-align: right;' class="search_button"><input onkeypress="checkEnterKeyPressedAppQte(event)" id= "qterevapp" value=''' +str(quoterev)+'''></input></div></th>'''
		elif str(i) == "REVISION":
			table = table+'''<th id= "actrevapp"><div title="REVISION" class='Col_name' id="sort_revision3" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div><div style='text-align: right;' class="search_button"><input onkeypress="checkEnterKeyPressedAppQte(event)" id= "actrevapp" value=''' +str(activrev)+''' ></input></div></th>'''
		elif str(i) == "STP ACC NAME":
			table = table+'''<th id="stpaccnameapp"><div title="STP ACC NAME" class='Col_name' id="sort_r4" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div><div style='text-align: right;' class="search_button"><input onkeypress="checkEnterKeyPressedAppQte(event)" id="stpaccnameapp" value=''' +str(stpaccountname)+''' ></input></div></th>'''
		elif str(i) == "OPPORTUNITY NAME":
			table = table+'''<th id="oppnameapp"><div title="OPPORTUNITY NAME" class='Col_name' id="sort_r5" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div><div style='text-align: right;' class="search_button"><input onkeypress="checkEnterKeyPressedAppQte(event)" id="oppnameapp" value=''' +str(opportname)+''' ></input></div></th>'''
		elif str(i) == "OPPORTUNITY STATUS":
			table = table+'''<th id="oppstatapp"><div title="OPPORTUNITY STATUS" class='Col_name' id="sort_r6" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div><div style='text-align: right;' class="search_button"><input onkeypress="checkEnterKeyPressedAppQte(event)" id="oppstatapp" value=''' +str(opportname)+''' ></input></div></th>'''
		elif str(i) == "PRIMARY CONTACT NAME":
			table = table+'''<th id="Pricontnameappr"><div title="PRIMARY CONTACT NAME" class='Col_name' id="sort_r7" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div><div style='text-align: right;' class="search_button"><input onkeypress="checkEnterKeyPressedAppQte(event)" id="Pricontnameapp" value='' ></input></div></th>'''
		elif str(i) == "QUOTE OWNER":
			table = table+'''<th id="qteownerappr"><div title="QUOTE OWNER" class='Col_name' id="sort_r8" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div><div style='text-align: right;' class="search_button"><input onkeypress="checkEnterKeyPressedAppQte(event)" id="Qtownerapp" value='' ></input></div></th>'''
		elif str(i) == "EMP RESPONSIBLE":
			table = table+'''<th id="Empresappr"><div title="EMP RESPONSIBLE" class='Col_name' id="sort_r9" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div><div style='text-align: right;' class="search_button"><input onkeypress="checkEnterKeyPressedAppQte(event)" id="Empresapp" value='' ></input></div></th>'''
		elif str(i) == "REV CREATION DATE":
			table = table+'''<th id="revcretdateappr"><div title="REV CREATION DATE" class='Col_name' id="sort_r10" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div><div style='text-align: right;' class="search_button"><input onkeypress="checkEnterKeyPressedAppQte(event)" id="revcretdateapp" value='' ></input></div></th>''' 
		elif str(i) == "REV EXPIRATION DATE":
			table = table+'''<th id="revexpdateappr"><div title="REV EXPIRATION DATE" class='Col_name' id="sort_r11" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div><div style='text-align: right;' class="search_button"><input onkeypress="checkEnterKeyPressedAppQte(event)" id="revexpdateapp" value='' ></input></div></th>''' 
		elif str(i) == "TOTAL QUOTE":
			table = table+'''<th id="Totqteappr"><div title="TOTAL QUOTE" class='Col_name' id="sort_r12" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div><div style='text-align: right;' class="search_button"><input onkeypress="checkEnterKeyPressedAppQte(event)" id="Totqteapp" value='' ></input></div></th>'''
		elif str(i) == "PRIMARY QUOTE":
			table = table+'''<th id="primaqte" class="simp_config cat-load-width-70">
						<div class='Col_name' id="sort_r13" onclick="sortQteGridCol(this)">'''+str(i)+'''<span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown" ></span></span></div>
						<div class="multiselect-qtlist-primaryapp">
							<div class="selectBox" onclick="showprimaryQteMultiChkboxapp()">
								<div id="listPrimaryQtyappSec"><div id="listPrimaryQtyapp" class="spanMutlichkBox appr-select-box">All</div><i class="selectArrow down"></i></div>
							</div>
							<div id="primaryQteMultiChkboxapp">
								<label class="selectAllqtpriapp">
									<input type="checkbox" name="qtelist-primaryapp-all" class="custom qtlist-th-checkbox-align-left custom-td-chkbox qtSelectAllCheck chkboxappPriOpt" onclick="selectAllPrimaryapp()" value="All" /><span class="lbl td-chk-tick-box lbl-multi-chkbox-span"></span><span class="wrap-prod-val">Select All</span>
								</label>
								<label class="selectConfig">
									<input type="checkbox" name="qtelist-primary-app" class="custom qtlist-th-checkbox-align-left custom-td-chkbox" onclick="choosePrimaryQteListapp()" value="True"><span class="lbl td-chk-tick-box lbl-multi-chkbox-span"></span><span class = 'primaryQteapp_chkbox_data'>True</span></label>
								<label class="selectConfig">
									<input type="checkbox" name="qtelist-primary-app" class="custom qtlist-th-checkbox-align-left custom-td-chkbox" onclick="choosePrimaryQteListapp()" value="False"><span class="lbl td-chk-tick-box lbl-multi-chkbox-span"></span><span class = 'primaryQteapp_chkbox_data'>False</span></label>
							</div>
						</div>
					</th>'''
		elif str(i) == "STATUS":
			table = table+'''<th id="Qtstatus" class="simp_config cat-load-width-70">
						<div title="STATUS" class='Col_name' id="sort_r14" onclick="sortQteGridCol(this)"><span class="quote_text">'''+str(i)+''' </span><span class='sortingQteSecCls'><span class="sortingImgTop"></span><span class="sortingImgDown"></span></span></div>
						<div class="multiselect-qtlist-appstatus">
							<div class="selectBox" onclick="showStatusInMultiChkboxapp()">                                
								<div id="listStatusoptionsappSec"><div id="listStatusoptionsapp" class="spanMutlichkBox appr-select-box">All</div><i class="selectArrow down"></i></div>
							</div>
							<div id="statusInMultiChkboxapp">
								<label class="selectAllstatapp">
									<input type="checkbox" name="prod-grp" class="custom qtlist-th-checkbox-align-left custom-td-chkbox qtSelectAllCheck chkboxappStatusOpt" onclick="selectAllStatusapp()" value="All" /><span class="lbl td-chk-tick-box lbl-multi-chkbox-span"></span><span class="wrap-prod-val">Select All</span></label>
								<label class="selectConfig">
									<input type="checkbox" name="qte-statusapp-type" class="custom qtlist-th-checkbox-align-left custom-td-chkbox" onclick="chooseappQteListStatus()" value="Level 2 Approval Requested"><span class="lbl td-chk-tick-box lbl-multi-chkbox-span"></span><span class = "Status_chkbox_data">Level 2 Approval Requested</span></label>
								<label class="selectConfig">
									<input type="checkbox" name="qte-statusapp-type" class="custom qtlist-th-checkbox-align-left custom-td-chkbox" onclick="chooseappQteListStatus()" value="Level 1 Approval Requested"><span class="lbl td-chk-tick-box lbl-multi-chkbox-span"></span><span class = "Status_chkbox_data">Level 1 Approval Requested</span></label>
								<label class="selectConfig">
									<input type="checkbox" name="qte-statusapp-type" class="custom qtlist-th-checkbox-align-left custom-td-chkbox" onclick="chooseappQteListStatus()" value="Level 3 Approval Requested"><span class="lbl td-chk-tick-box lbl-multi-chkbox-span"></span><span class = "Status_chkbox_data">Level 3 Approval Requested</span></label>
								<label class="selectConfig">
									<input type="checkbox" name="qte-statusapp-type" class="custom qtlist-th-checkbox-align-left custom-td-chkbox" onclick="chooseappQteListStatus()" value="Awaiting Approval"><span class="lbl td-chk-tick-box lbl-multi-chkbox-span"></span><span class = "Status_chkbox_data">Awaiting Approval</span></label>
								
							</div>
						</div>
					</th>'''
	table = table+'''</tr></thead><tbody>'''
	Trace.Write('table---'+table)
	Trace.Write('table---start'+str(startcnt))
	Trace.Write('table---end'+str(Fetch_Count))
	getquotelist = Sql.GetList("""select DISTINCT cc.* from (select c.cart_id, c.userid, c.date_created, c.date_modified, c.order_status, IsNull(c.customer_id,0) as customer_id, c.isBlocked, c.revision1, c.quoteNumber1,isnull(c.revision2,'') as revision3,c.r2, c.r3, c.r4, c.r5, c.r6, c.r7, c.r8, c.r9,c.r10,c.r11,c.r12,c.r13,c.r14,c.r15 from (select c.cart_id, c.userid, CONVERT(varchar,c.DATE_CREATED , 101) as r10,CONVERT(varchar,c.date_modified,101) as r11, c.order_status, c.date_modified, IsNull(c.customer_id,0) as customer_id, c2col.BlockedFromDeletion as isBlocked, revCol.Name as revision1,revCol.REVISION_ID as revision2, c2Col.CartCompositeNumber as quoteNumber1,c2Col.CartCompositeNumber as r2, ci.customer_company as r3, u.name as r8,c.DATE_CREATED, c2Col.MRC_TotalAmount as r12, IsNull(c.MarketTotalAmount, 0) as r15,  (select content from scparams with (nolock) where userid=c.userid and cart_id=c.cart_id and PARAMID=33) as r4,(select content from scparams with (nolock) where userid=c.userid and cart_id=c.cart_id and PARAMID=53) as r5,(select content from scparams with (nolock) where userid=c.userid and cart_id=c.cart_id and PARAMID=216) as r14,(select content from scparams with (nolock) where userid=c.userid and cart_id=c.cart_id and PARAMID=5) as r6 ,(select content from scparams with (nolock) where userid=c.userid and cart_id=c.cart_id and PARAMID=85) as r7,(select content from scparams with (nolock) where userid=c.userid and cart_id=c.cart_id and PARAMID=89) as r9,(select content from scparams with (nolock) where userid=c.userid and cart_id=c.cart_id and PARAMID=161) as r13  from cart c with (nolock)  left outer join cart2 c2Col with (nolock) on c.CART_ID = c2Col.cartid and c.USERID = c2Col.ownerid  left outer join customer_info ci with (nolock) on c.customer_id=ci.id left outer join cart_revisions revCol with (nolock) on c.CART_ID = revCol.cart_id and c.USERID = revCol.visitor_id  left outer join users u with (nolock) on c.userid=u.id  where (c.record_status=0 or c.record_status is null) and c.active_rev=1 and (c2Col.MarkedForDeletion is null or c2Col.MarkedForDeletion <> 1)  and c.ApprovalStatus = 9 ) c inner join (select responsible_approver_id, owner_id, cart_id, status from current_cart_responsibility ccr with (nolock) where isWaitingForApprove = 1 group by responsible_approver_id, owner_id, cart_id, status) ccr on c.cart_id=ccr.cart_id and c.userid=ccr.owner_id where 0 = 0  and ccr.responsible_approver_id='"""+str(userid)+"""' ) cc, (select distinct c.userid,c.cart_id from cart c with (nolock)  where 0=0 ) dd where cc.cart_id=dd.cart_id and cc.userid=dd.userid ORDER BY """+str(sortingorder)+""" OFFSET {startcnt} ROWS FETCH NEXT {Fetch_Count} ROWS ONLY
	""".format(startcnt=startcnt,Fetch_Count=Fetch_Count))
	
	if getquotelist is not None:	
		for item in getquotelist:
			Trace.Write("asas"+str(item.r14))
			usid = str(item.userid)
			crtid = str(item.cart_id)
			curr = SqlHelper.GetFirst(" select DEF_CURRENCY from cart (NOLOCK) where USERID='"+usid+"' and  CART_ID='"+crtid+"' ")
			tot_quo = str(item.r12)+" "+ str(curr.DEF_CURRENCY)
			if item.r13 == 'true':
				checked = "checked"
				Actbtns = "ACTION_NAME IN('DELETE REVISION','VIEW REVISION','NEW REVISION','RECALL')"
			else:
				checked = ""
				Actbtns = "ACTION_NAME IN('DELETE REVISION','VIEW REVISION','NEW REVISION','SET PRIMARY','RECALL')"
			a= Sql.GetList("Select DISTINCT ACTIONS.ACTION_NAME from ACTIONS (nolock) INNER JOIN ACTIONS_STATUS (NOLOCK) ON ACTIONS_STATUS.ACTION_ID = ACTIONS.ACTION_ID INNER JOIN ORDER_STATUS_DEFN (NOLOCK) ON ACTIONS_STATUS.START_ORDER_STATUS_ID = ORDER_STATUS_DEFN.ORDER_STATUS_ID and ACTIONS_STATUS.END_ORDER_STATUS_ID = ORDER_STATUS_DEFN.ORDER_STATUS_ID where ORDER_STATUS_DEFN.ORDER_STATUS_NAME = '"+str(item.r14)+"' and ACTIONS.GLOBAL_ACTION !='I' and "+str(Actbtns)+"")
			Actiondropdown =""
			if a is not None:
				for i in a:
					if(i.ACTION_NAME)=="SET PRIMARY":
						data="data-toggle='modal' data-target='#setprimary'"
					elif(i.ACTION_NAME)=="DELETE REVISION":
						data="data-toggle='modal' data-target='#delrevision'"
					else:
						data=""
					#Trace.Write("135lines"+str(i.ACTION_NAME))
					ONCLICKACTION=(i.ACTION_NAME).replace (" ", "_").upper()
					Actiondropdown += "<li><button class='btn btn-sm quote-list-action-button' id='"+str(item.r2)+"' "+str(data)+" onclick='quotelist_"+str(ONCLICKACTION)+"(this)'>"+str(i.ACTION_NAME)+"</button></li>"
					Trace.Write("tttt"+str(Actiondropdown))

				table = table + "<tr><td class='actions'><div class='fiori3-input-group' ><div class='btn-group dropdown' ><div class='dropdown' onclick='act_btn_dp(this)' id='ctr_drop'><i data-toggle='dropdown' id='dropdownMenuButton' class='fa fa-sort-desc dropdown-toggle' aria-expanded='true'></i><ul class='dropdown-menu left' aria-labelledby='dropdownMenuButton'>"+str(Actiondropdown)+"</ul></div></div></div></td><td id='quote_num_rev'><a onclick='gotquote_num_rev(this.innerHTML)'><abbr id='"+str(item.quoteNumber1)+"' title='"+str(item.quoteNumber1)+"'>"+str(item.quoteNumber1)+"</abbr></a></td><td>"+str(item.revision3)+"</td><td >"+str(item.r4)+"</td><td class='OppName'><a id='gotoopp' href='#' onclick='gotoopportunity(this.innerHTML);' data-bind='attr:{'title':value},htmlOrNbsp : $parent.isBlocked &amp;&amp; $data.columnName == 'order_status' ? options()[0].value : value' title='"+str(item.r5)+"'>"+str(item.r5)+"</a></td><td>"+str(item.r6)+"</td><td><a id='gotocon' href='#' onclick='gotocontacts(this);' data-bind='attr:{'title':value},htmlOrNbsp : $parent.isBlocked &amp;&amp; $data.columnName == 'order_status' ? options()[0].value : value' title='"+str(item.r7)+"'>"+str(item.r7)+"</a></td><td>"+str(item.r8)+"</td><td >"+str(item.r9)+"</td><td style = 'text-align:center'>"+str(item.r10)+"</td><td style = 'text-align:center'>"+str(item.r11)+"</td><td>"+str(tot_quo).encode()+"</td><td class='prim_qut'><input type='checkbox' class='quotelistchkbox custom'"+checked+" disabled=''><span class='lbl'></span></td><td>"+str(item.r14)+"</td></tr></div>"
	table=table+"</tbody></table></div>"+str(pagination)
	return table#+str(pagination)    


ACTION=Param.ACTION
if(ACTION == "WAIT_APPROVAL"):
	ApiResponse = ApiResponseFactory.JsonResponse(loadapprovalpage(ACTION,quoterev,activrev,stpaccountname,opportname,quotelistappStatus,Primarycontname,Qteowner,Employeeresponsible,Totalqte,SearchValue,Qstatus,primaryqte,StartandEnd,Fetch_Count))
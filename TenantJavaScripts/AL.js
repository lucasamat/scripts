/*===========================================================================================================================================
#   __script_name : AL.js
#   __script_description : APPROVAL Related javascript functions.
#   __primary_author__ : ALL BHC DEVELOPERS
#	__secondary_author__: 
#   __create_date   :   19/03/22
#   __modified_date : 
# ==========================================================================================================================================*/
$(document).ready(function() {
     window.parent.$(".overlay").css("display", "block");
window.parent.$("#pageloader").css("display", "block");});
      
function approvalReference() {
     var approvalref = $('#APPROVAL_REFERENCE_ID').val().length
     var ApprRefId = $('#APPROVAL_REFERENCE_ID').val()
	  console.log("ref id", ApprRefId);
     if (approvalref === 10) {
         cpq.server.executeScript("QTEMSGADDG", {
             'FieldVal': ApprRefId
         }, function() {});
     }
     if (approvalref === 10) {
         cpq.server.executeScript("QTAPVLQTCC", {
             'Action': 'saveApprRefVal',
             'FieldVal': ApprRefId,
             'FieldValLen': approvalref
         }, function(data) {
             console.log("Test approve", data);
             if (approvalref === 10 && data == true) {
                 $('#monapproval_self_btn').removeAttr('disabled');
             }
         });
     } else {
         $('#monapproval_self_btn').attr("disabled", "disabled")
     }
 }
 
 
 function res_fun() {
 
     var wd_ht = $(window).height();
 
     if ($('div#cart_contant_pg')) {
         var grd_ht_tp = $('div#approvalContainer').offset();
 
 
         if (grd_ht_tp) {
             var grd_ht = grd_ht_tp.top;
 
             var ht_grd = wd_ht - grd_ht;
 
             //var set_sty = 'max-height:'+ht_grd+'px;height:'+ht_grd+'px;';
             var set_sty = 'max-height:' + ht_grd + 'px !important;height:' + ht_grd + 'px;min-height:' + ht_grd + 'px !important;'
 
             $('div#approvalContainer').css('cssText', set_sty);
 
         }
     }
 }
 $(window).resize(function() {
 
     res_fun();
 
 });
 
 $(document).ready(function() {
	cpq.server.executeScript("QTAPRVLHST", {}, function(dataval) {
        $('#QTAppHistry').html(dataval[0]);
		if(dataval[7] != ""){
			$('#QTAppHistry').after('<div class = "noRecDisp" > No Approval Rules have been triggered. </div>');
			//$('#QTAppHistry').after(dataval[7]);
		}
			if ($('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(3)').text() == "Self Approval" && $('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(5)').text() == "Approval Submission Pending" && dataval[1] == "APR-APPROVAL PENDING" && dataval[8] == 1){
			$('#submit_appr').hide();
			$('#monapproval_self_btn').css('display', 'block');
	}
	else if($('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(5)').text() == "Approved" && $('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(3)').text() == "Self Approval") {
		$('#submit_appr').hide();
		$('#monapproval_self_btn').css('display', 'none');
	}
	else if($('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(5)').text() != "Approval Submission Pending" && dataval[1] == "APR-APPROVAL PENDING" && dataval[2] == 0){
		if (dataval[3] > 0){
			$('#retractButton').css('display', 'block');
			$('button#submit_appr').css('display', 'none');
		}
		else{
			$('#retractButton').css('display', 'none');
			$('button#submit_appr').css('display', 'none');
			$('#dyn_btn_Reject').hide();
			$('#dyn_btn_Approve').hide();
		}
	}
	else if(dataval[1] != "APR-APPROVAL PENDING")
	{
		$('#retractButton').css('display', 'none');
	}
	else if(dataval[2] > 0){
		$('#retractButton').css('display', 'none');
		$('button#submit_appr').text("Approve");
		$('button#submit_appr').css('display', 'block');
		if(dataval[4] == 0){
			$('button#submit_appr').css('display', 'none');
			$('#dyn_btn_Reject').show();
			$('#dyn_btn_Approve').show();
		}
		
	}
	
	if(dataval[6] > 0)
	{
		$('#retractButton').css('display', 'none');
	}
	
	if(dataval[5] == 1)
	{
		$('#retractButton').css('display', 'none');
		$('button#submit_appr').css('display', 'none');
		$('#dyn_btn_Reject').hide();
		$('#dyn_btn_Approve').hide();
	}
	
	});
	window.parent.$(".overlay").css("display", "none");
	window.parent.$("#pageloader").css("display", "none");
	});
	

 /*$(document).ready(function() {
     //console.log( "ready!" );
     setTimeout(function() {
         window.parent.$(".overlay").css("display", "block");
         window.parent.$("#pageloader").css("display", "block");
         cpq.server.executeScript("QTPRYHTPNL", {}, function(datas) {
             localStorage.setItem('HeaderQuotename', '');
             localStorage.setItem('HeaderAccountName', datas[1]);
             localStorage.setItem('HeaderOppName', datas[2]);
             localStorage.setItem('HeaderOppID', datas[3]);
             //console.log("data : " + datas[4]);
             localStorage.setItem('Headerstage', datas[4]);
             localStorage.setItem('HeaderAccountType', datas[6]);
             localStorage.setItem('HeaderRevisionStatus', datas[9]);
             $('.transaction_node p.sec_val abbr#qt_val3').text(datas[7]);
             Banner_HTML = datas[11]
             //localStorage.setItem('FRMETHOD',datas[8]);
             //localStorage.setItem('FRTERM',datas[9]);
             //localStorage.setItem('PYTERM',datas[10]);
             //localStorage.setItem('ShipTms',datas[11]);
             localStorage.setItem('priquote', datas[7]);
             localStorage.setItem('HeaderQuoteOwner', datas[8]);
             localStorage.setItem('RevisionQuoteNumber', datas[10]);
 
             var HeaderQuotename = localStorage.getItem('HeaderQuotename');
             var HeaderAccountName = localStorage.getItem('HeaderAccountName');
             var HeaderOppName = localStorage.getItem('HeaderOppName');
             var Headerstage = localStorage.getItem('Headerstage');
             var HeaderAccountType = localStorage.getItem('HeaderAccountType');
             var HeaderRevisionStatus = localStorage.getItem('HeaderRevisionStatus');
             var PrimaryQuote = localStorage.getItem('priquote');
             var HeaderQuoteOwner = localStorage.getItem('HeaderQuoteOwner');
             var RevisionQuoteNumber = localStorage.getItem('RevisionQuoteNumber');
             var apprbttn = datas[12];
             localStorage.setItem('CartId', datas[13]);
             localStorage.setItem('OwnrId', datas[14]);
             HeaderQuotename1 = HeaderQuotename + '-' + HeaderQuotename.substring(0, 1);
             localStorage.setItem('HeaderQuotename_sec_hilt_ban', HeaderQuotename1);
             localStorage.setItem('HeaderrevNum', HeaderQuotename.substring(0, 1));
             
             Primary_Quote = datas[7]
             if (Primary_Quote == "true") {
                 $('.quote-title-span6 input[type=checkbox]').prop('checked', true);
             } else {
                 $('.quote-title-span6 input[type=checkbox]').prop('checked', false);
             }
             
             cpq.server.executeScript("QTAPRVLHST", {}, function(dataval) {
                 $('#QTAppHistry').html(dataval);
                 //selfaprbtn=data[1];
                 //submitbtn=data[2];
                 //localStorage.setItem('selfaprbtn',selfaprbtn)
                 //localStorage.setItem('submitbtn',submitbtn)
 
 
                 var HeaderRevisionStatus = localStorage.getItem('HeaderRevisionStatus');
                 if ($('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(3)').text() == "Monarch Self Approval" && $('#QTAppHistry table').find('tbody tr:nth-child(2) td:nth-child(3)').text() == "Quote Extension Approval" && HeaderRevisionStatus == "Preparing Revision") {
                     $('#approval_act_btn').show();
                     $('#submit_appr').hide();
                 } else if ($('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(3)').text() == "Monarch Self Approval" && $('#QTAppHistry table').find('tbody tr:nth-child(2) td:nth-child(3)').text() == "Quote Extension Approval" && HeaderRevisionStatus == "Awaiting Approval") {
                     $('#monapproval_self_btn').hide();
                     //$('button#submit_appr').text("SUBMIT FOR APPROVAL");
                 } else if ($('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(3)').text() == "Multi-Use Quote Approval" && $('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(4)').text() == "Approval Requested") {
                     $('#monapproval_self_btn').hide();
 
                 }
 
 
                 if (HeaderRevisionStatus == "Awaiting Approval" && $('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(4)').text() == "Approved") {
                     $('#submit_appr').css('display', 'none');
                 }
                 if (HeaderRevisionStatus == "Awaiting Approval") {
                     var myapp = $('#app_tb_3').find('tbody tr:nth-child(1) td:nth-child(6)').text();
                     var reapp = $('#app_tb_2').find('tbody tr:nth-child(1) td:nth-child(2)').text();
                     var myappuser = $('#app_tb_3').find('tbody tr:nth-child(1) td:nth-child(4)').text().trim();
                     var reappuser = $('#app_tb_2').find('tbody tr:nth-child(1) td:nth-child(3)').text().trim();
                     var str2 = "Deal Health Approval";
                     var DealHealth = "";
                     if (myapp.indexOf(str2) != -1) {
                         DealHealth = "true";
                         myapp = myapp.split(";")[0];
                     } else if (reapp.indexOf(str2) != -1) {
                         DealHealth = "true";
                         myapp = reapp.split(";")[0];
                     } else {
                         DealHealth = "false";
                         myapp = myapp;
                     }
 
                     rowcount = $('#QTAppHistry tr').length - 1;
                     for (let i = 1; i <= rowcount; i++) {
                         var apphstry = $('#QTAppHistry table').find('tbody tr:nth-child(' + i + ') td:nth-child(3)').text();
                         var apphstry_status = $('#QTAppHistry table').find('tbody tr:nth-child(' + i + ') td:nth-child(4)').text();
                         if (myapp == apphstry && apphstry_status == "Approval Requested") {
                             $('button#submit_appr').css('display', 'block');
                             $('table#app_tb_2 thead tr th:nth-child(7)').hide();
                             $('table#app_tb_2 tbody tr td:nth-child(7)').hide();
                             $('table#app_tb_2 thead tr th:nth-child(5)').show();
                             $('table#app_tb_2 tbody tr td:nth-child(5)').show();
                             $('table#app_tb_2 thead tr th:nth-child(6)').show();
                             $('table#app_tb_2 tbody tr td:nth-child(6)').show();
                         }
                         if (reapp == apphstry && apphstry_status == "Approval Submission Pending") {
                             //$('button#submit_appr').css('display', 'block');
                         }
                         if (myappuser == reappuser) {
                             $('table#app_tb_2 thead tr th:nth-child(7)').hide();
                             $('table#app_tb_2 tbody tr td:nth-child(7)').hide();
                             $('table#app_tb_2 thead tr th:nth-child(5)').show();
                             $('table#app_tb_2 tbody tr td:nth-child(5)').show();
                             $('table#app_tb_2 thead tr th:nth-child(6)').show();
                             $('table#app_tb_2 tbody tr td:nth-child(6)').show();
                         } else {
                             $('table#app_tb_2 thead tr th:nth-child(7)').hide();
                             $('table#app_tb_2 tbody tr td:nth-child(7)').hide();
                             $('table#app_tb_2 thead tr th:nth-child(5)').hide();
                             $('table#app_tb_2 tbody tr td:nth-child(5)').hide();
                             $('table#app_tb_2 thead tr th:nth-child(6)').hide();
                             $('table#app_tb_2 tbody tr td:nth-child(6)').hide();
                         }
                         if (rowcount == i && apphstry_status == "Approval Requested" && DealHealth == "true") {
                             $('#dyn_btn_Approve').show();
                             //$('#dyn_btn_Reject').show();
                             $('button#submit_appr').css('display', 'none');
 
                         }
                     }
                     if (DealHealth == "true") {
                         $('table#app_tb_2 thead tr th:nth-child(7)').hide();
                         $('table#app_tb_2 tbody tr td:nth-child(7)').hide();
                         $('table#app_tb_2 thead tr th:nth-child(5)').show();
                         $('table#app_tb_2 tbody tr td:nth-child(5)').show();
                         $('table#app_tb_2 thead tr th:nth-child(6)').show();
                         $('table#app_tb_2 tbody tr td:nth-child(6)').show();
 
                     }
                     if (rowcount == 2) {
                         var apphstry_selffirst = $('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(3)').text();
                         var apphstry = $('#QTAppHistry table').find('tbody tr:nth-child(2) td:nth-child(3)').text();
                         var apphstry_status = $('#QTAppHistry table').find('tbody tr:nth-child(2) td:nth-child(4)').text();
                         var apphstry_per = $('#QTAppHistry table').find('tbody tr:nth-child(2) td:nth-child(5)').text();
                         var apphstry_user = $('#QTAppHistry table').find('tbody tr:nth-child(2) td:nth-child(6)').text();
                         if (apphstry_selffirst.indexOf("Self Approval") != -1 && apphstry_status == "Approval Requested") {
 
                             $('button#submit_appr').css('display', 'none');
                             $('button#retractButton').css('display', 'block');
                         }
                         if (apphstry.indexOf("Self Approval") != -1) {
 
                         } else {
                             $('button#submit_appr').css('display', 'block');
                             $('button#submit_appr').text("SUBMIT FOR APPROVAL");
                             $('button#monapproval_self_btn').css('display', 'none');
                             $('#approval_act_btn').css('display', 'none');
                             $('table#app_tb_2 thead tr th:nth-child(7)').hide();
                             $('table#app_tb_2 tbody tr td:nth-child(7)').hide();
                             $('table#app_tb_2 thead tr th:nth-child(5)').show();
                             $('table#app_tb_2 tbody tr td:nth-child(5)').show();
                             $('table#app_tb_2 thead tr th:nth-child(6)').show();
                             $('table#app_tb_2 tbody tr td:nth-child(6)').show();
                         }
                         if (apphstry_status == "Approval Requested" && window.parent.$(".quote-title-span7").text().trim() == apphstry_per) {
                             $('button#retractButton').css('display', 'block');
                         }
                         if (myapp == apphstry && apphstry_status == "Approval Requested" && myappuser == apphstry_user) {
                             $('button#retractButton').css('display', 'none');
                         }
 
                         if (apphstry_selffirst.indexOf("Self Approval") != -1 && rowcount == 2 && apphstry_status == "Approval Submission Pending") {
                             $('#monapproval_self_btn').css('display', 'block');
                             $('button#submit_appr').css('display', 'none');
                             $('button#retractButton').css('display', 'none');
                         }
                         if (apphstry.indexOf("Quote Extension Approval") != -1 && rowcount == 2 && apphstry_status == "Approval Submission Pending") {
                             $('#monapproval_self_btn').css('display', 'none');
                             $('button#submit_appr').css('display', 'block');
                             $('button#submit_appr').removeAttr("style");
                         }
                         if (apphstry.indexOf("Quote Extension Approval") != -1 && rowcount == 2 && apphstry_status == "Approval Requested") {
                             $('button#submit_appr').css('display', 'none');
                         }
                         if (myapp != "" && myapp.indexOf("Self Approval") != -1) {
                             $('button#retractButton').css('display', 'none');
                             $('#app_tb_3').find('thead tr:nth-child(1) th:nth-child(8)').css("display", "none");
                             $('#app_tb_3').find('tbody tr:nth-child(1) td:nth-child(8)').css("display", "none");
                         }
                         if (reapp.indexOf("Payment") != -1) {
                             $('table#app_tb_2 thead tr th:nth-child(7)').show();
                             $('table#app_tb_2 tbody tr td:nth-child(7)').show();
                         }
                     }
                 } else if (HeaderRevisionStatus == "Preparing Revision") {
 
                     if ($('button#submit_appr').is(":visible")) {
                         $('table#app_tb_2 thead tr th:nth-child(7)').hide();
                         $('table#app_tb_2 tbody tr td:nth-child(7)').hide();
                         $('table#app_tb_2 thead tr th:nth-child(5)').show();
                         $('table#app_tb_2 tbody tr td:nth-child(5)').show();
                         $('table#app_tb_2 thead tr th:nth-child(6)').show();
                         $('table#app_tb_2 tbody tr td:nth-child(6)').show();
                     }
                     if ($('button#submit_appr').is(":visible") && $('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(3)').text().indexOf("Payment") != -1) {
                         $('table#app_tb_2 thead tr th:nth-child(7)').show();
                         $('table#app_tb_2 tbody tr td:nth-child(7)').show();
                     }
 
                     var myapp = $('#app_tb_3').find('tbody tr:nth-child(1) td:nth-child(6)').text();
                     var reapp = $('#app_tb_2').find('tbody tr:nth-child(1) td:nth-child(2)').text();
                     var apphstry = $('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(3)').text();
                     var apphstry_status = $('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(4)').text();
                     var apphstry_status_second = $('#QTAppHistry table').find('tbody tr:nth-child(2) td:nth-child(4)').text();
                     if (reapp == apphstry && apphstry_status == "Approval Submission Pending") {
                         $('button#submit_appr').css('display', 'block');
                         $('button#monapproval_self_btn').css('display', 'none');
                         $('#approval_act_btn').css('display', 'none');
                     }
                     rowcount = $('#QTAppHistry tr').length - 1;
                     if (apphstry.indexOf("Self Approval") != -1 && rowcount == 1) {
                         $('#approval_act_btn').css('display', 'block');
                         $('button#submit_appr').css('display', 'none');
                     } else if (apphstry.indexOf("Self Approval") != -1 && rowcount == 2) {
                         $('#approval_act_btn').css('display', 'block');
                         $('button#submit_appr').css('display', 'none');
                     }
 
 
                     var visible = $('button#submit_appr').is(":visible")
                     var visble = $('button#approval_act_btn').is(":visible")
                     if (apphstry.indexOf("Incoterms Approval") != -1 && rowcount == 2) {
                         $('#approval_act_btn').css('display', 'block');
                         $('button#submit_appr').css('display', 'none');
                     } else {
                         $('#approval_act_btn').css('display', 'block');
                     }
 
                     window.parent.$(".overlay").css("display", "none");
                     window.parent.$("#pageloader").css("display", "none");
                 };
 
                 if (apprbttn == "True") {
                     $('#dyn_btn_Approve').show();
                     $('#dyn_btn_Reject').show();
                     //$('#dyn_btn_Approve').attr('onclick','submitapprovepopup(this)');  
                 } else {
                     $('#dyn_btn_Approve').hide();
                     //$('#submit_appr').hide();
                     $('#dyn_btn_Reject').hide();
                 }
                 if (PrimaryQuote == "true") {
                     $('#pri-check').prop('checked', true);
                 } else {
                     $('#pri-check').prop('checked', false);
                 }
 
                 var selfapprbtn = localStorage.getItem('selfaprbtn')
                 var appr_node = window.parent.$('#commontreeview li.node-selected').text()
                 var notification = window.parent.$('.notificationvalue').text();
                 if (HeaderRevisionStatus == "Preparing Revision") {
                     if ($('button#submit_appr').is(":visible") || notification == "Configuration Status : Incomplete") {
                         $('#approval_act_btn').css('display', 'none');
                         $('#monapproval_self_btn').css('display', 'none');
                         //$('button#submit_appr').css('display', 'none');
                     }
                     
                 }
                 setTimeout(function() {
                     var submit_text = $('#approvalContainer .cart-content span #submit_appr').text().trim();
                     if (submit_text == "Approve") {
                         $('#submit_appr').css('right', '160px')
                     } else {
                         $('#submit_appr').css('right', '10px')
                     }
 
                     if (HeaderRevisionStatus == "Approved") {
                         $('div#Apprvl_dtls').hide();
                         $('div#Apprvl_dtls').attr('style', 'display:none !important');
                         $('#approval_act_btn').css('display', 'none');
                         $('#app_trd_grd').attr('style', 'display:none');
                     }
 
                 }, 1000);
                 ApprovStat = window.parent.$('p#hd_status.quote-title-span8').text();
                 if (ApprovStat == "Approved") {
                     $('#approval_act_btn').css('display', 'none');
                 }
                 if (HeaderRevisionStatus != 'Approved' && HeaderRevisionStatus != "Level 1 Approval Requested" && HeaderRevisionStatus != "Level 2 Approval Requested" && HeaderRevisionStatus != "Level 3 Approval Requested" && HeaderRevisionStatus != "Awaiting Approval") {
                     //$("button#carticon").css('display', 'block');
                     //$("button#Approve").css('display', 'block');
                     $("button#NewRevision").css('display', 'block');
                     $("button#bk_to_lst").css('display', 'block');
                     $("button#DeleteRevision").css('display', 'block');
                     //$('#approval_act_btn').css('display', 'block');
                 } else {
                     $('#approval_act_btn').css('display', 'none');
                     $('#NewRevision').css('display', 'none');
                     //$('#Gen_Doc').css('display','block');
                     $("button#bk_to_lst").css('display', 'block');
                     $("button#DeleteRevision").css('display', 'none');
                     $("button#Approve").css('display', 'none');
                     $("button#carticon").css('display', 'none');
                     $('.select2.select2-container.select2-container--default').attr('id', 'levelonedrop')
                     setInterval(function() {
                         if ($('.select2-container--focus')) {
                             $('.select2.select2-container.select2-container--default.select2-container--focus').attr('id', 'levelonedropfocus')
                         }
                         if ($('.select2-container--dropdown-open')) {
                             $('.select2-container.select2-container--default.select2-container--open.select2-container--dropdown-open').attr('id', 'leveloneoption')
                         }
                     }, 100);
                 }
                 if (HeaderRevisionStatus == "Approved") {
                     $('div#Apprvl_dtls').hide();
                     $('div#Apprvl_dtls').attr('style', 'display:none !important');
                     $('#approval_act_btn').css('display', 'none');
                     $('#app_trd_grd').attr('style', 'display:none');
                 }
                 if (HeaderRevisionStatus == "Awaiting Approval") {
                     $('#approval_act_btn').css('display', 'none');
                     if (window.parent.$('a#field_MonarchSelfApprove span').length > 0) {
                         $('#monapproval_self_btn').css('display', 'block');
                     }
                     $('#submit_appr').text("Approve");
                     $('#submit_appr').css('right', '160px')
 
                 } else if (HeaderRevisionStatus == "Level 1 Approval Requested" || HeaderRevisionStatus == "Level 2 Approval Requested") {
                     $('button#submit_appr').text("Approve");
                 }
 
                 setTimeout(function() {
                     var app_trd_grd = $('div#app_trd_grd').css('display');
 
                     var app_frth_grd = $('div#app_frth_grd').css('display');
 
                     if (app_trd_grd == 'none' && app_frth_grd == 'none') {
 
                         // $('.table-responsive.tab_content_1,.table-responsive.tab_content_2').css('display','block');
                     }
 
                 }, 500);
                 setTimeout(function() {
                     var selfapprbtn = localStorage.getItem('selfaprbtn')
                     var submitbtn = localStorage.getItem('submitbtn')
                     var submit_visible = $('button#submit_appr').is(":visible")
                     var self_visble = $('button#approval_act_btn').is(":visible")
                     if (self_visble == true && selfapprbtn == "0") {
                         $('#approval_act_btn').css('display', 'none');
 
                     } else if (submit_visible == true && submitbtn == "0") {
 
                         $('button#submit_appr').css('display', 'none');
                     }
                 }, 500)
 
             });
 
             setTimeout(function() {
 
                 if ($('#submit_appr').css('display') != 'none' && $('#Approve').css('display') != 'none') {
                     $('button#Approve').css('display', 'none');
                 }
 
 
                 $('#app_tb_4 tbody tr td:first-child span').each(function(index) {
                     var value = $(this).parents("tr").children("td:first").text();
                     var indxlen = $('#app_tb_4 tbody tr td:first-child').length;
                     var lasindx = indxlen - 1;
                     var trimStr = $.trim(value);
                     //var Iconvar = '<i class="fa fa-check-circle text-success"></i> <span tabindex="0">Approved</span>'
                     //if (index != lasindx && trimStr == "Submitted for Approval"){$(this).parents("tr").children("td:first-child").html(Iconvar);$('#cancelBtn').css('display','none');}
                 });
 
                 var indxlen = $('#app_sec_grd tbody tr td:first-child').length;
                 //console.log(indxlen);
                 if (indxlen == 0) {
                     $('#Apprvl_hd').css('display', 'none');
                 } else {
                     $('#Apprvl_hd').css('display', 'block');
                 }
 
                 var indxlen = $('#app_trd_grd tbody tr td:first-child').length;
                 //console.log(indxlen);
                 if (indxlen == 0) {
                     $('#Apprvl_dtls').css('display', 'none');
                 } else {
                     $('#Apprvl_dtls').css('display', 'block');
                 }
 
 
                 //console.log('9999999999999');
                 res_fun();
                 //console.log('999999999999977777777777777');
 
             }, 1500);
             setTimeout(function() {
                 var environment_name = localStorage.getItem('environmentvar');
                 if (environment_name == 'SFEnvironment') {
                     notification_text = $('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(5)').text()
                     var HeaderRevisionStatus = localStorage.getItem('HeaderRevisionStatus');
 
 
                     if (notification_text.indexOf('Self') != -1 && HeaderRevisionStatus != "Approved") {
                         $('#approval_act_btn').css('display', 'block');
 
                     } else if (notification_text.indexOf('Self') == -1 && notification_text != "") {
                         $('#submit_appr').css('display', 'block');
                     }
                 }
             }, 1500);
 
             HeaderRevisionStatus = $('.quote-title-span8').text();
             if (HeaderRevisionStatus == "Approved") {
                 setTimeout(function() {
                     $('#approval_act_btn').css('display', 'none');
                 }, 1000);
             }
 
         }, 1500);
     });
 });*/
 
 function history_exp_col(ele) {
     $(ele).children('.more-less').toggleClass('glyphicon-chevron-up glyphicon-chevron-down');
 }
 
 function showApprNotify(message, title) {
 
     messagespan = document.getElementById("txt_area_cont_appr");
     messagespan.textContent = ""
     messagetxt = document.createTextNode(message);
     messagespan.appendChild(messagetxt);
 
     titlespan = document.getElementById("relatedDelete");
     titletxt = document.createTextNode(title);
     titlespan.appendChild(titletxt);
 
     $("#approval_notify_pop").modal("show");
 }
 
 function CommentsApprove() {
     /*var CommentsApp = $('#txt_cmd_sub_app').val().length
     if(CommentsApp == 25){
      $('#approval_act_btn').removeAttr('disabled')
     }*/
     /*var submit_text = $('#approvalContainer .cart-content span #submit_appr').text().trim();
     if (window.parent.$(".quote-title-span2").text() == "" && submit_text != "Approve") {
         console.error("Oppurtunity is empty, Cannot approve")
         var message_txt = "This quote has exceeded Self Approval Limits and as such it must be recreated from an Opportunity record."
         showApprNotify(message_txt, "APPROVAL NOTIFICATION")
         $('#approval_act_btn').attr('disabled', 'disabled');
         $('#txt_cmd_sub_app').val("")
     }*/
 }
 
 function recall_nm(ele) {
     var re_cl = $(ele).text().trim();
     //console.log('re_cl...'+re_cl);
	 localStorage.setItem("RecallQuote","yes");
	 recall_comments = $('.fiori3-input-group textarea').val();
	 localStorage.setItem("RecallComments",recall_comments);
     if (re_cl == 'RECALL') {
         setTimeout(function() {
             //console.log('RRRRR11111111');
             $('.modal.fade.in[aria-label="Retract Approval Dialog"] .modal-header h3.modal-title').text('Recall Comments');
             $('.modal .fiori3-retract-approval-modal').find('.modal-content .modal-footer button.fiori3-btn-primary').attr('onclick', 'submitApproval()');
         }, 300);
     }
 }
 
 function appr_sv() {
     //console.log('ZZZZZZZZZTTTTTTTTT');
     var ck_dyn_id = localStorage.getItem("dyn_id_val");
     //console.log('ck_dyn_id....'+ck_dyn_id);
     if (ck_dyn_id) {
         //console.log('get_dyn_id....iiiiiiffff');
         var get_dyn_id = 'button#' + ck_dyn_id;
         //console.log('get_dyn_id....'+get_dyn_id);
         $(get_dyn_id).trigger('click');
         localStorage.setItem("dyn_id_val", "");
     } else {
         //console.log('get_dyn_id....eeeeeellllll');
         $('button#submit_appr_hd').trigger('click');
     }
 }
 
 function rej_sv() {
     //console.log('ZZZZZZZZZTTTTTTTTTyyyyyyyyyyyyyy');
     $('button#Reject').trigger('click');
 }
 
 function sub_fr_appr(ele) {
     //console.log('sub_fr_appr....'+sub_fr_appr);
     var btn_txt = $(ele).text().trim().toLowerCase();
     //console.log('btn_txt....'+btn_txt);
     setTimeout(function() {
         //console.log('sub_fr_appr...TTTTTTTTTTTT.');
 
         var chg_btn_txt = '';
         if (btn_txt == 'submit for approval') {
             chg_btn_txt = 'submit';
         } else {
             chg_btn_txt = 'approve';
             btn_txt = 'Approval'
             $('p#delprod').text('Quote is approved.');
         }
         $('div#approval_cmd_bx span#relatedDelete').text(btn_txt);
         $('button#popUpBtn').text(chg_btn_txt);
     }, 300);
 }
 
 function kyprs(ele) {
     //console.log('aaaaa');
     var txt_val = $(ele).val();
     //console.log('txt_val....'+txt_val);
     $('textarea#txt_cmd_sub_app').val(txt_val)
 }
 
 function onchg(ele) {
     var a = $(ele).val();
     conole.log('aaaaa...' + a);
     $(ele).val();
 }
 
 function tran_head_txt(ele) {
     var tb_txt = $(ele).text().trim();
     //console.log('tb_txt....'+tb_txt);
     localStorage.setItem("tb_txt_nm", tb_txt);
 }
 localStorage.setItem("dyn_id_val", "");
 
 function app_btn_clk(ele) {
     var app_id = $(ele).attr('id');
     //console.log('app_id.....'+app_id);
     var dyn_id = 'dyn_btn_' + app_id
     //console.log('app_id.....'+app_id);
     localStorage.setItem("dyn_id_val", dyn_id);
     if (app_id == 'Approve') {
         $('div#approval_cmd_bx .modal-footer button#popUpBtn').text('Approve');
     }
 }
 
 function qut_lst_pg() {
     window.location.href = "https://sandbox.webcomcpq.com///quotation/LoadQuote.aspx";
 }
 
 function CreateNewRevision() {
     cpq.server.executeScript("CREATENEWREVISION", {}, function(QuoteId) {
         window.location.href = QuoteId;
     });
 
 }
 
 function DelRev() {
     $("#approval_matr_pop").modal("show");
 }
 
 function DelRevFunc() {
     var HeaderQuoteNum = localStorage.getItem('HeaderQuotename');
     HeaderQuoteNum = HeaderQuoteNum.toString();
     localStorage.setItem('DeleteRevision', HeaderQuoteNum);
     window.location.href = " https://sandbox.webcomcpq.com/quotation/LoadQuote.aspx";
 
 
     setTimeout(function() {
         cpq.server.executeScript("DELREVISION", {
             'QuoteId': JSON.stringify(HeaderQuoteNum)
         }, function(QuoteId) {
             //console.log("return : "+QuoteId);
         });
     }, 50);
 }
 
 function cart_cont_collap_exp(ele) {
     //console.log('AAAAAAAAAAAAAAAAA');   
     $(ele).children('.more-less').toggleClass('glyphicon-chevron-up glyphicon-chevron-down');
     //console.log('AAAAAAAAAAAAAAAAABBBBBBBBBB');   
 }
 
 
 $(document).ready(function() {
     //window.parent.$(".overlay").css("display", "block");
     //window.parent.$("#pageloader").css("display", "block");
     //var qtenum = $('.current_quote_header p.quote-title-span1').text();
     //console.log("qtenum",qtenum)
     ////var res = qtenum.split("-");
     //var revidsplit = res[1]
     //console.log("xxyyyyyyxx",qtenum);
     //console.log("xxxx",res)
     //console.log("ssss",revidsplit)
 
     //if (revidsplit != '0') {
 
         // $('#act_btn_dyn_wdh  #DeleteRevision').css('cssText','display:none !important;');
         //$('#act_btn_dyn_wdh  #DeleteRevision').remove();
 
     //}
 
     $('#dyn_btn_Reject').attr('onclick', 'rejectpopup(this)');
     //$('#submit_appr').attr('onclick','submitapprovepopup(this)');  
     //$('#dyn_btn_Approve').attr('onclick','submitapprovepopup(this)');  
     //window.parent.$(".overlay").css("display","none");
     //window.parent.$("#pageloader").css("display","none");
 });
 
 $('#approvalIframe').on('load', function() {
     setTimeout(function() {
         $('#approvalIframe').contents().find('#head_highlight').hide();
     }, 500)
 });
 

 function commentsSave() {
     //var environment_name = localStorage.getItem('environmentvar');
     //if (environment_name == 'CRMEnvironment') {
         //setTimeout(function() {
             var myapp = $('#QTAppHistry table').find('tbody tr:nth-child(1) td:nth-child(3)').text();
             //if (myapp.indexOf(";") != -1) {
                 //myapp = myapp.split(";")[0];
             //} else {
                 //myapp = myapp;
             //}
             var APPROVAL_RULE = myapp;
             var COMPETITOR = $('#txt_cmd_sub_app').val();
			 if (localStorage.getItem("RecallQuote") == 'yes'){
				 COMPETITOR = localStorage.getItem("RecallComments");
				 localStorage.setItem("RecallQuote","no");
			 }
             var JUSTIFICATION_COMMENTS = $('#approval_comment_longtext').val();
             cpq.server.executeScript("QTAPVLQTCC", {
                 'COMPETITOR': COMPETITOR,
                 'JUSTIFICATION_COMMENTS': JUSTIFICATION_COMMENTS,
                 'APPROVAL_RULE': APPROVAL_RULE
             }, function(datas) {});
         //}, 20);
     //}
 }
 
 function submitApproval(){
	 recall_comments = $('.fiori3-input-group textarea').val();
	 localStorage.setItem("RecallComments",recall_comments);
	 localStorage.setItem("add_new_functionality","TRUE");
	commentsSave();
	setTimeout(function(){
         parent.location.reload();
     }, 500);
 }
 /* function moved in custom action ASGAPPRULE - AGIMONARCH-13863 31-03-2022 */
 /* function ApplyTax_call(){
     cpq.server.executeScript("TAXWARECALLS", {Action: ''}, function (dataset) {$("[id='field_addtoquote_config'] span").click();});
 }*/
 
 function rejectpopup(ele) {
     var btn_txt = $(ele).text().trim().toLowerCase();
     if (btn_txt == 'reject')
         $('p#delprod').text('Quote is rejected.');
     setInterval(function() {
 
 
         var btn_txt = $(ele).text().trim().toLowerCase();
         if (btn_txt == 'reject')
             $('p#delprod').text('Quote is rejected.');
 
 
     }, 6);
 }
 
 function submitapprovepopup(ele) {
     setTimeout(function() {
         var btn_txt = $(ele).text().trim().toLowerCase();
         if (btn_txt == 'approve')
             $('p#delprod').text('Quote is approved.');
     }, 1000);
     setTimeout(function() {
         parent.location.reload();
     }, 1200);
 
     /*param = { action: "oppurtunityCheck" };
    if(window.parent.$("#Opportunity_name").text()==""){
     cpq.server.executeScript("QTDISCTUPD", param, function (datas) {
         console.log(datas)
         if (datas==true && window.parent.$("#Opportunity_name").text()=="")
         {
              console.error("Oppurtunity is empty, Cannot approve")
             var message_txt="This quote has exceeded Self Approval Limits and as such it must be recreated from an Opportunity record."
             showApprNotify(message_txt,"APPROVAL NOTIFICATION")
             $('#approval_act_btn').attr('disabled', 'disabled');
             $('#txt_cmd_sub_app').val("")        
           }
                
     });
      }*/
 
 
     /*var btn_txt = $(ele).text().trim().toLowerCase();
 if(btn_txt=='approve')
 $('p#delprod').text('Quote is approved.');
   setInterval(function(){
 
 var btn_txt = $(ele).text().trim().toLowerCase();
 if(btn_txt=='approve')
 $('p#delprod').text('Quote is approved.');
      },3);
   setTimeout(function(){                   
           parent.location.reload(); 
       },1200);*/
 }
 
 function iframeApproveBtn() {
     commentsSave();
     window.parent.$("[id='field_Update Status'] span").trigger('click');
     //$('.quote-title-span8').text('Approved');
     $('#approval_act_btn').hide();
     setTimeout(function() {
         parent.location.reload();
     }, 1200);
 }
 
 function iframeMonSelfApproveBtn() {
     commentsSave();
     window.parent.$("[id='field_MonarchSelfApprove'] span").trigger('click'); // $('.quote-title-span8').text('Approved');
     $('#approval_act_btn').hide();
     $('#monapproval_self_btn').hide();
     //parent.location.reload();
	 setTimeout(function() {
         parent.location.reload();
     }, 1200);
 }
 $(document).on("click", "#appr_notify_button", function() {
     // parent.location.reload();
 });
 
 
 function textareaFun() {
     var offsetHeight = document.getElementById('COMPETITOR').offsetHeight;
     document.getElementById('JUSTIFICATION_COMMENTS').style.height = offsetHeight + 'px';
 }
 
 function textareaFuntwo() {
     var offsetHeight = document.getElementById('JUSTIFICATION_COMMENTS').offsetHeight;
     document.getElementById('COMPETITOR').style.height = offsetHeight + 'px';
 }
 
 function textareaFunthree() {
     var offsetHeight = document.getElementById('APPROVAL_REFERENCE_ID').offsetHeight;
     document.getElementById('JUSTIFICATION_COMMENTS').style.height = offsetHeight + 'px';
     document.getElementById('COMPETITOR').style.height = offsetHeight + 'px';
 }
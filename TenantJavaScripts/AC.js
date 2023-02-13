/*===========================================================================================================================================
#   __script_name : AC.JS
#   __script_description : THIS SCRIPT IS USED TO DO THE FUNCTIONALITIES OF APPROVAL CENTER and CATALOG APP 
#   __primary_author__ : VETRIVEL
#	__secondary_author__: VIJAYAYAKUMAR
#   __create_date   :   
#   __modified_date :   16-07-2020
#   © BOSTON HARBOR TECHNOLOGY LLC - ALL RIGHTS RESERVED
# ==========================================================================================================================================*/
 
function closefullview() {
    $(".Clkfull_view").show();
    $(".closeview").hide();
    $("#content12345").removeClass("full_view");
    $(".fullviewdiv").removeClass("full_view_btn");
    $(".product-details-main-container").removeClass("full_view_btnstyle");
    $('#Countries_right_view').css('cssText', 'overflow-y: hidden;');
    $('#rightcarttree').css('cssText', 'max-height: 77vh !important; overflow-y: auto;');
    $(".product-detail-view").addClass("col-xl-4");
    $(".product-detail-view").addClass("col-lg-4");
    $(".product-detail-view").addClass("col-md-4");
    $(".product-detail-view").addClass("col-sm-4");
    $(".product-detail-view").addClass("col-xs-4");
    $("#righttreeview > div.col-md-12.col-lg-12.a2.segment_table").css('cssText', 'max-height: 516.4px !important;');
}
function EmiloverflowYoff() {
	$(".tab-content").css("overflow-y", "hidden");
	$(".BTN_MA_ALL_REFRESH").click();
}
function fullview() {
    $("#content12345").addClass("full_view");
    $(".Clkfull_view").hide();
    $(".closeview").show();
    $(".fullviewdiv").addClass("full_view_btn");
    $(".product-details-main-container").addClass("full_view_btnstyle");
    $('html').css('cssText', 'overflow-y:hidden !important');
    $('#rightcarttree').css('cssText', 'max-height: 80vh !important; overflow-y: hidden;');
    $('#Countries_right_view').css('cssText', 'max-height: 51vh !important; overflow-y: auto;');
    $(".product-detail-view").addClass("col-xs-4");
    $(".product-detail-view").removeClass("col-xl-4");
    $(".product-detail-view").removeClass("col-lg-4");
    $(".product-detail-view").removeClass("col-md-4");
    $(".product-detail-view").removeClass("col-sm-4");
    $(".product-detail-view").removeClass("col-xs-12");
    $("#righttreeview > div.col-md-12.col-lg-12.a2.segment_table").css('cssText', 'max-height: 580.4px !important;');
}

function RichTextAreafun() {
    let disable;
    try {
        currentVal = $('#RichTextArea').val();
        Action_Text = localStorage.getItem('Action_Text');
        if (Action_Text == "VIEW"|| $('#BTN_SYPGAC_AC_00003_SAVE').length==0 ) {
            disabled = true;
        } else {
            disabled = false;
        }
        $('#RichTextArea').jqxEditor({
            height: "350px !important",
            disabled: disabled
        });
        $('#RichTextArea').val(currentVal);
        if (disabled == false) {
            $(".jqx-editor-content iframe").on("load", function () {
                let head = $(".jqx-editor-content iframe").contents().find("head");
                let css = '<style>html,body{height: 100% !important;} body{background-color: lightyellow;}</style>';
                $(head).append(css);
            });
        }
    } catch (e) {
        console.log('Rich TextArea Error');
    }
}

function CategorybreadCrumb_redirection(leftNode) {
    var left_text = $(leftNode).text();
    $('#Categtreeview ul.list-group li.list-group-item.node-Categtreeview').each(function (index) {
        var nodeText = $(this).text();
        if (nodeText == left_text) {
            $(this).trigger('click');
        }
    });
}

function preview_approvals() {
    try {
        quotenumber = localStorage.getItem("keyData");
        try{
            AllParams ={}
            for (const [key, value] of Object.entries(dict)) {
                if (value.includes("<img")) {
                    val = value.split(">")[1]
                } else {
                    val = value
                }
                AllParams[key] = val
            }
            AllParams = JSON.stringify(AllParams);
        }
        catch(e){
            AllParams = JSON.stringify(dict);
        } 
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "PREVIEW_APPROVAL",
            'AllParams': AllParams,
            'QuoteNumber': quotenumber
        }, function (dataset) {
            $("#div_CTR_related_list").css("display", "block");
            $("#div_CTR_related_list").closest('.Related').show();
            $('#div_CTR_related_list').html(dataset[0]);
        });
    } catch (e) {
        console.log(e);
    }
}

function approvals_history() {
    try {
        quotenumber = localStorage.getItem("keyData");
        try{
            AllParams ={}
            for (const [key, value] of Object.entries(dict)) {
                if (value.includes("<img")) {
                    val = value.split(">")[1]
                } else {
                    val = value
                }
                AllParams[key] = val
            }
            AllParams = JSON.stringify(AllParams);
        }
        catch(e){
            AllParams = JSON.stringify(dict);
        } 
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "PREVIEW_APPROVAL",
            'AllParams': AllParams,
            'QuoteNumber': quotenumber
        }, function (dataset) {
            if (currenttab == "Quotes"){
				$("#div_CTR_related_list").css("display", "block");
				$("#div_CTR_related_list").closest('.Related').show();
				$('#div_CTR_related_list').html(dataset[0]);
				//$(".common_MyApprovalQueue ").hide();
				$('.container_banner_inner_sec').css('display', 'none');

				Subbaner("",CurrentNodeId, CurrentRecordId, 'ACAPTX')
			}
			else if (currenttab != "Quotes"){
				$("#div_CTR_Approval_History").css("display", "block");
				$(div_CTR_Approval_History).closest('.Related').show();
				$('#div_CTR_Approval_History').html(dataset[0]);
				//$(".common_MyApprovalQueue ").hide();
				$('.container_banner_inner_sec').css('display', 'none');

				Subbaner("",CurrentNodeId, CurrentRecordId, 'ACAPTX')
			}
        });
    } catch (e) {
        console.log(e);
    }
}

function quote_approvals_node() {
    try {
        //approval image based on chain step starts
        var approval_chain = ""
        quotenumber = localStorage.getItem("keyData");
        try{
            AllParams ={}
            for (const [key, value] of Object.entries(dict)) {
                if (value.includes("<img")) {
                    val = value.split(">")[1]
                } else {
                    val = value
                }
                AllParams[key] = val
            }
            AllParams = JSON.stringify(AllParams);
        }
        catch(e){
            AllParams = JSON.stringify(dict);
        } 
        if (localStorage.getItem("preview_approval_flag") == "True"){
            approval_chain = localStorage.getItem("current_tab_approvals")
            localStorage.setItem("preview_approval_flag","False")
            localStorage.setItem("current_tab_approvals","")    
        }
        //approval image based on chain step ends
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "PREVIEW_APPROVAL",
            'AllParams': AllParams,
            'QuoteNumber': quotenumber,
            'approval_chain': approval_chain,
        }, function (dataset) {
            // $("#div_CTR_All").css("display", "block");
            $('.container_banner_inner_sec').css('display', 'none');
            // $("#div_CTR_All").closest('.Related').show();
            $('#div_CTR_related_list').html(dataset[0]);
            //$(".common_MyApprovalQueue ").hide();
            $('.noRecDisp').css('display','none');
            //Secondary highlightpanel not dynamic in approvals node subtab
            data1 = dataset[1]
            if (approval_chain == "" && data1 != "" ) {
                approval_chain = data1[0][0]["Value"]
            }
            Subbaner(approval_chain,CurrentNodeId, CurrentRecordId, 'ACAPCH')
        });
        
    } catch (e) {
        console.log(e);
    }
}
function PriceApprovalHistory(ele) {
    GetCurrentchainName = $(ele).text().trim();
    if (GetCurrentchainName == 'All') {
        $('.CommonHistoryPAApp ').css('display', 'block');
    }
    else {
        testGetCurrentchainName = GetCurrentchainName.replace(/\ /g, '_')
        $('.CommonHistoryPAApp ').css('display', 'none');
        $('.' + testGetCurrentchainName).css('display', 'block');
    }
    //approval image based on chain step starts
    x = testGetCurrentchainName.split("_")
    x = x[x.length-1]
    localStorage.setItem("current_tab_approvals",x)
    localStorage.setItem("preview_approval_flag","True")
    quote_approvals_node() 
    //approval image based on chain step ends
}

function recall_for_edit() {
    quotenumber = localStorage.getItem("keyData");
    try {
        quotenumber = localStorage.getItem("keyData");
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': 'RECALL',
            'QuoteNumber': quotenumber
        }, function (dataset) {
			
            cpq.server.executeScript("ACSECTACTN", {
                'ACTION': "STATUS",
                'QuoteNumber': quotenumber
            }, function (data) {
                if (data != '') {
                    $("#approve_status").text(data);
                    $("#approve_status").attr("title",data);
                    //$("#approve_status").parent().css('background','#0060B1');
                    $("#approve_status_outer").removeClass('complete');
		            $("#approve_status_outer").removeClass('reject');
                    $("#approve_status_outer").addClass('active');
                    $("#approve_status_reject").css('display','none');
                    $("#approve_status_compl").css('display','none');
                    $("#approve_status_numb").css('display','block');
                    
                }                
            });   
        });
        quote_status_update();
        //$("#BTN_MA_ALL_REFRESH").click()
		CurrentNodeId = localStorage.getItem("CurrentNodeId");
		CommonRightView(CurrentNodeId);
		//localStorage.setItem("left_tree_refresh", "yes")
								localStorage.setItem("add_new_functionality","TRUE");
								//CurrentNodeId = localStorage.getItem("CurrentNodeId");
		window.location.reload();
		
    } catch (e) {
        console.log(e)
    }
}

function reject_segrev(ele, FromHistory = "") {
    try {
        Rejectpopup();
        quotenumber = localStorage.getItem("keyData");
        ApproveDesc = $("#PREVIEW_APPROVAL_BODY textarea").val();
        //Showing approve/reject in list grid starts
        var grid_approval = localStorage.getItem("grid_approval")
        var get_tab_value = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text().toUpperCase();

        var tab_array = ["MY APPROVAL QUEUE","QUOTES","TEAM APPROVAL QUEUE"]
        if ((tab_array.indexOf(get_tab_value) != -1) && grid_approval == 'True'){
            var dict_approval ={}
              dict_approval['TreeParam'] = 'Approvals'
              AllParams = JSON.stringify(dict_approval); 
              quotenumber = localStorage.getItem("approval_txn_id")
              localStorage.setItem("approval_txn_id","") 
              grid_flag = 'True'
        }
        //Showing approve/reject in list grid ends
        else{
            try{
                AllParams ={}
                for (const [key, value] of Object.entries(dict)) {
                    if (value.includes("<img")) {
                        val = value.split(">")[1]
                    } else {
                        val = value
                    }
                    AllParams[key] = val
                }
                AllParams = JSON.stringify(AllParams);
            }
            catch(e){
                AllParams = JSON.stringify(dict);
            } 
          grid_flag = 'False'
         }
        if (FromHistory == "True"){
            CurretntTranscationID = $(ele).attr('id');
        }else{
            CurretntTranscationID = localStorage.getItem("CurrentRecordId");
        }
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "REJECT",
            'AllParams': AllParams,
            'QuoteNumber': quotenumber,
            'ApproveDesc': ApproveDesc,
            'CurrentTransId': CurretntTranscationID
        }, function (dataset) {
            //$("#BTN_MA_ALL_REFRESH").click();
			CurrentNodeId = localStorage.getItem("CurrentNodeId");
			CommonRightView(CurrentNodeId);
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "STATUS",
            'QuoteNumber': quotenumber,
            'grid_flag' : grid_flag,
        }, function (data) {
            if (data != '') {
                $("#approve_status").text(data);
                //$("#approve_status").parent().css('background','#ea4335');
                $("#approve_status").attr("title",data);
                $("#approve_status_outer").removeClass('complete');
		        $("#approve_status_outer").addClass('reject');
		        $("#approve_status_outer").removeClass('active');
                $("#approve_status_numb").css('display','none');
                $("#approve_status_compl").css('display','none');
                $("#approve_status_reject").css('display','block');
				
            }
        });    
        });
        //Showing approve/reject in list grid starts
        if (grid_approval == 'True'){
            $("#BTN_MA_ALL_REFRESH").click();
            var approval_tab_array = ["MY APPROVAL QUEUE","TEAM APPROVAL QUEUE"]
            if (approval_tab_array.indexOf(get_tab_value) != -1){
                localStorage.setItem("grid_approval",'False')   
            }
        }
        //Showing approve/reject in list grid ends
        else{
            quote_status_update();
            $('#APPROVAL_TAB ul li.active').click()
        }
		//localStorage.setItem("left_tree_refresh", "yes")
		cpq.server.executeScript("CQAPPCALWB", {  }, function (dataset) {
	
		});
		localStorage.setItem("add_new_functionality","TRUE")
		window.location.reload();
		
    } catch (e) {
        console.log(e);
    }
}

function approve_segrev(ele, FromHistory = "") {
    try {
        Approvepopup();
        quotenumber = localStorage.getItem("keyData");
        ApproveDesc = $("#PREVIEW_APPROVAL_BODY textarea").val();
        //Showing approve/reject in list grid starts
        var grid_approval = localStorage.getItem("grid_approval")
        var get_tab_value = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text().toUpperCase();

        var tab_array = ["MY APPROVAL QUEUE","QUOTES","TEAM APPROVAL QUEUE"]
        if ((tab_array.indexOf(get_tab_value) != -1) && grid_approval == 'True'){
            var dict_approval ={}
              dict_approval['TreeParam'] = 'Approvals'
              AllParams = JSON.stringify(dict_approval); 
              quotenumber = localStorage.getItem("approval_txn_id")
              localStorage.setItem("approval_txn_id","") 
              grid_flag = 'True'
        }
        //Showing approve/reject in list grid ends
        else{
            try{
                AllParams ={}
                for (const [key, value] of Object.entries(dict)) {
                    if (value.includes("<img")) {
                        val = value.split(">")[1]
                    } else {
                        val = value
                    }
                    AllParams[key] = val
                }
                AllParams = JSON.stringify(AllParams);
            }
            catch(e){
                AllParams = JSON.stringify(dict);
            } 
            grid_flag = 'False'
        }
        if (FromHistory == "True"){
            CurretntTranscationID = $(ele).attr('id');
        }else{
            CurretntTranscationID = localStorage.getItem("CurrentRecordId");
        }
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "APPROVE",
            'AllParams': AllParams,
            'QuoteNumber': quotenumber,
            'ApproveDesc': ApproveDesc,
            'CurrentTransId': CurretntTranscationID
        }, function (dataset) {
            //$("#BTN_MA_ALL_REFRESH").click();
			primary_banner();
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "STATUS",
            'QuoteNumber': quotenumber,
            'grid_flag' : grid_flag,
        }, function (data) {
            if (data != '') {
                $("#approve_status").text(data);
                $("#approve_status").attr("title",data);
                //$("#approve_status").parent().css('background','#4CCA82');
                $("#approve_status_outer").removeClass('active');
                $("#approve_status_outer").addClass('complete');
                $("#approve_status_outer").removeClass('reject');
                $("#approve_status_reject").css('display','none');
                $("#approve_status_numb").css('display','none');
                $("#approve_status_compl").css('display','block');
            }
        });    
        });
        //Showing approve/reject in list grid strts
        if (grid_approval == 'True'){
            $("#BTN_MA_ALL_REFRESH").click();
            var approval_tab_array = ["MY APPROVAL QUEUE","TEAM APPROVAL QUEUE"]
            if (approval_tab_array.indexOf(get_tab_value) != -1){
                localStorage.setItem("grid_approval",'False')   
            }
        }
        //Showing approve/reject in list grid ends
        else{
            quote_status_update();
            $('#APPROVAL_TAB ul li.active').click()
        }
		CurrentNodeId = localStorage.getItem("CurrentNodeId");
			CommonRightView(CurrentNodeId);
		cpq.server.executeScript("CQAPPCALWB", {  }, function (dataset) {
	
		});	
    } catch (e) {
        console.log(e)
    }
}

function submitfor_approval() {
    $('#submit_for_approval').hide();
    try {
        Submitpopup();
        quotenumber = localStorage.getItem("keyData");
        RequestDesc = $("#SUBMIT_MODAL_SECTION textarea").val();
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': 'SUBMIT_FOR_APPROVAL',
            'QuoteNumber': quotenumber,
            'RequestDesc': RequestDesc
        }, function (dataset) {
            //$("#BTN_MA_ALL_REFRESH").click();
			
            cpq.server.executeScript("ACSECTACTN", {
                'ACTION': "STATUS",
                'QuoteNumber': quotenumber
            }, function (data) {
                if (data != '') {
                    $("#approve_status").text(data);
                    $("#approve_status").attr("title",data);
                    //$("#approve_status").parent().css('background','#0060B1');
                    $("#approve_status_outer").removeClass('complete');
		            $("#approve_status_outer").removeClass('reject');
                    $("#approve_status_outer").addClass('active');
                    $("#approve_status_reject").css('display','none');
                    $("#approve_status_compl").css('display','none');
                    $("#approve_status_numb").css('display','block');
					
                }
            });
        }
        
        );
        quote_status_update();
		cpq.server.executeScript("CQAPPCALWB", {  }, function (dataset) {
		});
        $('#APPROVAL_TAB ul li.active').click()
		//CurrentNodeId = localStorage.getItem("CurrentNodeId");
			//CommonRightView(CurrentNodeId);
			localStorage.setItem("add_new_functionality","TRUE")
		window.location.reload();
    } catch (e) {
        console.log(e)
    }
}
//A043S001P01-13245 start
function bulk_approve_request(ele) {
    try {
        quotenumber = localStorage.getItem("keyData");
        ApproveDesc = $("#PREVIEW_APPROVAL_BODY textarea").val();
        try{
            AllParams ={}
            for (const [key, value] of Object.entries(dict)) {
                if (value.includes("<img")) {
                    val = value.split(">")[1]
                } else {
                    val = value
                }
                AllParams[key] = val
            }
            AllParams = JSON.stringify(AllParams);
        }
        catch(e){
            AllParams = JSON.stringify(dict);
        }         
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "BULKAPPROVE",
            'AllParams': AllParams,
            'QuoteNumber': quotenumber,
            'ApproveDesc': ApproveDesc,            
        }, function (dataset) {
            $("#BTN_MA_ALL_REFRESH").click();
        });
    } catch (e) {
        console.log(e)
    }
}
function bulk_reject_request(ele) {
    try {
        quotenumber = localStorage.getItem("keyData");
        ApproveDesc = $("#PREVIEW_APPROVAL_BODY textarea").val();
        try{
            AllParams ={}
            for (const [key, value] of Object.entries(dict)) {
                if (value.includes("<img")) {
                    val = value.split(">")[1]
                } else {
                    val = value
                }
                AllParams[key] = val
            }
            AllParams = JSON.stringify(AllParams);
        }
        catch(e){
            AllParams = JSON.stringify(dict);
        }        
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "BULKREJECT",
            'AllParams': AllParams,
            'QuoteNumber': quotenumber,
            'ApproveDesc': ApproveDesc,            
        }, function (dataset) {
            $("#BTN_MA_ALL_REFRESH").click();
        });
    } catch (e) {
        console.log(e)
    }
}
//A043S001P01-13245 end
function ChangePreview() {
    if ($('#listPreview').is(":visible")) {
        $('#div_CTR_PRE_view').show();
        $('#listPreview').hide();

    } else {
        $('#div_CTR_PRE_view').hide();
        $('#listPreview').show();
    }

}
function ChangeViewOption() {
    if ($('#Tabler_view').is(":visible")) {
        $('#div_CTR_Table_view').show();
        $('#Tabler_view').hide();

    } else {
        $('#div_CTR_Table_view').hide();
        $('#Tabler_view').show();
    }
}
function ProductDetailview(ele) {
    MaterialId = $(ele).closest('.product-box').find('#materialid').text();
    ProdDesc = $(ele).closest('.product-box').find('#product_desc').text();
    try {
        cpq.server.executeScript("ACCRTABAQU", {
            'Action': 'ProductDetail',
            'MaterilId': MaterialId
        }, function (data) {
            $("#ProddetailBreadcrumb ul").append('<li><span class="angle_symbol"> / </span></li><li class="active">' + ProdDesc + '</li>');
            $('#Right_div_CTR_Countries').html(data);
        });
    } catch (e) {
        console.log(e);
    }
}
function cattreeparamfunction(CurrentNodeId, level) {
    Curlevel = level;
    var cur_id = $('#Categtreeview').treeview('getParent', CurrentNodeId).nodeId;
    if (cur_id != undefined) {
        cur_key = "TreeParentLevel" + Curlevel
        Categorydict[cur_key] = $('#Categtreeview').treeview('getNode', cur_id).text;
        Curlevel += 1
        cattreeparamfunction(cur_id, Curlevel)
    }
    return Categorydict
}
function productcountchange() {
    var pagecount = document.getElementById("productperpage").value;
    CurrentNodeId = localStorage.getItem("SecTreeCurrentNodeId");
    node = $('#Categtreeview').treeview('getNode', CurrentNodeId);
    CurrentNodeId = node.nodeId;
    var childrenNodes = _getChildren(node);
    if (childrenNodes.length > 0) {
        child = 'true';
    } else {
        child = 'false';
    }
    if (child == 'true') {
        Current_type = "Parent";
        CurrentRecordId = node.CurrentId;
    } else {
        Current_type = "current";
        CurrentRecordId = node.id;
    }

    CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
    TreeParam = node.text;
    if (TreeParam.includes("<img")) {
        TreeParam = Treeparamval .split(">")
		treeparam = TreeParam[TreeParam.length -1]
    } else {
        TreeParam = TreeParam
    }
    localStorage.setItem('Rel_List_Rec_ID', CurrentRecordId);
    localStorage.setItem('SecTreeCurrentNodeId', CurrentNodeId);
    $('#Categtreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
        silent: true
    }
    ]);
    wherecondition = "Where 1=1"
    if (dict['TreeParentLevel0'] == 'Country Catalogs') {
        treeparam = dict['TreeParam']
        if (treeparam.includes("<img")) {
			TreeParam = Treeparamval .split(">")
			treeparam = TreeParam[TreeParam.length -1]
        } else {
            treeparam = treeparam
        }
        wherecondition = "Where c.COUNTRY = '" + treeparam + "'";
    } else if (dict['TreeParentLevel1'] == 'Country Catalogs') {
        treeparam = dict['TreeParam']
        if (treeparam.includes("<img")) {
            TreeParam = Treeparamval .split(">")
			treeparam = TreeParam[TreeParam.length -1]
        } else {
            treeparam = treeparam
        }
        wherecondition = "Where c.COUNTRY = '" + dict['TreeParentLevel0'] + "' and c.PROGRAM_ID = '" + treeparam + "'";
    } else if (dict['TreeParentLevel2'] == 'Country Catalogs') {
        treeparam = dict['TreeParam']
        if (treeparam.includes("<img")) {
            TreeParam = Treeparamval .split(">")
			treeparam = TreeParam[TreeParam.length -1]
        } else {
            treeparam = treeparam
        }
        wherecondition = "Where c.COUNTRY = '" + dict['TreeParentLevel1'] + "' and c.PROGRAM_ID = '" + dict['TreeParentLevel0'] + "' and c.SEGREVPRGAWDLVL_ID = '" + treeparam + "' ";
    } else if (dict['TreeParentLevel3'] == 'Country Catalogs') {
        treeparam = dict['TreeParam']
        if (treeparam.includes("<img")) {
            TreeParam = Treeparamval .split(">")
			treeparam = TreeParam[TreeParam.length -1]
        } else {
            treeparam = treeparam
        }
        wherecondition = "Where c.COUNTRY = '" + dict['TreeParentLevel2'] + "' and c.PROGRAM_ID = '" + dict['TreeParentLevel1'] + "' and c.SEGREVPRGAWDLVL_ID = '" + dict['TreeParentLevel0'] + "' and c.SEGREVPRGAWDLVLGRP_ID = '" + treeparam + "'";
    }

    cpq.server.executeScript("ACCRTABAQU", {
        'Action': 'PoductDetails',
        'RecoedId': CurrentRecordId,
        'wherecondition': wherecondition,
        'Current_type': Current_type,
        'PerPage': pagecount,
        'startPage': '',
        'endPage': ''
    }, function (dataset) {
        ProducDetails = dataset[0];
        PaginationDetail = dataset[1];
        PaginationUI = dataset[2];
        $('#Right_div_CTR_Countries').css('display', 'block');
        if (document.getElementById('Right_div_CTR_Countries')) {
            document.getElementById('Right_div_CTR_Countries').innerHTML = ProducDetails;
            document.getElementById('paginationdetails').innerHTML = PaginationDetail;
            document.getElementById('productperpage').value = pagecount;
            eval(PaginationUI);
            $("#Right_div_CTR_Countries").append('<div class="row"> <div class="col-md-12"> <div class="col2_5">Privacy Policy</div> <div class="col2_5">Contact US</div> <div class="col2_5">Product Warranty</div> <div class="col2_5">Help</div> <div class="col2_5">Order History</div> </div> <div class="col-md-12 reserved"><p class=" footer__trademark">Â© O.C. Tanner All Rights Reserved</p></div> </div>');
        }
    });
}
function CategoryRightSide(ids) {
    var pagecount = ''
    if (document.getElementById("productperpage")) {
        pagecount = document.getElementById("productperpage").value;
    }
    CurrentNodeId = localStorage.getItem("SecTreeCurrentNodeId");
    if (CurrentNodeId != ' ') {
        node = $('#Categtreeview').treeview('getNode', CurrentNodeId);
        CurrentNodeId = node.nodeId
        var childrenNodes = _getChildren(node);
        if (childrenNodes.length > 0) {
            child = 'true';
        } else {
            child = 'false';
        }
        if (child == 'true') {
            Current_type = "Parent";
            CurrentRecordId = node.CurrentId;
        } else {
            Current_type = "current";
            CurrentRecordId = node.id;
        }
        TreeParam = node.text;
        if (TreeParam.includes("<img")) {
            TreeParam = Treeparamval .split(">")
			treeparam = TreeParam[TreeParam.length -1]
        } else {
            TreeParam = TreeParam
        }
        localStorage.setItem('Rel_List_Rec_ID', CurrentRecordId)
        localStorage.setItem('SecTreeCurrentNodeId', CurrentNodeId);
        $('#Categtreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
            silent: true
        }
        ]);
    } else {
        CurrentRecordId = ' '
        Current_type = 'AllProduct'
    }
    wherecondition = "Where 1=1"
    cpq.server.executeScript("ACCRTABAQU", {
        'Action': 'PoductDetails',
        'RecoedId': CurrentRecordId,
        'wherecondition': wherecondition,
        'Current_type': Current_type,
        'PerPage': pagecount,
        'startPage': '',
        'endPage': ''
    }, function (dataset) {
        ProducDetails = dataset[0];
        PaginationDetail = dataset[1];
        PaginationUI = dataset[2];
        if (document.getElementById('Right_div_CTR_Countries')) {
            document.getElementById('Right_div_CTR_Countries').innerHTML = ProducDetails;
            document.getElementById('paginationdetails').innerHTML = PaginationDetail;
            document.getElementById('productperpage').value = pagecount;
            $('#Right_div_CTR_Countries').append('<div class="row"> <div class="col-md-12"> <div class="col2_5">Privacy Policy</div> <div class="col2_5">Contact US</div> <div class="col2_5">Product Warranty</div> <div class="col2_5">Help</div> <div class="col2_5">Order History</div> </div> <div class="col-md-12 reserved"><p class=" footer__trademark">Â© O.C. Tanner All Rights Reserved</p></div> </div>')
            eval(PaginationUI);
        }
    });
}
function CategoryLeftTreeView() {
    try {
        var id = 'Categtreeview';
        $("#div_CTR_Catalog_Products").html('<div id = "div_CTR_Table_view" style = "display:none"></div><div id ="Tabler_view"s tyle = "display:block"><div class="row" id="ProddetailBreadcrumb" style="display: block;"></div><div class="control treeview cust_cate_list col-md-3" id="catlefttreeview" style="display: block;"><div class="row allprdlist"><h3 onclick="DisplayAllProducts()" style=" cursor: pointer; " >All Products</h3></div><div id ="Categtreeview" class = "row treeview"></div></div><div id="Right_div_CTR_Countries" class ="col-md-8"></div></div>');
        if ($("#FirstSecInformation").find(".fullviewdiv").length == 0) {
            $("#FirstSecInformation").append('<div class="fullviewdiv flt_rt" style="display: block;"> <a href="#" onclick="fullview()" class="Clkfull_view" style="display: inline;"><img src="../mt/OCTANNER_DEV/Additionalfiles/Minimize.svg" class="" height="18px"></a> <a href="#" onclick="closefullview()" class="closeview" style="display: none;"><img src="/mt/OCTANNER_DEV/Additionalfiles/minus_minimize.svg" class="" height="18px"></a> </div><div class="fullviewdiv flt_rt" style="display: block;"> <a href="#" onclick="ChangeViewOption()" class="Clkfull_view" style="display: inline;margin-right: 12px;"><img src="/mt/OCTANNER_DEV/Additionalfiles/swapwindow.svg" class="" height="18px"></a></div>')
        } else {
            $(".fullviewdiv").css("display", "block");
        }
        Json_dict = JSON.stringify(dict)
        wherecondition = "1=1"
        if (dict['TreeParentLevel0'] == 'Country Catalogs') {
            treeparam = dict['TreeParam']
            if (treeparam.includes("<img")) {
                TreeParam = Treeparamval .split(">")
				treeparam = TreeParam[TreeParam.length -1]
            } else {
                treeparam = treeparam
            }
            wherecondition = "a.COUNTRY = '" + treeparam + "'";
        } else if (dict['TreeParentLevel1'] == 'Country Catalogs') {
            treeparam = dict['TreeParam']
            if (treeparam.includes("<img")) {
                TreeParam = Treeparamval .split(">")
				treeparam = TreeParam[TreeParam.length -1]
            } else {
                treeparam = treeparam
            }
            wherecondition = "a.COUNTRY = '" + dict['TreeParentLevel0'] + "' and a.PROGRAM_ID = '" + treeparam + "'";
        } else if (dict['TreeParentLevel2'] == 'Country Catalogs') {
            treeparam = dict['TreeParam']
            if (treeparam.includes("<img")) {
                TreeParam = Treeparamval .split(">")
				treeparam = TreeParam[TreeParam.length -1]
            } else {
                treeparam = treeparam
            }
            wherecondition = "a.COUNTRY = '" + dict['TreeParentLevel1'] + "' and a.PROGRAM_ID = '" + dict['TreeParentLevel0'] + "' and a.SEGREVPRGAWDLVL_ID = '" + treeparam + "' ";
        } else if (dict['TreeParentLevel3'] == 'Country Catalogs') {
            treeparam = dict['TreeParam']
            if (treeparam.includes("<img")) {
                TreeParam = Treeparamval .split(">")
				treeparam = TreeParam[TreeParam.length -1]
            } else {
                treeparam = treeparam
            }
            wherecondition = "a.COUNTRY = '" + dict['TreeParentLevel2'] + "' and a.PROGRAM_ID = '" + dict['TreeParentLevel1'] + "' and a.SEGREVPRGAWDLVL_ID = '" + dict['TreeParentLevel0'] + "' and a.SEGREVPRGAWDLVLGRP_ID = '" + treeparam + "'";
        }
        cpq.server.executeScript("SYULODTREE", {
            'LOAD': 'CategoryTreeload',
            'values': Json_dict,
            'wherecondition': wherecondition
        }, function (dataset) {
            data = dataset[0];
            data1 = dataset[1];
            $('#Categtreeview').treeview({
                data: data,
                levels: 1,
                onNodeSelected: function (event, node) {
                    CurrentNodeId = node.nodeId;
                    localStorage.setItem("SecTreeCurrentNodeId", CurrentNodeId);
                    $(this).treeview('unselectNode', [node.nodeId, {
                        silent: false
                    }
                    ]);
                    try {
                        add_new_load = localStorage.getItem("add_new_load");
                        CurrentNodeId = parseInt(localStorage.getItem("SecTreeCurrentNodeId"));
                        if (CurrentNodeId != '' && CurrentNodeId != null) {
                            CurrentId = CurrentNodeId;
                        } else {
                            CurrentId = 0;
                            localStorage.setItem('CurrentNodeId', 0);
                        }
                        if (add_new_load == 'true') {
                            //console.log('not select................');
                        } else {
                            $('#Categtreeview').treeview('selectNode', [parseInt(CurrentId), {
                                silent: true
                            }
                            ]);
                        }
                        Categorydict = {}
                        Categorydict['TreeParam'] = $('#Categtreeview').treeview('getNode', CurrentNodeId).text;
                        AllTreeParam = cattreeparamfunction(CurrentNodeId, 0);
                        Josn_dict = JSON.stringify(Categorydict);

                        var unique_breadcrumb_list = [];
                        for (var k in AllTreeParam)
                            unique_breadcrumb_list.push(k);
                        var build_breadcrumb = '<ul class="breadcrumb"><li><a class="pad0_lft30" onclick = "DisplayAllProducts()">All Products</a></li>'
                        $(unique_breadcrumb_list.reverse()).each(function (index) {
                            build_breadcrumb += '<li><a onclick="CategorybreadCrumb_redirection(this)">';
                            build_breadcrumb += AllTreeParam[unique_breadcrumb_list[index]];
                            build_breadcrumb += '</a><span class="angle_symbol"> / </span></li>'
                            build_breadcrumb += '</a></li>'
                        });
                        build_breadcrumb += '</ul>'
                        $('div#ProddetailBreadcrumb').html(build_breadcrumb);
                        $('ul.breadcrumb > li > a').each(function (index) {
                            var a = $(this).text();
                            if (a.indexOf('function(e)') != -1) {
                                $(this).parent('li').remove();
                            }
                        });
                        CategoryRightSide(id);
                    } catch (e) {
                        console.log(e);
                    }
                },
                onNodeUnselected: function (event, node) {
                    $(this).treeview('selectNode', [node.nodeId, {
                        silent: true
                    }
                    ]);
                }
            });
            try {
                add_new_load = localStorage.getItem("add_new_load");
                CurrentNodeId = localStorage.getItem("SecTreeCurrentNodeId");
                if (CurrentNodeId != '' && CurrentNodeId != null) {
                    CurrentId = parseInt(CurrentNodeId);
                } else if (CurrentNodeId == '') { }
                else {
                    CurrentNodeId = 0;
                    localStorage.setItem('CurrentNodeId', 0);
                }
                if (add_new_load == 'true') { }
                else if (localStorage.getItem("SecTreeCurrentNodeId") == ' ') {
                    console.log("All products")
                } else {
                    $('#Categtreeview').treeview('selectNode', [parseInt(CurrentId), {
                        silent: true
                    }
                    ]);
                }
                Categorydict = {}
                var build_breadcrumb = '<ul class="breadcrumb"><li><a class="pad0_lft30" onclick = "DisplayAllProducts()">All Products</a></li>'
                if (CurrentNodeId != ' ') {
                    Categorydict['TreeParam'] = $('#Categtreeview').treeview('getNode', CurrentNodeId).text;
                }
                AllTreeParam = cattreeparamfunction(CurrentNodeId, 0);
                Josn_dict = JSON.stringify(Categorydict);

                var unique_breadcrumb_list = [];
                for (var k in AllTreeParam)
                    unique_breadcrumb_list.push(k);
                $(unique_breadcrumb_list.reverse()).each(function (index) {
                    build_breadcrumb += '<li><a onclick="CategorybreadCrumb_redirection(this)">';
                    build_breadcrumb += AllTreeParam[unique_breadcrumb_list[index]];
                    build_breadcrumb += '</a><span class="angle_symbol"> / </span></li>'
                    build_breadcrumb += '</a></li>'
                });
                build_breadcrumb += '</ul>'
                $('div#ProddetailBreadcrumb').html(build_breadcrumb);
                $('ul.breadcrumb > li > a').each(function (index) {
                    var a = $(this).text();
                    if (a.indexOf('function(e)') != -1) {
                        $(this).parent('li').remove();
                    }
                });
                CategoryRightSide(id);
            } catch (e) {
                console.log(e);
            }
        });
    } catch (e) {
        console.log(e);
    }
}

function ondatatypeFieldChanges(ele) {
    val = $(ele).val()
    if (val == 'TEXT') {
        $('textarea#PICKLIST_VALUES').closest('tr').addClass('disp_none');
        $('textarea').closest('tr').hide();
        $('select#FORMULA_DATA_TYPE').closest('tr').hide();
        $('input#PICKLIST').closest('tr').hide();
        $('input#LOOKUP_API_NAME').closest('tr').hide();
        $('input#DECIMALS').closest('tr').hide();
        $('input#CONTAINER_VALUES').closest('tr').hide();
        $('input#REV_API_NAM').closest('tr').hide();
        $('input#LENGTH').closest('tr').show();
        $('textarea#PICKLIST_VALUES').closest('tr').hide();
        $('input#FORMULA_LOGIC').closest('tr').hide();
        $('input#QUERY_BUILDER_CONTROL').closest('tr').hide();
        $('input#SOURCE_DATA').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('select#REV_DATA_TYPE').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('input#CONTAINER_SQL_EXPRESSION').closest('tr').hide();
        $('input#CONTAINER_NO_OF_ROW').closest('tr').hide();
        $('input#MODUSR_RECORD_ID').closest('tr').hide();
        $('input#ADDUSR_RECORD_ID').closest('tr').hide();
        $('input#API_FIELD_NAME').closest('tr').hide();
        $('input#REV_DECIMALS').closest('tr').hide();
        $('input#REV_LENGTH').closest('tr').hide();
        $('input#LENGTH').closest('tr').show();
        $('input#CURRENCY_INDEX').closest('tr').hide();
    }
    else if (val == 'CHECKBOX') {
        $('textarea#PICKLIST_VALUES').closest('tr').addClass('disp_none');
        $('select#FORMULA_DATA_TYPE').closest('tr').hide();
        $('textarea').closest('tr').hide();
        $('input#LOOKUP_API_NAME').closest('tr').hide();
        $('input#PICKLIST').closest('tr').hide();
        $('input#LENGTH').closest('tr').hide();
        $('input#DECIMALS').closest('tr').hide();
        $('input#CONTAINER_VALUES').closest('tr').hide();
        $('input#REV_API_NAM').closest('tr').hide();
        $('input#LENGTH').closest('tr').show();
        $('textarea#PICKLIST_VALUES').closest('tr').hide();
        $('input#FORMULA_LOGIC').closest('tr').hide();
        $('input#QUERY_BUILDER_CONTROL').closest('tr').hide();
        $('input#SOURCE_DATA').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('select#REV_DATA_TYPE').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('input#CONTAINER_SQL_EXPRESSION').closest('tr').hide();
        $('input#CONTAINER_NO_OF_ROW').closest('tr').hide();
        $('input#MODUSR_RECORD_ID').closest('tr').hide();
        $('input#ADDUSR_RECORD_ID').closest('tr').hide();
        $('input#API_FIELD_NAME').closest('tr').hide();
        $('input#REV_DECIMALS').closest('tr').hide();
        $('input#REV_LENGTH').closest('tr').hide();
        $('input#CURRENCY_INDEX').closest('tr').hide();
    }
    else if ( val == 'CURRENCY') {
        $('textarea#PICKLIST_VALUES').closest('tr').addClass('disp_none');
        $('select#FORMULA_DATA_TYPE').closest('tr').hide();
        $('textarea').closest('tr').hide();
        $('input#LOOKUP_API_NAME').closest('tr').hide();
        $('input#PICKLIST').closest('tr').hide();
        $('input#LENGTH').closest('tr').hide();
        $('input#DECIMALS').closest('tr').hide();
        $('input#CONTAINER_VALUES').closest('tr').hide();
        $('input#REV_API_NAM').closest('tr').hide();
        $('input#LENGTH').closest('tr').hide();
        $('textarea#PICKLIST_VALUES').closest('tr').hide();
        $('input#FORMULA_LOGIC').closest('tr').hide();
        $('input#QUERY_BUILDER_CONTROL').closest('tr').hide();
        $('input#SOURCE_DATA').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('select#REV_DATA_TYPE').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('input#CONTAINER_SQL_EXPRESSION').closest('tr').hide();
        $('input#CONTAINER_NO_OF_ROW').closest('tr').hide();
        $('input#MODUSR_RECORD_ID').closest('tr').hide();
        $('input#ADDUSR_RECORD_ID').closest('tr').hide();
        $('input#API_FIELD_NAME').closest('tr').hide();
        $('input#REV_DECIMALS').closest('tr').hide();
        $('input#REV_LENGTH').closest('tr').hide();
        $('input#CURRENCY_INDEX').closest('tr').show();
    }

    else if (val == 'LOOKUP') {
        $('textarea#PICKLIST_VALUES').closest('tr').addClass('disp_none');
        $('input#CURRENCY_INDEX').closest('tr').hide();
        $('textarea').closest('tr').hide();
        $('select#FORMULA_DATA_TYPE').closest('tr').hide();
        $('input#LOOKUP_API_NAME').closest('tr').show();
        $('input#PICKLIST').closest('tr').hide();
        $('input#LENGTH').closest('tr').show();
        $('input#DECIMALS').closest('tr').hide();
        $('input#CONTAINER_VALUES').closest('tr').hide();
        $('input#REV_API_NAM').closest('tr').hide();
        $('input#LENGTH').closest('tr').show();
        $('textarea#PICKLIST_VALUES').closest('tr').hide();
        $('input#FORMULA_LOGIC').closest('tr').hide();
        $('input#QUERY_BUILDER_CONTROL').closest('tr').hide();
        $('input#SOURCE_DATA').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('select#REV_DATA_TYPE').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('input#CONTAINER_SQL_EXPRESSION').closest('tr').hide();
        $('input#CONTAINER_NO_OF_ROW').closest('tr').hide();
        $('input#MODUSR_RECORD_ID').closest('tr').hide();
        $('input#ADDUSR_RECORD_ID').closest('tr').hide();
        $('input#API_FIELD_NAME').closest('tr').hide();
        $('input#REV_DECIMALS').closest('tr').hide();
        $('input#REV_LENGTH').closest('tr').hide();
    }
    else if (val == 'FORMULA') {
        $('textarea#PICKLIST_VALUES').closest('tr').addClass('disp_none');
        $('input#CURRENCY_INDEX').closest('tr').hide();
        $('input#LOOKUP_API_NAME').closest('tr').hide();
        $('input#PICKLIST').closest('tr').hide();
        $('input#LENGTH').closest('tr').hide();
        $('input#DECIMALS').closest('tr').hide();
        $('input#CONTAINER_VALUES').closest('tr').hide();
        $('input#REV_API_NAM').closest('tr').hide();
        $('input#LENGTH').closest('tr').show();
        $('textarea#PICKLIST_VALUES').closest('tr').hide();
        $('input#FORMULA_LOGIC').closest('tr').show();
        $('input#QUERY_BUILDER_CONTROL').closest('tr').hide();
        $('input#SOURCE_DATA').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('select#REV_DATA_TYPE').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('input#CONTAINER_SQL_EXPRESSION').closest('tr').hide();
        $('input#CONTAINER_NO_OF_ROW').closest('tr').hide();
        $('input#MODUSR_RECORD_ID').closest('tr').hide();
        $('input#ADDUSR_RECORD_ID').closest('tr').hide();
        $('input#API_FIELD_NAME').closest('tr').hide();
        $('input#REV_DECIMALS').closest('tr').hide();
        $('input#REV_LENGTH').closest('tr').hide();
        $('select#FORMULA_DATA_TYPE').closest('tr').show();
    }
    else if (val == 'NUMBER') {
        $('textarea#PICKLIST_VALUES').closest('tr').addClass('disp_none');
        $('input#CURRENCY_INDEX').closest('tr').hide();
        $('textarea').closest('tr').hide();
        $('select#FORMULA_DATA_TYPE').closest('tr').hide();
        $('input#LOOKUP_API_NAME').closest('tr').hide();
        $('input#PICKLIST').closest('tr').hide();
        $('input#LENGTH').closest('tr').hide();
        $('input#DECIMALS').closest('tr').show();
        $('input#CONTAINER_VALUES').closest('tr').hide();
        $('input#REV_API_NAM').closest('tr').hide();
        $('input#LENGTH').closest('tr').hide();
        $('textarea#PICKLIST_VALUES').closest('tr').hide();
        $('input#FORMULA_LOGIC').closest('tr').hide();
        $('input#QUERY_BUILDER_CONTROL').closest('tr').hide();
        $('input#SOURCE_DATA').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('select#REV_DATA_TYPE').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('input#CONTAINER_SQL_EXPRESSION').closest('tr').hide();
        $('input#CONTAINER_NO_OF_ROW').closest('tr').hide();
        $('input#MODUSR_RECORD_ID').closest('tr').hide();
        $('input#ADDUSR_RECORD_ID').closest('tr').hide();
        $('input#API_FIELD_NAME').closest('tr').hide();
        $('input#REV_DECIMALS').closest('tr').hide();
        $('input#REV_LENGTH').closest('tr').hide();
    }
    else if (val == 'PICKLIST' || val =='PICKLIST (MULTI-SELECT)'){
        $('input#LOOKUP_API_NAME').closest('tr').hide();
        $('input#PICKLIST').closest('tr').show();
        $('input#LENGTH').closest('tr').show();
        $('input#DECIMALS').closest('tr').hide();
        $('input#CONTAINER_VALUES').closest('tr').hide();
        $('input#REV_API_NAM').closest('tr').hide();
        $('select#FORMULA_DATA_TYPE').closest('tr').hide();
        $('textarea#PICKLIST_VALUES').closest('tr').show();
        $('input#FORMULA_LOGIC').closest('tr').hide();
        $('input#QUERY_BUILDER_CONTROL').closest('tr').hide();
        $('input#SOURCE_DATA').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('input#CURRENCY_INDEX').closest('tr').hide();
        $('select#REV_DATA_TYPE').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('input#CONTAINER_SQL_EXPRESSION').closest('tr').hide();
        $('input#CONTAINER_NO_OF_ROW').closest('tr').hide();
        $('input#MODUSR_RECORD_ID').closest('tr').hide();
        $('input#ADDUSR_RECORD_ID').closest('tr').hide();
        $('input#API_FIELD_NAME').closest('tr').hide();
        $('input#REV_DECIMALS').closest('tr').hide();
        $('input#REV_LENGTH').closest('tr').hide();
        $('textarea#PICKLIST_VALUES').closest('tr').addClass('disp_blk');
    }
    
    
    
   
    else if (val == 'DATE'){
        $('textarea#PICKLIST_VALUES').closest('tr').addClass('disp_none');
        $('input#CURRENCY_INDEX').closest('tr').hide();
        $('input#LOOKUP_API_NAME').closest('tr').hide();
        $('textarea').closest('tr').hide();
        $('select#FORMULA_DATA_TYPE').closest('tr').hide();
        $('input#PICKLIST').closest('tr').hide();
        $('input#LENGTH').closest('tr').hide();
        $('input#DECIMALS').closest('tr').show();
        $('input#CONTAINER_VALUES').closest('tr').hide();
        $('input#REV_API_NAM').closest('tr').hide();
        $('input#LENGTH').closest('tr').show();
        $('textarea#PICKLIST_VALUES').closest('tr').hide();
        $('input#FORMULA_LOGIC').closest('tr').hide();
        $('input#QUERY_BUILDER_CONTROL').closest('tr').hide();
        $('input#SOURCE_DATA').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('select#REV_DATA_TYPE').closest('tr').hide();
        $('input#CONTAINER_TYPE').closest('tr').hide();
        $('input#CONTAINER_SQL_EXPRESSION').closest('tr').hide();
        $('input#CONTAINER_NO_OF_ROW').closest('tr').hide();
        $('input#MODUSR_RECORD_ID').closest('tr').hide();
        $('input#ADDUSR_RECORD_ID').closest('tr').hide();
        $('input#API_FIELD_NAME').closest('tr').hide();
        $('input#REV_DECIMALS').closest('tr').hide();
        $('input#REV_LENGTH').closest('tr').hide();
    }
}
function rules_field_change(ele)
{
    if(currenttab === "Product Offering"){
        if(val == 'ON SPECIFIC ATTRIBUTE VALUE CHANGE'){
        $('input#PRDOFR_ATTRIBUTE_NAME').closest('tr').show()
        $('input#PRDOFR_ATTRIBUTE_UOM').closest('tr').show();
        $('input#PRDOFR_ATTRIBUTE_DESCRIPTION').closest('tr').show();
        $('input#PRDOFR_ATTRIBUTE_HELPTEXT').closest('tr').show();
        $('input#PRDOFR_ATTRIBUTE_RANK').closest('tr').show();
        $('input#PRDOFR_ATTVAL_VALUECODE').closest('tr').show();
        $('input#PRDOFR_ATTVAL_DISPLAYVAL').closest('tr').show();
        $('input#PRDOFR_ATTVAL_VALDESCRIPTION').closest('tr').show();
        $('input#PRDOFR_ATTVAL_VALRANK').closest('tr').show();
        $('textarea#RULE_CONDITIONEXPRESSION').val('').closest('tr').addClass('hide');
        }else if(val == 'ON ANY ATTRIBUTE VALUE CHANGE'){
            $('input#PRDOFR_ATTRIBUTE_NAME').closest('tr').show()
            $('input#PRDOFR_ATTRIBUTE_UOM').closest('tr').show();
            $('input#PRDOFR_ATTRIBUTE_DESCRIPTION').closest('tr').show();
            $('input#PRDOFR_ATTRIBUTE_HELPTEXT').closest('tr').show();
            $('input#PRDOFR_ATTRIBUTE_RANK').closest('tr').show();
            $('input#PRDOFR_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTVAL_RECORD_ID').removeAttr('value');
            $('input#PRDOFR_ATTVAL_DISPLAYVAL').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTVAL_VALDESCRIPTION').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTVAL_VALRANK').removeAttr('value').closest('tr').hide();
            $('textarea#RULE_CONDITIONEXPRESSION').val('').closest('tr').addClass('hide');
        }else if(val == 'ON CUSTOM CONDITION SATISFIED'){
            $('textarea#RULE_CONDITIONEXPRESSION').closest('tr').removeClass('hide');
            $('input#PRDOFR_ATTRIBUTE_RECORD_ID').removeAttr('value');
            $('input#PRDOFR_ATTVAL_RECORD_ID').removeAttr('value');
            $('input#PRDOFR_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTRIBUTE_UOM').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTRIBUTE_DESCRIPTION').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTRIBUTE_HELPTEXT').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTRIBUTE_RANK').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTVAL_DISPLAYVAL').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTVAL_VALDESCRIPTION').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTVAL_VALRANK').removeAttr('value').closest('tr').hide();
        }
    }
    else if (currenttab === "Product Specification"){
        if(val == 'ON SPECIFIC ATTRIBUTE VALUE CHANGE'){
            $('input#PRDSPC_ATTRIBUTE_NAME').closest('tr').show()
            $('input#PRDSPC_ATTRIBUTE_UOM').closest('tr').show();
            $('input#PRDSPC_ATTRIBUTE_DESCRIPTION').closest('tr').show();
            $('input#PRDSPC_ATTRIBUTE_HELPTEXT').closest('tr').show();
            $('input#PRDSPC_ATTRIBUTE_RANK').closest('tr').show();
            $('input#PRDSPC_ATTVAL_VALUECODE').closest('tr').show();
            $('input#PRDSPC_ATTVAL_DISPLAYVAL').closest('tr').show();
            $('input#PRDSPC_ATTVAL_VALDESCRIPTION').closest('tr').show();
            $('input#PRDSPC_ATTVAL_VALRANK').closest('tr').show();
            $('textarea#RULE_CONDITIONEXPRESSION').val('').closest('tr').addClass('hide');
        }else if(val == 'ON ANY ATTRIBUTE VALUE CHANGE'){
            $('input#PRDSPC_ATTRIBUTE_NAME').closest('tr').show()
            $('input#PRDSPC_ATTRIBUTE_UOM').closest('tr').show();
            $('input#PRDSPC_ATTRIBUTE_DESCRIPTION').closest('tr').show();
            $('input#PRDSPC_ATTRIBUTE_HELPTEXT').closest('tr').show();
            $('input#PRDSPC_ATTRIBUTE_RANK').closest('tr').show();
            $('input#PRDSPC_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTVAL_RECORD_ID').removeAttr('value');
            $('input#PRDSPC_ATTVAL_DISPLAYVAL').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTVAL_VALDESCRIPTION').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTVAL_VALRANK').removeAttr('value').closest('tr').hide();
            $('textarea#RULE_CONDITIONEXPRESSION').val('').closest('tr').addClass('hide');
        }else if(val == 'ON CUSTOM CONDITION SATISFIED'){                                  
            $('textarea#RULE_CONDITIONEXPRESSION').closest('tr').removeClass('hide');
            $('input#PRDSPC_ATTRIBUTE_RECORD_ID').removeAttr('value');
            $('input#PRDSPC_ATTVAL_RECORD_ID').removeAttr('value');
            $('input#PRDSPC_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTRIBUTE_UOM').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTRIBUTE_DESCRIPTION').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTRIBUTE_HELPTEXT').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTRIBUTE_RANK').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTVAL_DISPLAYVAL').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTVAL_VALDESCRIPTION').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTVAL_VALRANK').removeAttr('value').closest('tr').hide();
        }
    }
    if(currenttab === "Product Offering"){
        $('input#PRDSPC_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
        $('input#PRDSPC_ATTRIBUTE_UOM').removeAttr('value').closest('tr').hide();
        $('input#PRDSPC_ATTVAL_VALRANK').removeAttr('value').closest('tr').hide();
        $('input#PRDSPC_ATTRIBUTE_DESCRIPTION').removeAttr('value').closest('tr').hide();
        $('input#PRDSPC_ATTRIBUTE_HELPTEXT').removeAttr('value').closest('tr').hide();
        $('input#PRDSPC_ATTRIBUTE_RANK').removeAttr('value').closest('tr').hide();
        $('input#PRDSPC_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
        $('input#PRDSPC_ATTVAL_DISPLAYVAL').removeAttr('value').closest('tr').hide();
        $('input#PRDSPC_ATTVAL_VALDESCRIPTION').removeAttr('value').closest('tr').hide();
        $('input#PRDSPC_ATTRIBUTE_RECORD_ID').removeAttr('value');
        $('input#PRDSPC_ATTVAL_RECORD_ID').removeAttr('value');
    }
    else if(currenttab === "Product Specification"){
        $('input#PRDOFR_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
        $('input#PRDOFR_ATTRIBUTE_UOM').removeAttr('value').closest('tr').hide();
        $('input#PRDOFR_ATTVAL_VALRANK').removeAttr('value').closest('tr').hide();
        $('input#PRDOFR_ATTRIBUTE_DESCRIPTION').removeAttr('value').closest('tr').hide();
        $('input#PRDOFR_ATTRIBUTE_HELPTEXT').removeAttr('value').closest('tr').hide();
        $('input#PRDOFR_ATTRIBUTE_RANK').removeAttr('value').closest('tr').hide();
        $('input#PRDOFR_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
        $('input#PRDOFR_ATTVAL_DISPLAYVAL').removeAttr('value').closest('tr').hide();
        $('input#PRDOFR_ATTVAL_VALDESCRIPTION').removeAttr('value').closest('tr').hide();
        $('input#PRDOFR_ATTRIBUTE_RECORD_ID').removeAttr('value');
        $('input#PRDOFR_ATTVAL_RECORD_ID').removeAttr('value');
    }
}
function rule_action_change(val){
    if(val == 'EXECUTE SCRIPT'){
        $('input#SCRIPT_NAME').closest('tr').show();
        $('input#SCRIPT_DESCRIPTION').closest('tr').show();
        $('input#MESSAGE_CODE').removeAttr('value').closest('tr').hide();
        $('input#MESSAGE_TEXT').removeAttr('value').closest('tr').hide();
        $('input#IS_MANDATORY').prop("checked", false).closest('tr').hide();
        if(currenttab === "Product Offering"){
            $('input#PRDOFR_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTRIBUTE_RECORD_ID').removeAttr('value');
            $('input#PRDOFR_ATTVAL_RECORD_ID').removeAttr('value');
        }
        else{
            $('input#PRDSPC_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTRIBUTE_RECORD_ID').removeAttr('value');
            $('input#PRDSPC_ATTVAL_RECORD_ID').removeAttr('value'); 
        }
    }else if(val == 'DISPLAY MESSAGE'){
        $('input#MESSAGE_CODE').closest('tr').show();
        $('input#MESSAGE_TEXT').closest('tr').show();
        $('input#IS_MANDATORY').closest('tr').show();
        $('input#SCRIPT_NAME').removeAttr('value').closest('tr').hide();
        $('input#SCRIPT_DESCRIPTION').removeAttr('value').closest('tr').hide();
        $('input#IS_VISIBLE').prop("checked", false).closest('tr').hide();
        if(currenttab === "Product Offering"){
            $('input#PRDOFR_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTRIBUTE_RECORD_ID').removeAttr('value');
            $('input#PRDOFR_ATTVAL_RECORD_ID').removeAttr('value');
        }
        else{
            $('input#PRDSPC_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTRIBUTE_RECORD_ID').removeAttr('value');
            $('input#PRDSPC_ATTVAL_RECORD_ID').removeAttr('value'); 
        }   
    }else if(val == 'SET ATTRIBUTE VALUE'){
        if(currenttab === "Product Offering"){
            $('input#PRDOFR_ATTRIBUTE_NAME').closest('tr').show();
            $('input#PRDOFR_ATTVAL_VALUECODE').closest('tr').show();
        }
        else{
            $('input#PRDSPC_ATTRIBUTE_NAME').closest('tr').show();
            $('input#PRDSPC_ATTVAL_VALUECODE').closest('tr').show();
        }
        $('input#PRDOFR_ATTVAL_VALUECODE').closest('tr').show();
        $('input#SCRIPT_NAME').removeAttr('value').closest('tr').hide();
        $('input#SCRIPT_DESCRIPTION').removeAttr('value').closest('tr').hide();
        $('input#MESSAGE_CODE').removeAttr('value').closest('tr').hide();
        $('input#MESSAGE_TEXT').removeAttr('value').closest('tr').hide();
        $('input#IS_MANDATORY').prop("checked", false).closest('tr').hide();
        $('input#IS_VISIBLE').prop("checked", false).closest('tr').hide();
    }else if(val == 'EXECUTE UI ACTION'){
        $('input#IS_VISIBLE').closest('tr').show();
        $('input#SCRIPT_NAME').removeAttr('value').closest('tr').hide();
        $('input#SCRIPT_DESCRIPTION').removeAttr('value').closest('tr').hide();
        $('input#MESSAGE_CODE').removeAttr('value').closest('tr').hide();
        $('input#MESSAGE_TEXT').removeAttr('value').closest('tr').hide();
        $('input#IS_MANDATORY').prop("checked", false).closest('tr').hide();
        if(currenttab === "Product Offering"){
            $('input#PRDOFR_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTRIBUTE_RECORD_ID').removeAttr('value');
            $('input#PRDOFR_ATTVAL_RECORD_ID').removeAttr('value');
        }
        else{
            $('input#PRDSPC_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTRIBUTE_RECORD_ID').removeAttr('value');
            $('input#PRDSPC_ATTVAL_RECORD_ID').removeAttr('value'); 
        } 
    }else if(val == 'ABORT ACTION'){
        $('input#IS_VISIBLE').prop("checked", false).closest('tr').hide();
        $('input#SCRIPT_NAME').removeAttr('value').closest('tr').hide();
        $('input#SCRIPT_DESCRIPTION').removeAttr('value').closest('tr').hide();
        $('input#MESSAGE_CODE').removeAttr('value').closest('tr').hide();
        $('input#MESSAGE_TEXT').removeAttr('value').closest('tr').hide();
        $('input#IS_MANDATORY').prop("checked", false).closest('tr').hide();
        if(currenttab === "Product Offering"){
            $('input#PRDOFR_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDOFR_ATTRIBUTE_RECORD_ID').removeAttr('value');
            $('input#PRDOFR_ATTVAL_RECORD_ID').removeAttr('value');
        }
        else{
            $('input#PRDSPC_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
            $('input#PRDSPC_ATTRIBUTE_RECORD_ID').removeAttr('value');
            $('input#PRDSPC_ATTVAL_RECORD_ID').removeAttr('value'); 
        }
    }
    if(currenttab === "Product Offering"){
        $('input#PRDSPC_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
        $('input#PRDSPC_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
        $('input#PRDSPC_ATTRIBUTE_RECORD_ID').removeAttr('value');
        $('input#PRDSPC_ATTVAL_RECORD_ID').removeAttr('value');
    }
    else{
        $('input#PRDOFR_ATTRIBUTE_NAME').removeAttr('value').closest('tr').hide();
        $('input#PRDOFR_ATTVAL_VALUECODE').removeAttr('value').closest('tr').hide();
        $('input#PRDOFR_ATTRIBUTE_RECORD_ID').removeAttr('value');
        $('input#PRDOFR_ATTVAL_RECORD_ID').removeAttr('value'); 
    }
}
function oncheckchange(ele){
	currentattr = $(ele).attr('id')
	if (currentattr == 'REQUIRE_EXPLICIT_APPROVAL'){
	    $('input#ENABLE_SMARTAPPROVAL').not(this).prop('checked', false); 
	}	
	else {	    
	    $('input#REQUIRE_EXPLICIT_APPROVAL').not(this).prop('checked', false);
	}
}
function onFieldChanges(ele) {
    val = $(ele).val()
    if (val == undefined) {
        val = $('select#APPROVER_SELECTION_METHOD').val(); 
        if ( val == undefined){
            val = $('select#ACTION_TYPE').val();
        }
        if ( val == undefined){
            val = $('select#RULE_EXECUTION').val();
        }
    }
    // A043S001P01-11642 start
    if (val == undefined || val == ' ') {
        val = $('select#ITM_TYPE').val();
        val = $('select#ACTION_TYPE').val();
        val = $('select#DATATYPE').val();
    }
    // if (val == 'PRODUCT OFFERING') {
    //     $('input#ITM_SAP_PARTNERNUMBER').closest('tr').hide();
    //     $('input#ITM_SAP_DESCRIPTION').closest('tr').hide();
    //     $('input#ITM_PRDOFR_ID').closest('tr').show();
    //     $('input#ITM_PRDOFR_NAME').closest('tr').show();
    // } else if ((val == 'PART') || (val == 'PRODUCT')) {
    //     $('input#ITM_SAP_PARTNERNUMBER').closest('tr').show();
    //     $('input#ITM_SAP_DESCRIPTION').closest('tr').show();
    //     $('input#ITM_PRDOFR_ID').closest('tr').hide();
    //     $('input#ITM_PRDOFR_NAME').closest('tr').hide();
    // }
    if(val == 'EXECUTE SCRIPT' || val == 'DISPLAY MESSAGE' || val == 'SET ATTRIBUTE VALUE' || val == 'EXECUTE UI ACTION' || val == 'ABORT ACTION'){
        rule_action_change(val);
    }
        else if (val == 'ON SPECIFIC ATTRIBUTE VALUE CHANGE' || val == 'ON ANY ATTRIBUTE VALUE CHANGE' || val == 'ON CUSTOM CONDITION SATISFIED'){
            rules_field_change(val);
        }
        else if (val == 'PICKLIST' || val == 'PICKLIST MULTI-SELECT') {
            $('textarea#PICKLIST_VALUES').closest('tr').show();
            $('input#LENGTH').closest('tr').hide();
            $('input#DECIMAL_PLACES').closest('tr').hide();
            $('div .B49C97AD-981D-4632-9D1D-E036E7232945').hide();
            $('input#MIN_TABLEROWS').closest('tr').hide();
            $('input#MAX_TABLEROWS').closest('tr').hide();
            $('input#PAGE_TABLEROWS').closest('tr').hide();
            $('input#ADD_TABLEROW').closest('tr').hide();
            $('input#EDIT_TABLEROW').closest('tr').hide();
            $('input#CLONE_TABLEROW').closest('tr').hide();
            $('input#DELETE_TABLEROW').closest('tr').hide();
        } else if (val == 'NUMBER' || val == 'CURRENCY' || val == 'PERCENT') {
            $('input#DECIMAL_PLACES').closest('tr').show();
            $('input#LENGTH').closest('tr').show();
            $('textarea#PICKLIST_VALUES').closest('tr').addClass('hide');
            $('div .B49C97AD-981D-4632-9D1D-E036E7232945').hide();
            $('input#MIN_TABLEROWS').closest('tr').hide();
            $('input#MAX_TABLEROWS').closest('tr').hide();
            $('input#PAGE_TABLEROWS').closest('tr').hide();
            $('input#ADD_TABLEROW').closest('tr').hide();
            $('input#EDIT_TABLEROW').closest('tr').hide();
            $('input#CLONE_TABLEROW').closest('tr').hide();
            $('input#DELETE_TABLEROW').closest('tr').hide();
        }
        else if (val == 'TEXT' || val == 'PHONE' || val == 'EMAIL' || val == "TEXT AREA LONG" || val == "TEXT AREA RICH") {
            $('input#LENGTH').closest('tr').show();
            $('input#DECIMAL_PLACES').closest('tr').hide();
            $('textarea#PICKLIST_VALUES').closest('tr').addClass('hide');
            $('div .B49C97AD-981D-4632-9D1D-E036E7232945').hide();
            $('input#MIN_TABLEROWS').closest('tr').hide();
            $('input#MAX_TABLEROWS').closest('tr').hide();
            $('input#PAGE_TABLEROWS').closest('tr').hide();
            $('input#ADD_TABLEROW').closest('tr').hide();
            $('input#EDIT_TABLEROW').closest('tr').hide();
            $('input#CLONE_TABLEROW').closest('tr').hide();
            $('input#DELETE_TABLEROW').closest('tr').hide();
        }
        else if (val == 'TABLE') {
            $('div .B49C97AD-981D-4632-9D1D-E036E7232945').show();
            $('textarea#PICKLIST_VALUES').closest('tr').addClass('hide');
            $('input#DECIMAL_PLACES').closest('tr').hide();
            $('input#LENGTH').closest('tr').hide();
            $('input#MIN_TABLEROWS').closest('tr').show();
            $('input#MAX_TABLEROWS').closest('tr').show();
            $('input#PAGE_TABLEROWS').closest('tr').show();
            $('input#ADD_TABLEROW').closest('tr').show();
            $('input#EDIT_TABLEROW').closest('tr').show();
            $('input#CLONE_TABLEROW').closest('tr').show();
            $('input#DELETE_TABLEROW').closest('tr').show();
        }
        else {
            $('input#LENGTH').closest('tr').hide();
            $('input#DECIMAL_PLACES').closest('tr').hide();
            $('textarea#PICKLIST_VALUES').closest('tr').addClass('hide');
            $('div .B49C97AD-981D-4632-9D1D-E036E7232945').hide();
            $('input#MIN_TABLEROWS').closest('tr').hide();
            $('input#MAX_TABLEROWS').closest('tr').hide();
            $('input#PAGE_TABLEROWS').closest('tr').hide();
            $('input#ADD_TABLEROW').closest('tr').hide();
            $('input#EDIT_TABLEROW').closest('tr').hide();
            $('input#CLONE_TABLEROW').closest('tr').hide();
            $('input#DELETE_TABLEROW').closest('tr').hide();
        }
    
    // A043S001P01-11642 end
    role_val = $('input#ROLE_ID').val();
    profile_val = $('input#PROFILE_ID').val();
    if (val == 'INDIVIDUAL USERS') {
        $('textarea#CUSTOM_QUERY').closest('tr').hide();
        $('input#ROLE_ID').closest('tr').hide();
        $('input#PROFILE_ID').closest('tr').hide();
        //$('input#UNANIMOUS_CONSENT').closest('tr').hide();
        $('input#USERNAME').closest('tr').show();
        if (localStorage.getItem("ApproverAddNew")=="true"){
            $('input#USERNAME').removeAttr('disabled');
        }               
        $('textarea#CUSTOM_QUERY').attr('disabled', 'disabled');
        $("input#ROLE_ID").val("");
	    $('input#PROFILE_ID').val("");        
        $('textarea#CUSTOM_QUERY').val(""); 
    } else if (val == 'GROUP OF USERS') {
        if (role_val != "") {
            $('textarea#CUSTOM_QUERY').closest('tr').hide();
            //$('input#UNANIMOUS_CONSENT').closest('tr').show();
            $('input#ROLE_ID').closest('tr').show();
            $('input#PROFILE_ID').closest('tr').show();
            $('input#PROFILE_ID').css('display', 'none');
	        $('input#PROFILE_ID').closest('td').find('input:nth-child(2)').css('display','none');
            $('input#USERNAME').closest('tr').hide();
            $('input#USERNAME').val("");
            $('textarea#CUSTOM_QUERY').val(""); 
        } else if (profile_val != "") {
            $('textarea#CUSTOM_QUERY').closest('tr').hide();
            //$('input#UNANIMOUS_CONSENT').closest('tr').show();
            $('input#ROLE_ID').closest('tr').show();
            $('input#ROLE_ID').css('display', 'none');
	        $('input#ROLE_ID').closest('td').find('input:nth-child(2)').css('display','none');
            $('input#PROFILE_ID').closest('tr').show();
            $('input#USERNAME').closest('tr').hide();
            $('input#USERNAME').val("");
            $('textarea#CUSTOM_QUERY').val(""); 
        } else {
            $('textarea#CUSTOM_QUERY').closest('tr').hide();
            //$('input#UNANIMOUS_CONSENT').closest('tr').show();
            $('input#USERNAME').closest('tr').hide();
            $('input#ROLE_ID').closest('tr').show();
            if (localStorage.getItem("ApproverAddNew")=="true"){
                $('input#ROLE_ID').removeAttr('disabled');
            }  
            $('input#ROLE_ID').css('display','block');
	        $('input#ROLE_ID').closest('td').find('input:nth-child(2)').css('display','inline-block');
            $('input#PROFILE_ID').closest('tr').show();
            if (localStorage.getItem("ApproverAddNew")=="true"){
                $('input#PROFILE_ID').removeAttr('disabled');
            }  
            $('input#PROFILE_ID').css('display','block');
	        $('input#PROFILE_ID').closest('td').find('input:nth-child(2)').css('display','inline-block');
            $('input#USERNAME').val("");
            $('textarea#CUSTOM_QUERY').val(""); 
        }
        // $('input#USERNAME').closest('tr').hide();
        // $('input#UNANIMOUS_CONSENT').closest('tr').hide();
        // $('textarea#CUSTOM_QUERY').closest('tr').hide();
        // $('textarea#CUSTOM_QUERY').attr('disabled', 'disabled');
    } else if (val == 'CUSTOM QUERY') {
        $('textarea#CUSTOM_QUERY').closest('tr').show();        
        $('textarea#CUSTOM_QUERY').removeAttr('disabled');
        $('input#USERNAME').attr('disabled', 'disabled');
        //$('input#UNANIMOUS_CONSENT').closest('tr').show();
        $('input#USERNAME').closest('tr').hide();
        $('input#ROLE_ID').closest('tr').hide();
        $('input#PROFILE_ID').closest('tr').hide();
        $("input#ROLE_ID").val("");
	    $('input#PROFILE_ID').val("");
        $('input#USERNAME').val("");             
    }else if (val == 'Select'){
        $('textarea#CUSTOM_QUERY').closest('tr').hide();        
        //$('textarea#CUSTOM_QUERY').removeAttr('disabled');        
        //$('input#UNANIMOUS_CONSENT').closest('tr').hide();
        $('input#USERNAME').closest('tr').hide();
        //$('input#USERNAME').removeAttr('disabled');
        $('input#ROLE_ID').closest('tr').hide();
        $('input#PROFILE_ID').closest('tr').hide();
        $("input#ROLE_ID").val("");
	    $('input#PROFILE_ID').val("");
        $('input#USERNAME').val("");
        $('textarea#CUSTOM_QUERY').val("");         
    }
}
function configure_revisions() {
    try {
        quotenumber = localStorage.getItem("keyData");
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "GET_SEGMENT_ID",
            'QuoteNumber': quotenumber
        }, function (data) {
            if (data != '') {
                localStorage.setItem("AP_CTR_Clicked", data);
            }
        });
    } catch (e) {
        console.log(e);
    }
}
function DisplayAllProducts() {
    CurrentRecordId = ' '
    Current_type = 'AllProduct'
    wherecondition = "Where 1=1"
    var pagecount = ''
    if (document.getElementById("productperpage")) {
        pagecount = document.getElementById("productperpage").value;
    }
    $('#Categtreeview').treeview('unselectNode', [parseInt(CurrentNodeId), {
        silent: true
    }
    ]);
    var build_breadcrumb = '<ul class="breadcrumb"><li><a class="pad0_lft30" onclick = "DisplayAllProducts()">All Products</a></li>'
    build_breadcrumb += '</ul>'
    $('div#ProddetailBreadcrumb').html(build_breadcrumb);
    localStorage.setItem("SecTreeCurrentNodeId", ' ');
    cpq.server.executeScript("ACCRTABAQU", {
        'Action': 'PoductDetails',
        'RecoedId': CurrentRecordId,
        'wherecondition': wherecondition,
        'Current_type': Current_type,
        'PerPage': pagecount,
        'startPage': '',
        'endPage': ''
    }, function (dataset) {
        ProducDetails = dataset[0]; PaginationDetail = dataset[1]; PaginationUI = dataset[2];
        if (document.getElementById('Right_div_CTR_Countries')) {
            document.getElementById('Right_div_CTR_Countries').innerHTML = ProducDetails;
            document.getElementById('paginationdetails').innerHTML = PaginationDetail;
            document.getElementById('productperpage').value = pagecount;
            $('#Right_div_CTR_Countries').append('<div class="row"> <div class="col-md-12"> <div class="col2_5">Privacy Policy</div> <div class="col2_5">Contact US</div> <div class="col2_5">Product Warranty</div> <div class="col2_5">Help</div> <div class="col2_5">Order History</div> </div> <div class="col-md-12 reserved"><p class=" footer__trademark">Â© O.C. Tanner All Rights Reserved</p></div> </div>')
            eval(PaginationUI);
        }
    });
}

function ApprovalCommentEdit(ele) {
    try {
        RecordId = $(ele).attr("id");
        try{
            AllParams ={}
            for (const [key, value] of Object.entries(dict)) {
                if (value.includes("<img")) {
                    val = value.split(">")[1]
                } else {
                    val = value
                }
                AllParams[key] = val
            }
            AllParams = JSON.stringify(AllParams);
        }
        catch(e){
            AllParams = JSON.stringify(dict);
        } 
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "EDIT_COMMENT",
            'AllParams': AllParams,
            'QuoteNumber': RecordId
        }, function (dataset) {
            $('#preview_approval #PREVIEW_APPROVAL_CONTENT').html(dataset);
        });
    } catch (e) {
        console.log(e);
    }
}

function ApprovalCommentView(ele) {
    try {
        RecordId = $(ele).attr("id");
        try{
            AllParams ={}
            for (const [key, value] of Object.entries(dict)) {
                if (value.includes("<img")) {
                    val = value.split(">")[1]
                } else {
                    val = value
                }
                AllParams[key] = val
            }
            AllParams = JSON.stringify(AllParams);
        }
        catch(e){
            AllParams = JSON.stringify(dict);
        } 
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "VIEW_COMMENT",
            'AllParams': AllParams,
            'QuoteNumber': RecordId
        }, function (dataset) {
            $('#preview_approval #PREVIEW_APPROVAL_CONTENT').html(dataset);
        });
    } catch (e) {
        console.log(e);
    }
}

function SaveApproverComment(RecordId) {
    try {
        RecipientComment = $("textarea#RecipientComment").val();
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "SAVE_COMMENT",
            'QuoteNumber': RecordId,
            'RecipientComment': RecipientComment
        }, function (dataset) {
            $("#BTN_MA_ALL_REFRESH").click();
        });
    } catch (e) {
        console.log(e);
    }
}
function EailSectionEdit(ele) {
    getId = $(ele).attr('id')
    getbindId = $(ele).closest('li').attr('id')
    $(ele).closest("#ctr_drop").hide();
    getbindIdsplit = getbindId.split('_')
    $("#sec_" + getId + " .jqx-editor-content iframe").on("load", function () {
        let head = $("#sec_" + getId + " .jqx-editor-content iframe").contents().find("head");
        let css = '<style>html,body{height: 100% !important;} body{background-color: lightyellow;}</style>';
        $(head).append(css);
    });
    $('#' + getbindIdsplit[1]).jqxEditor({
        height: "350px !important",
        disabled: false
    });
    let head = $("#sec_" + getId + " .jqx-editor-content iframe").contents().find("head");
    let css = '<style>html,body{height: 100% !important;} body{background-color: lightyellow;}</style>';
    $(head).append(css);
    $("." + getId).append('<div  id = "sctionactionbuttons" class="g4 sec_' + getId + ' collapse in except_sec removeHorLine iconhvr sec_edit_sty"><button id="' + getbindIdsplit[1] + '__' + getId + '"  class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="EailSectionCancel(this)">CANCEL</button><button id="' + getbindIdsplit[1] + '__' + getId + '" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="EailSectionSave(this)">SAVE</button></div>');
    $("." + getId).addClass("SEC_EDIT_ARROW")
    $("." + getId).css({ "margin-top": "10px", "box-shadow": "1px 0px 8px -1px grey", "padding-bottom": "40px", "padding": "10px", "border-radius": "4px" })
    setTimeout(function(){$(ele).closest('#ctr_drop').click() }, 1500);
}
function EailSectionCancel(ele) {
    Common_Tabs('<span><</span>','Approvalstep_Email')
}
function EailSectionSave(ele) {
    getbindId = $(ele).attr('id')
    getbindIdsplit = getbindId.split('__')
    $('#' + getbindIdsplit[0]).jqxEditor({
        height: "350px !important",
        disabled: true
    });
    getmailbody = $('#' + getbindIdsplit[0]).val();
    cpq.server.executeScript("ACACSEMLBD", { 'Action': 'SecEmailContentsave', 'CurrentRecordId': getbindIdsplit[1], "emailbody": getmailbody }, function (dataset) {
        Common_Tabs('<span><</span>','Approvalstep_Email')
    });
}

function submit_comment(){
    //if (mode != 'lookup'){
        //localStorage.setItem('Action_Text_new','');
    //}
    localStorage.setItem('btn_txt_val','SAVE');
    localStorage.setItem("Action_Text_new", "SAVE");
    localStorage.setItem("bannerContentValueReset",'1')
    $('#textinformation').css('display', 'none');  
    if (TabName != "Approval Chain"){     
        try {
            RecordId = localStorage.getItem("keyData");
            try{
                AllParams ={}
                for (const [key, value] of Object.entries(dict)) {
                    if (value.includes("<img")) {
                        val = value.split(">")[1]
                    } else {
                        val = value
                    }
                    AllParams[key] = val
                }
                AllParams = JSON.stringify(AllParams);
            }
            catch(e){
                AllParams = JSON.stringify(dict);
            } 
            
            cpq.server.executeScript("ACSECTACTN", {
                'ACTION': "SUBMIT_COMMENT",
                'AllParams': AllParams,
                'QuoteNumber': RecordId
            }, function (dataset) {
                $('#SUBMIT_MODAL_SECTION #VIEW_DIV_ID').html(dataset);
				$('#SUBMIT_MODAL_SECTION #VIEW_DIV_ID').css("display","block");
            });
        } catch (e) {
            console.log(e);
        }
    }
}

function approve_request(ele){
    try {
        // Showing approve/reject in list grid starts	
        var get_tab_value = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text().toUpperCase();

        var tab_array = ["MY APPROVAL QUEUE","QUOTES","TEAM APPROVAL QUEUE"]
        if ($(ele).attr('class').includes('grid_approval') && (tab_array.indexOf(get_tab_value) != -1)){
            var dict_approval ={}
            RecordId = TransactionId = $(ele).attr('id');
            dict_approval['TreeParam'] = 'Approvals'
            AllParams = JSON.stringify(dict_approval);
            localStorage.setItem("approval_txn_id",TransactionId)
            localStorage.setItem("grid_approval",'True')
        }
        // Showing approve/reject in list grid	ends
        else{
            RecordId = localStorage.getItem("keyData");
            try{
                AllParams ={}
                for (const [key, value] of Object.entries(dict)) {
                    if (value.includes("<img")) {
                        val = value.split(">")[1]
                    } else {
                        val = value
                    }
                    AllParams[key] = val
                }
                AllParams = JSON.stringify(AllParams);
            }
            catch(e){
                AllParams = JSON.stringify(dict);
            } 
            var TransactionIdData = $(ele).attr('id');
            var TransactionId = TransactionIdData.split('_');
            if (TransactionId != undefined){
                TransactionId = TransactionId[1];
            }
        }
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "APPROVE_COMMENT",
            'AllParams': AllParams,
            'QuoteNumber': RecordId,
            'TransactionId':TransactionId
        }, function (dataset) {
            $('#preview_approval #PREVIEW_APPROVAL_CONTENT').html(dataset);
        });
    } catch (e) {
        console.log(e);
    }
}

function reject_request(ele){
    try {
        // Showing approve/reject in list grid starts	
        var get_tab_value = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text().toUpperCase();

        var tab_array = ["MY APPROVAL QUEUE","QUOTES","TEAM APPROVAL QUEUE"]
        if ($(ele).attr('class').includes('grid_approval') && (tab_array.indexOf(get_tab_value) != -1)){
            var dict_approval ={}
            RecordId = TransactionId = $(ele).attr('id');
            dict_approval['TreeParam'] = 'Approvals'
            AllParams = JSON.stringify(dict_approval);
            localStorage.setItem("approval_txn_id",TransactionId)
            localStorage.setItem("grid_approval",'True')
        }
        // Showing approve/reject in list grid	ends
        else{
            RecordId = localStorage.getItem("keyData");
            try{
                AllParams ={}
                for (const [key, value] of Object.entries(dict)) {
                    if (value.includes("<img")) {
                        val = value.split(">")[1]
                    } else {
                        val = value
                    }
                    AllParams[key] = val
                }
                AllParams = JSON.stringify(AllParams);
            }
            catch(e){
                AllParams = JSON.stringify(dict);
            } 
            var TransactionIdData = $(ele).attr('id');
            var TransactionId = TransactionIdData.split('_');
            if (TransactionId != undefined){
                TransactionId = TransactionId[1];
            }
        }
        
        cpq.server.executeScript("ACSECTACTN", {
            'ACTION': "REJECT_COMMENT",
            'AllParams': AllParams,
            'QuoteNumber': RecordId,
            'TransactionId':TransactionId
        }, function (dataset) {
            $('#preview_approval #PREVIEW_APPROVAL_CONTENT').html(dataset);
        });
    } catch (e) {
        console.log(e);
    }
}
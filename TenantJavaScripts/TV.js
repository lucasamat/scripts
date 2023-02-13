
/* To load the left side nodes in all the Tree view except Material Tab,Price Modal Tab and Segment Tab Tree views 'Begin' */

function CommonLeftView() {
    Action = localStorage.getItem('Action_Text')

    sales_current_tab = $("ul#carttabs_head li.active a span").text()
    btn_cancel = $('button[name="CANCEL"]').css('display')
    btn_save = $('button[name="SAVE"]').css('display')
    if (btn_cancel == 'block' && btn_save == 'block') {
        Mode = "ADDNEW"
    }
    else {
        Mode = localStorage.getItem('Action_Text_new')
    }
    // Focus on Quote Information node when landing from c4c - Start
    var ancestorOrigin = window.location.ancestorOrigins;
    if (localStorage.getItem("add_new_functionality") != "TRUE" && localStorage.getItem('generatingbillingmatrix') == '') {
        if (ancestorOrigin) {
            if (ancestorOrigin[0]) {
                if (ancestorOrigin[0].includes('crm.ondemand.com')) {
                    localStorage.setItem("CurrentNodeId", 0);
                    localStorage.setItem("AfterDelete", "NO");
                }
            }
        }
    }
    localStorage.setItem('generatingbillingmatrix', '')
    // console.log("masterquoteRecId ==========>>>>",localStorage.getItem('masterquoteRecId'))
    // Focus on Quote Information node when landing from c4c - End
    Currenttab = $('ul#carttabs_head li.active a span').text();
    localStorage.setItem("add_new_functionality", "FALSE")
    var entitlement_level_flag = ""
    entitlement_level_flag = localStorage.getItem("entitlement_level_flag")
    //localStorage.setItem("entitlement_level_flag","");
    cpq.server.executeScript("SYULODTREE", { 'LOAD': 'Treeload', 'ACTION': Mode, 'sales_current_tab': sales_current_tab, 'Currenttab': Currenttab, 'entitlement_level_flag': entitlement_level_flag }, function (dataset) {
        var [data, data1, data2] = [dataset[0], dataset[1], dataset[2]];
        localStorage.setItem('CommonTreedatasetnew', data1);
        localStorage.setItem('clean_booking_checklist', data2);
        $("#commontreeview").treeview({
            data: data,
            levels: 1,
            onNodeSelected: function (event, node) {

                CurrentNodeId = node.nodeId;
                localStorage.setItem("TREETAB", "YES");
                localStorage.setItem("CurrentNodeId", CurrentNodeId);

                $(this).treeview('unselectNode', [node.nodeId, { silent: false }]);
                $('#commontreeview ul li.node-commontreeview:has(.leftside-bar-icons)').addClass('minus_drop');
                if (document.getElementsByName('SAVE') && document.getElementsByName('CANCEL')) {
                    CANCEL_DISPLAY = $('button[name="CANCEL"]').css('display')
                    SAVE_DISPLAY = $('button[name="SAVE"]').css('display')
                    if (SAVE_DISPLAY == 'block' && CANCEL_DISPLAY == 'block') {
                        try {
                            $("#commontreeview").treeview('unselectNode', [node.nodeId, { silent: false }]);
                            //$('#commontreeview ul li.node-commontreeview:has(.leftside-bar-icons)').addClass('minus_drop');
                            $('#deleteMSG span#tabname').text(CurrentTab)
                            $('#segment_SavePopup').modal('show');
                            $('#commontreeview ul li:first-child').click();
                        }
                        catch (e) {
                            console.log(e);
                        }
                    }
                }
                if (localStorage.getItem('btn_txt_val') != "ADD NEW") {
                    CANCEL_DISPLAY = $('button[name="CANCEL"]').css('display')
                    SAVE_DISPLAY = $('button[name="SAVE"]').css('display')
                    if ((CANCEL_DISPLAY != 'block') && (SAVE_DISPLAY != 'block')) {
                        CommonRightView(CurrentNodeId);
                    }
                }
            },
            onNodeUnselected: function (event, node) {
                $(this).treeview('selectNode', [node.nodeId, { silent: true }]);
                try {
                    ProductId = cpq.models.configurator.productId();
                }
                catch {
                    ProductId = '2240'
                    $('#commontreeview ul li.node-commontreeview:has(.leftside-bar-icons)').addClass('minus_drop');
                }

                
            }
        });
        try {
            [add_new_load, CurrentNodeId, CurrentId] = [localStorage.getItem("add_new_load"), localStorage.getItem("CurrentNodeId"), ''];
            try {
                ProductId = cpq.models.configurator.productId();
            }
            catch {
                ProductId = '2240'
            }
            if (CurrentNodeId != '' && CurrentNodeId != null) {
                CurrentId = CurrentNodeId;
            } else {
                CurrentId = 0;
                localStorage.setItem('CurrentNodeId', 0);
                //A055S000P01-3300 while navigating from approval center to Quotes tab(my approval queue tab to quotes information node) currentnodeid is not getting - start
                CurrentNodeId = 0;
                //A055S000P01-3300 while navigating from approval center to Quotes tab(my approval queue tab to quotes information node) currentnodeid is not getting - end
                $("COMMON_TABS").css('display', 'none');
            }
            nodeExpand(CurrentNodeId)
            if (add_new_load == 'true') {
            } else {
                $('#commontreeview').treeview('selectNode', [parseInt(CurrentId), { silent: true }]);
                $('#commontreeview ul li.node-commontreeview:has(.leftside-bar-icons)').addClass('minus_drop');
            }
            //A043S001P01-10796 START BREADCRUB IN ADD NEW MODE
            CurrentNodeId = parseInt(localStorage.getItem("CurrentNodeId"));
            if (isNaN(CurrentNodeId)) {
                CurrentNodeId = 0
            }
            //A043S001P01-10796 START BREADCRUB IN ADD NEW MODE
            if (localStorage.getItem("left_tree_refresh") != "yes") {
                CommonRightView(CurrentNodeId);

            }
            localStorage.setItem("left_tree_refresh", "no")
        } catch (e) {
            console.log(e);
        }
        localStorage.setItem("quote_item_insert", "no")
        dynamic_status();

    });
    showpricingbenchmarknotify()
}

function chkbox_selection() {
    condensedview = $('#cv').is(':checked');
    lineitemdetailview = $('#lidv').is(':checked');
    if (condensedview == true) {
        $("#lidv").attr("disabled", true);
    }
    else if (lineitemdetailview == true) {
        $("#cv").attr("disabled", true);
    }
    else {
        $("#lidv").attr("disabled", false);
        $("#cv").attr("disabled", false);
    }
}

function CommonLeftTreeView(id) {
    try {
        var CurrentId = add_new_load = CurrentNodeId = CurrentRecordId = TreeParam = TreeParentParam = TreeParentNodeId = TreeParentNodeRecId = TreeSuperParentParam = TreeSuperParentId = TreeSuperParentRecId = TreeTopSuperParentParam = TreeTopSuperParentId = TreeTopSuperParentRecId = TreeSuperTopParentParam = TreeSuperTopParentRecId = TreeSuperTopParentId = TreeFirstSuperTopParentParam = TreeFirstSuperTopParentId = TreeFirstSuperTopParentRecId = '';
        Action = localStorage.getItem('Action_Text')
        //CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
        CurrentTab = $("ul#carttabs_head li.active a span").text();
        if (CurrentTab == "My Approvals Queue") {
            TabName = "My Approval Queue"
        }
        else if (CurrentTab == "") {
            Tab = $(".show-large.tabsmenu ul li a span").html()
            TabName = Tab.slice(0, -1);
        }
        else {
            TabName = CurrentTab
        }
        document.getElementById("header_label_left").innerHTML = TabName.toUpperCase() + ' EXPLORER';
        if (CurrentTab != "Quotes" && CurrentTab != "Contracts") {
            document.getElementById("header_label").innerHTML = CurrentTab.toUpperCase() + ' INFORMATION';
        }
        localStorage.setItem('CURRENT_ACTIVE_TAB', CurrentTab)
        try {
            ProductId = cpq.models.configurator.productId();
        }
        catch {
            ProductId = '2240'
        }
        if (ProductId == '271' || ProductId == '273' || ProductId == '610' || ProductId == '2240' || ProductId == '710' || ProductId == '5310') {
            // localStorage.setItem("add_new_functionality","TRUE");
            if (CurrentTab == "Approval Chain" && localStorage.getItem('BTNADDNEW') == '1') {
                localStorage.setItem("left_tree_refresh", "yes");
            }
            CommonLeftView();
        }

        else {
            cpq.server.executeScript("SYULODTREE", { 'LOAD': 'Treeload' }, function (dataset) {
                var [data, data1] = [dataset[0], dataset[1]];
                localStorage.setItem('CommonTreedatasetnew', data1);


                $('#commontreeview').treeview({
                    data: data,
                    levels: 1,
                    showTags: true,
                    onNodeSelected: function (event, node) {

                        dict = {}
                        CurrentNodeId = node.nodeId;
                        localStorage.setItem("TREETAB", "YES");
                        // localStorage.setItem("CurrentNodeId", CurrentNodeId);
                        // dict['TreeParam'] = $('#commontreeview').treeview('getNode', CurrentNodeId).text;
                        // var GetDynamicparams = maintreeparamfunction(CurrentNodeId, 0);
                        var related_in_edit_mode = localStorage.getItem("RelatedEdit");
                        var getempty = $(".product_txt_to_top_banner").text();
                        if (getempty == '' || related_in_edit_mode == '1') {
                            try {
                                cpq.server.executeScript("SYEDITREPO", {}, function (edit_val) {
                                    if (edit_val == 'True' || getempty == "" || related_in_edit_mode == '1') {
                                        if (getempty == '') {
                                            $('#related_POPUP_prcmdl p').text('Save the Material before proceeding further.')
                                        }
                                        else {
                                            $('#related_POPUP_prcmdl p').text('You have unsaved changes on this page. Are you sure you want to leave this page and discard your changes?')

                                        }
                                        $('#cata_related_edit').modal('show');
                                        localStorage.setItem("EditCurrentNodeId", node.nodeId);
                                        $('#commontreeview').treeview('unselectNode', [node.nodeId, {
                                            silent: false
                                        }]);
                                        //localStorage.setItem("RelatedEdit", '0');
                                        return false;
                                    }
                                });
                                
                            }
                            catch (e) {
                                console.log(e);
                            }
                        }
                        else {
                            $(this).treeview('unselectNode', [node.nodeId, { silent: false }]);
                            AllTreeParams = JSON.stringify(GetDynamicparams);
                            localStorage.setItem('AllTreeParams', AllTreeParams);
                            //  Accounts explorer 
                            // JIRA ID A043S001P01-7614 CODE START.
                            CurrentRecordId = node.id;
                            var node_text_var = node.text;

                            if (typeof (node_text_var) != 'function' && node_text_var.includes("<span")) {
                                TreeParam = node_text_var.split(">").pop();
                            }
                            else {
                                TreeParam = node_text_var
                            }
                            if (TreeParam.includes("<img")) {
                                TreeParam = TreeParam.split(">")
                                TreeParam = TreeParam[TreeParam.length - 1]
                            }
                            else {
                                TreeParam = TreeParam
                            }
                            if (TreeParam.includes("-")) {
                                if (!TreeParam.includes('- BASE') && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving')) {

                                    TreeParam = TreeParam.split("-")[0].trim()
                                }
                            }
                            else {
                                TreeParam = TreeParam
                            }
                            //added
                            localStorage.setItem("CurrentRecordId", CurrentRecordId)
                            localStorage.setItem("CurrentNodeId", CurrentNodeId);
                            data1 = localStorage.getItem('CommonTreedatasetnew');
                            if (data1) {
                                data = data1.split(',');
                            }
                            $('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), { silent: true }]);

                            if (CurrentNodeId != '' && CurrentNodeId != null) {
                                TreeParentParam = $('#commontreeview').treeview('getParent', CurrentNodeId).text;
                                if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("<img")) {
                                    TreeParentParam = TreeParentParam.split(">")
                                    TreeParentParam = TreeParentParam[TreeParentParam.length - 1]
                                }
                                if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("-")) {
                                    if (!TreeParentParam.includes('- BASE')) {
                                        TreeParentParam = TreeParentParam.split("-")[0].trim()
                                    }
                                }

                                TreeParentNodeId = $('#commontreeview').treeview('getParent', CurrentNodeId).nodeId;
                                TreeParentNodeRecId = $('#commontreeview').treeview('getParent', CurrentNodeId).id;
                            }
                            if (TreeParentNodeId != '' && TreeParentNodeId != null) {
                                TreeSuperParentParam = $('#commontreeview').treeview('getParent', TreeParentNodeId).text;
                                if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("<img")) {
                                    //TreeSuperParentParam = TreeSuperParentParam.split(">")[1];
                                    TreeSuperParentParam = TreeSuperParentParam.split(">")
                                    TreeSuperParentParam = TreeSuperParentParam[TreeSuperParentParam.length - 1];
                                }
                                if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("-")) {
                                    if (!TreeSuperParentParam.includes('- BASE')) {
                                        TreeSuperParentParam = TreeSuperParentParam.split("-")[0].trim()
                                    }
                                }

                                TreeSuperParentId = $('#commontreeview').treeview('getParent', TreeParentNodeId).nodeId;
                                TreeSuperParentRecId = $('#commontreeview').treeview('getParent', TreeParentNodeId).id;
                            }
                            if (TreeSuperParentId != '' && TreeSuperParentId != null) {
                                TreeTopSuperParentParam = $('#commontreeview').treeview('getParent', TreeSuperParentId).text;
                                if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
                                    TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")
                                    TreeTopSuperParentParam = TreeTopSuperParentParam[TreeTopSuperParentParam.length - 1];
                                }
                                if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("-")) {
                                    if (!TreeTopSuperParentParam.includes('- BASE')) {
                                        TreeTopSuperParentParam = TreeTopSuperParentParam.split("-")[0].trim()
                                    }
                                }

                                TreeTopSuperParentId = $('#commontreeview').treeview('getParent', TreeSuperParentId).nodeId;
                                TreeTopSuperParentRecId = $('#commontreeview').treeview('getParent', TreeSuperParentId).id;
                            }
                            if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null) {
                                TreeSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).text;

                                if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeSuperTopParentParam.includes("<img")) {
                                    //TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")[1];
                                    TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")
                                    TreeSuperTopParentParam = TreeSuperTopParentParam[TreeSuperTopParentParam.length - 1];
                                }
                                if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeSuperTopParentParam.includes("-")) {
                                    if (!TreeSuperTopParentParam.includes('- BASE')) {
                                        TreeSuperTopParentParam = TreeSuperTopParentParam.split("-")[0].trim()
                                    }
                                }

                                TreeSuperTopParentId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
                                TreeSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).id;
                            }
                            if (TreeSuperTopParentId != '' && TreeSuperTopParentId != null) {
                                TreeFirstSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).text;

                                if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeFirstSuperTopParentParam.includes("<img")) {
                                    //TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")[1];
                                    TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")
                                    TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam[TreeFirstSuperTopParentParam.length - 1];
                                }
                                if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeFirstSuperTopParentParam.includes("-")) {
                                    if (!TreeFirstSuperTopParentParam.includes('- BASE')) {
                                        TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split("-")[0].trim()
                                    }
                                }

                                TreeFirstSuperTopParentId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).nodeId;
                                TreeFirstSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).id;
                            }

                            if (TreeSuperParentId === undefined) {
                                TreeSuperParentParam = ''
                            }
                            if (TreeTopSuperParentId === undefined) {
                                TreeTopSuperParentParam = ''
                            }
                            if (TreeSuperTopParentRecId === undefined) {
                                TreeSuperTopParentParam = ''
                            }
                            if (TreeFirstSuperTopParentRecId === undefined) {
                                TreeFirstSuperTopParentParam = ''
                            }
                            try {
                                var childrenNodes = _getChildren(CurrentNodeId);
                                if (childrenNodes.length > 0) {
                                    child = 'true';
                                } else {
                                    child = 'false';
                                }
                            } catch (e) {
                                child = ''
                            }
                            try {
                                if (localStorage.getItem("Action_Text") == 'ADD NEW' && CurrentTab == 'Program Type') {
                                    if (CurrentNodeId > 0) {
                                        $('#commontreeview').treeview('unselectNode', [node.nodeId, { silent: false }]);
                                        $('#pgt_SavePopup').modal('show');
                                        $('#commontreeview').treeview('selectNode', [0, { silent: true }]);
                                    }
                                }
                                if (localStorage.getItem("Action_Text") != 'ADD NEW') {
                                    cpq.server.executeScript("SYULODTREE", { 'LOAD': 'GlobalSet', 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam, 'TreeFirstSuperTopParentParam': TreeFirstSuperTopParentParam }, function (dataset) {
                                        var current_prod = $("span#ModuleName").text()
                                        if (current_prod == "Price Models") {
                                            CommonRightView(CurrentNodeId);
                                        }
                                        else {
                                            Common_enable_disable(id);
                                        }
                                    });
                                }
                            } catch (e) {
                                console.log(e);
                            }
                            // accounts explorer 
                            //JIRA ID A043S001P01-7614 CODE END.
                            if (document.getElementsByName('SAVE') && document.getElementsByName('CANCEL')) {
                                CANCEL_DISPLAY = $('button[name="CANCEL"]').css('display')
                                SAVE_DISPLAY = $('button[name="SAVE"]').css('display')
                                if (SAVE_DISPLAY == 'block' && CANCEL_DISPLAY == 'block') {
                                    try {
                                        $("#commontreeview").treeview('unselectNode', [node.nodeId, { silent: false }]);
                                        $('#deleteMSG span#tabname').text(CurrentTab)
                                        $('#segment_SavePopup').modal('show');
                                        $('#commontreeview ul li:first-child').click();
                                        /*setTimeout(function(){
                                            $('#commontreeview').treeview('selectNode', [0, {silent: true}]);
                                        },500);*/

                                    }
                                    catch (e) {
                                        console.log(e);
                                    }
                                }
                            }
                        }
                        try {
                            cpq.server.executeScript("CQCRUDOPTN", {
                                'Opertion': 'GET',
                                'ActionType': 'SHOW_PRICING_BENCHMARKING_NOTIFICATION',
                                'NodeType': 'QUOTE LEVEL NOTIFICATION'
                            }, function (data) {



                            });
                        }
                        catch { console.log('error price bench mark notification') }
                    },
                    onNodeUnselected: function (event, node) {
                        $(this).treeview('selectNode', [node.nodeId, { silent: true }]);
                    }
                });

                try {
                    dict = {}

                    CurrentNodeId = parseInt(localStorage.getItem("CurrentNodeId"));

                    if (isNaN(CurrentNodeId)) {

                        CurrentNodeId = 0
                    }
                    dict['TreeParam'] = $('#commontreeview').treeview('getNode', CurrentNodeId).text;

                    if (dict['TreeParam'] != '' && dict['TreeParam'] != undefined && (typeof dict['TreeParam'] === 'string' || dict['TreeParam'] instanceof String) && dict['TreeParam'].includes("<img")) {
                        temp = dict['TreeParam'].split(">")
                        dict['TreeParam'] = temp[temp.length - 1];
                    }
                    if (dict['TreeParam'] != '' && dict['TreeParam'] != undefined && (typeof dict['TreeParam'] === 'string' || dict['TreeParam'] instanceof String) && dict['TreeParam'].includes("-")) {

                        if (!dict['TreeParam'].includes('- BASE') && dict['TreeParam'] != 'Add-On Products' && !dict['TreeParam'].includes('Sending') && !dict['TreeParam'].includes('Receiving')) {
                            temp = dict['TreeParam'].split("-")
                            dict['TreeParam'] = temp[0].trim();
                        }
                    }

                    var GetDynamicparams = maintreeparamfunction(CurrentNodeId, 0);
                    [add_new_load, CurrentNodeId, CurrentId] = [localStorage.getItem("add_new_load"), localStorage.getItem("CurrentNodeId"), ''];
                    if (CurrentNodeId != '' && CurrentNodeId != null) {
                        CurrentId = CurrentNodeId;
                        //added below lines to not collapse the current node while doing actions like edit,save,cancel in CM Class
                        if (CurrentTab = 'CM Class') {
                            $('#commontreeview').treeview('expandNode', [parseInt(CurrentNodeId), { silent: true }]);
                        }
                    } else {
                        CurrentId = 0;
                        localStorage.setItem('CurrentNodeId', 0);
                        $("COMMON_TABS").css('display', 'none');
                    }
                    if (add_new_load == 'true') {

                    } else {
                        $('#commontreeview').treeview('selectNode', [parseInt(CurrentId), { silent: true }]);
                    }
                    if (Action == 'ADD NEW') {
                        $(this).treeview('unselectNode', [node.nodeId, { silent: false }]);
                        //$('#segment_SavePopup').modal('show');
                        $('#treeview').treeview('selectNode', [0, { silent: true }]);
                        localStorage.setItem('CurrentNodeId', 0);
                    }
                    Common_enable_disable(id);

                    var [ActiveTab, current_url] = [$('ul#carttabs_head li.active a span').text(), window.location.href];
                    if (current_url.indexOf('quotation/Cart.aspx') > -1) {
                        ActiveTab = $('#cartHeader .tabbable ul li.active').text().trim()
                    }
                    // A043S001P01-11620 Start
                    else if (ActiveTab == "My Approvals Queue" || ActiveTab == "Team Approvals Queue") {
                        ActiveTab = "Approval"
                    }// A043S001P01-11620 End
                    document.getElementById("header_label_left").innerHTML = ActiveTab.toUpperCase() + ' EXPLORER';

                    if (document.getElementById("header_label")) {
                        document.getElementById("header_label").innerHTML = ActiveTab.toUpperCase() + ' INFORMATION';

                    }
                } catch (e) {
                    console.log(e);
                }
            });
        }

    } catch (e) {
        console.log(e);
    }
}
/* To load the left side nodes in all the Tree view except Material Tab,Price Modal Tab and Segment Tab Tree views 'End' */

function _getChildren(node) {
    if (node.nodes === undefined)
        return [];
    var childrenNodes = node.nodes;
    node.nodes.forEach(function (n) {
        childrenNodes = childrenNodes.concat(_getChildren(n));
    });
    return childrenNodes;
}

function onclick_treedatepicker(id) {
    $("#CommonTreeDetail input#" + id).datepicker({
        autoclose: true,
        todayHighlight: true
    });
}

cpq.events.sub("API:configurator:updated", function (data) {
    var [KeyToCurrency_value, KeyToCurrency_value, module_name] = [$('span.product_txt_to_top').text(), localStorage.getItem('KeyToCurrency'), localStorage.getItem("module_main_txt")];
    if (module_name == 'Order Management' || module_name == 'Price_models') {
        try {
            cpq.server.executeScript("SYUCURSYMB", { 'KeyToCurrency_value': KeyToCurrency_value }, function (datas) {
                var [data, data1] = [datas[0], datas[1]]
                if (data) {
                    $(data).each(function (index) {
                        var currency_field_label_symbol = lbl_txt = inp_val_to_concat = concatval = concat_val = concat_symbol_value = '';
                        var [count, currency_list_value, decimal_val] = [0, data[index], data1[index]];
                        if (currency_list_value) {
                            currency_field_label_symbol = currency_list_value.split('|');
                            $('.iconhvr label.col-md-11').each(function (indexval) {
                                lbl_txt = $(this).text().trim();
                                if (lbl_txt == currency_field_label_symbol[0]) {
                                    inp_val_to_concat = $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val();
                                    if ((/^[a-zA-Z0-9-., ]*$/).test(inp_val_to_concat) == false) {
                                        inp_val_to_concat = inp_val_to_concat.substring(1);
                                    }
                                    else {
                                        $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').attr('type', 'text');
                                        if (inp_val_to_concat != '') {
                                            concatval = inp_val_to_concat.replace(/,/g, '');
                                            concat_val = Number(concatval).toFixed(decimal_val);
                                            concat_val = concat_val.toLocaleString('en-US');
                                            concat_symbol_value = currency_field_label_symbol[1] + '' + concat_val;
                                            $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val(concat_symbol_value);
                                        }
                                    }
                                }
                            });
                        }
                    });
                }
            });
        } catch (e) {
            console.log(e);
        }
    }
});

function CommonRightView(CurrentNodeId) {
    $("#TREE_div").css('display', 'block');
    //$('#PageAlert').hide();
    //A055S000P01-3291 start
    $('#Newrevision1').hide()
    $('#Completesowbtn').hide()
    $('.cartContainer').css('display', 'none');
    if (localStorage.getItem('toolRE_matrix') == 'yes') {
        localStorage.setItem('toolRE_matrix', 'no')
        return
    }
    //A055S000P01-3291 end
    $('#Headerbnr').remove();
    $('#TREE_div').css('display', 'block');
    $('.fd-spinner').css('display', 'block');
    $('.overlay').css('opacity', '0.2');
    if (CurrentNodeId == '2_True') {
        CurrentNodeId = '2';
        var loadsection = 'True';
    }
    // Hide the details before load another tab/node details - Start
    if (document.getElementById("TREE_div")) {
        document.getElementById("TREE_div").innerHTML = "";
    }
    // Hide the details before load another tab/node details - End
    dict = {}
    dict['TreeParam'] = $('#commontreeview').treeview('getNode', CurrentNodeId).text;
    if (dict['TreeParam'] != '' && dict['TreeParam'] != undefined && (typeof dict['TreeParam'] === 'string' || dict['TreeParam'] instanceof String) && (dict['TreeParam'].includes("<img") || dict['TreeParam'].includes("<span"))) {
        //dict['TreeParam'] = dict['TreeParam'].split(">")[1];
        temp = dict['TreeParam'].split(">")
        dict['TreeParam'] = temp[temp.length - 1];
    }
    if (dict['TreeParam'] != '' && dict['TreeParam'] != undefined && (typeof dict['TreeParam'] === 'string' || dict['TreeParam'] instanceof String) && dict['TreeParam'].includes("-")) {
        if (!dict['TreeParam'].includes('- BASE') && AllTreeParam['TreeParentLevel2'] != 'Product Offerings' && AllTreeParam['TreeParentLevel3'] != 'Product Offerings' && AllTreeParam['TreeParentLevel4'] != 'Product Offerings' && dict['TreeParam'] != 'Add-On Products' && !dict['TreeParam'].includes('Sending') && !dict['TreeParam'].includes('Receiving')) { //changed the if condition to fix the Events not loading issue.. fixed the values eliminating issue after '-' in Tree nodes....
            temp = dict['TreeParam'].split("-")
            dict['TreeParam'] = temp[0].trim();
        }
    }

    localStorage.setItem("CommonRightView_CurrentNodeId", CurrentNodeId);
    AllTreeParam = maintreeparamfunction(parseInt(CurrentNodeId), 0);
    AllTreeParams = JSON.stringify(AllTreeParam);
    localStorage.setItem('AllTreeParams', AllTreeParam);
    AddEquipment = localStorage.getItem("AddEquipment")
    //dict['TreeParentParam'] = AllTreeParam['TreeParentLevel0'];
    //TreeParentParam = dict['TreeParentParam'];
    if (CurrentNodeId != '' && CurrentNodeId != null) {
        TreeParentParam = $('#commontreeview').treeview('getParent', CurrentNodeId).text;
        if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && (TreeParentParam.includes("<img") || TreeParentParam.includes("<span"))) {
            //                    TreeParentParam = TreeParentParam.split(">")[1];
            TreeParentParam = TreeParentParam.split(">")
            TreeParentParam = TreeParentParam[TreeParentParam.length - 1];
        }
        if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("-")) {
            if (!TreeParentParam.includes('- BASE')) {
                TreeParentParam = TreeParentParam.split("-")[0].trim()
            }
        }
        TreeParentNodeId = $('#commontreeview').treeview('getParent', CurrentNodeId).nodeId;
        TreeParentNodeRecId = $('#commontreeview').treeview('getParent', CurrentNodeId).id;
    }
    if (TreeParentNodeId != '' && TreeParentNodeId != null) {
        TreeSuperParentParam = $('#commontreeview').treeview('getParent', TreeParentNodeId).text;
        if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && (TreeSuperParentParam.includes("<img") || TreeSuperParentParam.includes("<span"))) {
            //TreeSuperParentParam = TreeSuperParentParam.split(">")[1];
            TreeSuperParentParam = TreeSuperParentParam.split(">")
            TreeSuperParentParam = TreeSuperParentParam[TreeSuperParentParam.length - 1];
        }
        if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("-")) {
            if (!TreeSuperParentParam.includes('- BASE')) {
                TreeSuperParentParam = TreeSuperParentParam.split("-")[0].trim()
            }
        }
        TreeSuperParentId = $('#commontreeview').treeview('getParent', TreeParentNodeId).nodeId;
        TreeSuperParentRecId = $('#commontreeview').treeview('getParent', TreeParentNodeId).id;
    }
    if (TreeSuperParentId != '' && TreeSuperParentId != null) {
        TreeTopSuperParentParam = $('#commontreeview').treeview('getParent', TreeSuperParentId).text;
        if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && (TreeTopSuperParentParam.includes("<img") || TreeTopSuperParentParam.includes("<span"))) {
            // TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")[1];
            TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")
            TreeTopSuperParentParam = TreeTopSuperParentParam[TreeTopSuperParentParam.length - 1];
        }
        if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("-")) {
            if (!TreeTopSuperParentParam.includes('- BASE')) {
                TreeTopSuperParentParam = TreeTopSuperParentParam.split("-")[0].trim()
            }
        }
        TreeTopSuperParentId = $('#commontreeview').treeview('getParent', TreeSuperParentId).nodeId;
        TreeTopSuperParentRecId = $('#commontreeview').treeview('getParent', TreeSuperParentId).id;
    }
    if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null) {
        TreeSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).text;
        if (TreeTopSuperParentId != '' && TreeTopSuperParentId != undefined && (typeof TreeTopSuperParentId === 'string' || TreeTopSuperParentId instanceof String) && (TreeTopSuperParentId.includes("<img") || TreeTopSuperParentId.includes("<span"))) {
            // TreeTopSuperParentId = TreeTopSuperParentId.split(">")[1];
            TreeTopSuperParentId = TreeTopSuperParentId.split(">")
            TreeTopSuperParentId = TreeTopSuperParentId[TreeTopSuperParentId.length - 1];
        }
        if (TreeTopSuperParentId != '' && TreeTopSuperParentId != undefined && (typeof TreeTopSuperParentId === 'string' || TreeTopSuperParentId instanceof String) && TreeTopSuperParentId.includes("-")) {
            if (!TreeTopSuperParentId.includes('- BASE')) {
                TreeTopSuperParentId = TreeTopSuperParentId.split("-")[0].trim()
            }
        }
        TreeSuperTopParentId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
        TreeSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).id;
    }
    if (TreeSuperTopParentId != '' && TreeSuperTopParentId != null) {
        TreeFirstSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).text;
        if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && (TreeFirstSuperTopParentParam.includes("<img") || TreeFirstSuperTopParentParam.includes("<span"))) {
            // TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")[1];
            TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")
            TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam[TreeFirstSuperTopParentParam.length - 1];
        }
        if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeFirstSuperTopParentParam.includes("-")) {
            if (!TreeFirstSuperTopParentParam.includes('- BASE')) {
                TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split("-")[0].trim()
            }
        }
        TreeFirstSuperTopParentId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).nodeId;
        TreeFirstSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).id;
    }
    if (TreeSuperParentId === undefined) {
        TreeSuperParentParam = ''
    }
    if (TreeTopSuperParentId === undefined) {
        TreeTopSuperParentParam = ''
    }
    if (TreeSuperTopParentRecId === undefined) {
        TreeSuperTopParentParam = ''
    }
    if (TreeFirstSuperTopParentRecId === undefined) {
        TreeFirstSuperTopParentParam = ''
    }
    var childrenNodes = _getChildren(CurrentNodeId);
    if (childrenNodes.length > 0) {
        child = 'true';
    } else {
        child = 'false';
    }

    localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    localStorage.setItem('CommonTopSuperParentParam', AllTreeParam['TreeParentLevel2']);
    localStorage.setItem('CommonTreeSuperTopParentParam', AllTreeParam['TreeParentLevel3']); //Accounts Tab 
    localStorage.setItem('CommonTreeFirstSuperTopParentParam', AllTreeParam['TreeParentLevel4']); //Accounts Tab


    localStorage.setItem('CommonParentNodeRecId', TreeParentNodeRecId);
    localStorage.setItem('CommonTreeSuperParentRecId', TreeSuperParentRecId);
    localStorage.setItem('CommonTopSuperParentRecId', TreeTopSuperParentRecId);
    $('#div_CTR_quote_prevw').css('display', 'none')
    var entitlement_level_flag = ""
    if (AllTreeParam['TreeParentLevel2'] == 'Product Offerings') {
        localStorage.setItem("entitlement_level_flag", "SAQSGE");
    }
    else if (AllTreeParam['TreeParentLevel1'] == 'Product Offerings') {
        localStorage.setItem("entitlement_level_flag", "SAQTSE");
    }
    else {
        localStorage.setItem("entitlement_level_flag", "");
    }
    entitlement_level_flag = localStorage.getItem("entitlement_level_flag")
    cpq.server.executeScript("SYULODTREE", { 'LOAD': 'CommonGlobalSet', 'AllTreeParams': AllTreeParams, 'entitlement_level_flag': entitlement_level_flag }, function (dataset) {
        $('.Detail, .CommonTreeDetail, .Related, #COMMON_TABS').css('display', 'none');
        $('#SegAlert').css('display', 'none');
        node = $('#commontreeview').treeview('getNode', CurrentNodeId);
        localStorage.setItem('CurrentNodeId', CurrentNodeId)
        if ((node.nodeId == 4) && node.objname == "SAQFBL") {
            CurrentRecordId = "SYOBJR-98789";
        }
        else {
            CurrentRecordId = node.id;
        }




        var node_text_var = node.text;

        if (typeof (node_text_var) != 'function' && node_text_var.includes("<span")) {
            TreeParam = node_text_var.split(">").pop();
        }
        else {
            TreeParam = node_text_var
        }
        if (TreeParam.includes("<img")) {

            TreeParam = TreeParam.split(">")
            TreeParam = TreeParam[TreeParam.length - 1]
        } else {
            TreeParam = TreeParam
        }
        if (TreeParam.includes("-")) {

            if (!TreeParam.includes('- BASE') && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving')) {
                TreeParam = TreeParam.split("-")[0].trim()
            }
        } else {
            TreeParam = TreeParam
        }
        ObjName = node.objname;
        SubTabList = node.SubTabs;
        subtab = JSON.stringify(SubTabList)
        localStorage.setItem('SubTabDetails', subtab);
        if ((CurrentNodeId == 0 && TreeParam != 'Quote Information') && (CurrentNodeId == 0 && TreeParam != 'Quote Information') && (CurrentNodeId == 0 && TreeParam != 'Approval Chain Information')) {
            $('.Detail').css('display', 'block');
        }
        if (localStorage.getItem('CURRENT_ACTIVE_TAB') == "Tab" && CurrentNodeId != 0 && localStorage.getItem('secEditMode') == 1) {
            sec_cancel_tab()
        };	// to cancel section edit after navigating to another node and come back to same(first) node
        breadCrumb_Reset();
        try {
            var cartcurrtab = $("#carttabs_head li.active a span").text();
        }
        catch {
            var cartcurrtab = ''
        }

        if (TreeParam == "Approvals" && cartcurrtab == 'Quotes') {
            //quote_approvals_node()
            //loadRelatedList(CurrentRecordId,'listPreview')
            $("#approvalIframe").contents().find("body").addClass("insideiframe");
            $("#approvalIframe").contents().find(".userdrop").remove();
            $('#approvalIframe').css('display', 'block');
            $('#div_CTR_related_list').css('display', 'none');
            if (localStorage.getItem('ApprovalCompleteStage') == "yes") {
                //localStorage.setItem("add_new_functionality","TRUE");
                //window.location.reload();
                setTimeout(function () {
                    localStorage.setItem("add_new_functionality", "TRUE");
                    window.location.reload();
                    document.getElementById('approvalIframe').contentDocument.location.reload(true);
                    localStorage.setItem("ApprovalCompleteStage", "no");
                    //window.location.reload();
                }, 3050);
                document.getElementById('approvalIframe').contentDocument.location.reload(true);
                //document.getElementById('approvalIframe').contentDocument.location.reload(true);


            } else {
                document.getElementById('approvalIframe').contentDocument.location.reload(true);
            }


        }
        if (TreeParam != "Approvals") {
            $('#approvalIframe').css('display', 'none');
            $('.segment_table_outer').removeClass('removemrgin');
        }
        if (SubTabList && SubTabList.length) {
            if (SubTabList.length > 0) {
                i = 0
                SubTabStr = '<ul class="nav nav-tabs">'
                $.each(SubTabList, function (key, value) {
                    $.each(value, function (k, v) {
                        $.each(v, function (k1, v1) {
                            ObjName = node.objname;
                            /* var a = '';
                            if (k1 == 'Related'){
                                $.each(v1[0], function( relatedRecordId, tabName ) {
                                    a = "'" + k + "', '" + k1 + "','" + ObjName + "', '" + relatedRecordId + "'"
                                });
                            }
                            else{ */
                            if (k == "Equipment" && TreeParentParam == "Fab Locations") {
                                if (Currenttab == 'Quotes') {
                                    ObjName = "SAQFEQ"
                                }
                                else {
                                    ObjName = "CTCFEQ"
                                }
                            }
                            if ((k == "Items" || k == "Details") && TreeParam == "Quote Items") {
                                ObjName = "SAQRIT"
                            }
                            if (k == "Approvers" && TreeParentParam == "Approval Chain Steps") {
                                ObjName = "ACACSA"
                            }
                            if (k == "Tracked Fields" && TreeParentParam == "Approval Chain Steps") {
                                ObjName = "ACAPTF"
                            }
                            if (k == "Contacts" && TreeParentParam == "Quote Information") {
                                ObjName = "SAQICT"
                            }
                            if (k == "Credits") {
                                ObjName = "SAQRCV"
                            }
                            if ((k == "Fab Locations" || k == "Equipment") && (TreeParam.includes('Sending') || TreeParam.includes('Receiving'))) {
                                if (k == "Fab Locations") {
                                    ObjName = "SAQFBL"
                                    CurrentRecordId = "SYOBJR-98789"
                                }
                                else if (k == "Equipment") {
                                    ObjName = "SAQFEQ"
                                    CurrentRecordId = "SYOBJR-98797"
                                }

                            }
                            if (k == "Equipment Details" && TreeSuperParentParam == "Sending Equipment" && TreeSuperTopParentParam == "Complementary Products") {
                                ObjName = "SAQSSE"
                            }
                            if (k == "Equipment" && (TreeSuperParentParam == "Product Offerings" || TreeTopSuperParentParam == "Product Offerings" || AllTreeParam["TreeParentLevel3"] == "Product Offerings")) {
                                if (Currenttab == 'Quotes') {
                                    ObjName = "SAQSCO"
                                }
                                else {
                                    ObjName = "CTCSCO"
                                }
                            }
                            if (k == "Equipment" && (TreeSuperParentParam == "Quote Items" || AllTreeParam['TreeParentLevel2'] == "Quote Items")) {
                                ObjName = "SAQICO"
                            }
                            a = "'" + k + "', '" + k1 + "','" + ObjName + "', '" + CurrentRecordId + "'"
                            /* }								 */
                            onclickstr = "subTabDetails(" + a + ")"
                            try {
                                if (typeof TreeParam != 'undefined') {
                                    //className = CurrentTab.replace(/\s/g, "_").concat(TreeParam.replace(/\s/g, "_"))
                                    if (((AllTreeParam['TreeParentLevel2'] != 'Comprehensive Services' && AllTreeParam['TreeParentLevel2'] != 'Complementary Products') || AllTreeParam['TreeParam'] == "Add-On Products")) {
                                        className = CurrentTab.replace(/\s/g, "_").concat(TreeParam.replace(/\s/g, "_").replace(",", "_"))
                                        className = className + "" + k.replace(/\s/g, "_")
                                    }
                                    else {
                                        className = CurrentTab.replace(/\s/g, "_").concat(AllTreeParam['TreeParam'].replace(/\s/g, "_").replace(",", "_"))
                                        className = className + "" + k.replace(/\s/g, "_")
                                    }
                                }
                                else {
                                    var node_text_var = node.text;

                                    if (typeof (node_text_var) != 'function' && node_text_var.includes("<span")) {
                                        TreeParam = node_text_var.split(">").pop();
                                    }
                                    else {
                                        TreeParam = node_text_var
                                    }
                                    if (TreeParam.includes("<img")) {
                                        TreeParam = TreeParam.split(">")
                                        TreeParam = TreeParam[TreeParam.length - 1]
                                    } else {
                                        TreeParam = TreeParam
                                    }
                                    if (TreeParam.includes("-")) {

                                        if (!TreeParam.includes('- BASE') && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving')) {
                                            TreeParam = TreeParam.split("-")[0].trim()
                                        }
                                    } else {
                                        TreeParam = TreeParam
                                    }
                                    className = CurrentTab.replace(/\s/g, "_").concat(TreeParam.replace(/\s/g, "_").replace(",", "_"))
                                    className = className + "" + k.replace(/\s/g, "_")
                                }
                            }
                            catch (e) {
                                console.log(e);
                            }
                            $('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
                                silent: true
                            }]);
                            $('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
                                silent: true
                            }]);
                            if (i == 0) {
                                className += ' active'
                                clickTrigger = onclickstr
                            }

                            if (k != 'No SubTab') {
                                SubTabStr += '<li onclick = "' + onclickstr + '" class="' + className + '" style="display:block;"> <a data-toggle="tab">' + k + '</a></li>';
                                if (i == 0) {
                                    if (TreeParam == "Approvals" && (CurrentTab == 'My Approvals Queue' || CurrentTab == 'Team Approvals Queue')) {
                                        approvals_history()
                                        loadRelatedList(CurrentRecordId, 'listPreview')
                                        Subbaner('Approvals', CurrentNodeId, CurrentRecordId, 'ACAPCH');
                                    }
                                    else if (TreeParam == "Approvals" && CurrentTab == 'Quotes') {
                                        quote_approvals_node()
                                        loadRelatedList(CurrentRecordId, 'listPreview')
                                    }
                                    else {
                                        var after_del = localStorage.getItem("AfterDeleteEquipment")
                                        if (after_del == "YES") {
                                            CoveredObjTreeTable();
                                            $('#TREE_div').css("display", "none");
                                        }
                                        else if (AddEquipment != "yes") {
                                            subTabDetails(k, k1, ObjName, CurrentRecordId)
                                        }
                                        //subTabDetails(k, k1, ObjName, CurrentRecordId)
                                    }
                                }
                                i++;
                            }

                            if (loadsection == "True") {
                                CurrentRecordId = "SYOBJR-98799_True"
                            }

                            if (k == 'No SubTab') {
                                if (TreeParam == "Approvals" && (CurrentTab == 'My Approval Queue' || CurrentTab == 'Team Approval Queue')) {
                                    approvals_history()
                                    loadRelatedList(CurrentRecordId, 'listPreview')
                                    Subbaner('Approvals', CurrentNodeId, CurrentRecordId, 'ACAPCH');
                                }
                                else if (TreeParam == "Approvals" && CurrentTab == 'Quotes') {
                                    quote_approvals_node()
                                    loadRelatedList(CurrentRecordId, 'listPreview')
                                    subTabDetails(k, k1, ObjName, CurrentRecordId)
                                }
                                else if ((TreeParam == "Quote Items" || AllTreeParam['TreeParam'] == "Quote Items") && ($('.segment_revision_Acc_text').text() == 'ZTBC - TOOL BASED' || $('.segment_revision_Acc_text').text() == 'TOOL' || $('.segment_revision_Acc_text').text() == 'ZWK1 - SPARES')) {
                                    localStorage.setItem("page_type", "OBJECT PAGE LISTGRID")
                                    //CommonParentTable();
                                    $("#div_CTR_related_list").css("display", "block");
                                    Subbaner('', CurrentNodeId, CurrentRecordId, 'QTQITM');
                                }
                                else if (TreeParam == "Contract Items" || AllTreeParam['TreeParam'] == "Contract Items") {
                                    localStorage.setItem("page_type", "OBJECT PAGE LISTGRID")
                                    $("#div_CTR_related_list").css("display", "none");
                                    $(".cartContainer").css("display", "block");
                                    Subbaner('', CurrentNodeId, CurrentRecordId, 'CTCITM');
                                }
                                else {
                                    subTabDetails(k, k1, ObjName, CurrentRecordId)
                                }
                            }
                            if (TreeParam == "Approvals" && CurrentTab == 'Quotes') {
                                quote_approvals_node()
                                loadRelatedList(CurrentRecordId, 'listPreview')
                                Subbaner('ApprovalsNode', CurrentNodeId, CurrentRecordId, ObjName)
                            }

                            //quote_approvals_node()

                            //Subbaner('ApprovalsNode',CurrentNodeId, CurrentRecordId, ObjName)

                        });
                    });
                });
                SubTabStr += '</ul>'
                document.getElementById('COMMON_TABS').innerHTML = SubTabStr
                $('#COMMON_TABS').css('display', 'block');
                if (ObjName == "SAQRIB") {
                    var div_text = $('#TREE_div').text()
                    if (div_text.includes('Billing Matrix is not applicable') || div_text.includes('No Records')) {
                        $('#COMMON_TABS').css('display', 'block');
                    }
                    else {
                        $('#COMMON_TABS').css('display', 'block');

                    }
                }
                $('div#COMMON_TABS').find("li a:contains('Kit Details')").parent().removeClass('active').css('display', 'none');
                $('div#COMMON_TABS').find("li a:contains('BoM')").parent().css('display', 'none');
                localStorage.removeItem('openedKit');
            }
        }

        //currenttab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
        currenttab = $("ul#carttabs_head li.active a span").text();
        if (currenttab == "") {
            currenttab = "Quotes"
        }

        if (AllTreeParam['TreeParam'] == "Quote Items") {
            /* RecId = "SYOBJR-00009"
            RecName = "div_CTR_Assemblies"
            loadRelatedList(RecId, RecName); */
            //CommonParentTable();
            if (localStorage.getItem("SaveSalesPrice") == 'yes') {
                $('div#COMMON_TABS').find("li a:contains('Annualized Items')").parent().addClass('active');
                $('div#COMMON_TABS').find("li a:contains('Summary')").parent().removeClass('active');

                localStorage.setItem("SaveSalesPrice", "no");
                subTabDetails('Annualized Items', 'Related', 'SAQICO', CurrentRecordId);
            }

        }
        //A055S000P01-15794 code starts ...
        if (AllTreeParam['TreeParam'] == "Customer Information") {////A055S000P01-17070 code starts.. ends...
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Sending Fab Locations')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Sending Equipment')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Fab Location Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Receiving Fab Locations')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Receiving Equipment')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Sending Account Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Receiving Account Details')").parent().css("display", "none");
        }

        //A055S000P01-15794 code ends...
        if (Action == 'ADD NEW') {
            $('ul.breadcrumb').append('<li><a onclick="breadCrumb_redirection(this)"><abbr title="ADD NEW">ADD NEW</abbr></a><span class="angle_symbol"><img src="/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>');
        }
        if (TreeParam == "Approvals") {
            ObjName = "ACAPTX"
            $('#div_CTR_related_list').css('display', 'none');
            $('#seginnerbnr').css('display', 'none');
            $('.segment_table_outer').addClass('removemrgin');
            //approvals_history();
            //Subbaner('',CurrentNodeId, CurrentRecordId, ObjName)
        }
        if (localStorage.getItem('COVERED_OBJ_SAVING') == 'yes' && (AllTreeParam['TreeParentLevel0'] == 'Comprehensive Services' || AllTreeParam['TreeParentLevel0'] == 'Complementary Products')) {
            localStorage.setItem("page_type", "OBJECT PAGE LISTGRID")
            subTabDetails('Equipment', 'Related', 'SAQSCO', CurrentRecordId);
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().addClass('active');
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
            //$('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");
            localStorage.setItem('COVERED_OBJ_SAVING', 'no');
            localStorage.setItem("covobjclicked", "yes");


        }
        //redirection after adding eqp fix
        if (localStorage.getItem('COVERED_OBJ_SAVING') == 'yes' && (AllTreeParam['TreeParentLevel0'] == "Add-On Products")) {
            subTabDetails('Equipment', 'Related', 'SAQSCO', CurrentRecordId);
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().addClass('active');
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
            localStorage.setItem("COVERED_OBJ_SAVING", "no");
        }
        if (AllTreeParam['TreeParentLevel1'] == "Approvals") {
            $('div#COMMON_TABS').find("li a:contains('Rule Criteria')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Chain')").parent().css("display", "none");
        }
        //Hide the QueryBuilder in other places code starts..
        if (AllTreeParam['TreeParentLevel0'] == "Approval Chain Steps") {
            //$('#SegmentQueryBuilder').load('mt/APPLIEDMATERIALS_PRD/AdditionalFiles/QueryBuilder/ApprovalChainCondition.html');
            $(".SegmentQuerybuilderclass").css("display", "none");
        }
        if (TreeParam == "Approval Chain Information") {
            $(".SegmentQuerybuilderclass").css("display", "none");
        }
        //Added the code to show and hide the Equipment and spare parts tab according to the entitlement value..
        if (AllTreeParam['TreeParentLevel0'] == "Complementary Products" || AllTreeParam['TreeParentLevel0'] == "Product Offerings" || AllTreeParam['TreeParentLevel0'] == "Add-On Products" || TreeParam == 'Add-On Products') {
            setTimeout(function () {
                if (AllTreeParam['TreeParam'] == "Z0100") {
                    $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "none");
                    if (localStorage.getItem('AddSpares') == 'yes') {
                        subTabDetails('Spare Parts', 'Related', 'SAQSPT', CurrentRecordId);
                        $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().addClass('active');
                        $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
                        localStorage.setItem("AddSpares", "no");
                    }
                }
                else if (AllTreeParam['TreeParam'].includes("Z0007")) {
                    $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
                }
                else {
                    // $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");

                }
            }, 1000);
            if ((!AllTreeParam['TreeParam'].includes("Z0110")) || (!AllTreeParam['TreeParam'].includes("Z0108"))) {
                $('#div_CTR_related_list').css('display', 'none');
                $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "none");
            }
        }
        //Added the code to show and hide the Equipment and spare parts tab according to the entitlement value..
        //if (AllTreeParam['TreeParentLevel1'] == "Approvals"){
        //$('#div_CTR_Rule_Criteria').load('mt/APPLIEDMATERIALS_PRD/AdditionalFiles/QueryBuilder/ApprovalChainCondition.html');
        //$("#div_CTR_Rule_Criteria").closest('.Related').css("display", "none");
        //}
        //Hide the QueryBuilder in other places code ends..
        else if (AllTreeParam['TreeParentLevel1'] == 'Fab Locations' && localStorage.getItem("currentSubTab") == 'Details') {
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            if (AllTreeParam['TreeParam'] == "UNMAPPED") {
                $('#COMMON_TABS').css('display', 'none');

            }
        }
        else if (AddEquipment == 'yes') {
            subTabDetails('Equipment', 'Related', 'SAQFEQ', AllTreeParam['TreeParam']);
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().addClass('active');
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().removeClass('active');
            localStorage.setItem("AddEquipment", "No")
            activetab = $('#COMMON_TABS li.active').text().trim();
            var Saletype = localStorage.getItem('saletype')
            if (activetab == 'Equipment' && CommonTreeParentParam == 'Fab Locations') {
                //$('#div_CTR_Equipments').css("display", "block");
                $('#div_CTR_related_list').css("display", "block");
                // var equipmentBtn = $('.secondary_highlight_panel').find('button#ADDNEW__SYOBJR_98797_SYOBJ_00904')
                // if (equipmentBtn.length == 0 && Saletype != 'TOOL RELOCATION'){							
                // 	$('.secondary_highlight_panel').append('<button id="ADDNEW__SYOBJR_98797_SYOBJ_00904" onclick="cont_openaddnew(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD FROM LIST</button>')
                // }
                // else if ( Saletype == 'TOOL RELOCATION'){
                // 	$('.secondary_highlight_panel').append('<button id="RELOCATE__SYOBJR_98797_SYOBJ_00904" onclick="cont_openaddnew(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">RELOCATE EQUIPMENT</button>')

                // }
            }
            else {
                var equipmentBtn = $('.secondary_highlight_panel').find('button#ADDNEW__SYOBJR_98797_SYOBJ_00937')
                if (equipmentBtn.length == 1) {
                    equipmentBtn.remove()
                }
            }
        }
        else if (localStorage.getItem('AddSpares') == 'yes' && AllTreeParam['TreeParentLevel0'] == 'Complementary Products') {
            subTabDetails('Spare Parts', 'Related', 'SAQSPT', CurrentRecordId);
            if (AllTreeParam['TreeParentLevel0'] == 'Complementary Products') {
                setTimeout(function () {
                    $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().addClass('active');
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
                }, 7050);
            } else {
                if (localStorage.getItem("AddSpares") != 'yes') {
                    $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().addClass('active');
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
                    $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "none");
                }
            }


            //$('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "none");
            localStorage.setItem("AddSpares", "no");
        }

        else if (AllTreeParam['TreeParentLevel1'] == 'Product Offerings') {
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().removeClass("active");
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().addClass("active");
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().click();
            if (localStorage.getItem("EntRefresh") == "YES") {
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().addClass('active');
                // $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
                //setTimeout(function () {
                $('#TREE_div').css("display", "none");
                subTabDetails('Entitlements', 'Detail', 'SAQTSV', CurrentRecordId);
                //$('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().addClass('active');

                //}, 2500);
                //$('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().click();
                //subTabDetails('Entitlements', 'Detail','SAQSCO', CurrentRecordId);
                //localStorage.setItem("EntRefresh", "NO");
            }
        }

        else if ((AllTreeParam['TreeParentLevel0'] == 'Comprehensive Services' || AllTreeParam['TreeParentLevel0'] == 'Complementary Products') && AllTreeParam['TreeParentLevel1'] == 'Product Offerings') {
            //$('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");

        }
        else if (AllTreeParam['TreeParentLevel0'] == 'Quote Items' || AllTreeParam['TreeParentLevel0'] == 'Contract Items') {
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
            // Added the code to show and hide Spares and Equipment subtabs in Quote items service level based on Z0100 service id - start
            $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "block");
            if (AllTreeParam['TreeParam'].includes('Z0100')) {
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
            }
            else {
                $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "block");
            }
            if (localStorage.getItem("SaveSalesPrice") == 'yes') {
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().addClass('active');
                $('div#COMMON_TABS').find("li a:contains('Annualized Items')").parent().removeClass('active');

                localStorage.setItem("SaveSalesPrice", "no");
                setTimeout(function () {
                    $('div#container').css("display", "none");
                    subTabDetails('Equipment', 'Related', 'SAQICO', CurrentRecordId);

                }, 1700);
            }
            // Added the code to show and hide Spares and Equipment subtabs in Quote items service level based on Z0100 service id - end
        }
        else if (AllTreeParam['TreeParentLevel1'] == 'Contract Items') {
            setTimeout(function () {
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            }, 1);
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");

        }

        else if (AllTreeParam['TreeParentLevel1'] == 'Quote Items') {
            setTimeout(function () {
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            }, 1);
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            if (localStorage.getItem("SaveSalesPrice") == 'yes') {
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().addClass('active');
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');

                localStorage.setItem("SaveSalesPrice", "no");
                setTimeout(function () {
                    $('div#container').css("display", "none");
                    subTabDetails('Equipment', 'Related', 'SAQICO', CurrentRecordId);

                }, 1700);
            }

        }
        else if (AllTreeParam['TreeParentLevel2'] == 'Quote Items') {
            setTimeout(function () {
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            }, 1);
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            if (localStorage.getItem("SaveSalesPrice") == 'yes') {
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().addClass('active');
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');

                localStorage.setItem("SaveSalesPrice", "no");
                subTabDetails('Equipment', 'Related', 'SAQICO', CurrentRecordId);
                setTimeout(function () {
                    $('div#container').css("display", "none");
                    subTabDetails('Equipment', 'Related', 'SAQICO', CurrentRecordId);

                }, 1700);
            }

        }
        if (AllTreeParam['TreeParentLevel0'] == 'Fab Locations') {
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
        }

        if (AllTreeParam['TreeParentLevel1'] == 'Fab Locations' && (AllTreeParam['TreeParentLevel0'].includes('Sending') || AllTreeParam['TreeParentLevel0'].includes('Receiving'))) {

            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            //subTabDetails('Equipment', 'Related','SAQFEQ', AllTreeParam['TreeParam'])
            localStorage.setItem("AssemblyId", "No")

        }
        if (AllTreeParam['TreeParentLevel2'] == 'Fab Locations' && (AllTreeParam['TreeParentLevel1'].includes('Sending') || AllTreeParam['TreeParentLevel1'].includes('Receiving'))) {

            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            localStorage.setItem("AssemblyId", "No")
            /*if (AllTreeParam['TreeParentLevel0'] == "UNMAPPED"){
                $('#COMMON_TABS').css('display','none');
    	
            }*/
        }

        if (AllTreeParam['TreeParentLevel2'] == 'Product Offerings' && (TreeParam == 'Receiving Equipment' || TreeParam == 'Sending Equipment')) {
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "none");
            //$('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "none");
            if (TreeParam == 'Sending Equipment') {
                $('div#COMMON_TABS').find("li a:contains('Sending Equipment')").parent().css("display", "block");
            }
            else if (TreeParam == 'Receiving Equipment') {
                $('div#COMMON_TABS').find("li a:contains('Receiving Equipment')").parent().css("display", "block");
                if (localStorage.getItem("EntRefresh") == "YES") {
                    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().addClass('active');
                    $('div#COMMON_TABS').find("li a:contains('Receiving Equipment')").parent().removeClass('active');
                    setTimeout(function () {
                        subTabDetails('Entitlements', 'Detail', 'SAQSCO', CurrentRecordId);
                    }, 1500);
                    //subTabDetails('Entitlements', 'Detail','SAQSCO', CurrentRecordId);
                    localStorage.setItem("EntRefresh", "NO");
                }
            }

        }
        if ((AllTreeParam['TreeParentLevel1'] == 'Receiving Equipment' && AllTreeParam['TreeParentLevel3'] == 'Complementary Products') || (AllTreeParam['TreeParentLevel1'] == 'Sending Equipment' && AllTreeParam['TreeParentLevel3'] == 'Complementary Products')) {
            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "none");

        }

        if ((AllTreeParam['TreeParentLevel2'] == 'Comprehensive Services' || AllTreeParam['TreeParentLevel2'] == 'Add-On Products') && AllTreeParam['TreeParam'] != 'Add-On Products') {
            $('#div_CTR_PM_Events').css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
            //$('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
            //$('div#COMMON_TABS').find("li a:contains('Equipment')").parent().addClass('active');
            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");
            //subTabDetails('Equipment', 'Related','SAQSCO', AllTreeParam['TreeParam']);
            $('div#conta2004').css('display', 'block');
            $('#div_CTR_Covered_Objects').css("display", "block");
            //Added the below code to restrict the wrong values in the breadcrumb trial.
            if (nobreadCrumb_Reset == true) {
                setTimeout(function () {
                    breadCrumb_Reset();
                }, 4000);
                var nobreadCrumb_Reset = false
            }
        }
        if (AllTreeParam['TreeParentLevel1'] == 'Comprehensive Services' && currenttab.indexOf('Contract') != -1 && (AllTreeParam['TreeParam'] != 'Sending Equipment' || AllTreeParam['TreeParam'] != 'Receiving Equipment')) {
            $("#TREE_div").hide()
            //$('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "none");
            $('#div_CTR_PM_Events').css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().addClass('active');
            //$('div#COMMON_TABS').find("li a:contains('Equipment')").parent().addClass('active');
            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            //subTabDetails('Details', 'Detail','CTCSGB', AllTreeParam['TreeParam']);
            $('div#conta2004').css('display', 'block');
            $('#div_CTR_Covered_Objects').css("display", "block");
        }
        if ((AllTreeParam['TreeParentLevel1'] == 'Comprehensive Services' || AllTreeParam['TreeParentLevel1'] == 'Complementary Products' || (AllTreeParam['TreeParentLevel3'] == 'Comprehensive Services' && AllTreeParam['TreeParentLevel1'] == 'Add-On Products')) && currenttab.indexOf('Quote') != -1 && (AllTreeParam['TreeParam'] != 'Sending Equipment' && AllTreeParam['TreeParam'] != 'Receiving Equipment')) {
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "none");
            //$('div#COMMON_TABS').find("li a:contains('Equipment')").parent().addClass('active');
            if (localStorage.getItem('openedKit') == null) {
                $('div#COMMON_TABS').find("li a:contains('Kit Details')").parent().css("display", "none").removeClass('active');
            }
            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");
            //if(AllTreeParam['TreeParentLevel1'] != 'Z0009' && AllTreeParam['TreeParentLevel0'] != 'Z0009'){
            //$('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "none");	
            //}
            $('#div_CTR_PM_Events').css("display", "none");

            if (localStorage.getItem("EntRefresh") == "YES") {
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().addClass('active');
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
                setTimeout(function () {
                    subTabDetails('Entitlements', 'Detail', 'SAQSCO', CurrentRecordId);
                }, 1500);
                //subTabDetails('Entitlements', 'Detail','SAQSCO', CurrentRecordId);
                localStorage.setItem("EntRefresh", "NO");
            }

        }
        if ((AllTreeParam['TreeParentLevel2'] == 'Complementary Products' || (AllTreeParam['TreeParentLevel3'] == 'Product Offerings') && currenttab.indexOf('Quote') != -1 && (AllTreeParam['TreeParam'] != 'Sending Equipment' && AllTreeParam['TreeParam'] != 'Receiving Equipment' && AllTreeParam['TreeParam'] != 'Add-On Products'))) {
            //if (AllTreeParam['TreeParentLevel0'] == "Sending Equipment" && AllTreeParam['TreeParentLevel0'] == "Receiving Equipment"){
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().addClass('active');
            $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "none");
            //$('div#COMMON_TABS').find("li a:contains('Equipment')").parent().addClass('active');
            if (localStorage.getItem('openedKit') == null) {
                $('div#COMMON_TABS').find("li a:contains('Kit Details')").parent().css("display", "none").removeClass('active');
            }
            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");
            //if (AllTreeParam['TreeParentLevel1'] != 'Z0009' && AllTreeParam['TreeParentLevel0'] != 'Z0009'){
            //$('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "none");
            //}
            $('#div_CTR_PM_Events').css("display", "none");
            // added condition to hide subtabs for unmapped node in product offering node
            if ((AllTreeParam['TreeParentLevel2'] == 'Complementary Products' || (AllTreeParam['TreeParentLevel3'] == 'Product Offerings') && AllTreeParam['TreeParam'] == 'Add-On Products')) {

                Subbaner("Add-on Products", CurrentNodeId, CurrentRecordId, "SAQSAO");

                //subTabDetails('Entitlements', 'Detail','SAQSCO', CurrentRecordId);
                localStorage.setItem("EntRefresh", "NO");

            }
            if (AllTreeParam['TreeParam'] != "UNMAPPED") {
                if (localStorage.getItem("EntRefresh") == "YES") {
                    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().addClass('active');
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
                    setTimeout(function () {
                        subTabDetails('Entitlements', 'Detail', 'SAQSCO', CurrentRecordId);
                    }, 1500);
                    //subTabDetails('Entitlements', 'Detail','SAQSCO', CurrentRecordId);
                    localStorage.setItem("EntRefresh", "NO");
                }
            }
            else {
                $('#COMMON_TABS').css('display', 'none');
            }
            //}

        }
        if (TreeParam == "Add-On Products") {
            if ($("#ADDNEW__SYOBJR_98882_SYOBJ_1177093").css('display') != 'block') {
                $('div#COMMON_TABS').find("li a:contains('Add-on Products')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('NSO Catalog')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Credits')").parent().css("display", "none");
                loadRelatedList('SYOBJR-98859', 'Add On Products');
            }
            else {
                $('div#COMMON_TABS').find("li a:contains('Add-on Products')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Credits')").parent().css("display", "none");
                //A055S000P01-20586 code starts..
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('NSO Catalog')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                //A055S000P01-205686 code ends..
            }
        }
        if (localStorage.getItem("AssemblyId") == 'Yes') {
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().addClass('active');
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "block");
            //subTabDetails('Events', 'Related','SAQIAP', '');
            subTabDetails('Assembly Details', 'Detail', 'SAQSCA', '')
            //$('#div_CTR_PM_Events').css("display", "block");
            $('#div_CTR_Covered_Objects').css("display", "none");
            localStorage.setItem("AssemblyId", "No")
            setTimeout(function () {

                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
            }, 100);
        }

        //A055S000P01-1981 code ends..
        //if(AllTreeParam['TreeParentLevel2'] == 'Complementary Products'){
        //if (AllTreeParam['TreeParentLevel0'] == "Sending Equipment" && AllTreeParam['TreeParentLevel0'] == "Receiving Equipment"){
        //$('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "none");
        //}
        //}
        if (TreeParam == "Material Information") {
            $("div label div:contains(PRICE SUMMARY)").parents('.Detail').css("display", "none");
            $("div label div:contains(FIELDS WITH QUESTIONS)").parents('.Detail').css("display", "none");
            $('.col8534').css('display', 'none');
            $('#div_PRICESUMMARY').closest('.Detail').hide();

            $("div label div:contains(MATERIAL + EMBLEM STYLES)").parents('.Detail').css("display", "none");
            $("div label div:contains(PERSONALIZATION SETTINGS)").parents("div.Detail").css('display', 'none');
            $('select#QSTN_SYSEFL_MA_00368').parents('div.Detail').css('display', 'none');

            $("div label div:contains(EMBLEM MANUFACTURING INFORMATION)").parents("div.Detail").css('display', 'none');

            var hide_fields_list = ['QSTN_SYSEFL_MA_00513', 'QSTN_SYSEFL_MA_00396', 'QSTN_SYSEFL_MA_00397', 'QSTN_SYSEFL_MA_00395', 'QSTN_SYSEFL_MA_00390', 'QSTN_SYSEFL_MA_00391', 'QSTN_SYSEFL_MA_00392', 'QSTN_SYSEFL_MA_00393', 'QSTN_SYSEFL_MA_00394', 'QSTN_SYSEFL_MA_05703', 'QSTN_SYSEFL_MA_05702']
            for (i = 0; i < hide_fields_list.length; i++) {
                $('#' + hide_fields_list[i]).parents('div.Detail').css('display', 'none')
            }
        }

        if ((AllTreeParam['TreeParentLevel0'] == 'Receiving Equipment' && AllTreeParam['TreeParentLevel2'] == 'Complementary Products') || (AllTreeParam['TreeParentLevel0'] == 'Sending Equipment' && AllTreeParam['TreeParentLevel2'] == 'Complementary Products')) {
            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "none");
        }

        if (TreeParam == "Quote Information" || TreeParam == "Contract Information") {
            $('div#COMMON_TABS').css('display', 'block');
            /*var getnotifymsg = localStorage.getItem('getbannermessage');
            if (getnotifymsg == "bannerNotify"){
            	
                var getdata = localStorage.getItem('getbannerdetail');
                $(".emp_notifiy").css('display','block');
                $(".emp_notifiy").html(getdata)
            }*/
            $('.common_quote_information').css('display', 'block');
            $('.common_opportunity').css('display', 'block');
            $('.common_opportunity').css('display', 'block');
            $('.common_legalsow').css('display', 'block');
            //$('.div_CTR_Involved_Parties').css('display', 'block');
            if (TreeParam == "Quote Information") {
                if (localStorage.getItem('clean_booking_checklist') == "Yes") {
                    subtab_HTML = '<li onclick="Common_Tabs(this,\'Quote_Information\')" class="common_quote_information active" style="display: block;"> <a data-toggle="tab" href=".Quote_Information">Details</a> <li onclick="Common_Tabs(this,\'involvedParties_Details\')" class="involvedparties_Details active" style="display: block;"> <a data-toggle="tab" href=".involvedparties_Details">Details</a> <li onclick="Common_Tabs(this,\'DetailOpportunity\')" class="common_opportunity" style="display: block;"> <a data-toggle="tab" href=".Opportunity">Opportunity</a><li onclick="Common_Tabs(this,\'DetailLegalSow\')" class="common_legalsow" style="display: block;"> <a data-toggle="tab" href=".LegalSow">Legal SoW</a><li onclick="Common_Tabs(this,\'Detail_clean_booking_list\')" class="common_clean_booking_list" style="display: block;"> <a data-toggle="tab" href=".cleanbookinglist">Clean Booking Checklist</a> <li onclick="Common_Tabs(this,\'SourceFabLocation\')" class="SourceFabLocation" style="display: block;"> <a data-toggle="tab" href=".SourceFabLocation">Sending Fab Locations</a>  <li onclick="Common_Tabs(this,\'Equipment\')" class="IP_Equipment" style="display: block;"> <a data-toggle="tab" href=".Equipment">Equipment</a> <li onclick="Common_Tabs(this,\'ToolRelocationMatrix\')" class="ToolRelocationMatrix" style="display: block;"> <a data-toggle="tab" href=".ToolRelocationMatrix">Tool Relocation Matrix</a> <li onclick="Common_Tabs(this,\'Involved_Parties\')" class="Involved_Parties" style="display: none;"> <a data-toggle="tab" href=".Involved_Parties">Involved Parties</a> </li> </li> </li></li></li>'
                }
                else {
                    subtab_HTML = '<li onclick="Common_Tabs(this,\'Quote_Information\')" class="common_quote_information active" style="display: block;"> <a data-toggle="tab" href=".Quote_Information">Details</a> <li onclick="Common_Tabs(this,\'involvedParties_Details\')" class="involvedparties_Details active" style="display: block;"> <a data-toggle="tab" href=".involvedparties_Details">Details</a> <li onclick="Common_Tabs(this,\'DetailOpportunity\')" class="common_opportunity" style="display: block;"> <a data-toggle="tab" href=".Opportunity">Opportunity</a><li onclick="Common_Tabs(this,\'DetailLegalSow\')" class="common_legalsow" style="display: block;"> <a data-toggle="tab" href=".LegalSow">Legal SoW</a> <li onclick="Common_Tabs(this,\'SourceFabLocation\')" class="SourceFabLocation" style="display: block;"> <a data-toggle="tab" href=".SourceFabLocation">Sending Fab Locations</a>  <li onclick="Common_Tabs(this,\'Equipment\')" class="IP_Equipment" style="display: block;"> <a data-toggle="tab" href=".Equipment">Equipment</a> <li onclick="Common_Tabs(this,\'ToolRelocationMatrix\')" class="ToolRelocationMatrix" style="display: block;"> <a data-toggle="tab" href=".ToolRelocationMatrix">Tool Relocation Matrix</a> <li onclick="Common_Tabs(this,\'Involved_Parties\')" class="Involved_Parties" style="display: none;"> <a data-toggle="tab" href=".Involved_Parties">Involved Parties</a> </li> </li> </li></li>'
                }
                Common_Tabs('', "Quote_Information");
            }
            else if (TreeParam == "Contract Information") {
                subtab_HTML = '<li onclick="Common_Tabs(this,\'Contract_Information\')" class="common_quote_information active" style="display: block;"> <a data-toggle="tab" href=".Quote_Information">Details</a> <li onclick="Common_Tabs(this,\'DetailOpportunity\')" class="common_opportunity" style="display: block;"> <a data-toggle="tab" href=".Opportunity">Opportunity</a> <li onclick="Common_Tabs(this,\'Involved_Parties\')" class="Involved_Parties" style="display: block;"> <a data-toggle="tab" href=".Involved_Parties">Involved Parties</a> </li> </li> </li></li></li>'
                Common_Tabs('', "Contract_Information");
            }
            $("div#COMMON_TABS ul.nav.nav-tabs").empty();
            $("div#COMMON_TABS ul.nav.nav-tabs").html(subtab_HTML);
            CurrentRecordId = $(".product_txt_to_top").html()
            if (CurrentRecordId == '') {
                CurrentRecordId = localStorage.getItem("masterquoteRecId")
            }
            //commented to check the secondary banner
            Subbaner("Details", CurrentNodeId, CurrentRecordId, ObjName);
        }


        if (TreeParam == "Approval Chain Information") {

            if ($('#BTN_SYACTI_AC_00006_SAVE').length == 0) {
                Common_Tabs('', "Approval_Chain_Information");
            }
            else {
                $('.Detail').css('display', 'block');
            }

        }
        
        if (TreeParam == "Quote Items") {
            if (localStorage.getItem("currentSubTab") == "Summary") {
                $("#cust_fields_div").css("display", "block");
                $(".quote_summary_new").css("display", "none");
                $(".alert").css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css('display', 'none');
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css('display', 'none');
                $('div#COMMON_TABS').find("li a:contains('Object List')").parent().css('display', 'none');
                $('div#COMMON_TABS').find("li a:contains('Product List')").parent().css('display', 'none');
                $('div#COMMON_TABS').find("li a:contains('Assortment Module')").parent().css('display', 'none');
                $('div#COMMON_TABS').find("li a:contains('Billing Plan')").parent().css('display', 'none');
                cpq.server.executeScript("CQQTEITEMS", {
                    'SUBTAB': "Summary",
                    'ACTION': "VIEW"
                }, function (dataset) {
					revision_status = dataset[7];
                    if ($(".segment_revision_poes_text .custom").val() == "True") {
                        $("#custom-fields-section").css("display", "none");
                        document.getElementById("TREE_div").innerHTML = dataset;
                    } else {
                        $('#custom-fields-section').css("display", "block");
                        $('.quote_sec').html(dataset[0]);
                        $("#ctr_drop").css("display", "inline-block");
						//  INC08890238 M
						$(".quote_tab").find("#ctr_drop").css("display", "inline-block");
						//  INC08890238 M
                        // $('#total_sales_price').html(dataset[1]);
                        // $('input#discount').val(dataset[2]);

                        $('#total_excluding_tax').html(dataset[1]);
                        $('#total_tax').html(dataset[2]);
                        $('#total_est_net').html(dataset[3]);
                        $('#total_amt').html(dataset[4]);
                        $('#total_margin').html(dataset[5]);
                        $('#total_margin_pct').html(dataset[6]);
                    }
					//  INC08890238 M
					option = $("#IdlingAllowed").val();
					//  INC08890238 M
					$(".quote_summary_sec").find('#ctr_drop').css("display", "none");
					//  INC08890238 M
					if ((option == "No" || option == null)) {
					//  INC08890238 M
						$(".quote_tab").find("#ctr_drop").css("display", "none");
					} else {
						//setTimeout(function () {

                $(".quote_tab").find("#ctr_drop").css("display", "inline-block");
            //}, 3500);
						
					}

                });
            }
            else {
                $("#cust_fields_div").css("display", "none");
            }
        }
        if (CurrentNodeId != 0 && AllTreeParam['TreeParentLevel1'] != 'Quote Items' && AllTreeParam['TreeParentLevel1'] != 'Fab Locations') {
            //commented to check the secondary banner
            //Subbaner(CurrentNodeId, CurrentRecordId, ObjName);
            //A043S001P01-10765 STARTS
            if ($("[name='SECT_CANCEL']").css('display') == 'block' && $("[name='SECT_SAVE']").css('display') == 'block') {
                localStorage.setItem("CANCEL_CLICK", "TRUE");
            }
            //A043S001P01-10765 ENDS
        }

        //A055S000P01-1173 start
        if (currenttab == "Quotes") {
            //var getopptype = $( "#QSTN_SYSEFL_QT_00723 option:selected" ).text();
            //var getopptype = $( "#DOCTYP_ID" ).val();
            var getopptype = localStorage.getItem("getopptype");
        }
        else {
            var getopptype = $("#QSTN_SYSEFL_QT_016912 option:selected").text();
        }
        if (TreeParam == "Quote Information") {
            $('div#COMMON_TABS').find("li a:contains('Source Fab Location')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().css("display", "none");
            $(".involvedparties_Details ").hide();
            $('.SourceFabLocation').hide();
        }
        if (localStorage.getItem('toolRE_matrix') == 'yes' && TreeParam == "Quote Information") {
            involvedid = localStorage.getItem("sourcefab")
            Common_Tabs('', 'Involved_Parties');
            $('#' + involvedid).click();
            Common_Tabs('', 'ToolRelocationMatrix');
            $('div#COMMON_TABS').find("li a:contains('Involved Parties')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Opportunity')").parent().css("display", "none");
            $("#div_CTR_Involved_Parties").closest('.Related').css("display", "none");
            $(".common_quote_information ").hide();
            $(".involvedparties_Details ").show();
            $(".involvedparties_Details ").removeClass('active');
            $('#ADDNEW__SYOBJR_98798_7F4F4C8D_73C7_4779_9BE5_38C695').hide();
            $('div#COMMON_TABS').find("li a:contains('Source Fab Location')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().addClass('active');
            setTimeout(function () {
                $("#TREE_div ").hide();
                $(".common_quote_information ").hide();
            }, 8000);
            localStorage.setItem('toolRE_matrix', 'no');


        }
        if (getopptype == "ZTBC - TOOL BASED" && (TreeSuperParentParam == "Product Offerings" || TreeSuperTopParentParam == "Product Offerings" || TreeParam == 'Add-On Products')) {
            setTimeout(function () {
                //$('#COMMON_TABS li[class*=Spare_Parts]').css('display','none');
                $('#COMMON_TABS li[class*=Forecast_Summary]').css('display', 'none');
                $('#COMMON_TABS li[class*=Delivery_Schedules]').css('display', 'none');
                $('#COMMON_TABS li[class*=Equipment]').css('display', 'block');
                //$('#COMMON_TABS li[class*=Entitlements]').css('display','block');
                $('#COMMON_TABS li[class*=Equipment]').css('display', 'block');
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                $('#COMMON_TABS li[class*=Assemblies]').css('display', 'block');
                $('div#COMMON_TABS').find("li a:contains('Tool')").parent().css("display", "none");
                $('#COMMON_TABS li[class*=Equipment_Details]').css('display', 'none');
                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                $('#COMMON_TABS li[class*=Spare_Parts_details]').css('display', 'none');
                $('.CC119201-572D-41BB-8C53-5C063EEAAD4F').css('display', 'none');
                //$(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display','none');


            }, 1);


        }
        //if (getopptype == "ZWK1 - SPARES")
        if (getopptype == "ZWK1") {
            $('#COMMON_TABS li[class*=Spare_Parts]').css('display', 'block');
            $('#COMMON_TABS li[class*=Forecast_Summary]').css('display', 'block');
            $('#COMMON_TABS li[class*=Delivery_Schedules]').css('display', 'block');
            $('#COMMON_TABS li[class*=Covered_Objects]').css('display', 'none');
            $('#COMMON_TABS li[class*=Assemblies]').css('display', 'none');
            $('#COMMON_TABS li[class*=Equipment]').css('display', 'none');
            $('#COMMON_TABS li[class*=Equipment_Details]').css('display', 'none');
            $('#COMMON_TABS li[class*=Spare_Parts_details]').css('display', 'none');
            $('#COMMON_TABS li[class*=Spare_Part_Details]').css('display', 'none');
            $('.F5414216-018E-47EB-9778-53F0FD95D273').css('display', 'none');
            $("#ADDNEW__SYOBJR_00005_SYOBJ_00272").css('display', 'none');
            $(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display', 'block');
            //$('#COMMON_TABS li[class*=Entitlements]').css('display','none');

        }
        //A055S000P01-1173 end
        if (localStorage.getItem("AfterDeleteEquipment") == "YES") {
            localStorage.setItem("AfterDeleteEquipment", "NO");
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().addClass('active');
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
        }
        if (CurrentNodeId == 0) {
            $("#seginnerbnr").css("display", "none");
            //A043S001P01-10765 STARTS
            CANCEL_CLICK = localStorage.getItem("CANCEL_CLICK")
            if (CANCEL_CLICK == 'TRUE') {
                if ($("[name='SECT_CANCEL']").css('display') == 'block' && $("[name='SECT_SAVE']").css('display') == 'block') {
                    $("[name='SECT_CANCEL']").click();
                    localStorage.setItem("CANCEL_CLICK", "")
                }
            }
            //A043S001P01-10765 ENDS
        }
        if (currenttab == "Quotes") {
            //QuoteStatus();
            dynamic_status();
        }
    });
}
function nodeExpand(CurrentNodeId) {
    var cur_id = $('#commontreeview').treeview('getParent', parseInt(CurrentNodeId)).nodeId;
    if (cur_id != undefined) {
        $('#commontreeview').treeview('expandNode', [parseInt(cur_id), { silent: true }]);
        nodeExpand(cur_id)
    }
    else {
        $('#commontreeview').treeview('expandNode', [parseInt(CurrentNodeId), { silent: true }]);
    }
}
/* To load Subtab details */
function subTabDetails(subTabName, subTabType, ObjName, CurrentRecordId) {
    $(".display_gird").css("display", "none");
    $("#TREE_div").css('display', 'block');
    //CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
    localStorage.removeItem("InlineEdit");
    $('.cpq_notification_div').css('display', "none");
    //INC08632845 M
	if (subTabName == "Receiving Fab Details"){
		subTabType = "Detail"
		ObjName = "SAQFBL"
		CurrentRecordId = localStorage.getItem("fts_fab_location_record_id");
		loadDetails(CurrentRecordId, ObjName, AllTreeParams)
		Subbaner(subTabName, CurrentNodeId, CurrentRecordId, ObjName);
	}
	if (subTabName == "Sending Fab Details"){
		subTabType = "Detail"
		ObjName = "SAQSAF"
		CurrentRecordId = localStorage.getItem("fts_fab_location_record_id");
		loadDetails(CurrentRecordId, ObjName, AllTreeParams)
		Subbaner(subTabName, CurrentNodeId, CurrentRecordId, ObjName);
	}
	//#INC08632845 M
    if (subTabType == "Detail") {
        $("#div_CTR_related_list").css("display", "none");
    }
    if (subTabType == "Related") {
        $('#TREE_div').css("display", "none");
        //$("#div_CTR_related_list").css("display", "block");
    }
    if (ObjName == "SAQRIT" && subTabName == "Details") {
        breadCrumb_Reset();
        CurrentRecordId = localStorage.getItem("CurrentRecordId")
        tool_breadcrumb();
    }
    if (ObjName == "SAQSGB" && subTabName == "Details") {
        breadCrumb_Reset();
        CurrentRecordId = localStorage.getItem("CurrentRecordId")
        tool_breadcrumb();
    }
    if (subTabName == "Object List" || subTabName == "Product List" || subTabName == "Billing Plan" || subTabName == "Assortment Module") {
        breadCrumb_Reset();
        CurrentRecordId = localStorage.getItem("CurrentRecordId")
        tool_breadcrumb();
    }
    if (TreeParam == "Quote Items" && subTabName == "Entitlements") {
        breadCrumb_Reset();
        CurrentRecordId = localStorage.getItem("CurrentRecordId")
        tool_breadcrumb();
    }
    active_subtab = $('#COMMON_TABS ul li.active').text().trim();
    CurrentTab = $("ul#carttabs_head li.active a span").text();
    CommonTreeParam = localStorage.getItem('CommonTreeParam', TreeParam);
    CommonTreeParentParam = localStorage.getItem('CommonTreeParentParam', TreeParentParam);
    CommonTopSuperParentParam = localStorage.getItem('CommonTopSuperParentParam', TreeTopSuperParentParam);
    CommonNodeTreeSuperParentParam = localStorage.getItem('CommonNodeTreeSuperParentParam')
    $("#pricing_picklist").css("display", "none");
    if (localStorage.getItem("equipment_level") != null) {
        equipment_level = localStorage.getItem("equipment_level")
    }
    else {
        equipment_level = ''
    }
    if (CommonNodeTreeSuperParentParam == 'Approvals' && CurrentTab == 'Quotes') {
        active_chain_step = $('#COMMON_TABS ul li.active').text().trim()
        localStorage.setItem("active_chain_step_from_approvals", active_chain_step);
        if (active_chain_step != "Round 1 : Disposition") {
            EventsTreeTable();
        }
    }
    // Hide the details before load another tab/node details - Start
    if (document.getElementById("TREE_div")) {
        document.getElementById("TREE_div").innerHTML = "";
    }
    localStorage.setItem("CurrentObject", ObjName);
    // Hide the details before load another tab/node details - End
    if (subTabName == "Spare Parts" || subTabName == "Events" || subTabName == "Parts List") {
        localStorage.setItem("InlineEdit", "NO");
    }
    //document genrerate starts..

    if (subTabName == "Document Generator" && TreeParam == "Quote Documents") {
        cpq.server.executeScript("CQLANGSELT", {
            'LOAD': 'DOCUMENT',

        }, function (dataset) {
            console.log('dataset', dataset)

        })
    }

    //adding pricing picklist in line item subtab starts .. 
    if (subTabName == "Annualized Items" && AllTreeParam['TreeParam'] == "Quote Items" && ProductId == '2240') {
        $("#cust_fields_div").css("display", "none");
        localStorage.setItem("picklist_rec_id", CurrentRecordId)
        cpq.server.executeScript("SYULODTREE", {
            'ACTION': "VIEW",
            'LOAD': 'PRICING PICKLIST',

        }, function (dataset) {
            console.log('dataset', dataset)
            if (dataset) {
                if ($('#pricing_picklist').length == 0) {
                    $('<li  class="pull-right line_item_picklist" id ="pricing_picklist"><select name="Pricing Picklist" id="pricing_picklist_select" onchange="PricingPickListOnclick()"><option id="document_curr" value="Document Currency" >Line Items in Document Currency</option><option id="global_curr" value="Global Currency">Line Items in Global Currency</option><option id="pricing" value="Pricing" >Pricing View</option></select></li>').insertAfter(".QuotesQuote_ItemsLine_Item_Details");
                }
                else if ($('#pricing_picklist').length) {
                    $("#pricing_picklist").css("display", "block");
                }

                $('#pricing_picklist_select').val(dataset);
            }
        })
    }
    else {
        $("#pricing_picklist").css("display", "none");
    }

    if (subTabName == "Attachments" || subTabName == "Output Documents") {
        $("#div_CTR_related_list").removeClass("display_none");
        if (subTabName == "Attachments") {
            $("#divDocAttachement").html("<iframe src='/quotation/Attachments.aspx' height='100%' width='100%' style='border: none;' id='docAttachement' ></iframe>");
            $("#docAttachement").contents().find("body").addClass("bodyAttachment");
        }
    }


    //Hide the QueryBuilder in other subtabs except chain step condition code starts..
    if (subTabName != 'Chain Step Conditions' && subTabName != 'Rule Criteria') {
        $(".SegmentQuerybuilderclass").css("display", "none");
        $('.QBeditbtn').removeClass('disp_blk');
        $('.QBeditbtn').addClass('disp_none');
        if (subTabName != 'Receiving Equipment' && subTabName != 'Equipment Details' && subTabName != 'Equipment Entitlements' && CommonTopSuperParentParam == 'Quote Items')//A055S000P01-17070 added the condition for receiving equipment to restrict breadcrumb reset...
            breadCrumb_Reset();
    }
    if ((subTabName == 'Equipment Details' || subTabName == 'Equipment Assemblies' || subTabName == 'Equipment Entitlements') && (CommonTopSuperParentParam == 'Comprehensive Services' || CommonTopSuperParentParam == 'Complementary Products') && currenttab.indexOf('Quotes') != -1) {
        localStorage.setItem('currentSubTab', subTabName);
        breadCrumb_Reset();
        if (subTabName != "Entitlement Assemblies") {
            $('.fixed-table-body').css('display', 'none')
        }
        equipment_serialnumber = localStorage.getItem("coveredobject_equipment_serial_number")
        Pmevents_breadcrumb(equipment_serialnumber)
    }
    else if (subTabName == "Sending Fab Locations" && TreeParam == "Customer Information") {////A055S000P01-17070 code starts.. ends...
        //ObjectName = "SAQSAF"
        //tool_breadcrumb()
        account_id = localStorage.getItem("account_id")
        breadCrumb_Reset();
        fts_breadcrumb(account_id)
        var sending_fab_id = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
        localStorage.setItem("CurrentRecordId", sending_fab_id)
    }
    else if (subTabName == "Receiving Fab Locations" && TreeParam == "Customer Information") {////A055S000P01-17070 code starts.. ends...
        account_id = localStorage.getItem("account_id")
        breadCrumb_Reset();
        fts_breadcrumb(account_id);
        var receiving_fab_id = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
        localStorage.setItem("CurrentRecordId", receiving_fab_id)
    }
    if (subTabName == 'Assembly Entitlements') {
        Values = localStorage.getItem("EquipmentSerialNumber")
        Assembly_Id = localStorage.getItem("AssemblyIdValue")
        breadCrumb_Reset();
        Pmevents_breadcrumb(Values);
        Pmevents_breadcrumb(Assembly_Id);
    }
    //Hide the QueryBuilder in other subtabs except chain step condition code ends..
    //Enable the add from list button after adding the Equipments.
    if (subTabName != 'Equipment' && (CommonTreeParentParam == 'Comprehensive Services' || CommonTreeParentParam == 'Complementary Products')) {
        $('#billingmatrix_save').css('display', 'none');
        $('#billingmatrix_cancel').css('display', 'none');
        localStorage.setItem("covobjclicked", "no");
    }

    if (CurrentRecordId == 'SYOBJR-98799_True') {
        CurrentRecordId = 'SYOBJR-98799';
        loadsection = 'True';
    }
    else {
        loadsection = 'False';
    }
    if ((CommonNodeTreeSuperParentParam == 'Fab Locations' || CommonTopSuperParentParam == 'Comprehensive Services' || CommonTopSuperParentParam == 'Complementary Products' || CommonTopSuperParentParam == 'Quote Items' || CommonTreeParentParam == 'Quote Items') && (subTabName == 'Equipment Details' || subTabName == 'Spare Part Details') && CurrentRecordId == CommonTreeParam) {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
    }
    if ((subTabName == 'Spare Part Details' || subTabName == 'Entitlements') && CommonTreeParentParam == 'Quote Items') {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
    }
    if (subTabName == 'Assembly Details') {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
    }

    // To load query builder - start
    if (AllTreeParam['TreeParentLevel0'] == "Approval Chain Steps" && subTabName == "Chain Step Conditions") {
        //$('#SegmentQueryBuilder').load('mt/APPLIEDMATERIALS_PRD/AdditionalFiles/QueryBuilder/ApprovalChainCondition.html');
        $(".SegmentQuerybuilderclass").css("display", "none");
        loadRelatedList("SYOBJR-98120", "div_CTR_Approvers");
        $("#div_CTR_Approvers").closest('.Related').css("display", "block");
        $(".QBeditbtn").hide();
    }
    // To load query builder - end
    localStorage.setItem('CommonTreeSuperTopParentParam', AllTreeParam['TreeParentLevel3']);
    localStorage.setItem('CommonTreeFirstSuperTopParentParam', AllTreeParam['TreeParentLevel4']);
    Commonparamlevel3 = localStorage.getItem('CommonTreeSuperTopParentParam');
    Commonparamlevel4 = localStorage.getItem('CommonTreeFirstSuperTopParentParam');
    localStorage.setItem('currentSubTab', subTabName);
    $('.CommonTreeDetail, .Related').css('display', 'none');
    SubTabList = localStorage.getItem("SubTabDetails")
    SubTabList = JSON.parse(SubTabList);
    //|| AllTreeParam['TreeParentLevel0'] == "UNMAPPED"
    if (AllTreeParam['TreeParam'] == "UNMAPPED") {
        SubTabList.shift();
        subTabName = "Equipment"
        subTabType = "Related"
    }
    $.each(SubTabList, function (key, value) {
        $.each(value, function (k, v) {
            $.each(v, function (k1, v1) {
                if (k == subTabName) {
                    if (k1 == subTabType) {

                        if (subTabName == 'Equipment' && CommonTreeParam == 'Fab Locations') {
                            $('#div_CTR_Equipments').css("display", "block");
                            $("#ADDNEW__SYOBJR_98789_SYOBJ_00919").hide();
                        }
                        if (subTabName == 'Fab Locations' && CommonTreeParam == 'Fab Locations') {
                            $("#ADDNEW__SYOBJR_98789_SYOBJ_00919").show();
                        }
                        if (subTabName == "Approval Transactions") {
                            breadCrumb_Reset();
                        }
                        if (CommonNodeTreeSuperParentParam == 'Approvals' && CurrentTab == 'Quotes') {
                            breadCrumb_Reset();
                        }
                        if (CommonTreeParam == "Delivery Schedule" && subTabName == 'Delivery Schedule') {
                            $('div#COMMON_TABS').find("li a:contains('Delivery Schedule')").parent().css("display", "none");
                            $('#seginnerbnr').append('<button id="delivery_save" onclick="showSdeliverysave(this)"  style= "display: none;" class="btnconfig" >SAVE</button><button id="delivery_cancel" style= "display: none;" onclick="showSdeliverycancel(this)"   class="btnconfig" >CANCEL</button>')
                            $('div#COMMON_TABS').find("li a:contains('Delivery Schedule')").parent().css("display", "none");
                            setTimeout(function () {
                                //$('.secondary_highlight_panel').append('<button id="REFRESH_MATRIX" onclick="refresh_billingmatrix(this)" class="btnconfig" >REFRESH</button>')
                                $('.secondary_highlight_panel').append('<button id="delivery_save" onclick="showSdeliverysave(this)"  style= "display: none;" class="btnconfig" >SAVE</button>')
                                $('.secondary_highlight_panel').append('<button id="delivery_cancel" onclick="showSdeliverycancel(this)"   style= "display: none;" class="btnconfig" >CANCEL</button>')
                                $('div#COMMON_TABS').find("li a:contains('Delivery Schedule')").parent().css("display", "none");
                            }, 2000);
                            $('div#COMMON_TABS').find("li a:contains('Delivery Schedule')").parent().css("display", "none");
                        }
                        if (CommonTreeParam == "Billing" && subTabName == 'Detail') {
                            var BillingmatrixBtn = $('.secondary_highlight_panel').find('button#REFRESH_MATRIX')
                            $('#REFRESH_MATRIX').show()
                            if (BillingmatrixBtn.length == 0) {
                                setTimeout(function () {
                                    //$('.secondary_highlight_panel').append('<button id="REFRESH_MATRIX" onclick="refresh_billingmatrix(this)" class="btnconfig" >REFRESH</button>')
                                    $('.secondary_highlight_panel').append('<button id="billingmatrix_save" onclick="showSBillMatBulksave(this)" style= "display: none;" class="btnconfig" >SAVE</button>')
                                    $('.secondary_highlight_panel').append('<button id="billingmatrix_cancel" onclick="showSBillMatBulkcancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>')
                                }, 2000);
                            }
                        }
                        else {

                            var BillingmatrixBtn = $('.secondary_highlight_panel').find('button#REFRESH_MATRIX')
                            if (BillingmatrixBtn.length == 1 && subTabName.startsWith("Year") == true) {
                                //BillingmatrixBtn.remove()
                                $('#REFRESH_MATRIX').hide()
                                $('#seginnerbnr').append('<button id="billingmatrix_save" onclick="showSBillMatBulksave(this)" style= "display: none;" class="btnconfig" >SAVE</button>')
                                $('#seginnerbnr').append('<button id="billingmatrix_cancel" onclick="showSBillMatBulkcancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>')
                            }
                            else {
                                $('#REFRESH_MATRIX').show()
                                $('#seginnerbnr').append('<button id="billingmatrix_save" onclick="showSBillMatBulksave(this)" style= "display: none;" class="btnconfig" >SAVE</button>')
                                $('#seginnerbnr').append('<button id="billingmatrix_cancel" onclick="showSBillMatBulkcancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>')
                            }
                        }
                        if (subTabName == 'Equipment' && CommonTreeParentParam == 'Fab Locations') {
                            //$('#div_CTR_Equipments').css("display", "block");
                            $('#div_CTR_related_list').css("display", "block");
                            localStorage.setItem("eqclicked", "yes");
                            var equipmentBtn = $('.secondary_highlight_panel').find('button#ADDNEW__SYOBJR_98797_SYOBJ_00937')
                            var Saletype = localStorage.getItem('saletype')
                            // if (currenttab == "Quote"){
                            // 	if (equipmentBtn.length == 0 && Saletype != 'TOOL RELOCATION'){							
                            // 		$('.secondary_highlight_panel').append('<button id="ADDNEW__SYOBJR_98797_SYOBJ_00904" onclick="cont_openaddnew(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD FROM LIST</button>')
                            // 	}
                            // 	// else if ( Saletype == 'TOOL RELOCATION'){
                            // 	// 	$('.secondary_highlight_panel').append('<button id="RELOCATE__SYOBJR_98797_SYOBJ_00904" onclick="cont_openaddnew(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">RELOCATE EQUIPMENT</button>')
                            // 	// }
                            // }
                        }
                        else {
                            var equipmentBtn = $('.secondary_highlight_panel').find('button#ADDNEW__SYOBJR_98797_SYOBJ_00937')
                            if (equipmentBtn.length == 1) {
                                equipmentBtn.remove()
                            }
                        }

                        if (subTabName == 'Spare Parts' && (CommonNodeTreeSuperParentParam == "Product Offerings" || CommonTreeParentParam == 'Complementary Products' || CommonTreeParentParam == 'Add-On Products')) {
                            localStorage.setItem("spareclicked", "yes");
                            $("#ADDNEW__SYOBJR_00005_SYOBJ_00272").css('display', 'none');
                            var sparePartsBulkAddBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-add-modal-btn')
                            if (sparePartsBulkAddBtn.length == 0) {
                                $("#ADDNEW__SYOBJR_00005_SYOBJ_00272").css('display', 'none');
                                $('.secondary_highlight_panel').append('<button id="spare-parts-bulk-add-modal-btn" onclick="showSparePartsBulkAddModal(this)" class="btnconfig" data-target="#bulkaddpopup" data-toggle="modal">BULK ADD</button>')
                                $('.secondary_highlight_panel').append('<button id="spare-parts-bulk-edit-btn" onclick="showSparePartsBulkEdit(this)" style= "display: none;" class="btnconfig" >BULK EDIT</button>')
                                $('.secondary_highlight_panel').append('<button id="spare-parts-bulk-save-btn" onclick="showSparePartsBulksave(this)" style= "display: none;" class="btnconfig" >SAVE</button>')
                                $('.secondary_highlight_panel').append('<button id="spare-parts-bulk-cancel-btn" onclick="showSparePartsBulkcancel(this)"  style= "display: none;" class="btnconfig" >CANCEL</button>')
                            }
                        }
                        else {
                            /*var getnotifymsg = localStorage.getItem('getbannermessage');
                            if (getnotifymsg == "bannerNotify"){
                            	
                                var getdata = localStorage.getItem('getbannerdetail');
                                $(".emp_notifiy").css('display','block');
                                $(".emp_notifiy").html(getdata)
                            }*/
                            var sparePartsBulkAddBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-add-modal-btn')
                            var sparePartsBulkEDITBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-edit-btn')
                            var sparePartsBulkSAVEBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-save-btn')
                            var sparePartsBulkCANCELBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-cancel-btn')
                            if (sparePartsBulkAddBtn.length == 1) {
                                sparePartsBulkAddBtn.remove()
                            }
                            if (sparePartsBulkEDITBtn.length == 1) {
                                sparePartsBulkEDITBtn.remove()
                            }
                            if (sparePartsBulkSAVEBtn.length == 1) {
                                sparePartsBulkSAVEBtn.remove()
                            }
                            if (sparePartsBulkCANCELBtn.length == 1) {
                                sparePartsBulkCANCELBtn.remove()
                            }
                        }
                        if (subTabName == 'Equipment' && (CommonTreeParentParam == 'Comprehensive Services' || CommonTreeParentParam == 'Complementary Products' || CommonNodeTreeSuperParentParam == 'Comprehensive Services' || CommonNodeTreeSuperParentParam == 'Complementary Products' || CommonTreeParentParam == 'Add-On Products')) {
                            localStorage.setItem("covobjclicked", "yes");
                            var equipmentBtn = $('.secondary_highlight_panel').find('button#ADDNEW__SYOBJR_98800_SYOBJ_00904')
                            // if (currenttab == "Quote"){
                            // 	if (equipmentBtn.length == 0){		
                            // 		$('.secondary_highlight_panel').append('<button id="ADDNEW__SYOBJR_98800_0D035FD5_F0EA_4F11_A0DB_B4E10928B59F" onclick="cont_openaddnew(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD FROM LIST</button>')
                            // 	}
                            // }
                        }
                        else {
                            var equipmentBtn = $('.secondary_highlight_panel').find('button#ADDNEW__SYOBJR_98800_SYOBJ_00904')
                            if (equipmentBtn.length == 1) {
                                equipmentBtn.remove()
                            }
                        }

                        if (CommonTreeParam == "Quote Items") {
                            var QuoteItemsBtn = $('.secondary_highlight_panel').find('button#CALCULATE_QItems')
                            $('#CALCULATE_QItems').show();

                            if (QuoteItemsBtn.length == 0) {
                                quote_type = $(".segment_revision_Acc_text").text()
                                sale_type = localStorage.getItem("saletype");
                                //setTimeout(function () {
                                //	if(quote_type == "ZTBC - TOOL BASED" && sale_type != "TOOL RELOCATION"){
                                //		$('#CALCULATE_QItems').show();
                                //$('.secondary_highlight_panel').append('<button id="CALCULATE_QItems" onclick="calculate_QItems(this)" class="btnconfig" >CALCULATE</button>')
                                //	}
                                //	else{
                                //		$('#CALCULATE_QItems').hide()
                                //	}
                                //}, 2000);
                            }
                        }
                        else {
                            var QuoteItemsBtn = $('.secondary_highlight_panel').find('button#CALCULATE_QItems')
                            if (QuoteItemsBtn.length == 1) {
                                $('#CALCULATE_QItems').hide()
                            }
                        }
                        if (subTabName == 'PAYTERM' && (CommonTreeParam == 'Approvals')) {
                            var submitapproval = $('.secondary_highlight_panel').find('button#SUBMIT_FOR_APPROVAL')
                            $('#SUBMIT_FOR_APPROVAL').show()
                            if (submitapproval.length == 0) {
                                setTimeout(function () {
                                    $('.secondary_highlight_panel').append('<button id="SUBMIT_FOR_APPROVAL" onclick="submit_for_approval(this)" class="btnconfig" >SUBMIT FOR APPROVAL</button>')
                                }, 2000);
                            }
                        }
                        else {
                            var submitapproval = $('.secondary_highlight_panel').find('button#SUBMIT_FOR_APPROVAL')
                            if (submitapproval.length == 1) {
                                $('#SUBMIT_FOR_APPROVAL').hide()
                            }
                        }
                        if (subTabName == 'Email Templates') {
                            $('.Approval_ChainChain_Step_1Email_Templates').addClass('active');
                            CurrentRecordId = localStorage.getItem("CurrentRecordId");
                            try {
                                cpq.server.executeScript("ACACSEMLBD", { 'Action': 'EmailContent', 'CurrentRecordId': CurrentRecordId }, function (dataset) {
                                    //console.log("dataset-----> ",dataset);
                                    if (dataset != '') {
                                        if (document.getElementById("div_CTR_Email_Templates")) {
                                            $(".CommonTreeDetail").css("display", "block");
                                            document.getElementById('div_CTR_Email_Templates').innerHTML = dataset[0];
                                            eval(dataset[1])
                                            $('#div_CTR_Email_Templates').closest('.Related').css('display', 'block');
                                            $('#div_CTR_Email_Templates').css('display', 'block');
                                        }
                                    }
                                });
                            } catch (e) {
                                console.log(e);
                            }
                        }
                        // && CommonTreeParentParam != 'Add-On Products' condition added to show SAQTSE in add on product
                        if ((TreeSuperTopParentParam == 'Product Offerings' && subTabName == 'Entitlements' && currenttab == "Quotes" && CommonTreeParentParam != 'Add-On Products' && CommonTreeParentParam != 'Receiving Equipment' && CommonTreeParentParam != 'Sending Equipment') || (subTabName == 'Entitlements' && currenttab == "Quotes" && TreeTopSuperParentParam == 'Add-On Products') || (TreeSuperTopParentParam == 'Complementary Products' && subTabName == 'Entitlements' && currenttab == "Quotes" && TreeSuperParentParam == 'Receiving Equipment')) {
                            v1 = ['343C544E-8A39-49CE-AAB2-6FA6384DC503', '68855FCB-F4D7-4641-93AB-B515A41F29E2']
                        }
                        else if (TreeTopSuperParentParam == 'Quote Items' && subTabName == 'Entitlements' && currenttab == "Quotes") {
                            v1 = ['03E35264-455A-4697-A017-DE4CDAE3FB50', '68C30A98-154E-436F-B4E5-73D8186DB68D']
                        }
                        else if (TreeTopSuperParentParam == 'Product Offerings' && subTabName == 'Entitlements' && currenttab == "Contracts") {
                            v1 = ['9020F322-C390-4CDC-AD77-ADCE87566815', '9EB2C7B4-0CE7-479E-BDCA-B2B2B55A6A5E']
                        }
                        else if (TreeTopSuperParentParam == 'Quote Items' && subTabName == 'Details' && currenttab == "Quotes") {
                            v1 = ['7CEBECF4-33DB-4891-AE5F-A6321C336C2D', '7C9013EF-075E-4319-9FBD-882BCC677840', '4E854950-70A8-4A11-9994-DA11DF3DF8ED', '689B00F5-8AE5-434D-AE30-8FF84A5BE6C9'];
                        }
                        else if (TreeSuperParentParam == 'Fab Locations' && subTabName == 'Details' && currenttab == "Quotes") {
                            v1 = ['B4F3F411-DD24-4D07-B72A-614E407EE7BA', 'BC796A59-56F8-4EA0-B149-A10E6E525692'];
                        }
                        else if (TreeTopSuperParentParam == 'Comprehensive Services' && subTabName == 'Details' && CurrentTab == "Quotes" && TreeParentParam != 'Add-On Products') {
                            v1 = ['F462317B-FFD6-45D2-BA99-B9D9643E4386', 'D6AF69DA-E769-4CFC-843C-92FF76F62BA8'];
                        }
                        else if (TreeTopSuperParentParam == 'Add-On Products' && subTabName == 'Details' && currenttab == "Quotes") {
                            v1 = ['F462317B-FFD6-45D2-BA99-B9D9643E4386', 'D6AF69DA-E769-4CFC-843C-92FF76F62BA8'];
                        }
                        else if (TreeTopSuperParentParam == 'Complementary Products' && subTabName == 'Details' && currenttab == "Quotes") {
                            v1 = ['D6AF69DA-E769-4CFC-843C-92FF76F62BA8', 'F462317B-FFD6-45D2-BA99-B9D9643E4386'];
                        }
                        else if (TreeSuperParentParam == 'Quote Items' && subTabName == 'Details' && currenttab == "Quotes") {
                            v1 = ['0D6B8611-04AC-4AF3-B1C1-C5E616B1B080', '8308766F-CFD8-4259-808F-0FF4A78F6223', 'EEC89073-94FC-4A31-AE25-7EF9055E1E16', '8540BDD6-1A1E-4870-8E69-46522F5EDCFE'];
                        }
                        if (k1 == 'Related') {
                            localStorage.setItem("page_type", "OBJECT PAGE LISTGRID")
                            $.each(v1, function (k2, v2) {
                                $.each(v2, function (k3, v3) {
                                    RecId = k3.toString()
                                    RecName = 'div_CTR_' + v3.replace(/\ /g, '_')

                                    if (RecId != "SYOBJR-00045" && RecId != "SYOBJR-00024" && RecId != "SYOBJR-98846" && RecId != "SYOBJR-98797" && RecId != "SYOBJR-98800" && RecId != "SYOBJR-98865" && RecId != "SYOBJR-00018" && RecId != "SYOBJR-00011" && RecId != "SYOBJR-00011" && RecId != "SYOBJR-98818" && RecId != "SYOBJR-98827" && RecId != "SYOBJR-00020") {

                                        if (loadsection == 'True') {
                                            loadsection = 'True';
                                        }
                                        else {
                                            //CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
                                            CurrentTab = $("ul#carttabs_head li.active a span").text();
                                            if (CurrentTab == "Quotes") {
                                                //var getopptype = $(".segment_revision_Acc_text").text();
                                                var getopptype = localStorage.getItem("getopptype")
                                            }
                                            // if ((getopptype == "ZTBC - TOOL BASED") && CommonTreeParam == "Quote Items" &&  subTabName == "Line Item Details" && (localStorage.getItem("AddSpares")!= 'yes')){
                                            // 	$('.cartContainer').css('display', 'none');
                                            // 	RecId = "SYOBJR-00009"
                                            // 	RecName = "div_CTR_Assemblies"
                                            // 	loadRelatedList(RecId, RecName);

                                            // 	//CommonParentTable();

                                            // }

                                            // if (CommonTreeParam == "Contract Items" &&  subTabName == "Line Item Details"){
                                            // 	$('.cartContainer').css('display', 'none');
                                            // 	RecId = "SYOBJR-91822"
                                            // 	RecName = "div_CTR_Assemblies"
                                            // 	loadRelatedList(RecId, RecName);
                                            // }

                                            if (CommonTreeParam == "Quote Items" && subTabName == "Annualized Items") {
                                                $('.cartContainer').css('display', 'none');
                                                $('#custom-fields-section').css('display', 'none');
                                                $("#cust_fields_div").css("display", "none");
                                                RecId = "SYOBJR-00009"
                                                //RecName = "div_CTR_related-list"
                                                RecName = "div_CTR_Assemblies"
                                                loadRelatedList(RecId, RecName);
                                            }
                                            //Us 4432 code starts..
                                            else if (getopptype == "ZWK1 - SPARES" && ((subTabName == "Line Item Details" && CommonTreeParam == "Quote Items") || (subTabName == "Equipment" && CommonTreeParentParam == "Quote Items"))) {
                                                RecId = "SYOBJR-00010"
                                                RecName = "div_CTR_Spare_Parts"
                                                loadRelatedList(RecId, RecName);
                                                $('.cartContainer').css('display', 'none');
                                                $('.fiori3-custom-fields-container').hide();
                                                $('.line_item_col_hdr').hide();
                                            }
                                            //Us 4432 code ends..
                                            else if ((subTabName == "Spare Parts Line Item Details" && CommonTreeParam == "Quote Items")) {
                                                RecId = "SYOBJR-00010"
                                                RecName = "div_CTR_Spare_Parts"
                                                loadRelatedList(RecId, RecName);
                                                //SparePartsList(RecId, RecName);
                                                $('.cartContainer').css('display', 'none');
                                                $('.fiori3-custom-fields-container').hide();
                                                $('.line_item_col_hdr').hide();
                                            }
                                            else if (CommonTreeParam == "Contract Items") {
                                                CommonParentTable();
                                            }
                                            else {
                                                if (localStorage.getItem("AddSpares") != 'yes' && subTabName != 'Events') {
                                                    $("#cust_fields_div").css("display", "none");
                                                    if (subTabName != 'Receiving Equipment') {
                                                        loadRelatedList(RecId, RecName);
                                                    }
                                                }
                                            }
                                        }
                                        $("div[id='" + RecName + "']").closest('.Related').css('display', 'block');
                                        $('.container_banner_inner_sec').css('display', 'none');
                                        $('#Items').css('display', 'none');
                                        $(".quote_summary_sec").css("display", "none");
                                        $(".quote_summary_new").css("display", "none");
                                    }
                                    //if (RecId == 'SYOBJR-98799'){ pending_grid(); }
                                    //pending_grid();
                                });
                            });
                            //if (subTabName == "Sending Fab Locations" && RecId == "SYOBJR-00032"){
                            //tool_breadcrumb()
                            //}

                            if (subTabName == 'Equipment' && RecId != 'SYOBJR-98800' && RecId != 'SYOBJR-00009' && RecId != 'SYOBJR-00010' && RecId != 'SYOBJR-98795' && currenttab.indexOf('Quotes') != -1) {
                                $('.container_banner_inner_sec').css('display', 'none');
                                if (TreeParentParam == "Sending Equipment" || TreeParentParam == "Receiving Equipment" || TreeSuperParentParam == "Sending Equipment" || TreeSuperParentParam == "Receiving Equipment" && TreeParam != "Customer Information") {
                                    SendingEquipmentTreeTable();
                                }
                                else if (TreeParam == "Add-On Products") {
                                    CoveredObjTreeTable(subTabName)
                                }
                                else {
                                    EquipmentTreeTable();
                                    $('#div_CTR_related_list').css("display", "block");
                                    $('#TREE_div').css("display", "none");
                                }

                            }
                            else if (subTabName == 'Sending Equipment' && RecId != 'SYOBJR-98800' && RecId != 'SYOBJR-00009' && RecId != 'SYOBJR-98795' && currenttab.indexOf('Quotes') != -1 && TreeParam != "Customer Information") {
                                $('.container_banner_inner_sec').css('display', 'none');
                                // if (TreeParentParam == "Complementary Products" || TreeSuperParentParam == "Complementary Products"){
                                SendingEquipmentTreeTable();
                                // }								
                                $('#div_CTR_related_list').css("display", "block");
                                $('#TREE_div').css("display", "none");


                            }
                            else if (subTabName == 'Receiving Equipment' && TreeParam == "Customer Information") {
                                $('.container_banner_inner_sec').css('display', 'none');
                                EquipmentTreeTable();
                                //$('#div_CTR_related_list').css("display", "block");
                                $('#TREE_div').css("display", "none");
                            }
                            else if (subTabName == 'BoM' && TreeTopSuperParentParam == "Comprehensive Services") {
                                Subbaner('BoM', CurrentNodeId, CurrentRecordId, 'SAQSKP');
                            }
                            else if (subTabName == 'Equipment' && RecId != 'SYOBJR-91822' && RecId != 'SYOBJR-98822' && RecId != 'SYOBJR-98842' && currenttab == "Contracts" && (CommonTreeParentParam == 'Fab Locations' || CommonNodeTreeSuperParentParam == 'Fab Locations' || CommonTreeParam == 'Fab Locations')) {
                                $('.container_banner_inner_sec').css('display', 'none');
                                ContractEquipmentTreeTable();
                            }
                            // else if (subTabName == 'Equipment Assemblies' && currenttab.indexOf('Quotes') != -1)
                            // {
                            // 	AssembliesTreeTable();
                            // }
                            else if (subTabName.includes('Disposition')) {
                                $('#div_CTR_related_list').css("display", "block");
                                $('.noRecDisp').css('display', 'none');
                                quote_approvals_node();
                            }
                            else if (subTabName == 'Equipment Assemblies' && currenttab == "Contracts") {
                                ContractAssembliesTreeTable();
                            }
                            else if (subTabName == 'Events') {
                                $('div#conta2004').css('display', 'none');
                                $('.container_banner_inner_sec').css('display', 'none');

                                if (RecId == 'SYOBJR-00011') {
                                    PreventiveMaintainenceTreeTable();
                                    $('#div_CTR_PM_Events').css("display", "block");
                                }
                                else {
                                    EventsTreeTable();
                                }
                            }
                            else if (ObjName == 'SAQRGG' && CommonNodeTreeSuperParentParam == 'Z0009') {
                                loadRelatedList("SYOBJR-95555", "div_CTR_related_list");
                                $('#div_CTR_related_list').css("display", "block");
                            }
                            else if (subTabName == 'Chain Step Conditions') {
                                //$('#SegmentQueryBuilder').load('mt/APPLIEDMATERIALS_PRD/AdditionalFiles/QueryBuilder/ApprovalChainCondition.html');
                                //$(".SegmentQuerybuilderclass").css('display', 'block');
                                $(".SegmentQuerybuilderclass").css("display", "none");
                                loadRelatedList("SYOBJR-98120", "div_CTR_Approvers");
                                $("#div_CTR_Approvers").closest('.Related').css("display", "block");
                                $(".QBeditbtn").hide();
                            }

                            else if (RecId == 'SYOBJR-98800' && (subTabName == 'Equipment' || subTabName == 'Sending Equipment') && (AllTreeParam['TreeParentLevel0'] == 'Comprehensive Services' || AllTreeParam['TreeParentLevel1'] == 'Product Offerings' || AllTreeParam['TreeParentLevel1'] == 'Comprehensive Services' || AllTreeParam['TreeParentLevel2'] == 'Comprehensive Services' || AllTreeParam['TreeParentLevel3'] == 'Comprehensive Services' || AllTreeParam['TreeParentLevel4'] == 'Comprehensive Services' || AllTreeParam['TreeParentLevel0'] == 'Complementary Products' || AllTreeParam['TreeParentLevel1'] == 'Complementary Products' || AllTreeParam['TreeParentLevel2'] == 'Complementary Products' || AllTreeParam['TreeParentLevel3'] == 'Complementary Products' || AllTreeParam['TreeParentLevel0'] == 'Add-On Products') && currenttab.indexOf('Quotes') != -1) {
                                $('.container_banner_inner_sec').css('display', 'none');
                                if (subTabName.includes("Equipment")) {
                                    localStorage.setItem("restrict_covered_obj_grid", "no")
                                }
                                if (localStorage.getItem("restrict_covered_obj_grid") != "yes") {

                                    if (subTabName == "Sending Equipment" || TreeSuperParentParam == "Sending Equipment" && TreeParam != "Customer Information") {
                                        SendingEquipmentTreeTable();
                                    }
                                    else {
                                        CoveredObjTreeTable(subTabName)
                                    }
                                }
                                localStorage.setItem("restrict_covered_obj_grid", "no");
                                $('div#conta2004').css('display', 'block');
                                $('#div_CTR_Covered_Objects').css("display", "block");
                                $('#TREE_div').css("display", "none");
                            }
                            else if (subTabName == 'Equipment' && currenttab == "Contracts" && TreeParentParam != "Contract Items") {
                                $('.container_banner_inner_sec').css('display', 'none');
                                ContractCoveredObjTreeTable();
                                $('div#conta2004').css('display', 'block');
                                $('#div_CTR_Covered_Objects').css("display", "block");
                            }
                            else if (subTabName == 'Fab Locations' && (TreeParam.includes("Sending") || TreeParam.includes("Receiving"))) {
                                loadRelatedList("SYOBJR-98789", "div_CTR_related_list")
                                $('#div_CTR_related_list').css("display", "block");
                                chainsteps_breadcrumb(subTabName)
                            }
                            else if (subTabName == 'Equipment' && (TreeParam.includes("Sending") || TreeParam.includes("Receiving"))) {
                                chainsteps_breadcrumb(subTabName)
                            }
                        }
                    }
                    if (k1 == 'Detail') {
                        $("#div_CTR_related_list").css("display", "none");
                        localStorage.setItem("page_type", "OBJECT PAGE LAYOUT")
                        if (k == 'Calculation Factors') {
                            localStorage.setItem('Load_action', 'FCTR_VIEW');
                            a = JSON.parse(AllTreeParams)

                            localStorage.setItem('PrcTreeParentParam', AllTreeParam['TreeParentLevel0']);
                            localStorage.setItem('CurrentRecordId', CurrentRecordId);
                            subtabs_load()
                        }

                        else if (subTabName == 'Assembly Details') {
                            Common_Tabs('', 'Offerings_Assembly_Details');
                        }
                        else if (subTabName == 'Details' && TreeParam == "Customer Information") {
                            Common_Tabs('', 'Sending_Account_Details');
                        }
                        else if (subTabName == 'Sending Account Details' && TreeParam == "Customer Information") {
                            // INC08616028 - Start - M
                            Common_Tabs('', 'Sending_Account_Details');
                            // INC08616028 - End - M
                        }
                        else if (subTabName == 'Receiving Account Details' && TreeParam == "Customer Information") {
                            // INC08616028 - Start - M
                            Common_Tabs('', 'Sending_Account_Details');
                            // INC08616028 - End - M
                        }
                        else if (subTabName == 'Details' && TreeParam == "Customer Information") {//A055S000P01-17070 code starts..ends..
                            Common_Tabs('', 'account_details');
                        }
                        else if (subTabName == 'Details' && TreeParam == "Add-On Products") {
                            Common_Tabs('', 'addon_details');
                        }
                        else if (subTabName == 'Equipment Details' && (CommonTopSuperParentParam == 'Comprehensive Services' || CommonTopSuperParentParam == 'Complementary Products')) {
                            Common_Tabs('', 'Equipment Details');
                        }
                        else if (subTabName == 'Equipment Details' && (CommonTreeParentParam == 'Comprehensive Services' || CommonTreeParentParam == 'Complementary Products')) {
                            Common_Tabs('', 'Equipment Details');
                        }
                        else if (subTabName == 'Equipment Details' && (CommonTreeParentParam == 'Quote Items' || CommonTreeParentParam == 'Contract Items' || CommonNodeTreeSuperParentParam == 'Quote Items' || CommonNodeTreeSuperParentParam == 'Contract Items')) {
                            Common_Tabs('', 'Equipment_Details');
                        }
                        else if (subTabName == 'Equipment Details' && (AllTreeParam['TreeParentLevel2'] == 'Quote Items' || CommonNodeTreeSuperParentParam == 'Quote Items')) {
                            Common_Tabs('', 'Equipment_Details');
                        }
                        else if ((subTabName == 'Spare Part Details' && CommonTreeParentParam == 'Quote Items') || (subTabName == 'Spare Part Details' && CommonTreeParentParam == 'Contract Items')) {
                            Common_Tabs('', 'Spare_parts_details');
                        }
                        else if (subTabName == 'Equipment Details') {
                            Common_Tabs('', 'Equipment Details');
                        }
                        else if (subTabName == 'Spare Part Details') {
                            Common_Tabs('', 'Spare Part Details');
                        }
                        //Equipment Entitlements addon cond added
                        // else if (subTabName == 'Equipment Entitlements' &&( TreeSuperTopParentParam =='Product Offerings' || TreeTopSuperParentParam == 'Add-On Products' )) {
                        // 	Common_Tabs('','Equipment Entitlements');
                        // 	}
                        //for entitlement view
                        else if (subTabName == 'Equipment Entitlements' || subTabName == 'Entitlements' || subTabName == 'Assembly Entitlements') {
                            if (TreeParam == 'Add-On Products') {
                                CurrentRecordId = localStorage.getItem("CurrentRecordId")
                            }
                            EntitlementView(CurrentRecordId, ObjName, subTabName, v1);
                        }
                        else if (TreeParam == "Quote Items" && ProductId == "2240" && subTabName == "Summary") {
                            $("#TREE_div").css("display", "none");
                            $("#div_CTR_related_list").css("display", "none");
                            $('.cartContainer').css('display', 'block');
                            $('.fiori3-custom-fields-container').show();
                            $('.line_item_col_hdr').show();
                            $('#Items').css('display', 'block');
                            $(".quote_summary_sec").css("display", "block");
                            $(".quote_summary_new").css("display", "block");
                            hide_year_columns()
                            $("#cust_fields_div").css("display", "block");
                            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css('display', 'none');
                            $('div#COMMON_TABS').find("li a:contains('Product List')").parent().css('display', 'none');
                            $('div#COMMON_TABS').find("li a:contains('Assortment Module')").parent().css('display', 'none');
                            $('div#COMMON_TABS').find("li a:contains('Billing Plan')").parent().css('display', 'none');
                            $(".quote_summary_new").css("display", "none");
                            $(".alert").css("display", "none");
                            cpq.server.executeScript("CQQTEITEMS", {
                                'SUBTAB': "Summary",
                                'ACTION': "VIEW"
                            }, function (dataset) {
								revision_status = dataset[7];
                                if ($(".segment_revision_poes_text .custom").val() == "True") {
                                    $("#custom-fields-section").css("display", "none");
                                    document.getElementById("TREE_div").innerHTML = dataset;
                                } else {
                                    $('#custom-fields-section').css("display", "block");
                                    $('.quote_sec').html(dataset[0]);
                                    $("#ctr_drop").css("display", "inline-block");
									//  INC08890238 M
									$(".quote_tab").find("#ctr_drop").css("display", "inline-block");
									//  INC08890238 M
                                    // $('#total_sales_price').html(dataset[1]);
                                    // $('input#discount').val(dataset[2]);

                                    $('#total_excluding_tax').html(dataset[1]);
                                    $('#total_tax').html(dataset[2]);
                                    $('#total_est_net').html(dataset[3]);
                                    $('#total_amt').html(dataset[4]);
                                    $('#total_margin').html(dataset[5]);
                                    $('#total_margin_pct').html(dataset[6]);
                                }
								//  INC08890238 M
                                option = $("#IdlingAllowed").val();
								//  INC08890238 M
								$(".quote_summary_sec").find('#ctr_drop').css("display", "none");
								//  INC08890238 M
								if ((option == "No" || option == null)) {
								//  INC08890238 M
									$(".quote_tab").find("#ctr_drop").css("display", "none");
								} else {


                $(".quote_tab").find("#ctr_drop").css("display", "inline-block");

								}
                                
                            });
                        }
                        else if (TreeParam == "Contract Items" && ProductId == "2240") {
                            $("#TREE_div").css("display", "none");
                            $("#div_CTR_related_list").css("display", "none");
                            $('.cartContainer').css('display', 'block');
                        }
                        else if (subTabName == "Kit Details") {
                            var openedKit = localStorage.getItem('openedKit');
                            var kitDetailsDisplay = $('div#COMMON_TABS').find("li a:contains('Kit Details')").parent().css("display");
                            if (openedKit != null && kitDetailsDisplay == 'block') {
                                loadDetails(localStorage.getItem('openedKit'), 'SAQSKP', AllTreeParams)
                            }
                        }
                        else if (subTabName == "Document Generator" && TreeParam == "Quote Documents") {
                            cpq.server.executeScript("CQLANGSELT", {
                                'LOAD': 'DOCUMENT',

                            }, function (dataset) {
                                console.log('dataset', dataset)
                                if (document.getElementById("TREE_div")) {
                                    document.getElementById("TREE_div").innerHTML = dataset;
                                    $("#div_CTR_related_list").css("display", "none");
                                    $("#TREE_div").css('display', 'block');
                                }

                            })
                        }
                        else {

                            $('.cartContainer').css('display', 'none');
                            // addon product hyperlink entitilement cond added
                            if (subTabName == 'Equipment Entitlements' || (subTabName == 'Entitlements' && TreeTopSuperParentParam == 'Product Offerings' && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving'))) {
                                CurrentRecordId = localStorage.getItem("CurrentRecordId")
                            }
                            var EquipmentId = localStorage.getItem("EquipmentIdValue")
                            var AssemblyId = localStorage.getItem("AssemblyIdValue")
                            $('.CommonTreeDetail').css('display', 'block');
                            localStorage.setItem('EntCurrentId', CurrentRecordId)
                            if (TreeParentParam == "Quote Items") {
                                CurrentRecordId = TreeParam.split(" -")[0]
                            }
                            getprevdatadict = localStorage.getItem("prventdict");
                            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': v1, 'SubtabName': subTabName, 'EquipmentId': EquipmentId, 'AssemblyId': AssemblyId, 'getprevdatadict': getprevdatadict }, function (dataset) {
                                $("#div_CTR_related_list").css("display", "none");
                                //	$('div#COMMON_TABS').find("li a:contains('Delivery Schedule')").parent().css("display", "none");
                                var [datas, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17, data18, data19, data20, data21, data22, data23, data24, data25, data26, data27, data28, data29, data30, data31, data32, data33, data34, data35, data36, data37, data38, data39] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[6], dataset[7], dataset[8], dataset[9], dataset[10], dataset[11], dataset[12], dataset[13], dataset[14], dataset[15], dataset[16], dataset[17], dataset[18], dataset[19], dataset[20], dataset[21], dataset[22], dataset[23], dataset[24], dataset[25], dataset[26], dataset[27], dataset[28], dataset[29], dataset[30], dataset[31], dataset[32], dataset[33], dataset[34], dataset[35], dataset[36], dataset[37], dataset[38], dataset[39]];
                                if (dataset[8] == "True") {
                                    $('div#COMMON_TABS').find("li a:contains('Add On Products')").parent().css("display", "block");
                                }
                                else {
                                    $('div#COMMON_TABS').find("li a:contains('Add On Products')").parent().css("display", "none");
                                }

                                if (TreeParam == 'Complementary Products') {
                                    if (dataset[9] == "True") {
                                        $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "block");
                                        //$('div#COMMON_TABS').find("li a:contains('Delivery Schedule')").parent().css("display", "none");
                                    }
                                    else {
                                        $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "none");
                                        //$('div#COMMON_TABS').find("li a:contains('Delivery Schedule')").parent().css("display", "none");
                                    }
                                }
                                if (typeof (add_on_products) == "undefined") {
                                    add_on_products = "";
                                }
                                if (add_on_products == "True") {
                                    addon_prd = $('div#COMMON_TABS').find("li a:contains('Add On Products')").parent().css("display", "block").attr("class");
                                    details_tab = $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "block").attr("class");
                                    $("." + addon_prd).click();
                                    $("." + details_tab).removeClass("active");
                                    $("." + addon_prd).addClass("active");
                                    add_on_products = ""

                                }
                                if (TreeParentParam == 'Complementary Products' || TreeParentParam == 'Comprehensive Services') {
                                    if ($(".segment_revision_sale_id_text").text() == 'BOK-CONTRACT BOOKED') {
                                        setTimeout(function () {
                                            $(".dropdown").hide();
                                        }, 2000);

                                    }
                                }
                                localStorage.setItem('Lookupobjd', data5)
                                if (document.getElementById("TREE_div")) {
                                    document.getElementById("TREE_div").innerHTML = datas;
                                    //$(".emp_notifiy").css('display','block');
                                    //var getnotifymsg = localStorage.getItem('getbannermessage');
                                    /*if (getnotifymsg == "bannerNotify"){
                                    	
                                        var getdata = localStorage.getItem('getbannerdetail');
                                        $(".emp_notifiy").css('display','block');
                                        $(".alertnotify").html(getdata)
                                    }*/

                                    $("#div_CTR_related_list").css("display", "none");
                                    $("#TREE_div").css('display', 'block');

                                    if (localStorage.getItem("EntRefresh") == "YES") {
                                        $("#TREE_div").css('display', 'none');
                                        $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().click();
                                        $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
                                        $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().addClass('active');
                                        localStorage.setItem("EntRefresh", "NO");
                                    }
                                    if (data5 == "SAQRIB") {
                                        var div_text = $('#TREE_div').text()
                                        if (div_text.includes('Billing Matrix is not applicable') || div_text.includes('No Records')) {
                                            $('#COMMON_TABS').css('display', 'block');
                                            try {

                                                $('.QuotesBillingYear_1').click();
                                                $('.QuotesBillingYear_1').addClass('active');
                                                $('.QuotesBillingDetails').removeClass('active');

                                            }
                                            catch (e) {
                                                console.log(e);
                                            }
                                        }
                                        else {
                                            $('#COMMON_TABS').css('display', 'block');
                                            try {

                                                $('.QuotesBillingYear_1').click();
                                                $('.QuotesBillingYear_1').addClass('active');
                                                $('.QuotesBillingDetails').removeClass('active');

                                            }
                                            catch (e) {
                                                console.log(e);
                                            }

                                        }

                                    }
                                    if (subTabName == 'Equipment Entitlements' || subTabName == 'Entitlements' || subTabName == 'Assembly Entitlements') {
                                        // Enabling Add On Products in Entitlements subtab
                                        if (subTabName == 'Entitlements' && TreeParentParam == "Comprehensive Services") {
                                            $('div#COMMON_TABS').find("li a:contains('Add On Products')").parent().css("display", "block");
                                            $('#PageAlert').show();
                                        }
                                        document.getElementById('TREE_div').innerHTML = data7
                                        $('#TREE_div').prepend(datas);
                                        $('#Headerbnr').css('display', 'block');
                                        localStorage.setItem('EDITENT_SEC', '');
                                        localStorage.setItem("prvdatadict", JSON.stringify(data8));

                                        $.each(data8, function (k, v) {

                                            $.each(v, function (index2, value2) {
                                                ctid = 'sec_' + index2


                                                $('#' + index2).bootstrapTable({
                                                    data: value2
                                                });

                                                //Hide the section , if the section does not nave attributes to show code starts....
                                                if (TabName != "Contracts") {
                                                    if (data38.includes(ctid)) {

                                                        $('#' + ctid).css('display', 'none');
                                                        $('#' + index2).css('display', 'none');
                                                    }
                                                }
                                                //Hide the section , if the section does not nave attributes to show code ends...
                                                if (value2 == '') {

                                                    $('#' + index2).html('<div class="noRecDisp">No Records to Display</div>');
                                                }
                                                if (typeof (pre_rec_id) == 'undefined' || index2 != pre_rec_id) {
                                                    $("#" + index2 + "  tbody tr").addClass('hovergreyent');
                                                    $("#" + index2 + "  tbody tr td:nth-child(2)").css('text-align', 'left');
                                                    $("#" + index2 + "  tbody tr td:nth-child(2)").each(function () { var ent_desc = $(this).text(); $(this).html(ent_desc); });
                                                    $("#" + index2 + "  tbody tr td:nth-child(3)").each(function () { var ent_val = $(this).text(); $(this).html(ent_val); });
                                                    $("#" + index2 + "  tbody tr td:nth-child(4)").each(function () { var data_typrval = $(this).text(); $(this).html(data_typrval); });
                                                    $("#" + index2 + "  tbody tr td:nth-child(1)").each(function () { var ent_val_im = $(this).text(); $(this).html(ent_val_im); });
                                                    $("#" + index2 + "  tbody tr td:nth-child(6)").each(function () { var factcurr = $(this).text(); $(this).html(factcurr); });
                                                    $("#" + index2 + "  tbody tr td:nth-child(5)").each(function () { var ent_val_cf = $(this).text(); $(this).html(ent_val_cf); });
                                                    $("#" + index2 + "  tbody tr td:nth-child(7)").each(function () { var ent_val_imp = $(this).text(); $(this).html(ent_val_imp); });
                                                    $("#" + index2 + "  tbody tr td:nth-child(8)").each(function () { var ent_val_primp = $(this).text(); $(this).html(ent_val_primp); });
                                                }
                                                pre_rec_id = index2
                                                if (data15 === undefined || data15 == null) { data15 = "" }
                                                if (data16 === undefined || data16 == null) { data16 = "" }
                                                if (data17 === undefined || data17 == null) { data17 = "" }
                                                if (data18 === undefined || data18 == null) { data18 = "" }
                                                if (data19 === undefined || data19 == null) { data19 = "" }
                                                if (data20 === undefined || data20 == null) { data20 = "" }
                                                if (data21 === undefined || data21 == null) { data21 = "" }
                                                if (data23 === undefined || data23 == null) { data23 = "" }
                                                if (data24 === undefined || data24 == null) { data24 = "" }
                                                if (data22 === undefined || data22 == null) { data22 = "" }
                                                if (data26 === undefined || data26 == null) { data22 = "" }
                                                if (data27 === undefined || data27 == null) { data27 = "" }
                                                if (data28 === undefined || data28 == null) { data28 = "" }
                                                if (data29 === undefined || data29 == null) { data29 = "" }
                                                if (data30 === undefined || data30 == null) { data30 = "" }
                                                if (data31 === undefined || data31 == null) { data31 = "" }
                                                if (data32 === undefined || data32 == null) { data32 = "" }
                                                if (data33 === undefined || data33 == null) { data33 = "" }
                                                if (data34 === undefined || data34 == null) { data34 = "" }
                                                if (data35 === undefined || data35 == null) { data35 = "" }
                                                if (data36 === undefined || data36 == null) { data36 = "" }
                                                var deinstall = $('#INSTALLATION_LABOR_Z_07').val();



                                            });

                                        });
                                        if (data39 != "" && data39 != undefined) {
                                            arr_list = data39

                                            for (const [key, value] of Object.entries(arr_list)) {
                                                if (value != "") {
                                                    defaultText = value
                                                }
                                                else {
                                                    defaultText = 'Select Below'
                                                }
                                                $("#" + key).CreateMultiCheckBox({ width: '230px', defaultText: defaultText, height: '250px', attr_id: key });
                                                $('#' + key).closest('td').attr('title', defaultText);
                                            };

                                        }

                                        $.each(data11, function (index, value) {
                                            $("#" + value).closest('tr').css('display', 'none');
                                        });
                                        if (data13 != '' && data13 != null) {
                                            $.each(data13, function (index, value) {
                                                $('#' + value).css('color', '#0060B1');
                                            });
                                        }
                                        
                                        try {
                                            eval(data9);
                                            eval(data37)
                                            if (subTabName != 'Assembly Entitlements') {
                                                if ($('#approve_status').text() == "APPROVALS") {
                                                    eval(data9);
                                                }
                                                var getdataprevent = eval(data10)

                                            }
                                        } catch { console.log('error---') }
                                    }
                                    //A055S000P01-8873 hide entitlement attribute 
                                    if (subTabName == 'Entitlements' && AllTreeParam['TreeParentLevel1'] == 'Z0091' && (AllTreeParam['TreeParam'] == 'PDC' || AllTreeParam['TreeParam'] == 'MPS')) {
                                        $('#AGS_Z0091_NET_PRMALB').closest('tr').css('display', 'none');
                                    }

                                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                    popover()
                                    if (CurrentTab == "Quotes") {
                                        //var getopptype = $( "#QSTN_SYSEFL_QT_00723 option:selected" ).text();
                                        var getopptype = localStorage.getItem("getopptype")
                                    }
                                    else if (CurrentTab == "Contracts") {
                                        var getopptype = $("#QSTN_SYSEFL_QT_016912 option:selected").text();
                                    }
                                    else if (CurrentTab == "Currency" && TreeParentParam == "Sales Orgs" && subTabName == "Details") {
                                        breadCrumb_Reset()
                                    }


                                    if (getopptype == "ZTBC - TOOL BASED") {
                                        $('.CC119201-572D-41BB-8C53-5C063EEAAD4F').css('display', 'none');
                                        //$(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display','none');


                                    }
                                    //if (getopptype == "ZWK1 - SPARES")
                                    if (getopptype == "ZWK1") {
                                        $('.F5414216-018E-47EB-9778-53F0FD95D273').css('display', 'none');
                                        $(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display', 'block');
                                        // Billing Matrix - Start
                                        // If there no Billing Matrix record, show the notification and hide the Subtab 
                                        if (datas.indexOf('Billing Matrix is not applicable for this Quote configuration.') != -1) {
                                            $('#COMMON_TABS').css('display', 'none');
                                        }
                                        // Billing Matrix - End
                                    }

                                }
                                onFieldChanges();
                                /*save_flag = localStorage.getItem("save_flag");
                                if(AllTreeParam['TreeParentLevel1'] == 'Receiving Equipment' && subTabName == 'Equipment Entitlements' && save_flag == 'True' ){
                                    localStorage.setItem("save_flag",'false')
                                    getprevdatadict = localStorage.getItem("prventdict");
                                    ent_dict_new = JSON.parse(localStorage.getItem("ent_dict_new"))
                                    try {
                                        cpq.server.executeScript("CQENTLMENT", {
                                            'ACTION': 'SAVE',
                                            'newdict': "",
                                            'subtabName': subTabName,
                                            'EquipmentId':EquipmentId,'ENT_IP_DICT':ent_dict_new,
                                            'getprevdict': getprevdatadict,				
                                        }, function (datas) {
                                                                            	
                                        });
                                    } catch (e) {
                                        console.log(e);
                                    }
                        	
                                }*/
                            });

                            if (subTabName == 'Details' && AllTreeParam['TreeParentLevel1'] == 'Quote Items') {
                                Subbaner("Details", CurrentNodeId, CurrentRecordId, 'SAQIFL');
                            }
                            if (subTabName == 'Details' && (AllTreeParam['TreeParentLevel3'] == 'Product Offerings' && AllTreeParam['TreeParentLevel0'] != 'Add-On Products' && AllTreeParam['TreeParentLevel0'] != 'Sending Equipment' && AllTreeParam['TreeParentLevel0'] != 'Receiving Equipment')) {
                                Subbaner("Details", CurrentNodeId, CurrentRecordId, 'SAQSgb');
                            }
                            // if (subTabName == 'Details' && AllTreeParam['TreeParentLevel1'] == 'Fab Locations'){
                            // 	Subbaner("Details",CurrentNodeId,CurrentRecordId,'SAQFGB');
                            // }
                            if (subTabName == 'Entitlements' && TreeTopSuperParentParam == 'Quote Items') {
                                Subbaner(subTabName, CurrentNodeId, CurrentRecordId, 'SAQICO');
                            }
                            if (subTabName == 'Entitlements' && TreeParam == 'Quote Items') {
                                Subbaner(subTabName, CurrentNodeId, CurrentRecordId, 'SAQITE');
                            }
                            if (CurrentTab == "Quotes") {
                                //var getopptype = $( "#QSTN_SYSEFL_QT_00723 option:selected" ).text();
                                var getopptype = localStorage.getItem("getopptype")
                            }
                            else if (CurrentTab == "Contracts") {
                                var getopptype = $("#QSTN_SYSEFL_QT_016912 option:selected").text();
                            }


                            if (getopptype == "ZTBC - TOOL BASED") {
                                $('.CC119201-572D-41BB-8C53-5C063EEAAD4F').css('display', 'none');
                                //$(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display','none');
                            }
                        }
                    }
                }
                if (CurrentTab == "Quotes") {
                    //var getopptype = $( "#QSTN_SYSEFL_QT_00723 option:selected" ).text();
                    var getopptype = localStorage.getItem("getopptype");
                }
                else if (CurrentTab == "Contracts") {
                    var getopptype = $("#QSTN_SYSEFL_QT_016912 option:selected").text();
                }


                if (getopptype == "ZTBC - TOOL BASED") {
                    $('.CC119201-572D-41BB-8C53-5C063EEAAD4F').css('display', 'none');
                    //$(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display','none');
                }
                //if (getopptype == "ZWK1 - SPARES")
                if (getopptype == "ZWK1") {
                    $('.F5414216-018E-47EB-9778-53F0FD95D273').css('display', 'none');
                    $(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display', 'block');
                }



            });
        });
    });
    if ((TreeParam == "Add-On Products") && (ObjName == "SAQSAO" || ObjName == "SAQRCV")) {
        adnprd_id = localStorage.getItem('TreeParamRecordId');
        if (!$('.breadcrumb').text().includes(adnprd_id)) {
            breadCrumb_Reset();
            chainsteps_breadcrumb(adnprd_id);
        }
    }
    if (subTabName == 'Equipment' && TreeSuperParentParam == 'Quote Items') {
        Subbaner("Details", CurrentNodeId, CurrentRecordId, 'SAQICO');
    }
    if (subTabName == 'Equipment' && CommonTreeParam == "Fab Locations") {
        breadCrumb_Reset()
    }
    if (subTabName == 'Equipment Details' && CommonTopSuperParentParam == 'Fab Locations') {
        breadCrumb_Reset()
    }
    if (subTabName == 'Equipment' && (AllTreeParam['TreeParentLevel0'] == 'Fab Locations' || AllTreeParam['TreeParentLevel1'] == 'Fab Locations' || AllTreeParam['TreeParentLevel2'] == 'Fab Locations')) {
        breadCrumb_Reset()
    }
    if ((subTabName == 'Approvers' || subTabName == 'Tracked Fields') && AllTreeParam['TreeParentLevel0'] == 'Approval Chain Steps') {
        breadCrumb_Reset()
        chainsteps_breadcrumb(subTabName)
        Subbaner(subTabName, CurrentNodeId, RecId, ObjName);
    }
    else {
        // To restrict repeated scripts execution  - starts
        if (typeof (equipment_details) == 'undefined') {
            equipment_details = "False"
        }
        if (equipment_details == "True") {

            equipment_details = "False"
        }
        if ((subTabName != "Sending Equipment" && subTabName != "Receiving Equipment") && TreeSuperParentParam == "Complementary Products") {
            $('#ADDNEW__SYOBJR_98800_SYOBJ_00904').css('display', 'none')
            Subbaner(subTabName, CurrentNodeId, CurrentRecordId, ObjName);
        }
        else {
            if (CurrentNodeId == "" || CurrentNodeId == null || CurrentNodeId == undefined) {
                CurrentNodeId = node.nodeId
            }
            Subbaner(subTabName, CurrentNodeId, CurrentRecordId, ObjName);
            if (subTabName == "Annualized Items") { $('#CALCULATE_QItems').css('display', 'none'); }
            //if (subTabName == "Subtotal by Offerings"){
            //console.log('575687678-----')

            //var itemsTable = $('#itemsTable');
            //if(itemsTable.children().length == 0)
            //{
            //console.log('no records');
            //itemsTable.html("<tr id = 'itemhide_generate'><td colspan='18'><div class='noRecDisp'>No Records to Display</div></td></tr>")
            //}

            //}
        }
        // To restrict repeated scripts execution  - ends
    }
    if (CurrentTab == "Quotes") {
        //QuoteStatus();
        dynamic_status();
    }
}


function doc_attachment() {
    $(".fileupload-preview").html("");
    $(".attchSelect select option:first").prop("selected", true);
    att_filename = $(".fileupload-preview").text();
    att_type = $("#attachment_type").val();



    setTimeout(function () {
        $("#docAttachement").contents().find("body").addClass("bodyAttachment");
    }, 50);

    setTimeout(function () {
        var $iframe = $("#docAttachement");
        $iframe.ready(function () {
            $iframe.contents().find("body.bodyAttachment .fileUploadInput label").html("Attachment File Name");
            $iframe.contents().find("body.bodyAttachment .fileUploadInput form div.input-group span.btn-file span").css("visibility", "hidden");
            $iframe.contents().find("body.bodyAttachment #fileUploadInput span.uploadFileName").text("");
            $iframe
                .contents()
                .find("body.bodyAttachment .fileUploadInput form div.input-group span.btn-file")
                .after(' <a class="attachmentIcon"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/document_upload_icon.svg"></a>');
            $iframe.contents().find("body.bodyAttachment .fileUploadInput form div.input-group-btn span.btn-file a.fileupload-new").hide();
            $iframe.contents().find("body.bodyAttachment .fileUploadInput .attInfoIcon").slice(1).remove();
            $iframe.contents().find("body.bodyAttachment .fileUploadInput .atthAstricIcon").slice(1).remove();
            $iframe.contents().find("body.bodyAttachment .fileUploadInput .attachmentIcon").slice(1).remove();
            $iframe.contents().find("body.bodyAttachment .fileUploadInput .attachEdit").slice(1).remove();
            $iframe.contents().find("body.bodyAttachment .fileUploadInput .fa-file").hide();

            //  $iframe.contents().find("body.bodyAttachment #wrap").hide();

            $iframe.contents().find("body.bodyAttachment  .input-group-btn .fileupload-preview").after('<span class="fileupload-filename"></span>');

            $iframe
                .contents()
                .find("body.bodyAttachment  input[type='file']")
                .attr(
                    "onchange",
                    '(function(e){ e.preventDefault(); $("#fileUploadInput span").remove();let filenames = [];dile = e.target.files;for (let i in dile) {if (dile.hasOwnProperty(i)) { filenames.push(dile[i].name) }} $(".fileupload-preview").hide(); $("#fileUploadInput i").after("<span class=uploadFileName>"+ filenames.join(",") +"</span>"); localStorage.setItem("file_name",filenames.join(","));console.log(filenames.join(","));})(event)'
                );

            //$iframe.contents().find("body.bodyRFOAttachment input[type='file']").attr('test', 'FunctionNam');
            $iframe.contents().find("body.bodyAttachment  .input-group-btn .fileupload-new i.fa").hide();

        });
    }, 500);


}


/* To load the Right side content of the Tree view based on the selected node on the Left side 'Begin' */
function Common_enable_disable(id) {

    var TreeNodeName = GridtableName = RecName = RecId = child = childrenNodes = data = data1 = CurrentTab = CurrentRecordId = CurrentNodeId = node = TreeParam = TreeParentParam = TreeParentNodeId = TreeParentNodeRecId = TreeSuperParentParam = TreeSuperParentId = TreeSuperParentRecId = TreeTopSuperParentParam = TreeTopSuperParentId = TreeTopSuperParentRecId = TreeSuperTopParentParam = TreeSuperTopParentRecId = TreeSuperTopParentId = TreeFirstSuperTopParentParam = TreeFirstSuperTopParentId = TreeFirstSuperTopParentRecId = GrandTreeFirstSuperTopParentParam = GrandTreeFirstSuperTopParentId = GrandTreeFirstSuperTopParentRecId = Grand_GrandTreeFirstSuperTopParentParam = Grand_GrandTreeFirstSuperTopParentId = Grand_GrandTreeFirstSuperTopParentRecId = '';

    CurrentNodeId = localStorage.getItem("CurrentNodeId");
    CurrentRecordId = localStorage.getItem("Rel_List_Rec_ID");
    //A043S001P01-11642 start
    AllTreeParams = JSON.parse(localStorage.getItem('AllTreeParams'));
    //A043S001P01-11642 end
    $('#COMMON_TABS').css('display', 'none');
    //A043S001P01-9621 start
    $(".Award_Group_segment_Revision_Id").css("display", "none");
    //A043S001P01-9621 end
    //A043S001P01-12462 Start,A043S001P01-9628 Start
    $(".common_profile_app").css("display", "none");
    $(".common_profile_tab").css("display", "none");
    $(".common_profile_Sec").css("display", "none");
    $(".common_profile_Obj").css("display", "none");
    //A043S001P01-12462,A043S001P01-9628 end
    //A043S001P01-11642 start
    $(".Attribute_Tab_Id").css("display", "none");
    $(".Attribute_Value_Subtab").css("display", "none");

    $(".Rule_Tab_Id").css("display", "none");
    $('#Rule_Actions_id').css('display', 'none');
    $('#Rule_Details_id').css('display', 'none');
    $(".Personalization_Tab_Id").css("display", "none");
    $('#Personalization_Details_id').css('display', 'none');
    $('#Personalization_Attributes_id').css('display', 'none');
    $('#Attribute_Details_id').css('display', 'none');
    $('#Attribute_Values_id').css('display', 'none');
    $('#Attribute_Dependency_Rule_id').css('display', 'none');
    $('.Layout_tabs_cls_Id').css('display', 'none');
    $('#Layout_Details_id').css('display', 'none');
    $('#Layout_tabs_id').css('display', 'none');
    $('#Layout_sections_id').css('display', 'none');
    $('#Layout_questions_id').css('display', 'none');
    $('#Layout_Preview_id').css('display', 'none');
    $('#Perz_AttrVal_Details_id').css('display', 'none');
    $('#Perz_AttrVal_id').css('display', 'none');
    $(".Perz_AttrVal_Tab").css("display", "none");
    $(".Layout_qstn_Id").css("display", "none");
    $(".Attributes_cls_dtls").css("display", "none");
    $('#Attributecls_dtl_id').css('display', 'none');
    $('#Attribute_at_id').css('display', 'none');
    $('#Layout_Rules_id').css('display', 'none');
    //A043S001P01-11642 end
    //A043S001P01-6118 start
    $(".common_AttrVal_Attr_Tab").css("display", "none");
    //A043S001P01-6118 end
    // price classes
    $(".Price_Class_Price_Factors_Details").css("display", "none");
    //price classes
    //$('.row.tab-content.bg_wt').css('display','none');
    //A043S001P01-9694 start
    $(".Service_Details_Programs").css("display", "none");
    $('#service_Details_id').css('display', 'none');
    $('#service_Programs_id').css('display', 'none');
    //A043S001P01-9694 end
    //$(".common_Where_Used_Prog_Tab_Detail").css("display", "none");
    $(".common_Award_Levels_Lvl1_Prog_Tab_Detail").css("display", "none");
    $(".common_Prog_Quotas_Lvl1_Prog_Tab_Detail").css("display", "none");
    $('.Prc_Mthd_Entry_Tab').css('display', 'none');
    $('#seginnerbnr').css('display', 'none');
    $('#seginner_relbnr').css('display', 'none');
    $(".fullviewdiv").css("display", "none");
    $(".Quotas_detail_Accounts").css("display", "none");
    $(".Quotas_Related_Accounts").css("display", "none");
    $('.Assignment_Related_Accounts').css("display", "none");
    $(".Program_Related_Accounts").css("display", "none");
    $(".Participant_Related_Accounts").css("display", "none");
    // A043S001P01-12165 STARTS
    $(".Account_Participant_Related_Accounts").css("display", "none");
    // A043S001P01-12165 ENDS
    $(".category_program_quota").css("display", "none");
    // A043S001P01-10455 Start
    $('.SegRevPricebookset').hide();
    $('.SegRevApprRuleLvl').hide();
    $('.SegRevApprRule').hide();
    $('.SegRevApprCond').hide();
    $('.SegRevPricemodel').hide();
    // A043S001P01-10455 End
    //A043S001P01-10425 START
    $(".common_Where_Used_Prog_tpy_Tab").css("display", "none");
    $(".common_Account_Quotas_Lvl1_QuoCat_Tab_Detail").css("display", "none");
    //A043S001P01-10425 END
    // A043S001P01-12164 STARTS
    $(".Account_tab_Participant_Related_Accounts").css('display', 'none');
    // A043S001P01-12164 ENDS
    $('.common_Account_Quotas_Lvl5').css('display', 'none');
    $('.Quota_Category_Program_types').css('display', 'none');

    $('.Fulfillment_Combo_Models_page').css('display', 'none');
    $('.Countries_fulfilled').css('display', 'none');
    $('.Fulfillment_Combo_Models').css('display', 'none');
    // A043S001P01-12254 Start
    $("#FirstSecInformation").find(".fullviewdiv").remove()
    //A043S001P01-12254 End
    $('.Fulfillment_vendor').css('display', 'none');
    $(".SegmentQuerybuilderclass").css("display", "none");
    node = $('#commontreeview').treeview('getNode', CurrentNodeId);
    CurrentNodeId = node.nodeId
    CurrentRecordId = node.id;
    //CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
    CurrentTab = $("ul#carttabs_head li.active a span").text();
    var node_text_var = node.text;

    if (typeof (node_text_var) != 'function' && node_text_var.includes("<span")) {
        TreeParam = node_text_var.split(">").pop();
    }
    else {
        TreeParam = node_text_var
    }
    if (TreeParam.includes("<img")) {
        TreeParam = TreeParam.split(">")
        TreeParam = TreeParam[TreeParam.length - 1]
    } else {
        TreeParam = TreeParam
    }
    if (TreeParam.includes("-")) {

        if (!TreeParam.includes('- BASE') && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving')) {
            TreeParam = TreeParam.split("-")[0].trim()
        }
    } else {
        TreeParam = TreeParam
    }
    ObjName = node.objname;
    localStorage.setItem('Rel_List_Rec_ID', CurrentRecordId)
    localStorage.setItem("CurrentNodeId", CurrentNodeId);
    data1 = localStorage.getItem('CommonTreedatasetnew');
    if (CurrentTab == 'Quota Category') {
        $('.container_banner_inner_sec').css('display', 'none');
    }
    if (data1) {
        data = data1.split(',');
    }
    $('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), { silent: true }]);
    if (CurrentNodeId != '' && CurrentNodeId != null) {
        TreeParentParam = $('#commontreeview').treeview('getParent', CurrentNodeId).text;
        if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("<img")) {
            // TreeParentParam = TreeParentParam.split(">")[1];
            TreeParentParam = TreeParentParam.split(">")
            TreeParentParam = TreeParentParam[TreeParentParam.length - 1];
        }
        if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("-")) {
            if (!TreeParentParam.includes('- BASE')) {
                TreeParentParam = TreeParentParam.split("-")[0].trim()
            }
        }
        TreeParentNodeId = $('#commontreeview').treeview('getParent', CurrentNodeId).nodeId;
        TreeParentNodeRecId = $('#commontreeview').treeview('getParent', CurrentNodeId).id;
    }
    if (TreeParentNodeId != '' && TreeParentNodeId != null) {
        TreeSuperParentParam = $('#commontreeview').treeview('getParent', TreeParentNodeId).text;
        if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("<img")) {
            // TreeSuperParentParam = TreeSuperParentParam.split(">")[1];
            TreeSuperParentParam = TreeSuperParentParam.split(">")
            TreeSuperParentParam = TreeSuperParentParam[TreeSuperParentParam.length - 1];
        }
        TreeSuperParentId = $('#commontreeview').treeview('getParent', TreeParentNodeId).nodeId;
        TreeSuperParentRecId = $('#commontreeview').treeview('getParent', TreeParentNodeId).id;
    }
    if (TreeSuperParentId != '' && TreeSuperParentId != null) {
        TreeTopSuperParentParam = $('#commontreeview').treeview('getParent', TreeSuperParentId).text;
        if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
            //   TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")[1];
            TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")
            TreeTopSuperParentParam = TreeTopSuperParentParam[TreeTopSuperParentParam.length - 1];
        }
        if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("-")) {
            if (!TreeTopSuperParentParam.includes('- BASE')) {
                TreeTopSuperParentParam = TreeTopSuperParentParam.split("-")[0].trim()
            }
        }
        TreeTopSuperParentId = $('#commontreeview').treeview('getParent', TreeSuperParentId).nodeId;
        TreeTopSuperParentRecId = $('#commontreeview').treeview('getParent', TreeSuperParentId).id;
    }
    if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null) {
        TreeSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).text;
        if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeSuperTopParentParam.includes("<img")) {
            //   TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")[1];
            TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")
            TreeSuperTopParentParam = TreeSuperTopParentParam[TreeSuperTopParentParam.length - 1];
        }
        if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeSuperTopParentParam.includes("-")) {
            if (!TreeSuperTopParentParam.includes('- BASE')) {
                TreeSuperTopParentParam = TreeSuperTopParentParam.split("-")[0].trim()
            }
        }
        TreeSuperTopParentId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
        TreeSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).id;
    }
    if (TreeSuperTopParentId != '' && TreeSuperTopParentId != null) {
        TreeFirstSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).text;
        if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeFirstSuperTopParentParam.includes("<img")) {
            //    TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")[1];
            TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")
            TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam[TreeFirstSuperTopParentParam.length - 1];
        }
        if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeFirstSuperTopParentParam.includes("-")) {
            if (!TreeFirstSuperTopParentParam.includes('- BASE')) {
                TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split("-")[0].trim()
            }
        }
        TreeFirstSuperTopParentId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).nodeId;
        TreeFirstSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).id;
    }

    if (TreeFirstSuperTopParentId != '' && TreeFirstSuperTopParentId != null) {
        GrandTreeFirstSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeFirstSuperTopParentId).text;
        if (GrandTreeFirstSuperTopParentParam != '' && GrandTreeFirstSuperTopParentParam != undefined && (typeof GrandTreeFirstSuperTopParentParam === 'string' || GrandTreeFirstSuperTopParentParam instanceof String) && GrandTreeFirstSuperTopParentParam.includes("<img")) {
            //  GrandTreeFirstSuperTopParentParam = GrandTreeFirstSuperTopParentParam.split(">")[1];
            GrandTreeFirstSuperTopParentParam = GrandTreeFirstSuperTopParentParam.split(">")
            GrandTreeFirstSuperTopParentParam = GrandTreeFirstSuperTopParentParam[GrandTreeFirstSuperTopParentParam.length - 1];
        }
        if (GrandTreeFirstSuperTopParentParam != '' && GrandTreeFirstSuperTopParentParam != undefined && (typeof GrandTreeFirstSuperTopParentParam === 'string' || GrandTreeFirstSuperTopParentParam instanceof String) && GrandTreeFirstSuperTopParentParam.includes("-")) {
            if (!GrandTreeFirstSuperTopParentParam.includes('- BASE')) {
                GrandTreeFirstSuperTopParentParam = GrandTreeFirstSuperTopParentParam.split("-")[0].trim()
            }
        }
        GrandTreeFirstSuperTopParentId = $('#commontreeview').treeview('getParent', TreeFirstSuperTopParentId).nodeId;
        GrandTreeFirstSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeFirstSuperTopParentId).id;
    }
    if (GrandTreeFirstSuperTopParentId != '' && GrandTreeFirstSuperTopParentId != null) {
        Grand_GrandTreeFirstSuperTopParentParam = $('#commontreeview').treeview('getParent', GrandTreeFirstSuperTopParentId).text;
        if (Grand_GrandTreeFirstSuperTopParentParam != '' && Grand_GrandTreeFirstSuperTopParentParam != undefined && (typeof Grand_GrandTreeFirstSuperTopParentParam === 'string' || Grand_GrandTreeFirstSuperTopParentParam instanceof String) && Grand_GrandTreeFirstSuperTopParentParam.includes("<img")) {
            //    Grand_GrandTreeFirstSuperTopParentParam = Grand_GrandTreeFirstSuperTopParentParam.split(">")[1];
            Grand_GrandTreeFirstSuperTopParentParam = Grand_GrandTreeFirstSuperTopParentParam.split(">")
            Grand_GrandTreeFirstSuperTopParentParam = Grand_GrandTreeFirstSuperTopParentParam[Grand_GrandTreeFirstSuperTopParentParam.length - 1];
        }
        if (Grand_GrandTreeFirstSuperTopParentParam != '' && Grand_GrandTreeFirstSuperTopParentParam != undefined && (typeof Grand_GrandTreeFirstSuperTopParentParam === 'string' || Grand_GrandTreeFirstSuperTopParentParam instanceof String) && Grand_GrandTreeFirstSuperTopParentParam.includes("-")) {
            if (!Grand_GrandTreeFirstSuperTopParentParam.includes('- BASE')) {
                Grand_GrandTreeFirstSuperTopParentParam = Grand_GrandTreeFirstSuperTopParentParam.split("-")[0].trim()
            }
        }
        Grand_GrandTreeFirstSuperTopParentId = $('#commontreeview').treeview('getParent', GrandTreeFirstSuperTopParentId).nodeId;
        Grand_GrandTreeFirstSuperTopParentRecId = $('#commontreeview').treeview('getParent', GrandTreeFirstSuperTopParentId).id;
    }

    if (TreeSuperParentId === undefined) {
        TreeSuperParentParam = '';
    }
    if (TreeTopSuperParentId === undefined) {
        TreeTopSuperParentParam = '';
    }
    if (TreeSuperTopParentRecId === undefined) {
        TreeSuperTopParentParam = '';
    }
    if (TreeFirstSuperTopParentRecId === undefined) {
        TreeFirstSuperTopParentParam = '';
    }
    try {
        childrenNodes = _getChildren(node);
        if (childrenNodes.length > 0) {
            child = 'true';
        }
        else {
            child = 'false';
        }
    }
    catch (e) {
        child = '';
    }

    localStorage.setItem('CommonTreeParam', TreeParam);
    localStorage.setItem('CommonTreeParentParam', TreeParentParam);
    localStorage.setItem('CommonNodeTreeSuperParentParam', TreeSuperParentParam);
    localStorage.setItem('CommonTopSuperParentParam', TreeTopSuperParentParam);
    localStorage.setItem('common_TreeFirstSuperTopParentParam', TreeFirstSuperTopParentParam)
    localStorage.setItem('CommonParentNodeRecId', TreeParentNodeRecId);
    localStorage.setItem('CommonTreeSuperParentRecId', TreeSuperParentRecId);
    localStorage.setItem('CommonTopSuperParentRecId', TreeTopSuperParentRecId);
    localStorage.setItem('CommonSuperTopParentParam', TreeSuperTopParentParam);
    var a = '0';
    if (!TreeSuperParentParam) {

        a = '1';
    }


    setTimeout(function () {

        if (!TreeParentParam) {
            TreeSuperParentParam = '';
        }
        if (TreeSuperParentParam) {

            if (a == '1') {
                TreeSuperParentParam = '';
            }
        }
        var unique_breadcrumb_list = [Grand_GrandTreeFirstSuperTopParentParam, GrandTreeFirstSuperTopParentParam, TreeFirstSuperTopParentParam, TreeSuperTopParentParam, TreeTopSuperParentParam, TreeSuperParentParam, TreeParentParam, TreeParam];
        var unique_breadcrumb_list_filtered = unique_breadcrumb_list.filter(function (el) {
            return el != '' || el.indexOf('function(e)') != -1 || el.indexOf('ƒ (e)') != -1 || el.indexOf('ƒ') != -1;
        });

        var build_breadcrumb = '<ul class="breadcrumb">'
        $(unique_breadcrumb_list_filtered).each(function (index) {
            build_breadcrumb += '<li><a onclick="tree_breadCrumb_redirection(this,parent_node)"><abbr title="' + unique_breadcrumb_list_filtered[index] + '">';
            build_breadcrumb += unique_breadcrumb_list_filtered[index];
            build_breadcrumb += '</abbr></a><span class="angle_symbol"><img src = "/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"/></span></li>'
        });
        build_breadcrumb += '</ul>'

        $('div#header_label').html(build_breadcrumb);

        $('ul.breadcrumb > li > a').each(function (index) {

            var a = $(this).text();

            if (a.indexOf('function(e)') != -1) {
                $(this).parent('li').remove();
            }
        });

        $('div#header_label ul.breadcrumb abbr[title=null]').closest('li').remove();

        var header_label_parent_height = $('div#header_label').parent().css('height');
        var breadcrumb_height = $('div#header_label ul.breadcrumb').css('height');
        var header_label_parent_height_split = header_label_convert_to_int = breadcrumb_height_split = breadcrumb_height_convert_to_int = header_label_parent_width_split = header_label_width_convert_to_int = breadcrumb_width_split = breadcrumb_width_convert_to_int = '';
        if (header_label_parent_height) {
            header_label_parent_height_split = header_label_parent_height.split('px');
            header_label_convert_to_int = parseInt(header_label_parent_height_split[0]);
        }
        if (breadcrumb_height) {
            breadcrumb_height_split = breadcrumb_height.split('px');
            breadcrumb_height_convert_to_int = parseInt(breadcrumb_height_split[0]);
        }

        var header_label_parent_width = $('div#header_label').parent().css('width');
        if (header_label_parent_width) {
            header_label_parent_width_split = header_label_parent_width.split('px');
            header_label_width_convert_to_int = parseInt(header_label_parent_width_split[0]) - 50;
        }

        var breadcrumb_width = $('div#header_label ul.breadcrumb').css('width');
        if (breadcrumb_width) {
            breadcrumb_width_split = breadcrumb_width.split('px');
            breadcrumb_width_convert_to_int = parseInt(breadcrumb_width_split[0]);
        }


        var breadcrumb_content_length = unique_breadcrumb_list_filtered.length;
        var set_width_for_breadcrumb = set_width_for_breadcrumb_px = set_width_for_breadcrumb_level2 = set_width_for_breadcrumb_level2_last = '';
        set_width_for_breadcrumb = parseInt(header_label_parent_width_split[0] / breadcrumb_content_length);
        set_width_for_breadcrumb_px = set_width_for_breadcrumb + 'px';
        set_width_for_breadcrumb_level2 = set_width_for_breadcrumb - 20;
        set_width_for_breadcrumb_level2 = set_width_for_breadcrumb_level2 + 'px';
        //set_width_for_breadcrumb_level2_last = set_width_for_breadcrumb - 70;
        //set_width_for_breadcrumb_level2_last = set_width_for_breadcrumb_level2_last + 'px';

        if ((header_label_convert_to_int < breadcrumb_height_convert_to_int) || (breadcrumb_width_convert_to_int > header_label_width_convert_to_int)) {
            $('div#header_label ul.breadcrumb li').css('width', set_width_for_breadcrumb_px);
            $('span.angle_symbol').css('padding', '0 5px 0 0px');
            $('div#header_label').children('ul.breadcrumb').find('a').css('width', set_width_for_breadcrumb_level2);
            //$('div#header_label').children('ul.breadcrumb').children('li:last-child').find('a').css('width',set_width_for_breadcrumb_level2_last);
            $('div#header_label').children('ul.breadcrumb').children('li:last-child').css('float', 'unset');
        }

        $('div#conta7159').parent().css('margin-top', '10px');
        //A043S001P01-8621 START // COMMENTED DUE TO EDIT BUTTON IS SHOWING IN SECTIONAL EDIT.
        /*$('div#righttreeview div[id^=dyn] div#ctr_drop').each(function(index){
    	
        $(this).css('cssText','display:inline-block');
        });*/

        EDIT_DIRECT = localStorage.getItem("DIRECT_EDT")
        if (EDIT_DIRECT) {
            $('div#righttreeview div[id^=dyn] div#ctr_drop').css('display', 'none')
            localStorage.setItem("DIRECT_EDT", "")
        }

        btn_Val = localStorage.getItem("btn_txt_val")
        if (btn_Val == 'ADD NEW') {
            $('div[id^=dyn] div#ctr_drop').css('display', 'none');
        }
        //A043S001P01-8621 END 

        $('table#Used_in_Catalog_Products thead tr th.bs-checkbox .th-inner, table#Used_in_Segment_Revisions thead tr th.bs-checkbox .th-inner').each(function () {
            var sel_catalog_prd = $(this).siblings('.selcatalog_prd').remove();

            $(this).before('<div class="selcatalog_prd">SELECT</div>');


        });


    }, 1500);

    var count_val = 0;
    setInterval(function () {
        if (count_val < 5) {
            var img_src = $('.comm_tree_view .material_btn > .material_btn_bg > .product_tab_icon img').attr('src');
            var first_head = $('.comm_tree_view .material_btn > .material_btn_bg > .product_txt_div span.product_txt').text();
            var first_val = $('.comm_tree_view .material_btn > .material_btn_bg > .product_txt_div span.product_txt_to_top_banner').text();
            var second_head = $('.comm_tree_view .material_btn > .material_btn_bg > .segment_part_number span.segment_part_number_heading').text();
            var second_val = $('.comm_tree_view .material_btn > .material_btn_bg > .segment_part_number span.segment_part_number_text').text();
            var third_head = $('.comm_tree_view .material_btn > .material_btn_bg > .segment_part_description_tree span.segment_part_heading').text();
            var third_val = $('.comm_tree_view .material_btn > .material_btn_bg > .segment_part_description_tree span.segment_part_text').text();

            $('.treeView_inner_ban_details .product_tab_icon img').attr('src', img_src);
            $('.treeView_inner_ban_details span.product_txt').text(first_head);
            $('.treeView_inner_ban_details .product_txt_div span.product_txt_to_top').text(first_val);
            $('.treeView_inner_ban_details .segment_part_number span.segment_part_number_heading').text(second_head);
            $('.treeView_inner_ban_details .segment_part_number span.segment_part_number_text').text(second_val);
            $('.treeView_inner_ban_details .segment_part_description span.segment_part_heading').text(third_head);
            $('.treeView_inner_ban_details .segment_part_description span.segment_part_text').text(third_val);

            count_val = count_val + 1;
        }
    }, 1000);
    /*function Prc_Mthd_Tab(){
            $('#COMMON_TABS').css('display','block');
            $('div#COMMON_TABS').find("li").removeClass('active');
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().addClass('active');
            $("#Prc_Mthd_Details").addClass('active in');
            $('div#COMMON_TABS').find('div').find('div:not(.active)').css('display','none');
            Prc_Mthd_Tabs('Prc_Mthd_Details');
        } */

    if (TreeSuperParentParam == 'Fulfillment by Sales Org') {
        [TreeParentNodeRecId, TreeParentParam] = ['SYOBJR-90047', 'Fulfillment by Sales Org'];
    }
    /*  ####  Price Factor Grid Load Starts--------->     */

    // #### 10236 and 10232 Starts .....


    /*  ####  Price Factor Grid Load Ends--------->     */

    // A043S001P01-9202 start 
    else if ((jQuery.inArray(TreeParam, data) !== -1 || TreeParam == 'Pricing Conditions' || TreeParam == 'Components' || TreeParam == 'Account Quotas' || TreeParam == 'Header Pricing Conditions' || TreeParam == 'Program Participants' || TreeParam == 'Program Types' || TreeParam == 'Eligible Materials' || TreeParam == 'Invoice Lines' || TreeParam == 'Sales Orders' || TreeParam == 'Parent Accounts' || TreeParam == 'Simple Materials' || TreeParam == 'Sections' || TreeParam == 'Section Fields' || TreeParam == 'Questions' || TreeParam == 'Tabs' || (TreeParentParam == 'Program Type Promotions' && CurrentTab != 'Program Type') || TreeSuperParentParam == 'Program Type Promotions' || TreeParam == 'Sales Order Line Program' || TreeParam == 'Invoice Line Program' || TreeTopSuperParentParam == 'Program Type Promotions' || TreeParentParam == 'Participants' || TreeSuperParentParam == 'Participants' || TreeTopSuperParentParam == 'Participants' || ((TreeParam == 'Programs' || TreeParam == 'Program Type Promotions' || TreeParam == 'Program Quotas' || TreeParam == 'Sales Orders' || TreeParam == 'Invoices') && CurrentTab == 'Program Type') || ((TreeParam == 'Sales Areas' || TreeParentParam == 'Sales Areas' || TreeSuperParentParam == 'Sales Areas' || TreeTopSuperParentParam == 'Sales Areas') && currenttab == 'Business Unit') || (TreeSuperParentParam == 'Sales Territories' && currenttab == 'Sales Area') || (TreeParentParam == 'Sales Territories' && currenttab == 'Sales Area') || (((TreeParam == 'Invoices') || (TreeParam == 'Sales Orders')) && ((CurrentTab == 'Quota Category') || (CurrentTab == 'Quota Subcategory')))) && CurrentTab != 'Invoice' || TreeParam == 'Approval Chains')
    //A043S001P01-9202 end
    {
        ActiveTab = $('#attributesContainer ul li.active span:first').text()
        if (TreeParam == 'Profile Information') {
            $('.Detail').css('display', 'block');
            $('.CommonTreeDetail, .Related').css('display', 'none');
        }
        else if (TreeParam == 'Pages' && ActiveTab == 'App') {
            RecName = 'div_CTR_Pages'
            loadRelatedList(CurrentRecordId, RecName);

            $('.Detail, .CommonTreeDetail,.Related').css('display', 'none');
            $("#div_CTR_Pages").closest('.Related').css('display', 'block');
        }
        else if (TreeParam == 'Section Actions' && ActiveTab == 'App') {
            RecName = 'div_CTR_Section_Actions'
            CurrentRecordId = "SYOBJR-94587";
            loadRelatedList(CurrentRecordId, RecName);

            $('.Detail, .CommonTreeDetail,.Related').css('display', 'none');
            $("#div_CTR_Section_Actions").closest('.Related').css('display', 'block');
        }
        else if (TreeParam == 'Actions' && ActiveTab == 'App') {
            RecName = 'div_CTR_Actions'
            CurrentRecordId = "SYOBJR-98784";
            loadRelatedList(CurrentRecordId, RecName);

            $('.Detail, .CommonTreeDetail,.Related').css('display', 'none');
            $("#div_CTR_Actions").closest('.Related').css('display', 'block');
        }
        else {
            $('.Detail, .CommonTreeDetail, .Related').css('display', 'none');
            $('.Detail').removeClass('disp_blk');

        }

        $('#COMMON_TABS').css('display', 'none');
        //A043S001P01-11419 -Dhurga-Start
        if (TreeParam == 'Tabs' && CurrentRecordId == 'SYOBJR-93159') {

            $('.CommonTreeDetail').hide();
            RecId = "SYOBJR-93159";
            RecName = "div_CTR_Tab_Field_Settings";
            loadRelatedList(RecId, RecName);
            $("div[id='" + RecName + "']").closest('.Related').css('display', 'block');

        }
        else if (TreeParam == 'Sections' && CurrentRecordId == 'SYOBJR-93160') {

            $('.CommonTreeDetail').hide();
            RecId = "SYOBJR-93160";
            RecName = "div_CTR_Section_Field_Settings";
            loadRelatedList(RecId, RecName);
            $("div[id='" + RecName + "']").closest('.Related').css('display', 'block');


        }
        //A043S001P01-11642 Starts
        else if (TreeParam == 'Tabs' && CurrentRecordId == 'SYOBJR-95812') {
            loadRelatedList('SYOBJR-95812', 'div_CTR_Tabs')
            $("#div_CTR_Tabs").closest('.Related').css('display', 'block');
        }
        else if (TreeParam == 'Sections' && CurrentRecordId == 'SYOBJR-95814') {
            loadRelatedList('SYOBJR-95814', 'div_CTR_Sections')
            $("#div_CTR_Sections").closest('.Related').css('display', 'block');
        }
        else if (TreeParam == 'Questions' && CurrentRecordId == 'SYOBJR-95813') {
            loadRelatedList('SYOBJR-95813', 'div_CTR_Questions')
            $("#div_CTR_Questions").closest('.Related').css('display', 'block');
        }
        //A043S001P01-11642 End
        else if (TreeParam == 'Approval Chains') {
            $("#div_CTR_Approval_Chains").html('<div id = "div_CTR_PRE_view" style = "display:block"></div><div id ="listPreview" style = "display:none"></div>');
            if ($("#FirstSecInformation").find(".previewdiv").length == 0) {
                $("#FirstSecInformation").append('<div class="previewdiv flt_rt" style="display: block;"> <a href="#" onclick="ChangePreview()" class="Clkfull_view" style="display: inline;margin-right: 12px;"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Minimize.svg" class="" height="18px"></a></div>')
            }
            else {
                $('.previewdiv.flt_rt').css('display', 'block');
            }
            preview_approvals();
            loadRelatedList('SYOBJR-94462', 'listPreview');
            //console.log("inside Approval Chains node--------->");
        }// A043S001P01-12254 Start, A043S001P01-12838 Start
        else if (TreeParam == 'Approval History') {
            $("#div_CTR_Approval_History").html('<div id = "div_CTR_PRE_view" style = "display:block"></div><div id ="listPreview" style = "display:none"></div>');
            if ($("#FirstSecInformation").find(".fullviewdiv").length == 0) {
                $("#FirstSecInformation").append('<div class="fullviewdiv flt_rt" style="display: block;"> <a href="#" onclick="ChangePreview()" class="Clkfull_view" style="display: inline;margin-right: 12px;"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Minimize.svg" class="" height="18px"></a></div>')
            } else {
                $('.previewdiv.flt_rt').css('display', 'block');
            }
            preview_approvals();
            loadRelatedList(CurrentRecordId, 'listPreview');
            $("div[id='div_CTR_Approval_History']").closest('.Related').css('display', 'block');
            //$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
            //$("div[id='"+RecName+"']").closest('.Related').removeClass("tree_second_child tree_third_child tree_forth_child");
        }// A043S001P01-12254 End, A043S001P01-12838 End
        else if (TreeParam == 'Simple Materials') {
            //loadRelatedList('SYOBJR-94480','div_CTR_Variant_Materials');
            $("#div_CTR_Simple_Materials").closest('.Related').css("display", "block");
            loadVariantGrid();
        }// A043S001P01-6738 Start
        // A043S001P01-8665 Start

        else if (TreeParam == 'Price Model' && ActiveTab == 'My Approvals Queue') {
            try {
                $('.CommonTreeDetail').css('display', 'block');
                $('.Detail, .Related').css('display', 'none');
                $('.CommonTreeDetail').show();
                Table_id = 'SYOBJ-00273'
                CurrentRecordId = $('.product_txt_div span:nth-child(3)').text().trim();
                cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'TableId': Table_id, 'TreeParam': TreeParam, 'TreeParentParam': '', 'TreeSuperParentParam': '', 'TreeTopSuperParentParam': '', 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                    var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];

                    localStorage.setItem('Lookupobjd', data5)
                    if (document.getElementById("TREE_div")) {
                        document.getElementById("TREE_div").innerHTML = datas;
                        // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                        popover()
                    }
                    $('#COMMON_TABS').show()
                    $('.SegRevPricemodel').show()
                    $('.SYSECT-SE-00134').hide();
                    $('.SYSECT-SE-00135').hide();
                });
            }
            catch (e) {
                console.log(e);
            }
        }





        //if (document.getElementById("header_label"))
        //{
        //	document.getElementById("header_label").innerHTML = TreeParam.toUpperCase();
        //}
        //$(".CommonTreeDetail").removeClass("tree_second_child");

        $('#sub_child_content_banner, #sub_parent_child_content_banner, #sub_content_banner, #content_banner').css("display", "none");
    }
    //RAMESH A043S001P01-7259 Quota Category Explorer ReWork DATE 21-01-2020  START
    // A043S001P01-8147 START




    else if (TreeParentParam == 'Tabs' && TreeTopSuperParentParam == 'App Level Permissions' && TreeParam != '') {
        if (currenttab == 'Profile') {



            $('.Detail,.Related').css('display', 'none');
            $('.CommonTreeDetail').css('display', 'block');
            Table_id = 'SYOBJR-93159'
            //console.log('3692----TableId-----',TableId)
            localStorage.setItem('TableId_cancel_fun', Table_id);
            $(".common_profile_tab").css("display", "block");
            $("#COMMON_TABS").css("display", "block");
            $('div#COMMON_TABS').find("li").removeClass('active');
            $($('.common_profile_tab')[0]).addClass('active');

            loadRelatedList('SYOBJR-93160', 'div_CTR_Section_Field_Settings')
            try {

                cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'TableId': Table_id, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeFirstSuperTopParentParam': TreeFirstSuperTopParentParam, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                    var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                    localStorage.setItem('Lookupobjd', data5)
                    if (document.getElementById("TREE_div")) {
                        document.getElementById("TREE_div").innerHTML = datas;
                        // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                        popover()
                    }
                });
            }
            catch (e) {
                console.log(e);
            }
        }
    }
    else if (TreeParentParam == 'Fields' && TreeTopSuperParentParam == 'Object Level Permissions' && TreeParam != '') {




        $('.Detail,.Related').css('display', 'none');
        $('.CommonTreeDetail').css('display', 'block');
        Table_id = 'SYOBJR-93130'
        //console.log('3692----TableId-----',TableId)
        localStorage.setItem('TableId_cancel_fun', Table_id);
        try {

            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'TableId': Table_id, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeFirstSuperTopParentParam': TreeFirstSuperTopParentParam, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                localStorage.setItem('Lookupobjd', data5)
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                }
            });
        }
        catch (e) {
            console.log(e);
        }
    }
    else if (TreeParentParam == 'Actions' && TreeTopSuperParentParam == 'Tabs' && TreeSuperParentParam != '' && TreeParam != '') {




        var current_tab_val = $('ul#carttabs_head .active').text().trim();
        if (currenttab == 'Profile') {
            $('.Detail, .Related').css('display', 'none');
            $('.CommonTreeDetail').css('display', 'block');
            Table_id = 'SYOBJR-93169'
            //console.log('3692----TableId-----',TableId)
            localStorage.setItem('TableId_cancel_fun', Table_id);
            try {

                cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'TableId': Table_id, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                    var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                    localStorage.setItem('Lookupobjd', data5)
                    if (document.getElementById("TREE_div")) {
                        document.getElementById("TREE_div").innerHTML = datas;
                        // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                        popover()
                    }
                });
            }
            catch (e) {
                console.log(e);
            }
        }
    }
    else if (TreeParentParam == 'Tabs' && TreeParam != '') {




        var current_tab_val = $('ul#carttabs_head li.active a span').text().trim();
        if (currenttab == 'App') {
            $('.Detail, .Related').css('display', 'none');
            $('.CommonTreeDetail').css('display', 'block');
            Table_id = 'SYOBJR-94441'
            //console.log('3692----TableId-----',TableId)
            localStorage.setItem('TableId_cancel_fun', Table_id);
            try {

                cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'TableId': Table_id, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                    var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                    localStorage.setItem('Lookupobjd', data5)
                    if (document.getElementById("TREE_div")) {
                        document.getElementById("TREE_div").innerHTML = datas;
                        // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                        popover()
                    }
                });
            }
            catch (e) {
                console.log(e);
            }
        }
    }
    else if ((TreeSuperParentParam = 'Program Type Quota Categories') && TreeParam != '' && TreeParentParam != '' && currenttab == 'Quota Category') {
        $('.CommonTreeDetail').css('display', 'block');
        $('.Detail, .Related').css('display', 'none');


    } else if (CurrentNodeId == 0 && TreeParam != '') {
        $('.Detail').css('display', 'block');
        $('.CommonTreeDetail, .Related').css('display', 'none');
        //if (document.getElementById("header_label")) {
        //	document.getElementById("header_label").innerHTML = TreeParam.toUpperCase();
        //}
        if (localStorage.getItem('CommonTreeParam') == 'Pricebook Entry Information' && localStorage.getItem('err_msg_avail') == '1') {
            $('div#SegAlert').css('display', 'block');
        }
        $('#sub_child_content_banner, #sub_content_banner, #content_banner').css("display", "none");
    }
    else if ((jQuery.inArray(TreeParam, data) !== -1 || TreeParam == 'Components') && CurrentTab == 'Invoice') {
        $('.Detail, .CommonTreeDetail, .Related').css('display', 'none');
        if (TreeParam == 'Invoice Lines') {
            var InvoiceJsondata = [{ 'SYOBJR-90086': 'Invoice Lines', 'SYOBJR-90088': 'Invoice Line Programs', 'SYOBJR-90087': 'Invoice Line Program Participants' }];
        }
        else if (TreeParam == 'Invoice Line Programs') {
            var InvoiceJsondata = [{ 'SYOBJR-90088': 'Invoice Line Programs', 'SYOBJR-90087': 'Invoice Line Program Participants' }];
        }
        else if (TreeParam == 'Invoice Line Program Participants') {
            var InvoiceJsondata = [{ 'SYOBJR-90087': 'Invoice Line Program Participants' }];
        }
        else if (TreeParam == 'Components') {
            var InvoiceJsondata = [{ 'SYOBJR-90086': 'Invoice Lines' }];
        }
        setTimeout(function () {
            $.each(InvoiceJsondata, function (key, value) {
                $.each(value, function (ind, rec) {
                    [RecId, RecName] = [ind.toString(), 'div_CTR_' + rec.replace(/\ /g, '_')];
                    loadRelatedList(RecId, RecName);
                    $("div[id='" + RecName + "']").closest('.Related').css('display', 'block');
                    //$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
                    //$("div[id='"+RecName+"']").closest('.Related').removeClass("tree_second_child tree_third_child tree_forth_child tree_fifth_child");
                });
            });
            if (document.getElementById("header_label") && (TreeParam == 'Programs' || TreeParam == 'Components')) {
                document.getElementById("header_label").innerHTML = 'Invoice Line ' + TreeParam.toUpperCase();
            } else if (document.getElementById("header_label") && (TreeParam == 'Invoice Lines' || TreeParam == 'Program Participants')) {
                document.getElementById("header_label").innerHTML = TreeParam.toUpperCase();
            }
            $(".CommonTreeDetail").removeClass("tree_second_child");
            $('#sub_child_content_banner, #sub_content_banner, #content_banner').css("display", "none");
            $("div[id='" + RecName + "']").closest('.Related').css('display', 'block');
            $("div[id='" + RecName + "']").closest('.Related').addClass("tree_first_child");
            $("div[id='" + RecName + "']").closest('.Related').removeClass("tree_second_child tree_third_child tree_forth_child");
        }, 1000);
    }

    else if (TreeParam == 'Fields') {

        $('.Detail, .CommonTreeDetail').css('display', 'none');
        RecId = "SYOBJR-93162";
        RecName = "div_CTR_Section_Field_Settings";
        loadRelatedList(RecId, RecName);
        $("div[id='" + RecName + "']").closest('.Related').css('display', 'block');


    }
    else if (TreeParam != '' && TreeParentParam == 'Fields') {

        $('.Detail,.Related').css('display', 'none');
        $('.CommonTreeDetail').css('display', 'block');


        Table_id = 'SYOBJR-93162'
        //console.log('3692----TableId-----',TableId)
        localStorage.setItem('TableId_cancel_fun', Table_id);
        try {

            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'TableId': Table_id, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                localStorage.setItem('Lookupobjd', data5)
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                }
            });
        }
        catch (e) {
            console.log(e);
        }

    }

    else if (TreeParam != '' && TreeParentParam == 'Actions' && TreeSuperTopParentParam != '' && TreeSuperParentParam != '') {

        $('.Detail,.Related').css('display', 'none');
        $('.CommonTreeDetail').css('display', 'block');


        Table_id = 'SYOBJR-93169'
        //console.log('3692----TableId-----',TableId)
        localStorage.setItem('TableId_cancel_fun', Table_id);
        try {

            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'TableId': Table_id, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                localStorage.setItem('Lookupobjd', data5)
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                }
            });
        }
        catch (e) {
            console.log(e);
        }

    }
    else if (TreeParam == 'Actions' && TreeSuperParentParam != '') {
        $('.Detail, .CommonTreeDetail').css('display', 'none');
        RecId = "SYOBJR-93188";
        RecName = "div_CTR_Action_Settings";
        loadRelatedList(RecId, RecName);
        $("div[id='" + RecName + "']").closest('.Related').css('display', 'block');

    }
    else if (TreeParentParam == 'Role Users' && TreeParam != '') {
        $('.Detail,.Related').css('display', 'none');
        $('.CommonTreeDetail').css('display', 'block');


    }
    else {




        $('.Detail, .CommonTreeDetail, .Related').css('display', 'none');
        //if (document.getElementById("header_label")) 
        //{
        //	document.getElementById("header_label").innerHTML = TreeParam.toUpperCase();
        //}
        $('#sub_child_content_banner, #sub_content_banner, #content_banner').css("display", "none");
    }
    var [Materials_node_ban, Materials_node_ban_txt] = ['0', ''];
    activeUser();
    /* Current User Name - Tooltip 'End' */
    /* A043S001P01-10055 - Start */ //11285 start
    if (CurrentNodeId != 0) {
        Subbaner(CurrentNodeId, CurrentRecordId, ObjName);
    }//11285 end
    /* A043S001P01-10055 - End */
    /* Tree dynamic height 'Start' */
    var count_val_inner = 0;
    setInterval(function () {
        if (count_val_inner < 10) {
            ot_srl();

            $('[id^="div_PICKLISTLOAD_"] > select').each(function (index) {
                var txt_sel = $(this).closest('div[id^=drop_]').attr('id');
                $('div#' + txt_sel).css({ 'height': 'auto', 'padding': '10px 0 3px' });

                var find_disa = $(this).attr('disabled');
                if (find_disa == 'disabled') {
                    $(this).siblings('div[id^=button_mvmt]').children('button').attr('disabled', 'disabled');
                }
                else {
                    $(this).siblings('div[id^=button_mvmt]').children('button').removeAttr('disabled');
                }
            });

            count_val_inner = count_val_inner + 1;
        }
    }, 500);
	/* Tree dynamic height 'End' */;
}
//11285 start for loading subbaner we can call this function where ever needed

function approval_toggle() {
    //$('.chainstep_arrow_out_collapse a').click(function() {
    $(this).find('i').toggleClass('fa-plus fa-minus')
        .closest('panel').siblings('panel')
        .find('i')
        .removeClass('fa-minus').addClass('fa-plus');
    //});
}

function Subbaner(subTabName, CurrentNodeId, CurrentRecordId, ObjName) {
    try {
        ProductId = cpq.models.configurator.productId();
    }
    catch {
        ProductId = '2240'
    }

    showpricingbenchmarknotify()

    if (subTabName != "Approvers" && subTabName != "Tracked Fields") {
        var node = TreeParam = TreeParentParam = TreeParentNodeId = TreeParentNodeRecId = TreeSuperParentParam = TreeSuperParentId = TreeSuperParentRecId = TreeTopSuperParentParam = TreeTopSuperParentId = TreeTopSuperParentRecId = TreeSuperTopParentParam = TreeSuperTopParentRecId = TreeSuperTopParentId = TreeFirstSuperTopParentParam = TreeFirstSuperTopParentId = TreeFirstSuperTopParentRecId = GrandTreeFirstSuperTopParentParam = GrandTreeFirstSuperTopParentId = GrandTreeFirstSuperTopParentRecId = Grand_GrandTreeFirstSuperTopParentParam = Grand_GrandTreeFirstSuperTopParentId = Grand_GrandTreeFirstSuperTopParentRecId = '';
        node = $('#commontreeview').treeview('getNode', parseInt(CurrentNodeId));
        CurrentNodeId = node.nodeId
        if (CurrentRecordId == null) {
            CurrentRecordId = node.id;
        }
        //CurrentRecordId = node.id;
        var node_text_var = node.text;

        if (typeof (node_text_var) != 'function' && node_text_var.includes("<span")) {
            TreeParam = node_text_var.split(">").pop();
        }
        else {
            TreeParam = node_text_var
        }
        if (typeof TreeParam === 'string') {
            if (TreeParam.includes("<img")) {
                TreeParam = TreeParam.split(">")
                TreeParam = TreeParam[TreeParam.length - 1]
            } else {
                TreeParam = TreeParam
            }
            if (TreeParam.includes("-")) {

                if (!TreeParam.includes('- BASE') && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving')) {
                    TreeParam = TreeParam.split("-")[0].trim()
                }
            } else {
                TreeParam = TreeParam
            }
        }
    }
    if (CurrentNodeId != '' && CurrentNodeId != null) {
        TreeParentParam = $('#commontreeview').treeview('getParent', CurrentNodeId).text;
        if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("<img")) {
            // TreeParentParam = TreeParentParam.split(">")[1];
            TreeParentParam = TreeParentParam.split(">")
            TreeParentParam = TreeParentParam[TreeParentParam.length - 1]
        }
        if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("-")) {
            if (!TreeParentParam.includes('- BASE')) {
                TreeParentParam = TreeParentParam.split("-")[0].trim()
            }
        }
        TreeParentNodeId = $('#commontreeview').treeview('getParent', CurrentNodeId).nodeId;
        TreeParentNodeRecId = $('#commontreeview').treeview('getParent', CurrentNodeId).id;
    }
    if (TreeParentNodeId != '' && TreeParentNodeId != null) {
        TreeSuperParentParam = $('#commontreeview').treeview('getParent', TreeParentNodeId).text;
        if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("<img")) {
            //  TreeSuperParentParam = TreeSuperParentParam.split(">")[1];
            TreeSuperParentParam = TreeSuperParentParam.split(">")
            TreeSuperParentParam = TreeSuperParentParam[TreeSuperParentParam.length - 1];
        }
        if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("-")) {
            if (!TreeSuperParentParam.includes('- BASE')) {
                TreeSuperParentParam = TreeSuperParentParam.split("-")[0].trim()
            }
        }
        TreeSuperParentId = $('#commontreeview').treeview('getParent', TreeParentNodeId).nodeId;
        TreeSuperParentRecId = $('#commontreeview').treeview('getParent', TreeParentNodeId).id;
    }
    if (TreeSuperParentId != '' && TreeSuperParentId != null) {
        TreeTopSuperParentParam = $('#commontreeview').treeview('getParent', TreeSuperParentId).text;
        if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
            //   TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")[1];
            TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")
            TreeTopSuperParentParam = TreeTopSuperParentParam[TreeTopSuperParentParam.length - 1];
        }
        if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("-")) {
            if (!TreeTopSuperParentParam.includes('- BASE')) {
                TreeTopSuperParentParam = TreeTopSuperParentParam.split("-")[0].trim()
            }
        }
        TreeTopSuperParentId = $('#commontreeview').treeview('getParent', TreeSuperParentId).nodeId;
        TreeTopSuperParentRecId = $('#commontreeview').treeview('getParent', TreeSuperParentId).id;
    }
    if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null) {
        TreeSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).text;
        if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeSuperTopParentParam.includes("<img")) {
            //  TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")[1];
            TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")
            TreeSuperTopParentParam = TreeSuperTopParentParam[TreeSuperTopParentParam.length - 1];
        }
        if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeSuperTopParentParam.includes("-")) {
            if (!TreeSuperTopParentParam.includes('- BASE')) {
                TreeSuperTopParentParam = TreeSuperTopParentParam.split("-")[0].trim()
            }
        }
        TreeSuperTopParentId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
        TreeSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).id;
    }
    if (TreeSuperTopParentId != '' && TreeSuperTopParentId != null) {
        TreeFirstSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).text;
        if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeFirstSuperTopParentParam.includes("<img")) {
            //    TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")[1];
            TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")
            TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam[TreeFirstSuperTopParentParam.length - 1];
        }
        if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeFirstSuperTopParentParam.includes("-")) {
            if (!TreeFirstSuperTopParentParam.includes('- BASE')) {
                TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split("-")[0].trim()
            }
        }
        TreeFirstSuperTopParentId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).nodeId;
        TreeFirstSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).id;
    }

    if (TreeFirstSuperTopParentId != '' && TreeFirstSuperTopParentId != null) {
        GrandTreeFirstSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeFirstSuperTopParentId).text;
        if (GrandTreeFirstSuperTopParentParam != '' && GrandTreeFirstSuperTopParentParam != undefined && (typeof GrandTreeFirstSuperTopParentParam === 'string' || GrandTreeFirstSuperTopParentParam instanceof String) && GrandTreeFirstSuperTopParentParam.includes("<img")) {
            //   GrandTreeFirstSuperTopParentParam = GrandTreeFirstSuperTopParentParam.split(">")[1];
            GrandTreeFirstSuperTopParentParam = GrandTreeFirstSuperTopParentParam.split(">")
            GrandTreeFirstSuperTopParentParam = GrandTreeFirstSuperTopParentParam[GrandTreeFirstSuperTopParentParam.length - 1];
        }
        if (GrandTreeFirstSuperTopParentParam != '' && GrandTreeFirstSuperTopParentParam != undefined && (typeof GrandTreeFirstSuperTopParentParam === 'string' || GrandTreeFirstSuperTopParentParam instanceof String) && GrandTreeFirstSuperTopParentParam.includes("-")) {
            if (!GrandTreeFirstSuperTopParentParam.includes('- BASE')) {
                GrandTreeFirstSuperTopParentParam = GrandTreeFirstSuperTopParentParam.split("-")[0].trim()
            }
        }
        GrandTreeFirstSuperTopParentId = $('#commontreeview').treeview('getParent', TreeFirstSuperTopParentId).nodeId;
        GrandTreeFirstSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeFirstSuperTopParentId).id;
    }
    if (GrandTreeFirstSuperTopParentId != '' && GrandTreeFirstSuperTopParentId != null) {
        Grand_GrandTreeFirstSuperTopParentParam = $('#commontreeview').treeview('getParent', GrandTreeFirstSuperTopParentId).text;
        if (Grand_GrandTreeFirstSuperTopParentParam != '' && Grand_GrandTreeFirstSuperTopParentParam != undefined && (typeof Grand_GrandTreeFirstSuperTopParentParam === 'string' || Grand_GrandTreeFirstSuperTopParentParam instanceof String) && Grand_GrandTreeFirstSuperTopParentParam.includes("<img")) {
            //  Grand_GrandTreeFirstSuperTopParentParam = Grand_GrandTreeFirstSuperTopParentParam.split(">")[1];
            Grand_GrandTreeFirstSuperTopParentParam = Grand_GrandTreeFirstSuperTopParentParam.split(">")
            Grand_GrandTreeFirstSuperTopParentParam = Grand_GrandTreeFirstSuperTopParentParam[Grand_GrandTreeFirstSuperTopParentParam.length - 1];
        }
        if (Grand_GrandTreeFirstSuperTopParentParam != '' && Grand_GrandTreeFirstSuperTopParentParam != undefined && (typeof Grand_GrandTreeFirstSuperTopParentParam === 'string' || Grand_GrandTreeFirstSuperTopParentParam instanceof String) && Grand_GrandTreeFirstSuperTopParentParam.includes("-")) {
            if (!Grand_GrandTreeFirstSuperTopParentParam.includes('- BASE')) {
                Grand_GrandTreeFirstSuperTopParentParam = Grand_GrandTreeFirstSuperTopParentParam.split("-")[0].trim()
            }
        }
        Grand_GrandTreeFirstSuperTopParentId = $('#commontreeview').treeview('getParent', GrandTreeFirstSuperTopParentId).nodeId;
        Grand_GrandTreeFirstSuperTopParentRecId = $('#commontreeview').treeview('getParent', GrandTreeFirstSuperTopParentId).id;
    }

    if (TreeSuperParentId === undefined) {
        TreeSuperParentParam = '';
    }
    if (TreeTopSuperParentId === undefined) {
        TreeTopSuperParentParam = '';
    }
    if (TreeSuperTopParentRecId === undefined) {
        TreeSuperTopParentParam = '';
    }
    if (TreeFirstSuperTopParentRecId === undefined) {
        TreeFirstSuperTopParentParam = '';
    }
    if (CurrentTab == 'CM Class' && (ObjName == 'CMCLSE' || ObjName == 'CMCLTB' || ObjName == 'CMCMQU')) {
        TreeTopSuperParentParam = localStorage.getItem('CommonTopSuperParentParam');
    }

    AllTreeParam = maintreeparamfunction(CurrentNodeId, 0);
    AllTreeParams = JSON.stringify(AllTreeParam);
    localStorage.setItem('AllTreeParams', AllTreeParam);
    //commented the below code it throwns an error
    /*localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    localStorage.setItem('CommonTopSuperParentParam', AllTreeParam['TreeParentLevel2']);
    localStorage.setItem('CommonTreeSuperTopParentParam', AllTreeParam['TreeParentLevel3']); //Accounts Tab 
    localStorage.setItem('CommonTreeFirstSuperTopParentParam', AllTreeParam['TreeParentLevel4']); //Accounts Tab*/
    AssemblyId = EquipmentId = SerialNumber = ''
    //Commented the below code
    /*if (ObjName == 'SAQSCO'){
        EquipmentId = localStorage.getItem("ToolEquipment")
        SerialNumber = localStorage.getItem("ToolSerial")
    }*/
    EquipmentId = localStorage.getItem("EquipmentIdValue")
    SerialNumber = localStorage.getItem("SerialNumberValue")
    if (ObjName != "SAQICO") {
        AssemblyId = localStorage.getItem("AssemblyIdValue")
    }
    /*if (ObjName == "SAQICO"){
        EquipmentId = localStorage.getItem("EquipmentIdValue")
        SerialNumber = localStorage.getItem("SerialNumberValue")
    }
    else {
        AssemblyId = localStorage.getItem("AssemblyIdValue")
        EquipmentId = localStorage.getItem("EquipmentIdValue")
        SerialNumber = localStorage.getItem("SerialNumberValue")
    }*/
    if (TreeParam == "Billing") {
        CurrentRecordId = $('#QUOTE_BILLING_PLAN_RECORD_ID').val();
        console.log('CurrentRecordId-----', CurrentRecordId)
    }
    if (TreeParentParam == "Add-On Products" && subTabName == "Spare Part Details") {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
    }
    page_type = localStorage.getItem("page_type")
    CurrentTab = $("ul#carttabs_head li.active a span").text();
    cpq.server.executeScript("SYSUBANNER", { 'subTabName': subTabName, 'ObjName': ObjName, 'CurrentRecordId': CurrentRecordId, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam, 'AssemblyId': AssemblyId, 'EquipmentId': EquipmentId, 'SerialNumber': SerialNumber, 'page_type': page_type, 'CurrentTab': CurrentTab }, function (dataset) {

        $('.notify_info_top_cls').html(dataset[4]);
        $('.notify_info_top_cls').hide();

        if (dataset != '') {
            var dispRecall = ''
            if (dataset[1]) {
                dispRecall = dataset[1]
            }
            if (dataset[2] == 'Hide_button') {
                $('#CALCULATE_QItems').css('display', 'none');
                localStorage.setItem("get_button_price", "hide_button");
                $("#step1").removeClass("disabled").addClass("active");
                //$("[id='qtn_save'] span").click();
            }

            //else if (dataset[2] == 'Show_button'){$('#CALCULATE_QItems').css('display','block');
            //$("#step1").removeClass("disabled").addClass("complete");
            //$("#step1 .bar_number").css("display","none");
            //$("#step1 .bar_tick_img").css("display","block");
            //$("#step2").removeClass("disabled").addClass("active");}
            else {
                localStorage.setItem("get_button_price", "show_button");
                //Subbaner(subTabName,CurrentNodeId, 'SYOBJR-00009', 'SAQITM');
                $('#CALCULATE_QItems').css('display', 'block');
                $('.cpq_notification_div').css('display', 'block');
                $('.cpq_cust_notify').css('display', 'block');
                $('.alert-warning').css('display', 'block');
                //A055S000P01-20612 start A
                var ibase_text = $('.cpq_notification_div .cpq_cust_warning').html();
                if(!(ibase_text.includes('MISSING ATTRIBUTES FROM IBASE') || ibase_text.includes('NO ASSEMBLY') || ibase_text.includes('REQUIRED EVENT IS MISSING'))){
                    $('.cpq_cust_warning').css('display', 'none');
                    $('.cpq_cust_warning').removeClass('d-flex');
                }
                //A055S000P01-20612 end A
                $('.cpq_cust_notify').html(dataset[5]);
                //var get_currentnode = node.nodeId;
                //CommonRightView(get_currentnode);

                //$("[id='qtn_save'] span").click();
                //$("#step1").removeClass("disabled active").addClass("complete");
                //$("#step1 .bar_number").css("display","none");
                //$("#step1 .bar_tick_img").css("display","block");
                //$("#step2").removeClass("disabled").addClass("active");				
            }
            // Got Sale type from Primary banner
            var sale_type = $(".segment_revision_Sale_text").text();
            localStorage.setItem('saletype', sale_type);
            // 
            localStorage.setItem("dispRecall", dispRecall)
            if (document.getElementById("seginnerbnr") && TreeParam != "Quote Information") {
                $("#seginnerbnr").css("display", "block");
                document.getElementById('seginnerbnr').innerHTML = dataset[0];
            }
            // for showing save & cancel buttons based on mode - start
            if (localStorage.getItem('key_id') == "EDIT") {
                $("#seginnerbnr").append('<button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="CommontreeSAVE(this)">SAVE</button><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="CommontreeCancel(this)">CANCEL</button>')
                localStorage.setItem('key_id', '');
            }
            // for showing save & cancel buttons based on mode - end
            /*A043S001P01-8146 START */
            if (CurrentRecordId != undefined) {
                if (CurrentRecordId.startsWith("SYOBJR") == true) {
                    $(".container_banner_inner_sec").css("display", "none");
                }
                else if (currenttab == "Contracts" && TreeParam == "Contract Information") {
                    $(".container_banner_inner_sec").css("display", "none");
                }
            }
            else {
                $(".container_banner_inner_sec").css("display", "block");
            }
            CurrentTabName = $('ul#carttabs_head li.active a span').text().trim();
            // A043S001P01-6738 Start
            if (CurrentTabName == 'Catalog' && TreeParam == 'Catalog Products') {
                $("#seginnerbnr").css("display", "none");
            }// A043S001P01-6738 End
            /* A043S001P01-8146 END*/
            //A043S001P01-13676 START
            if (CurrentTabName == 'Program' && TreeParam == 'Where Used') {
                $(".container_banner_inner_sec").css("display", "block");
            }
            //A043S001P01-13676 END
            //Commented the below code for testing
            if (localStorage.getItem('covobjclicked') == 'yes' && (localStorage.getItem("CommonTreeParentParam") == 'Comprehensive Services' || localStorage.getItem("CommonTreeParentParam") == 'Complementary Products')) {
                // if (currenttab.indexOf('Quote') != -1){
                // 	$('.secondary_highlight_panel').append('<button id="ADDNEW__SYOBJR_98800_0D035FD5_F0EA_4F11_A0DB_B4E10928B59F" onclick="cont_openaddnew(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD FROM LIST</button>')	
                // }
            }
            else if ((localStorage.getItem('covobjclicked') == 'yes' && subTabName == "Equipment") && (localStorage.getItem("CommonTreeParentParam") == 'Add-On Products')) {
                // if (currenttab.indexOf('Quote') != -1){
                // 	$('.secondary_highlight_panel').append('<button id="ADDNEW__SYOBJR_98800_0D035FD5_F0EA_4F11_A0DB_B4E10928B59F" onclick="cont_openaddnew(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD FROM LIST</button>')	
                // }
            }
            else if (localStorage.getItem('eqclicked') == 'yes' && localStorage.getItem("CommonTreeParentParam") == 'Fab Locations') {
                var Saletype = localStorage.getItem('saletype')
                // if (currenttab.indexOf('Quote') != -1){
                // 	if (subTabName == 'Equipment' && Saletype != 'TOOL RELOCATION'){
                // 	// 	$('.secondary_highlight_panel').append('<button id="RELOCATE__SYOBJR_98797_SYOBJ_00904" onclick="cont_openaddnew(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">RELOCATE EQUIPMENT</button>')
                // 	// }
                // 	$('.secondary_highlight_panel').append('<button id="ADDNEW__SYOBJR_98797_SYOBJ_00904" onclick="cont_openaddnew(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD FROM LIST</button>')
                // 	}					
                // }
                localStorage.setItem("eqclicked", "no");
            } else if ((localStorage.getItem('spareclicked') == 'yes' && subTabName == 'Spare Parts') && (localStorage.getItem("CommonTreeParentParam") == 'Complementary Products' || localStorage.getItem("CommonTreeParentParam") == 'Add-On Products')) {
                // $('.secondary_highlight_panel').append('<button id="spare-parts-bulk-add-modal-btn" onclick="showSparePartsBulkAddModal(this)" class="btnconfig" data-target="#bulkaddpopup" data-toggle="modal">BULK ADD</button>')
                if (localStorage.getItem("CommonTreeParentParam") == 'Add-On Products') {
                    $("#ADDNEW__SYOBJR_00005_SYOBJ_00272").css('display', 'none');
                }
                localStorage.setItem("spareclicked", "no");
            } else if (localStorage.getItem("showrefresh") == "yes" && localStorage.getItem("CommonTreeParam") == 'Documents') {
                $('.secondary_highlight_panel').append('<button id="refreshdoc" onclick="CommonRightView(2)" class="btnconfig">REFRESH</button>');

            } else if (TreeParam == "Sending Equipment" && subTabName == "Sending Equipment") {
                $('.secondary_highlight_panel').append('<button id="ADDNEW__SYOBJR_98800_SYOBJ_00904" onclick="cont_openaddnew(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">ADD FROM LIST</button>')
            }
            /*else if (localStorage.getItem("bktolist") == "yes" && localStorage.getItem("CommonTreeParam")=='Documents'){
                $('.secondary_highlight_panel').append('<button id="refreshdoc" onclick="CommonRightView(2)" class="btnconfig">BACK TO LIST</button>');
                localStorage.setItem("bktolist","no");
            }*/
            if (CurrentTabName == "Quotes") {
                //QuoteStatus();
                dynamic_status();
            }
            if (TreeParam == 'Billing') {
                $('.QuotesBillingDetails').css('display', 'none');
            }
            else { $('#TREE_div').css('display', 'block'); }
            if (dataset[2] == 'Hide_button') {
                $('#CALCULATE_QItems').css('display', 'none');
                var getrevisions = localStorage.getItem('NEW_REV')

            }

            else {
                $('#CALCULATE_QItems').css('display', 'block');


            }
        }

    });




}//11285 end for loading subbaner we can call this function where ever needed
/* To load the Right side content of the Tree view based on the selected node on the Left side 'End' */

function Commonteree_view_RL(ele) {
    //set localstorage to make it USER NAME field as ediatble & non editable based on mode under Approvers subtab in Approval chains tab - start
    $('#TREE_div').css('display', 'block');
    localStorage.setItem("ApproverAddNew", "false")
    //set localstorage to make it USER NAME field as ediatble & non editable based on mode under Approvers subtab in Approval chains tab - end
    var table_id = $(ele).closest('table').attr('id');
    var grid_obj = $(ele).attr('id');
    // 19572 - start
    var MODE = $(ele).text();
    var currentSubTab = localStorage.getItem('currentSubTab');
    if(CommonTreeParam == 'Quote Items' && currentSubTab == 'Annualized Items' && MODE == 'VIEW')
    { 
        $("#anual_pick").css('display','none')
    }
    // 19572 - end
    localStorage.setItem("equipment_level", "true");
    if (table_id == 'table_covered_obj_parent') {
        var cov = $(ele).attr('id');
        //INC08634400-M
        var equp_index = $(ele).closest('table').find('[data-field="EQUIPMENT_ID"]').index()+1;
        EquipmentId = $(ele).closest('tr').find('td:nth-child('+equp_index+')').text();
        //INC08634400-M
        localStorage.setItem("Ent_EquipmentId", EquipmentId)
    
    }
    else if (table_id.includes("covered_obj_child")) {
        var coveredobjectchild = $(ele).attr('id');
    }
    else if (table_id.includes("table_events_child")) {
        localStorage.setItem('openedKit', $(ele).attr('title'));
    }
    else if (table_id.includes("table_sending_equipment_child")) {
        var tablesendingeqpchild = $(ele).attr('id');
    }
    else if (table_id.includes("SYOBJR_98798")) {
        var account_details_hyperlink = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
        localStorage.setItem('account_details_hyperlink', account_details_hyperlink);
        localStorage.setItem("CurrentRecordId", account_details_hyperlink);
    }
    else if (table_id.includes("SYOBJR_00032") || table_id.includes("SYOBJR_00038")) {//A055S000P01-17070 code starts.. ends...
        var fts_fab_location_id = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
        localStorage.setItem("CurrentRecordId", fts_fab_location_id);
        localStorage.setItem("fts_fab_location_record_id", fts_fab_location_id); //INC08632845
    }
    else if (table_id.includes("SYOBJR_98857") || table_id.includes('SYOBJR_98858') || table_id.includes('SYOBJR_00028')) {
        var sourcefab = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
    }
    else if (table_id == 'SYOBJR_00010_C32BD9D5_A954_49A9_861A_544F30C66C26') {
        var spare_parts_id = $(ele).closest('tr').find('td:nth-child(4) a abbr').attr('id');
    }
    else if (table_id == 'table_contract_covered_obj_parent') {
        table_id = 'table_ContractCovered_obj_parent'
        var contract_cov = $(ele).attr('id');
    }
    else if (table_id == 'table_equipment_parent') {
        var eqp = $(ele).attr('id');
    }
    else if (table_id == 'table_Contract_equipment_parent') {
        table_id = "table_ContractEquipment_parent"
        var eqp = $(ele).attr('id');
    }
    else if (table_id == 'SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F') {
        var cov1 = $(ele).closest('tr').find('td:nth-child(4) a abbr').attr('id');
        //	$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F').wrapAll('<div class="benchmarkdiv"></div>');
    }
    else if (table_id == 'SYOBJR_91822_7A8F0522_9728_4CF9_A4C9_3F905D3B6130') {
        var itm = $(ele).closest('tr').find('td:nth-child(4) a abbr').attr('id');
    }
    else if (table_id.includes('SYOBJR_00024') || table_id.includes('SYOBJR_98806') || table_id.includes('SYOBJR_98825') || table_id.includes('SYOBJR_00643')) {
        var transaction_record_id = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
        var sourcefab = localStorage.setItem('sourcefab', transaction_record_id);
        var involvedparties_details = localStorage.setItem('involvedparties_details', transaction_record_id);
    }
    else if (table_id.includes('SYOBJR_98870') || table_id.includes('SYOBJR_00029')) { //9646 code starts..ends..
        var transaction_record_id = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
        localStorage.setItem("CurrentRecordId", transaction_record_id);
        subTabText = localStorage.getItem('currentSubTab');
        $('#spare-parts-bulk-add-modal-btn').css('display', 'none');
        chainsteps_breadcrumb(subTabText);
        tool_breadcrumb();
    }
    else if (table_id.includes('table_Preventive_Maintainence_parent')) { //9646 code starts..ends..
        var pm_events_record = $(ele).attr('id');
        localStorage.setItem("CurrentRecordId", pm_events_record);
        subTabText = localStorage.getItem('currentSubTab');
        chainsteps_breadcrumb(subTabText);
        tool_breadcrumb();
    }
    else if (table_id == 'SYOBJR_00026_C99C2FF0_42E0_4822_8B56_B3FD3F2D8F3B') {
        var Trackedobj = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
    }

    else if (table_id.includes('CommonChildTable')) {
        var qte_itm_dobj = $(ele).attr('id');
    }
    else if (table_id.includes('SYOBJR_98868')) {
        var service_assembly = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
    }
    var [TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam] = [localStorage.getItem('CommonTreeParam'), localStorage.getItem('CommonTreeParentParam'), localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam')];
    if (table_id == 'table_equipment_parent' && TreeParam == 'Fab Locations') {
        equipment_details = "True";
        fab_equipment_Id = $(ele).closest('tr').find('td:nth-child(4)').text();
        fab_serial_number = $(ele).closest('tr').find('td:nth-child(6)').text();
        localStorage.setItem("EquipmentIdValue", fab_equipment_Id)
        localStorage.setItem("SerialNumberValue", fab_serial_number)
        fab_equipment_serial_number = fab_equipment_Id + '-' + fab_serial_number
        localStorage.setItem("fab_equipment_serial_number", fab_equipment_serial_number)
        localStorage.getItem("fab_equipment_serial_number")
        //A055S000P01-21009
        GB = $(ele).closest('tr').find('td:nth-child(9)').text();
        FB_ID = $(ele).closest('tr').find('td:nth-child(13)').text();
        //A055S000P01-21009
        x = localStorage.getItem('CurrentNodeId')
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(x), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            y = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
            left_node = (y.text).split("-")[0].trim()
            if (left_node == FB_ID) {
                vi = y.nodeId
                node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(vi), { silent: true }]);
                var childrenNodes = _getChildren(node);
                $(childrenNodes).each(function () {
                    z = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

                    if (z.text == GB) {

                        //console.log(childrenNodes);
                        equipment_greenbook_level_nodeid = z.nodeId
                        CommonRightView(equipment_greenbook_level_nodeid)
                        //Assign the CurrentNodeId for breadcrumb functionality starts..
                        CurrentNodeId = equipment_greenbook_level_nodeid
                        localStorage.setItem('CurrentNodeId', CurrentNodeId)
                        //Assign the CurrentNodeId for breadcrumb functionality ends..
                        $('#table_equipment_parent').hide();
                        setTimeout(function () {
                            //$('#' + eqp).click();
                            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': eqp, 'ObjName': "SAQFEQ", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                                localStorage.setItem('Lookupobjd', data5)
                                if (document.getElementById("TREE_div")) {
                                    document.getElementById("TREE_div").innerHTML = datas;
                                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                    popover()
                                }
                                fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                                breadCrumb_Reset();
                                Pmevents_breadcrumb(fab_equser_id)
                                //var nobreadCrumb_Reset = true
                                Subbaner("Equipment Details", CurrentNodeId, eqp, "SAQFEQ");
                            });
                            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');


                        }, 2500);
                        //$('#lefttreepan #commontreeview').treeview('selectNode', [parseInt(vi), { silent: true } ]);
                    }
                });
                //$('#lefttreepan #commontreeview').treeview('selectNode', [parseInt(vi), { silent: true } ]);
                //Common_enable_disable()
            }
        });
    }
    else if (table_id.includes('covered_obj_child') && (TreeParentParam == 'Z0090' || TreeParam == 'Z0090') && $('.quote_type_value').text().toUpperCase() == "CHAMBER BASED" && !grid_obj.includes('SAQSCA')) {
        var par_tableId = $(ele).closest('.detail-view').closest('table').attr('id');
        greenbookIndex = $('#' + par_tableId).find('[data-field="GREENBOOK"]').index() + 1;
        var greenbook_Id = $(ele).closest('.detail-view').prev().find("td:nth-child(" + greenbookIndex + ")").text();
        var EquipmentIdValue = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(5)').text();
        var Assembly_id_value = $(ele).closest('tr').find('td:nth-child(5)').text();
        localStorage.setItem("EquipmentIdValue", EquipmentIdValue)
        localStorage.setItem("AssemblyIdValue", Assembly_id_value)
        $('#table_equipment_parent').hide();
        $('.listContStyle ').css('display', 'none')
        x = localStorage.getItem('CurrentNodeId')
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            y1 = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
            left_node = (y1.text).split("-")[0].trim()
            if (left_node == greenbook_Id) {
                vi = y1.nodeId
                gb_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(vi), { silent: true }]);
                $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
                var childrenNodes = _getChildren(node);
                $(childrenNodes).each(function () {
                    y2 = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                    if (y2.text == greenbook_Id) {
                        vii = y2.nodeId
                        CommonRightView(vii)
                        CurrentNodeId = vii
                        localStorage.setItem('CurrentNodeId', CurrentNodeId)
                        setTimeout(function () {
                            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': coveredobjectchild, 'ObjName': "SAQSCA", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                                localStorage.setItem('Lookupobjd', data5)
                                if (document.getElementById("TREE_div")) {
                                    $('#table_covered_obj_parent').hide();
                                    document.getElementById("TREE_div").innerHTML = datas;
                                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                    popover()
                                }
                                equipment_serialnumber = localStorage.getItem("EquipmentIdValue") + "-" + localStorage.getItem("SerialNumberValue")
                                breadCrumb_Reset();
                                Pmevents_breadcrumb(equipment_serialnumber)
                                Subbaner("Assembly Details", CurrentNodeId, coveredobjectchild.split('|')[0], "SAQSCA");
                            });
                            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
                            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "block");
                            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().addClass('active');
                        }, 2500);
                    }
                });
            }
        });


    }
    else if (table_id.includes('covered_obj_child') && TreeParentParam == 'Complementary Products' && !grid_obj.includes('SAQSCA')) {
        equipment_details = "True";
        fab_Id = $(ele).closest('tr').find('td:nth-child(11)').text();
        //A055S000P01-20418 start
        //Parent_table_Greenbook = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(8)').text();
        Parent_table_Greenbook = $(ele).closest('tr').find('td:nth-child(9)').text();
        //A055S000P01-20418 end
        var EquipmentIdValue = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(5)').text();
        var Assembly_id_value = $(ele).closest('tr').find('td:nth-child(5)').text();
        localStorage.setItem("EquipmentIdValue", EquipmentIdValue)
        localStorage.setItem("AssemblyIdValue", Assembly_id_value)
        $('#table_equipment_parent').hide();
        $('.listContStyle ').css('display', 'none')
        x = localStorage.getItem('CurrentNodeId')
        fab_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(x), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {

            y1 = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
            left_node = (y1.text).split("-")[0].trim()
            if (left_node == fab_Id) {
                vi = y1.nodeId
                gb_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(vi), { silent: true }]);
                $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
                var childrenNodes = _getChildren(node);
                $(childrenNodes).each(function () {
                    y2 = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                    if (y2.text == Parent_table_Greenbook) {
                        vii = y2.nodeId
                        CommonRightView(vii)
                        CurrentNodeId = vii
                        localStorage.setItem('CurrentNodeId', CurrentNodeId)
                        setTimeout(function () {
                            //$('#' + eqp).click();
                            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': coveredobjectchild, 'ObjName': "SAQSCA", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                                localStorage.setItem('Lookupobjd', data5)
                                if (document.getElementById("TREE_div")) {
                                    document.getElementById("TREE_div").innerHTML = datas;
                                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                    popover()
                                }
                                fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                                breadCrumb_Reset();
                                Pmevents_breadcrumb(fab_equser_id)
                                //var nobreadCrumb_Reset = true
                                Subbaner("Equipment Details", CurrentNodeId, eqp, "SAQFEQ");
                            });
                            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
                            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "block");
                            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().addClass('active');
                            $('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "block");
                        }, 2500);
                    }
                });
            }
        });


    }
    else if ((!table_id.includes('covered_obj_child') && table_id != 'table_covered_obj_parent') && (AllTreeParam['TreeParentLevel1'] == 'Complementary Products' || AllTreeParam['TreeParentLevel2'] == 'Complementary Products') && TreeParam != 'Add-On Products') {
        equipment_details = "True";
        fab_index = $("#"+table_id).find("[data-field='FABLOCATION_ID']").index() + 1;
        fab_Id = $(ele).closest('tr').find('td:nth-child('+fab_index+')').text();
        gb_index = $("#"+table_id).find("[data-field='GREENBOOK']").index() + 1;
        Parent_table_Greenbook = $(ele).closest('tr').find('td:nth-child('+gb_index+')').text();
        eqp_id_index = $("#"+table_id).find("[data-field='EQUIPMENT_ID']").index() + 1;
        var EquipmentIdValue = $(ele).closest('tr').find('td:nth-child('+eqp_id_index+')').text();
        Assembly_id_value = $(ele).closest('tr').find('td:nth-child(5)').text();
        localStorage.setItem("EquipmentIdValue", EquipmentIdValue)
        localStorage.setItem("AssemblyIdValue", Assembly_id_value)
        $('#table_equipment_parent').hide();
        $('.listContStyle ').css('display', 'none')
        x = localStorage.getItem('CurrentNodeId')
        fab_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(x), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        if (childrenNodes.length != 0) {
            $(childrenNodes).each(function () {
                y2 = $('#lefttreepan #commontreeview').treeview('getNode', [x, { silent: true }]);
                if (y2.text == Parent_table_Greenbook) {
                    vii = y2.nodeId
                    CommonRightView(vii)
                    CurrentNodeId = vii
                    localStorage.setItem('CurrentNodeId', CurrentNodeId)
                    setTimeout(function () {
                        //$('#' + eqp).click();
                        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': coveredobjectchild, 'ObjName': "SAQSCA", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                            localStorage.setItem('Lookupobjd', data5)
                            if (document.getElementById("TREE_div")) {
                                document.getElementById("TREE_div").innerHTML = datas;
                                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                popover()
                            }
                            fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                            breadCrumb_Reset();
                            Pmevents_breadcrumb(fab_equser_id)
                            //var nobreadCrumb_Reset = true
                            //Subbaner("Equipment Details",CurrentNodeId, eqp, "SAQFEQ");		
                            Subbaner("Assembly Details", CurrentNodeId, eqp, "SAQSCA");
                        });
                        $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Greenbook Customer Value Drivers')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Customer Value Drivers')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Greenbook Product Value Drivers')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Customer Value Drivers')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Product Value Drivers')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().addClass('active');
                    }, 2500);
                }
            });
        }
        else {
            vii = node.nodeId
            CommonRightView(vii)
            CurrentNodeId = vii
            localStorage.setItem('CurrentNodeId', CurrentNodeId)
            setTimeout(function () {
                //$('#' + eqp).click();
                cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': coveredobjectchild, 'ObjName': "SAQSCA", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                    var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                    localStorage.setItem('Lookupobjd', data5)
                    if (document.getElementById("TREE_div")) {
                        document.getElementById("TREE_div").innerHTML = datas;
                        // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                        popover()
                    }
                    fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                    breadCrumb_Reset();
                    Pmevents_breadcrumb(fab_equser_id)
                    //var nobreadCrumb_Reset = true
                    //Subbaner("Equipment Details",CurrentNodeId, eqp, "SAQFEQ");		
                    Subbaner("Assembly Details", CurrentNodeId, eqp, "SAQSCA");
                });
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Greenbook Customer Value Drivers')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Customer Value Drivers')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Greenbook Product Value Drivers')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Customer Value Drivers')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Product Value Drivers')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().addClass('active');
            }, 2500);
        }



    }
    else if (table_id.includes('SYOBJR_98868') && (AllTreeParam['TreeParentLevel2'] == 'Complementary Products' || AllTreeParam['TreeParentLevel2'] == 'Comprehensive Services')) {

        //$('#' + eqp).click();
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': service_assembly, 'ObjName': "SAQSCA", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            $("#div_CTR_related_list").css("display", "none")
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                popover()
            }
            fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
            breadCrumb_Reset();
            Pmevents_breadcrumb(fab_equser_id)
            //var nobreadCrumb_Reset = true
            //Subbaner("Equipment Details",CurrentNodeId, eqp, "SAQSCA");							
        });
        $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
        $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
        $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
        $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "block");
        $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().addClass('active');

    }
    else if (table_id.includes('table_sending_equipment_child') && (TreeParam == 'Sending Equipment' || TreeParam == 'Receiving Equipment')) {
        equipment_details = "True";
        fab_Id = $(ele).closest('tr').find('td:nth-child(9)').text();
        Parent_table_Greenbook = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(6)').text();
        x = localStorage.getItem('CurrentNodeId')
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(x), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            y = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

            if (y.text == fab_Id) {
                vi = y.nodeId
                node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(vi), { silent: true }]);
                var childrenNodes = _getChildren(node);
                $(childrenNodes).each(function () {
                    z = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

                    if (z.text == Parent_table_Greenbook) {

                        //console.log(childrenNodes);
                        equipment_greenbook_level_nodeid = z.nodeId
                        CommonRightView(equipment_greenbook_level_nodeid)
                        //Assign the CurrentNodeId for breadcrumb functionality starts..
                        CurrentNodeId = equipment_greenbook_level_nodeid
                        localStorage.setItem('CurrentNodeId', CurrentNodeId)
                        //Assign the CurrentNodeId for breadcrumb functionality ends..
                        $('#table_equipment_parent').hide();
                        setTimeout(function () {
                            //$('#' + eqp).click();
                            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': tablesendingeqpchild, 'ObjName': "SAQSSA", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                                localStorage.setItem('Lookupobjd', data5)
                                if (document.getElementById("TREE_div")) {
                                    document.getElementById("TREE_div").innerHTML = datas;
                                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                    popover()
                                }
                                fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                                breadCrumb_Reset();
                                Pmevents_breadcrumb(fab_equser_id)
                                //var nobreadCrumb_Reset = true
                                Subbaner("Equipment Details", CurrentNodeId, eqp, "SAQFEQ");
                            });
                            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
                            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "block");
                            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().addClass('active');

                        }, 2500);
                        //$('#lefttreepan #commontreeview').treeview('selectNode', [parseInt(vi), { silent: true } ]);
                    }
                });
                //$('#lefttreepan #commontreeview').treeview('selectNode', [parseInt(vi), { silent: true } ]);
                //Common_enable_disable()
            }
        });
    }
    else if (table_id.includes('table_sending_equipment_child') && (TreeParentParam == 'Sending Equipment' || TreeParentParam == 'Receiving Equipment')) {
        equipment_details = "True";
        fab_Id = $(ele).closest('tr').find('td:nth-child(9)').text();
        Parent_table_Greenbook = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(6)').text();
        x = localStorage.getItem('CurrentNodeId')
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(x), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            y = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

            if (y.text == Parent_table_Greenbook) {
                vi = y.nodeId

                CommonRightView(vi)
                CurrentNodeId = vi
                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                //Assign the CurrentNodeId for breadcrumb functionality ends..
                $('#table_equipment_parent').hide();
                setTimeout(function () {
                    //$('#' + eqp).click();
                    cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': tablesendingeqpchild, 'ObjName': "SAQSSA", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                        var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                        localStorage.setItem('Lookupobjd', data5)
                        if (document.getElementById("TREE_div")) {
                            document.getElementById("TREE_div").innerHTML = datas;
                            // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                            popover()
                        }
                        fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                        breadCrumb_Reset();
                        Pmevents_breadcrumb(fab_equser_id)
                        //var nobreadCrumb_Reset = true
                        Subbaner("Equipment Details", CurrentNodeId, eqp, "SAQFEQ");
                    });
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().addClass('active');

                }, 2500);
            }
        });
    }

    else if (table_id.includes('table_sending_equipment_child') && (TreeSuperParentParam == 'Sending Equipment' || TreeSuperParentParam == 'Receiving Equipment')) {
        equipment_details = "True";
        fab_Id = $(ele).closest('tr').find('td:nth-child(9)').text();
        Parent_table_Greenbook = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(6)').text();
        $('#table_equipment_parent').hide();
        $('.listContStyle ').css('display', 'none')
        setTimeout(function () {
            //$('#' + eqp).click();
            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': tablesendingeqpchild, 'ObjName': "SAQSSA", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                localStorage.setItem('Lookupobjd', data5)
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                }
                fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                breadCrumb_Reset();
                Pmevents_breadcrumb(fab_equser_id)
                //var nobreadCrumb_Reset = true
                Subbaner("Equipment Details", CurrentNodeId, eqp, "SAQFEQ");
            });
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
            $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().addClass('active');
            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "block");

        }, 2500);
    }
    else if (table_id.includes('table_sending_equipment_child') && TreeParentParam == 'Complementary Products') {
        equipment_details = "True";
        fab_Id = $(ele).closest('tr').find('td:nth-child(9)').text();
        Parent_table_Greenbook = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(6)').text();
        $('#table_equipment_parent').hide();
        $('.listContStyle ').css('display', 'none')
        x = localStorage.getItem('CurrentNodeId')
        fab_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(x), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            y = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
            if (y.text == 'Sending Equipment') {
                v = y.nodeId
                fb_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(v), { silent: true }]);
                $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
                var childrenNodes = _getChildren(node);
                $(childrenNodes).each(function () {
                    y1 = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                    if (y1.text == fab_Id) {
                        vi = y1.nodeId
                        gb_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(vi), { silent: true }]);
                        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
                        var childrenNodes = _getChildren(node);
                        $(childrenNodes).each(function () {
                            y2 = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                            if (y2.text == Parent_table_Greenbook) {
                                vii = y2.nodeId
                                CommonRightView(vii)
                                CurrentNodeId = vii
                                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                                setTimeout(function () {
                                    //$('#' + eqp).click();
                                    cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': tablesendingeqpchild, 'ObjName': "SAQSSA", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                                        var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                                        localStorage.setItem('Lookupobjd', data5)
                                        if (document.getElementById("TREE_div")) {
                                            document.getElementById("TREE_div").innerHTML = datas;
                                            // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                            popover()
                                        }
                                        fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                                        breadCrumb_Reset();
                                        Pmevents_breadcrumb(fab_equser_id)
                                        //var nobreadCrumb_Reset = true
                                        Subbaner("Equipment Details", CurrentNodeId, eqp, "SAQFEQ");
                                    });
                                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                                    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
                                    $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                                    $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
                                    $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "block");
                                    $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().addClass('active');
                                }, 2500);
                            }
                        });
                    }
                });
            }

        });


    }
    else if (table_id == 'table_ContractEquipment_parent' && TreeParam == 'Fab Locations') {
        GB = $(ele).closest('tr').find('td:nth-child(8)').text();
        FB_ID = $(ele).closest('tr').find('td:nth-child(12)').text();
        x = localStorage.getItem('CurrentNodeId')
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(x), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            y = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

            if (y.text == FB_ID) {
                vi = y.nodeId
                node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(vi), { silent: true }]);
                var childrenNodes = _getChildren(node);
                $(childrenNodes).each(function () {
                    z = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

                    if (z.text == GB) {

                        //console.log(childrenNodes);
                        contract_equipment_greenbook_level_nodeid = z.nodeId
                        CommonRightView(contract_equipment_greenbook_level_nodeid)
                        //Assign the CurrentNodeId for breadcrumb functionality starts..
                        CurrentNodeId = contract_equipment_greenbook_level_nodeid
                        localStorage.setItem('CurrentNodeId', CurrentNodeId)
                        //Assign the CurrentNodeId for breadcrumb functionality ends..
                        $('#table_equipment_parent').hide();
                        setTimeout(function () {
                            $('#' + eqp).click();
                        }, 1000);
                        //$('#lefttreepan #commontreeview').treeview('selectNode', [parseInt(vi), { silent: true } ]);
                    }
                });
                //$('#lefttreepan #commontreeview').treeview('selectNode', [parseInt(vi), { silent: true } ]);
                //Common_enable_disable()
            }
        });
    }
    //View from covered object subtab ends...
    else if (table_id == 'table_equipment_parent' && TreeParentParam == 'Fab Locations') {
        equipment_details = "True";
        fab_equipment_Id = $(ele).closest('tr').find('td:nth-child(4)').text();
        fab_serial_number = $(ele).closest('tr').find('td:nth-child(6)').text();
        localStorage.setItem("EquipmentIdValue", fab_equipment_Id)
        localStorage.setItem("SerialNumberValue", fab_serial_number)
        localStorage.setItem("CurrentRecordIdEQUIP", eqp);
        fab_equipment_serial_number = fab_equipment_Id + '-' + fab_serial_number
        localStorage.setItem("fab_equipment_serial_number", fab_equipment_serial_number)
        localStorage.getItem("fab_equipment_serial_number")
        //A055S000P01-21009
        GreenBook = $(ele).closest('tr').find('td:nth-child(9)').text();
		//A055S000P01-21009
        CurrentNodeId = localStorage.getItem('CurrentNodeId')
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

            if (child_node_id.text == GreenBook) {
                fablevel_equipment_greenbook_level_nodeid = child_node_id.nodeId
                CommonRightView(fablevel_equipment_greenbook_level_nodeid)
                //Assign the CurrentNodeId for breadcrumb functionality starts..
                CurrentNodeId = fablevel_equipment_greenbook_level_nodeid
                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                //Assign the CurrentNodeId for breadcrumb functionality ends..
                setTimeout(function () {
                    //$('#' + eqp).click();
                    cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': eqp, 'ObjName': "SAQFEQ", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                        var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                        localStorage.setItem('Lookupobjd', data5)
                        if (document.getElementById("TREE_div")) {
                            document.getElementById("TREE_div").innerHTML = datas;
                            // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                            popover()
                        }
                        fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                        breadCrumb_Reset();
                        Pmevents_breadcrumb(fab_equser_id)
                        //var nobreadCrumb_Reset = true
                        Subbaner("Equipment Details", CurrentNodeId, eqp, "SAQFEQ");
                    });
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                }, 3000);
            }
        });
    }
    else if ((table_id == 'table_equipment_parent' && TreeSuperParentParam == 'Fab Locations') && (TreeParentParam.includes('Sending') || TreeParentParam.includes('Receiving'))) {
        equipment_details = "True";
        fab_equipment_Id = $(ele).closest('tr').find('td:nth-child(4)').text();
        fab_serial_number = $(ele).closest('tr').find('td:nth-child(6)').text();
        localStorage.setItem("EquipmentIdValue", fab_equipment_Id)
        localStorage.setItem("SerialNumberValue", fab_serial_number)
        localStorage.setItem("CurrentRecordIdEQUIP", eqp);
        fab_equipment_serial_number = fab_equipment_Id + '-' + fab_serial_number
        localStorage.setItem("fab_equipment_serial_number", fab_equipment_serial_number)
        localStorage.getItem("fab_equipment_serial_number")
        GreenBook = $(ele).closest('tr').find('td:nth-child(8)').text();
        CurrentNodeId = localStorage.getItem('CurrentNodeId')
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

            if (child_node_id.text == GreenBook) {
                fablevel_equipment_greenbook_level_nodeid = child_node_id.nodeId
                CommonRightView(fablevel_equipment_greenbook_level_nodeid)
                //Assign the CurrentNodeId for breadcrumb functionality starts..
                CurrentNodeId = fablevel_equipment_greenbook_level_nodeid
                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                //Assign the CurrentNodeId for breadcrumb functionality ends..

                setTimeout(function () {
                    //$('#' + eqp).click();
                    cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': eqp, 'ObjName': "SAQFEQ", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                        var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                        localStorage.setItem('Lookupobjd', data5)
                        if (document.getElementById("TREE_div")) {
                            document.getElementById("TREE_div").innerHTML = datas;
                            // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                            popover()
                        }
                        fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                        breadCrumb_Reset();
                        Pmevents_breadcrumb(fab_equser_id)
                        //var nobreadCrumb_Reset = true
                        Subbaner("Equipment Details", CurrentNodeId, eqp, "SAQFEQ");
                    });

                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                }, 3000);
            }
        });
    }
    else if (table_id == 'table_equipment_parent' && (TreeParentParam.includes('Sending') || TreeParentParam.includes('Receiving') || TreeParentParam == 'Complementary Products' || TreeParam == 'Sending Equipment')) {
        equipment_details = "True";
        fab_equipment_Id = $(ele).closest('tr').find('td:nth-child(4)').text();
        //fab_serial_number =	$(ele).closest('tr').find('td:nth-child(6)').text();
        fab_serial_number = ''
        localStorage.setItem("EquipmentIdValue", fab_equipment_Id)
        localStorage.setItem("SerialNumberValue", fab_serial_number)
        localStorage.setItem("CurrentRecordIdEQUIP", eqp);
        //fab_equipment_serial_number = fab_equipment_Id+'-'+fab_serial_number
        fab_equipment_serial_number = fab_equipment_Id
        localStorage.setItem("fab_equipment_serial_number", fab_equipment_serial_number)
        localStorage.getItem("fab_equipment_serial_number")
        GreenBook = $(ele).closest('tr').find('td:nth-child(6)').text();
        CurrentNodeId = localStorage.getItem('CurrentNodeId')
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        // Hided for key navigation issue in Sending Equipment Unmapped node
        // sendingequipment_childnodes = childrenNodes[0]
        // var childrenNodes = _getChildren(sendingequipment_childnodes);
        $(childrenNodes).each(function () {
            child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

            if (child_node_id.text == GreenBook) {
                fablevel_equipment_greenbook_level_nodeid = child_node_id.nodeId
                CommonRightView(fablevel_equipment_greenbook_level_nodeid)
                //Assign the CurrentNodeId for breadcrumb functionality starts..
                CurrentNodeId = fablevel_equipment_greenbook_level_nodeid
                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                //Assign the CurrentNodeId for breadcrumb functionality ends..
                setTimeout(function () {
                    //$('#' + eqp).click();
                    cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': eqp, 'ObjName': "SAQSSE", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                        var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                        localStorage.setItem('Lookupobjd', data5)
                        if (document.getElementById("TREE_div")) {
                            document.getElementById("TREE_div").innerHTML = datas;
                            // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                            popover()
                        }
                        fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                        breadCrumb_Reset();
                        Pmevents_breadcrumb(fab_equser_id)
                        //var nobreadCrumb_Reset = true
                        Subbaner("Equipment Details", CurrentNodeId, eqp, "SAQSSE");
                    });
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                }, 3000);
            }
        });
    }
    else if (table_id == 'table_ContractEquipment_parent' && TreeParentParam == 'Fab Locations') {
        GreenBook = $(ele).closest('tr').find('td:nth-child(8)').text();
        CurrentNodeId = localStorage.getItem('CurrentNodeId')
        fab_equipment_Id = $(ele).closest('tr').find('td:nth-child(4)').text();
        fab_serial_number = $(ele).closest('tr').find('td:nth-child(6)').text();
        localStorage.setItem("EquipmentIdValue", fab_equipment_Id)
        localStorage.setItem("SerialNumberValue", fab_serial_number)
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

            if (child_node_id.text == GreenBook) {
                contract_fablevel_equipment_greenbook_level_nodeid = child_node_id.nodeId
                CommonRightView(contract_fablevel_equipment_greenbook_level_nodeid)
                //Assign the CurrentNodeId for breadcrumb functionality starts..
                CurrentNodeId = contract_fablevel_equipment_greenbook_level_nodeid
                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                //Assign the CurrentNodeId for breadcrumb functionality ends..
                setTimeout(function () {
                    cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': eqp, 'ObjName': "CTCFEQ", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                        var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                        localStorage.setItem('Lookupobjd', data5)
                        if (document.getElementById("TREE_div")) {
                            document.getElementById("TREE_div").innerHTML = datas;
                            // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                            popover()
                        }
                        fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                        localStorage.setItem("CurrentRecordId", eqp)
                        ObjectName = "CTCFEQ";
                        tool_breadcrumb();
                        // breadCrumb_Reset();
                        // Pmevents_breadcrumb(fab_equser_id)
                        //var nobreadCrumb_Reset = true
                        Subbaner("Equipment Details", CurrentNodeId, eqp, "CTCFEQ");
                    });
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                }, 3000);
                // 	$('#' + eqp).click();
                // }, 1000);
            }
        });
    }
    else if (table_id == 'SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F' && (TreeParentParam == 'Contract Items')) {
        localStorage.setItem("CurrentRecordId", cov1);
        itemGreenBook = $(ele).closest('tr').find('td:nth-child(8)').text();
        CurrentNodeId = localStorage.getItem('CurrentNodeId')
        node_id = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node_id);
        $(childrenNodes).each(function () {
            child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
            if (child_node_id.text == itemGreenBook) {
                itemlevel_equipment_node_id = child_node_id.nodeId
                CommonRightView(itemlevel_equipment_node_id)
                //Assign the CurrentNodeId for breadcrumb functionality starts..
                CurrentNodeId = itemlevel_equipment_node_id
                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                //Assign the CurrentNodeId for breadcrumb functionality ends..
                setTimeout(function () {
                    $('#' + cov1).click();
                }, 1500);
            }
        });
    }
    else if (table_id == 'JColResizer0' && TreeParam == 'Quote Items') {
        service = $(ele).closest('tr').find('td:nth-child(3) a span').text();
        ServiceId = service.slice(0, -1);
        line_item_id = $(ele).closest('tr').find('td:nth-child(2) span').text();
        x = localStorage.getItem('CurrentNodeId')
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(x), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            y = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
            //service = (y.text).split("-")[1].trim()
            if (((y.text).includes(ServiceId) && (y.text).includes(line_item_id))) {
                vi = y.nodeId
                CommonRightView(vi)
            }
        });
    }


    else if (table_id == 'SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F' && AllTreeParam['TreeParentLevel1'] == 'Quote Items') {
        localStorage.setItem("CurrentRecordId", cov1);
        GreenBook = $(ele).closest('tr').find('td:nth-child(10)').text();
        SerialNumber = $(ele).closest('tr').find('td:nth-child(8)').text();
        EquipmentId = $(ele).closest('tr').find('td:nth-child(7)').text();
        localStorage.setItem('EquipmentIdValue', EquipmentId);
        localStorage.setItem('SerialNumberValue', SerialNumber);
        var equipment_serialnumber = EquipmentId.concat('-' + SerialNumber);// to load for breadcrumb and secondary banner
        CurrentNodeId = localStorage.getItem('CurrentNodeId')
        //$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F').wrapAll('<div class="benchmarkdiv"></div>');
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

            if (child_node_id.text == GreenBook) {
                SYOBJR_00009_greenbook_level_node_id = child_node_id.nodeId
                CommonRightView(SYOBJR_00009_greenbook_level_node_id)
                //Assign the CurrentNodeId for breadcrumb functionality starts..
                CurrentNodeId = SYOBJR_00009_greenbook_level_node_id
                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                //Assign the CurrentNodeId for breadcrumb functionality ends..
                setTimeout(function () {
                    //$('#' + cov1).click();
                    CurrentRecordId = cov1

                    ObjName = 'SAQICO';
                    $('.CommonTreeDetail').css('display', 'block');
                    cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {

                        var [datas, data1, data2, data3, data4, data5, data7] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[7]];
                        localStorage.setItem('Lookupobjd', data5)
                        if (document.getElementById("TREE_div")) {
                            document.getElementById("TREE_div").innerHTML = datas;
                            popover()
                        }
                        onFieldChanges();
                        ///////////////////A055S000P01-3187 start
                        $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');

                        setTimeout(function () {
                            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");

                        }, 1);
                        Pmevents_breadcrumb(equipment_serialnumber);
                        Subbaner("Equipment Details", CurrentNodeId, cov1, "SAQICO");
                        //////////////////A055S000P01-3187 end						
                    });
                }, 2500);
            }
        });
    }
    // Quote Items SAQICO redirection - Starts
    else if (table_id.includes('CommonChildTable') && TreeParam == 'Quote Items') {
        GB = $(ele).closest('tr').find('td:nth-child(10)').text();
        FB_ID = $(ele).closest('tr').find('td:nth-child(11)').text();
        ServiceId = $(ele).closest('tr').find('td:nth-child(5)').text();

        SerialNumber = $(ele).closest('tr').find('td:nth-child(9)').text();
        EquipmentId = $(ele).closest('tr').find('td:nth-child(8)').text();
        var equipment_serialnumber = EquipmentId.concat('-' + SerialNumber);
        localStorage.setItem('EquipmentIdValue', EquipmentId);
        localStorage.setItem('SerialNumberValue', SerialNumber);

        //	$('#SYOBJR_00009_E5504B40_36E7_4EA6_9774_EA686705A63F').wrapAll('<div class="benchmarkdiv"></div>');
        x = localStorage.getItem('CurrentNodeId')
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(x), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            y = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
            //service = (y.text).split("-")[1].trim()
            text = y.text;
            Line = text.split("-")[0];
            Line = Line.trim();
            if (ServiceId.includes(Line)) {
                vi = y.nodeId
                node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(vi), { silent: true }]);
                var childrenNodes = _getChildren(node);
                $(childrenNodes).each(function () {
                    z = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

                    if (z.text == FB_ID) {
                        Items_FB_nodeid = z.nodeId
                        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(Items_FB_nodeid), { silent: true }]);
                        var childrenNodes = _getChildren(node);
                        $(childrenNodes).each(function () {
                            j = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                            if (j.text == GB) {
                                Items_equipment_nodeid = j.nodeId
                                CommonRightView(Items_equipment_nodeid)
                                //Assign the CurrentNodeId for breadcrumb functionality starts..
                                CurrentNodeId = Items_equipment_nodeid
                                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                                //Assign the CurrentNodeId for breadcrumb functionality ends..						
                                setTimeout(function () {
                                    //$('#' + cov1).click();
                                    CurrentRecordId = qte_itm_dobj

                                    ObjName = 'SAQICO';
                                    $('.CommonTreeDetail').css('display', 'block');
                                    cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {

                                        var [datas, data1, data2, data3, data4, data5, data7] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[7]];
                                        localStorage.setItem('Lookupobjd', data5)
                                        if (document.getElementById("TREE_div")) {
                                            document.getElementById("TREE_div").innerHTML = datas;
                                            popover()
                                        }
                                        //onFieldChanges();
                                        tool_breadcrumb();
                                        $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                                        $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "none");
                                        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                                        $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                                        $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                                        $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                                        setTimeout(function () {
                                            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
                                            Subbaner("Equipment Details", CurrentNodeId, cov1, "SAQICO")
                                        }, 1);
                                        Pmevents_breadcrumb(equipment_serialnumber)
                                    });
                                }, 2500);
                            }
                        });

                    }
                });

            }
        });
    }
    // Quote Items SAQICO redirection - Ends

    //View from covered object subtab starts...dont revert the below code
    else if (table_id == 'table_covered_obj_parent' && (TreeParentParam == 'Comprehensive Services' || TreeParentParam == 'Complementary Products')) {
        localStorage.setItem("CurrentRecordId", cov);
        equipment_details = "True";
        coveredobject_equipmentId = $(ele).closest('tr').find('td:nth-child(6)').text();
        coveredobject_serial_number = $(ele).closest('tr').find('td:nth-child(7)').text();
        coveredobject_equipment_serial_number = coveredobject_equipmentId + '-' + coveredobject_serial_number
        localStorage.setItem("coveredobject_equipment_serial_number", coveredobject_equipment_serial_number)
        product_fablocation = $(ele).closest('tr').find('td:nth-child(13)').text();
        product_greenbook = $(ele).closest('tr').find('td:nth-child(9)').text();
        CurrentNodeId = localStorage.getItem('CurrentNodeId')
        localStorage.setItem("EquipmentIdValue", coveredobject_equipmentId)
        localStorage.setItem("SerialNumberValue", coveredobject_serial_number)
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        if (TreeParentParam == "Comprehensive Services" || TreeParentParam == "Complementary Products") {
            //var childrenNodes = _getChildren(node);
            //$(childrenNodes).each(function(){
            //fabnodes = $('#lefttreepan #commontreeview').treeview('getNode', [ this.nodeId, { silent: true } ]);
            //fab_node = (fabnodes.text).split("-")[0].trim()
            //if ((typeof(fab_status)=="undefined") || (fab_status == "In-Active")){
            //if (fab_node == product_fablocation){
            //fab_node_id = fabnodes.nodeId
            //fab_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(fab_node_id), { silent: true } ]);
            //fab_status = "Active"
            var childrenNodes = _getChildren(node);
            $(childrenNodes).each(function () {
                child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                if (child_node_id.text == product_greenbook) {
                    Greenbook_node_id = child_node_id.nodeId
                    localStorage.setItem('AddEquipment','yes');
                    CommonRightView(Greenbook_node_id)
                    CurrentNodeId = Greenbook_node_id
                    localStorage.setItem('CurrentNodeId', CurrentNodeId)
                }
            });
            //}
            //}
            //else{

            //return
            //}
            setTimeout(function () {
                cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': cov, 'ObjName': "SAQSCO", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                    var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                    localStorage.setItem('Lookupobjd', data5)
                    if (document.getElementById("TREE_div")) {
                        $('#div_CTR_related_list').css('display','none');
                        document.getElementById("TREE_div").innerHTML = datas;
                        // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                        popover()
                        equipment_serialnumber = localStorage.getItem("coveredobject_equipment_serial_number")
                        breadCrumb_Reset();
                        Pmevents_breadcrumb(equipment_serialnumber)
                        //var nobreadCrumb_Reset = true
                        onFieldChanges();
                        Subbaner("Equipment Details", CurrentNodeId, cov, "SAQSCO");
                        if (TreeParam == 'Z0007_AG' || TreeParam == 'Z0007') {
                            $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "block");
                        }
                        else {
                            $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "none");
                        }
                    }
                    if (ObjName == 'ACACSA') {
                        onFieldChanges();
                    }
                });
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().removeClass('active')
                $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().removeClass('active')
                eqp_subtab = $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                eqp_subtab_class = eqp_subtab.attr("class");
                $("." + eqp_subtab_class).addClass("active");
                localStorage.setItem('currentSubTab', 'Equipment Details');
                fab_status = "In-Active";
            }, 1500);
            //});	
        }
    }



    else if (table_id == 'table_covered_obj_parent' && (TreeParentParam == 'Add-On Products' || TreeSuperParentParam == 'Add-On Products')) {
        localStorage.setItem("CurrentRecordId", cov);
        equipment_details = "True";
        coveredobject_equipmentId = $(ele).closest('tr').find('td:nth-child(5)').text();
        coveredobject_serial_number = $(ele).closest('tr').find('td:nth-child(6)').text();
        coveredobject_equipment_serial_number = coveredobject_equipmentId + '-' + coveredobject_serial_number
        localStorage.setItem("coveredobject_equipment_serial_number", coveredobject_equipment_serial_number)
        product_fablocation = $(ele).closest('tr').find('td:nth-child(12)').text();
        product_greenbook = $(ele).closest('tr').find('td:nth-child(8)').text();
        CurrentNodeId = localStorage.getItem('CurrentNodeId')
        localStorage.setItem("EquipmentIdValue", coveredobject_equipmentId)
        localStorage.setItem("SerialNumberValue", coveredobject_serial_number)
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        if (TreeParentParam == "Add-On Products") {
            var childrenNodes = _getChildren(node);
            $(childrenNodes).each(function () {
                fabnodes = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                left_node = (fabnodes.text).split("-")[0].trim()
                if (left_node == product_fablocation) {
                    fab_node_id = fabnodes.nodeId
                    fab_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(fab_node_id), { silent: true }]);
                    var childrenNodes = _getChildren(fab_node);
                    $(childrenNodes).each(function () {
                        child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                        if (child_node_id.text == product_greenbook) {
                            Greenbook_node_id = child_node_id.nodeId
                            CommonRightView(Greenbook_node_id)
                            CurrentNodeId = Greenbook_node_id
                            localStorage.setItem('CurrentNodeId', CurrentNodeId)
                        }
                    });

                    setTimeout(function () {
                        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': cov, 'ObjName': "SAQSCO", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                            localStorage.setItem('Lookupobjd', data5)
                            if (document.getElementById("TREE_div")) {
                                document.getElementById("TREE_div").innerHTML = datas;
                                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                popover()
                                equipment_serialnumber = localStorage.getItem("coveredobject_equipment_serial_number")
                                breadCrumb_Reset();
                                Pmevents_breadcrumb(equipment_serialnumber)
                                //var nobreadCrumb_Reset = true
                                onFieldChanges();
                                Subbaner("Equipment Details", CurrentNodeId, cov, "SAQSCO");
                                if (TreeParam == 'Z0007_AG' || TreeParam == 'Z0007') {
                                    $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "block");
                                }
                                else {
                                    $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "none");
                                }
                            }
                            if (ObjName == 'ACACSA') {
                                onFieldChanges();
                            }
                        });
                        $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
                        eqp_subtab = $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                        eqp_subtab_class = eqp_subtab.attr("class");
                        $("." + eqp_subtab_class).addClass("active");
                    }, 3000);
                }
            });
        }
        else if (TreeSuperParentParam == "Add-On Products") {
            var childrenNodes = _getChildren(node);
            $(childrenNodes).each(function () {
                gbnodes = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                if (gbnodes.text == product_greenbook) {
                    gb_node_id = gbnodes.nodeId
                    gb_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(gb_node_id), { silent: true }]);
                    CommonRightView(gb_node_id)
                    CurrentNodeId = gb_node_id
                    localStorage.setItem('CurrentNodeId', CurrentNodeId)

                    setTimeout(function () {
                        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': cov, 'ObjName': "SAQSCO", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                            localStorage.setItem('Lookupobjd', data5)
                            if (document.getElementById("TREE_div")) {
                                document.getElementById("TREE_div").innerHTML = datas;
                                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                popover()
                                equipment_serialnumber = localStorage.getItem("coveredobject_equipment_serial_number")
                                breadCrumb_Reset();
                                Pmevents_breadcrumb(equipment_serialnumber)
                                //var nobreadCrumb_Reset = true
                                onFieldChanges();
                                Subbaner("Equipment Details", CurrentNodeId, cov, "SAQSCO");
                                if (TreeParam == 'Z0007_AG' || TreeParam == 'Z0007') {
                                    $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "block");
                                }
                                else {
                                    $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "none");
                                }
                            }
                            if (ObjName == 'ACACSA') {
                                onFieldChanges();
                            }
                        });
                        $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
                        eqp_subtab = $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                        eqp_subtab_class = eqp_subtab.attr("class");
                        $("." + eqp_subtab_class).addClass("active");
                    }, 3000);
                }
            });
        }

        else if (TreeSuperParentParam == 'Comprehensive Services' || TreeSuperParentParam == 'Complementary Products') {
            var childrenNodes = _getChildren(node);
            $(childrenNodes).each(function () {
                child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

                if (child_node_id.text == product_greenbook) {
                    covered_object_greenbook_level_node_id = child_node_id.nodeId
                    CommonRightView(covered_object_greenbook_level_node_id)
                    //Assign the CurrentNodeId for breadcrumb functionality starts..
                    CurrentNodeId = covered_object_greenbook_level_node_id
                    localStorage.setItem('CurrentNodeId', CurrentNodeId)
                    //Assign the CurrentNodeId for breadcrumb functionality ends..
                    setTimeout(function () {
                        $('#' + cov).click();
                    }, 1500);
                }
            });
        }
    }//Changed the below condition because of fab removal in tree node...
    else if (table_id == 'table_covered_obj_parent' && (TreeParentParam == 'Complementary Products' || TreeParentParam == 'Comprehensive Services' || TreeParentParam == 'Receiving Equipment')) {
        localStorage.setItem("CurrentRecordId", cov);
        coveredobject_equipmentId = $(ele).closest('tr').find('td:nth-child(5)').text();
        coveredobject_serial_number = $(ele).closest('tr').find('td:nth-child(6)').text();
        coveredobject_equipment_serial_number = coveredobject_equipmentId + '-' + coveredobject_serial_number
        localStorage.setItem("coveredobject_equipment_serial_number", coveredobject_equipment_serial_number)
        product_fablocation = $(ele).closest('tr').find('td:nth-child(12)').text();
        product_greenbook = $(ele).closest('tr').find('td:nth-child(8)').text();
        CurrentNodeId = localStorage.getItem('CurrentNodeId')
        localStorage.setItem("EquipmentIdValue", coveredobject_equipmentId)
        localStorage.setItem("SerialNumberValue", coveredobject_serial_number)
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        if (TreeParentParam == "Complementary Products" || TreeParentParam == "Comprehensive Services") {
            var childrenNodes = _getChildren(node);
            $(childrenNodes).each(function () {
                fabnodes = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                left_node = (fabnodes.text).split("-")[0].trim()
                if (left_node == product_fablocation) {
                    fab_node_id = fabnodes.nodeId
                    fab_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(fab_node_id), { silent: true }]);

                    var childrenNodes = _getChildren(fab_node);
                    $(childrenNodes).each(function () {
                        child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                        if (child_node_id.text == product_greenbook) {
                            Greenbook_node_id = child_node_id.nodeId
                            CommonRightView(Greenbook_node_id)
                            CurrentNodeId = Greenbook_node_id
                            localStorage.setItem('CurrentNodeId', CurrentNodeId)
                            setTimeout(function () {
                                //$('#' + cov).click();
                                cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': cov, 'ObjName': "SAQSCO", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                                    var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                                    localStorage.setItem('Lookupobjd', data5)
                                    if (document.getElementById("TREE_div")) {
                                        document.getElementById("TREE_div").innerHTML = datas;
                                        // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                        popover()
                                        equipment_serialnumber = localStorage.getItem("coveredobject_equipment_serial_number")
                                        breadCrumb_Reset();
                                        Pmevents_breadcrumb(equipment_serialnumber)
                                        //var nobreadCrumb_Reset = true
                                        onFieldChanges();
                                        Subbaner("Equipment Details", CurrentNodeId, cov, "SAQSCO");
                                        if (TreeParam == 'Z0007_AG' || TreeParam == 'Z0007') {
                                            $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "block");
                                        }
                                        else {
                                            $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "none");
                                        }
                                    }
                                    if (ObjName == 'ACACSA') {
                                        onFieldChanges();
                                    }
                                });
                                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                                $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "block");
                                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
                            }, 1500);
                        }
                    });
                }
            });
        }

        else if (TreeSuperParentParam == 'Complementary Products' || TreeTopSuperParentParam == 'Complementary Products' || TreeSuperParentParam == 'Comprehensive Services' || TreeTopSuperParentParam == 'Comprehensive Services') {
            var childrenNodes = _getChildren(node);
            $(childrenNodes).each(function () {
                child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

                if (child_node_id.text == product_greenbook) {
                    covered_object_greenbook_level_node_id = child_node_id.nodeId
                    CommonRightView(covered_object_greenbook_level_node_id)
                    //Assign the CurrentNodeId for breadcrumb functionality starts..
                    CurrentNodeId = covered_object_greenbook_level_node_id
                    localStorage.setItem('CurrentNodeId', CurrentNodeId)
                    //Assign the CurrentNodeId for breadcrumb functionality ends..
                    setTimeout(function () {
                        //$('#' + cov).click();
                        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': cov, 'ObjName': "SAQSCO", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                            localStorage.setItem('Lookupobjd', data5)
                            if (document.getElementById("TREE_div")) {
                                document.getElementById("TREE_div").innerHTML = datas;
                                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                popover()
                                equipment_serialnumber = localStorage.getItem("coveredobject_equipment_serial_number")
                                breadCrumb_Reset();
                                Pmevents_breadcrumb(equipment_serialnumber)
                                //var nobreadCrumb_Reset = true
                                onFieldChanges();
                                Subbaner("Equipment Details", CurrentNodeId, cov, "SAQSCO");
                                if (TreeParam == 'Z0007_AG' || TreeParam == 'Z0007') {
                                    $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "block");
                                }
                                else {
                                    $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "none");
                                }
                            }
                            if (ObjName == 'ACACSA') {
                                onFieldChanges();
                            }
                        });
                        $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                        $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
                    }, 1500);
                }
            });
        }
    }
    //View from covered object subtab ends...
    else if (table_id == 'table_ContractCovered_obj_parent' && (TreeParentParam == 'Comprehensive Services' || TreeParentParam == 'Complementary Products')) {
        Serial = $(ele).closest('tr').find('td:nth-child(6)').text();
        Eqp_id = $(ele).closest('tr').find('td:nth-child(4)').text();
        var Eqp_ser = Eqp_id.concat("-", Serial)
        GreenBook = $(ele).closest('tr').find('td:nth-child(7)').text();
        CurrentNodeId = localStorage.getItem('CurrentNodeId')
        node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node);
        $(childrenNodes).each(function () {
            child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);

            if (child_node_id.text == GreenBook) {
                contract_covered_object_greenbook_level_node_id = child_node_id.nodeId
                CommonRightView(contract_covered_object_greenbook_level_node_id)
                //Assign the CurrentNodeId for breadcrumb functionality starts..
                CurrentNodeId = contract_covered_object_greenbook_level_node_id
                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                //Assign the CurrentNodeId for breadcrumb functionality ends..
                $("#div_CTR_related_list").hide();
                setTimeout(function () {
                    //$('#' + contract_cov).click();
                    cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': contract_cov, 'ObjName': "CTCSCO", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                        var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                        localStorage.setItem('Lookupobjd', data5)
                        if (document.getElementById("TREE_div")) {
                            document.getElementById("TREE_div").innerHTML = datas;
                            // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                            popover()
                            //equipment_serialnumber = localStorage.getItem("coveredobject_equipment_serial_number")
                            breadCrumb_Reset();
                            Pmevents_breadcrumb(Eqp_ser)
                            //var nobreadCrumb_Reset = true
                            onFieldChanges();
                            Subbaner("Equipment Details", CurrentNodeId, contract_cov, "CTCSCO");
                            //subTabDetails("Equipment Details", 'Detail', 'CTCSCO', contract_cov)

                        }

                    });
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block").addClass('active');
                    $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "block").removeClass('active');
                    $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block").removeClass('active');
                }, 1000);
            }
        });
    }
    else if (table_id == 'SYOBJR_91822_7A8F0522_9728_4CF9_A4C9_3F905D3B6130' && TreeParentParam == 'Contract Items') {
        itemGreenBook = $(ele).closest('tr').find('td:nth-child(9)').text();
        CurrentNodeId = localStorage.getItem('CurrentNodeId')
        node_id = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
        $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
        var childrenNodes = _getChildren(node_id);
        $(childrenNodes).each(function () {
            child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
            if (child_node_id.text == itemGreenBook) {
                itemlevel_equipment_node_id = child_node_id.nodeId
                CommonRightView(itemlevel_equipment_node_id)
                //Assign the CurrentNodeId for breadcrumb functionality starts..
                CurrentNodeId = itemlevel_equipment_node_id
                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                //Assign the CurrentNodeId for breadcrumb functionality ends..
                setTimeout(function () {
                    $('#' + itm).click();
                }, 1500);
            }
        });
    }
    //View from covered object subtab ends...dont revert the above code
    else {////A055S000P01-17070 code starts.. ends...
        if ((table_id.includes('SYOBJR_98798') || table_id.includes('SYOBJR_00032') || table_id.includes('SYOBJR_00038') || table_id.includes('SYOBJR_98789')) && TreeParam == "Customer Information") {
            var Role = $(ele).closest('tr').find('td:nth-child(9)').text();
            var account_record_id = $(ele).closest('tr').find('td:nth-child(3)').text();
            if (!table_id.includes('SYOBJR_00038')) {
                var account_id = $(ele).closest('tr').find('td:nth-child(4)').text();
                localStorage.setItem("account_id", account_id)
            }
            var subtabName = localStorage.getItem("currentSubTab")
            if (Role) {
                if (Role.includes("SENDING")) {
                    breadCrumb_Reset()
                    account_id = localStorage.getItem("account_id")
                    fts_breadcrumb(account_id)
                    //localStorage.setItem("account_record_id",account_record_id)
                    $('div#COMMON_TABS').find("li a:contains('Accounts')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Contacts')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Sending Fab Locations')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Sending Account Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Receiving Account Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().addClass('active');


                }
                else if (Role.includes("RECEIVING")) {
                    breadCrumb_Reset()
                    account_id = localStorage.getItem("account_id")
                    fts_breadcrumb(account_id)
                    //localStorage.setItem("account_record_id",account_record_id)
                    $('div#COMMON_TABS').find("li a:contains('Accounts')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Contacts')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Receiving Account Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Sending Account Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Receiving Fab Locations')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().addClass('active');
                }
                else {
                    breadCrumb_Reset()
                    account_id = localStorage.getItem("account_id")
                    fts_breadcrumb(account_id)
                }
            }
            else if (subtabName == "Sending Fab Locations" && TreeParam == "Customer Information") {////A055S000P01-17070 code starts.. ends...
                ObjectName = "SAQSAF"
                tool_breadcrumb()
                //account_id = localStorage.getItem("account_id")
                //fts_breadcrumb(account_id)
                //var sending_fab_id = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
                //localStorage.setItem("CurrentRecordId",sending_fab_id)
                $('div#COMMON_TABS').find("li a:contains('Accounts')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Contacts')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Sending Fab Details')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Sending Equipment')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Sending Fab Locations')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Sending Fab Details')").parent().addClass('active');
            }
            else if (subtabName == "Receiving Fab Locations" && TreeParam == "Customer Information") {////A055S000P01-17070 code starts.. ends...
                //account_id = localStorage.getItem("account_id")
                //fts_breadcrumb(account_id);
                //var receiving_fab_id = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
                //localStorage.setItem("CurrentRecordId",receiving_fab_id)
                ObjectName = "SAQFBL"
                tool_breadcrumb()
                $('div#COMMON_TABS').find("li a:contains('Accounts')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Contacts')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Sending Fab Location Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Receiving Fab Details')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Receiving Equipment')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Receiving Fab Locations')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Receiving Fab Details')").parent().addClass('active');
            }

        }
        if (localStorage.getItem("currentSubTab") == "Items" && TreeParam == "Quote Items") {
            $('div#COMMON_TABS').find("li a:contains('Summary')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Items')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Offerings')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Annualized Items')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Entitlement Cost/Price')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css('display', 'block');
            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css('display', 'block');
            $('div#COMMON_TABS').find("li a:contains('Object List')").parent().css('display', 'block');
            $('div#COMMON_TABS').find("li a:contains('Product List')").parent().css('display', 'block');
            $('div#COMMON_TABS').find("li a:contains('Assortment Module')").parent().css('display', 'block');
            $('div#COMMON_TABS').find("li a:contains('Billing Plan')").parent().css('display', 'block');
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().addClass('active');
            //INC08812229 - Start - M
            var line_index = $(ele).closest('table').find('[data-field="QUOTE_REVISION_CONTRACT_ITEM_ID"]').index()+1;
            line = $(ele).closest('tr').find('td:nth-child('+line_index+') abbr').attr('id');
            //line = $(ele).closest('tr').find('td:nth-child(4) abbr').attr('id');
            var line_item_index = $(ele).closest('table').find('[data-field="LINE"]').index()+1;
            line_item = $(ele).closest('tr').find('td:nth-child('+line_item_index+')').text();
            //line_item = $(ele).closest('tr').find('td:nth-child(5) a').text();
            //INC08812229 - End - M
            localStorage.setItem("line_item", line_item);
            localStorage.setItem("CurrentRecordId", line)
            ObjectName = "SAQRIT"
            tool_breadcrumb();
            Subbaner("Details", CurrentNodeId, line, 'SAQRIT');
        }
        if (TreeParam == 'Add-On Products') {
            add_on_service = $(ele).closest('tr').find('td:nth-child(3) abbr').text();
            add_on_rec_id = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
            localStorage.setItem("CurrentRecordId", add_on_rec_id);
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
            if (add_on_service == "Z0123") {
                $('div#COMMON_TABS').find("li a:contains('Add-on Products')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('NSO Catalog')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().addClass('active');
                tool_breadcrumb();

            }
            else {
                $('div#COMMON_TABS').find("li a:contains('Add-on Products')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
                if (add_on_service == 'Z0116') { //A055S000P01-20741 - M
                    $('div#COMMON_TABS').find("li a:contains('Credits')").parent().css("display", "block");
                }
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().addClass('active');
                add_on_rec_id = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
                localStorage.setItem("CurrentRecordId", add_on_rec_id);
                breadCrumb_Reset()
                chainsteps_breadcrumb($(ele).closest('tr').find('td:nth-child(3) a abbr').text());
            }

        }
        if (localStorage.getItem("currentSubTab") == "Annualized Items" && TreeParam == "Quote Items") {
            $('div#COMMON_TABS').find("li a:contains('Summary')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Items')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Offerings')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Annualized Items')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Entitlement Cost/Price')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().css('display', 'block');
            $('div#COMMON_TABS').find("li a:contains('Details')").parent().addClass('none');
            var RecordId = $(ele).closest('tr').find('td:nth-child(4)').text();
            line = $(ele).closest('tr').find('td:nth-child(5)').text();
            localStorage.setItem("RecordIds", RecordId)
            localStorage.setItem("RecordId", line)
            ObjName = "SAQICO"
            tool_breadcrumb();
            Subbaner("Details", CurrentNodeId, RecordId, 'SAQICO');
        }
        if (table_id.includes("SYOBJR_00009") && AllTreeParam['TreeParentLevel2'] == 'Quote Items') {
            if (EquipmentId != null && SerialNumber != null) {
                SerialNumber = $(ele).closest('tr').find('td:nth-child(7)').text();
                EquipmentId = $(ele).closest('tr').find('td:nth-child(6)').text();
                localStorage.setItem('EquipmentIdValue', EquipmentId);
                localStorage.setItem('SerialNumberValue', SerialNumber);
            }
        }
        if (table_id.includes("SYOBJR_98857") || table_id.includes('SYOBJR_98858') || table_id.includes('SYOBJR_00028')) {
            localStorage.setItem('CurrentRecordId', sourcefab);
            localStorage.setItem('eqp_details', 'true');
            localStorage.setItem('srcfab_details', 'true');
            localStorage.setItem('toolmatrix_details', 'true');
            $('.involvedparties_Details ').hide();
            $('div#COMMON_TABS').find("li a:contains('Source Fab Locations')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().css("display", "none");
            $(".SourceFabLocation").hide()

            tool_breadcrumb();
        }
        if (table_id.includes("table_covered_obj_parent")) {
            //INC08634400-M
            var equp_index = $(ele).closest('table').find('[data-field="EQUIPMENT_ID"]').index()+1;
            var equpserial_index = $(ele).closest('table').find('[data-field="SERIAL_NO"]').index()+1;
            coveredobject_equipmentId = $(ele).closest('tr').find('td:nth-child('+equp_index+')').text();
            coveredobject_serial_number = $(ele).closest('tr').find('td:nth-child('+equpserial_index+')').text();
            //INC08634400-M
            coveredobject_equipment_serial_number = coveredobject_equipmentId + '-' + coveredobject_serial_number
            localStorage.setItem("EquipmentIdValue", coveredobject_equipmentId)
            localStorage.setItem("SerialNumberValue", coveredobject_serial_number)
            localStorage.setItem("coveredobject_equipment_serial_number", coveredobject_equipment_serial_number)
        }

        if (table_id.includes("table_equipment_parent")) {
            fab_equipment_Id = $(ele).closest('tr').find('td:nth-child(4)').text();
            fab_serial_number = $(ele).closest('tr').find('td:nth-child(6)').text();
            localStorage.setItem("EquipmentIdValue", fab_equipment_Id)
            localStorage.setItem("SerialNumberValue", fab_serial_number)
            var fab_equipment_serial_number = fab_equipment_Id.concat('-', fab_serial_number);
            localStorage.setItem("coveredobject_equipment_serial_number", fab_equipment_Id)
            if (AllTreeParam['TreeParentLevel0'] == "UNMAPPED" && AllTreeParam['TreeParentLevel2'] == "Fab Locations") {
                var eqp = $(ele).attr('id');
                localStorage.setItem("CurrentRecordIdEQUIP", eqp);
            };


        }
        //View from Assembly table starts...
        if (table_id.includes("covered_obj_child") && (TreeParentParam == "Comprehensive Services" || TreeParentParam == "Complementary Products")) {
            //A055S000P01-20381 - A
            var assembly_index = $(ele).closest('table').find('[data-field="ASSEMBLY_ID"]').index()+1;
            var greenbook_index = $('#table_covered_obj_parent').find('[data-field="GREENBOOK"]').index()+1;
            var fab_index = $('#table_covered_obj_parent').find('[data-field="FABLOCATION_ID"]').index()+1;
            var SerialNumber_index = $('#table_covered_obj_parent').find('[data-field="SERIAL_NO"]').index()+1;
            var EquipmentId_index = $('#table_covered_obj_parent').find('[data-field="EQUIPMENT_ID"]').index()+1;
            Assembly_id_value = $(ele).closest('tr').find('td:nth-child('+assembly_index+')').text();
            Covered_object_record_id = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(3) a:last').attr('id');
            Parent_table_Greenbook = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child('+greenbook_index+')').text();
            Fab_Id = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child('+fab_index+')').text();
            SerialNumber = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child('+SerialNumber_index+')').text();
            EquipmentId = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child('+EquipmentId_index+')').text();
            //A055S000P01-20381 - A
            Equipment_serial_number = EquipmentId + '-' + SerialNumber
            localStorage.setItem("Covered_object_record_id", Covered_object_record_id)
            localStorage.setItem("AssemblyIdValue", Assembly_id_value)
            localStorage.setItem("EquipmentIdValue", EquipmentId)
            localStorage.setItem("SerialNumberValue", SerialNumber)
            localStorage.setItem("EquipmentSerialNumber", Equipment_serial_number)
            localStorage.setItem("AssemblyId", "Yes")
            CurrentNodeId = localStorage.getItem('CurrentNodeId')
            node_id = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
            $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
            if (TreeParentParam == "Comprehensive Services" || TreeParentParam == "Complementary Products") {
                var childrenNodes = _getChildren(node_id);
                $(childrenNodes).each(function () {
                    child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                    if (child_node_id.text == Parent_table_Greenbook) {
                        Greenbook_pm_events_node_id = child_node_id.nodeId
                        CommonRightView(Greenbook_pm_events_node_id)
                        CurrentNodeId = Greenbook_pm_events_node_id
                        localStorage.setItem('CurrentNodeId', CurrentNodeId)
                    }
                });
            }
            // FROM FAB LOCATION LEVEL CODE STARTS..
            else if (table_id.includes("covered_obj_child") && (TreeSuperParentParam == 'Comprehensive Services' || TreeSuperParentParam == 'Complementary Products')) {
                Assembly_id_value = $(ele).closest('tr').find('td:nth-child(4)').text();
                Covered_object_record_id = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(3) a:last').attr('id');
                Parent_table_Greenbook = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(6)').text();
                //Fab_Id = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(12)').text();
                Fab_Id = $(ele).closest("table").closest('tr').find('td:nth-child(9)').text();
                //SerialNumber = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(6)').text();
                EquipmentId = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(4)').text();
                //Equipment_serial_number = EquipmentId+'-'+SerialNumber
                localStorage.setItem("Covered_object_record_id", Covered_object_record_id)
                localStorage.setItem("AssemblyIdValue", Assembly_id_value)
                localStorage.setItem("EquipmentIdValue", EquipmentId)
                localStorage.setItem("SerialNumberValue", SerialNumber)
                localStorage.setItem("EquipmentSerialNumber", Equipment_serial_number)
                localStorage.setItem("AssemblyId", "Yes")
                CurrentNodeId = localStorage.getItem('CurrentNodeId')
                node_id = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
                $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
                var childrenNodes = _getChildren(node_id);
                $(childrenNodes).each(function () {
                    fab_child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                    if (fab_child_node_id.text == Parent_table_Greenbook) {
                        fab_greenbook_node_id = fab_child_node_id.nodeId
                        CommonRightView(fab_greenbook_node_id)
                        CurrentNodeId = fab_greenbook_node_id
                        localStorage.setItem('CurrentNodeId', CurrentNodeId)
                    }
                });
            }
            //FROM FAB LOCATION LEVEL CODE ENDS..
            else {
                CommonRightView(CurrentNodeId)
            }

        }
        else if (table_id.includes("table_sending_equipment_child") && TreeParentParam == "Complementary Products") {
            Assembly_id_value = $(ele).closest('tr').find('td:nth-child(5)').text();
            Covered_object_record_id = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(3) a:last').attr('id');
            Parent_table_Greenbook = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(6)').text();
            Fab_Id = $(ele).closest('tr').find('td:nth-child(9)').text();
            //SerialNumber = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(6)').text();
            EquipmentId = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(4)').text();
            //Equipment_serial_number = EquipmentId+'-'+SerialNumber
            localStorage.setItem("Covered_object_record_id", Covered_object_record_id)
            localStorage.setItem("AssemblyIdValue", Assembly_id_value)
            localStorage.setItem("EquipmentIdValue", EquipmentId)
            //localStorage.setItem("SerialNumberValue",SerialNumber)
            //localStorage.setItem("EquipmentSerialNumber",Equipment_serial_number)
            localStorage.setItem("AssemblyId", "Yes")
            CurrentNodeId = localStorage.getItem('CurrentNodeId')
            node_id = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
            $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
            if (TreeParentParam == "Complementary Products") {
                var childrenNodes = _getChildren(node_id);
                $(childrenNodes).each(function () {
                    fabnodes = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                    if ((typeof (fab_status) == "undefined") || (fab_status == "In-Active")) {
                        if (fabnodes.text == Fab_Id) {
                            fab_node_id = fabnodes.nodeId
                            fab_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(fab_node_id), { silent: true }]);
                            fab_status = "Active"
                            var childrenNodes = _getChildren(fab_node);
                            $(childrenNodes).each(function () {
                                child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                                if (child_node_id.text == Parent_table_Greenbook) {
                                    Greenbook_pm_events_node_id = child_node_id.nodeId
                                    CommonRightView(Greenbook_pm_events_node_id)
                                    CurrentNodeId = Greenbook_pm_events_node_id
                                    localStorage.setItem('CurrentNodeId', CurrentNodeId)
                                    setTimeout(function () {
                                        //$('#' + eqp).click();
                                        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': tablesendingeqpchild, 'ObjName': "SAQSSA", 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'DetailList': '' }, function (dataset) {
                                            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                                            localStorage.setItem('Lookupobjd', data5)
                                            if (document.getElementById("TREE_div")) {
                                                document.getElementById("TREE_div").innerHTML = datas;
                                                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                                popover()
                                            }
                                            fab_equser_id = localStorage.getItem("fab_equipment_serial_number")
                                            breadCrumb_Reset();
                                            Pmevents_breadcrumb(fab_equser_id)
                                            //var nobreadCrumb_Reset = true
                                            Subbaner("Assembly Details", CurrentNodeId, eqp, "SAQSSA");
                                        });
                                        $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                                        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                                        $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
                                        $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                                    }, 3000);
                                }
                            });
                        }
                    }
                    else {
                        return
                    }
                    setTimeout(function () {
                        fab_status = "In-Active";
                    }, 3000);
                });
            }
            // else{
            // CommonRightView(CurrentNodeId)
            // }
        }
        if (table_id.includes("covered_obj_child") && (TreeSuperParentParam == 'Comprehensive Services' || TreeSuperParentParam == 'Add-On Products')) {

            //A055S000P01-20381 - A
            var assembly_index = $(ele).closest('table').find('[data-field="ASSEMBLY_ID"]').index()+1;
            var greenbook_index = $('#table_covered_obj_parent').find('[data-field="GREENBOOK"]').index()+1;
            var fab_index = $('#table_covered_obj_parent').find('[data-field="FABLOCATION_ID"]').index()+1;
            var SerialNumber_index = $('#table_covered_obj_parent').find('[data-field="SERIAL_NO"]').index()+1;
            var EquipmentId_index = $('#table_covered_obj_parent').find('[data-field="EQUIPMENT_ID"]').index()+1;
            Assembly_id_value = $(ele).closest('tr').find('td:nth-child('+assembly_index+')').text();
            Covered_object_record_id = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(3) a:last').attr('id');
            Parent_table_Greenbook = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child('+greenbook_index+')').text();
            Fab_Id = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child('+fab_index+')').text();
            SerialNumber = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child('+SerialNumber_index+')').text();
            EquipmentId = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child('+EquipmentId_index+')').text();
            //A055S000P01-20381 - A
            Equipment_serial_number = EquipmentId + '-' + SerialNumber
            localStorage.setItem("Covered_object_record_id", Covered_object_record_id)
            localStorage.setItem("AssemblyIdValue", Assembly_id_value)
            localStorage.setItem("EquipmentIdValue", EquipmentId)
            localStorage.setItem("SerialNumberValue", SerialNumber)
            localStorage.setItem("EquipmentSerialNumber", Equipment_serial_number)
            localStorage.setItem("AssemblyId", "Yes")
            CurrentNodeId = localStorage.getItem('CurrentNodeId')
            node_id = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
            $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
            var childrenNodes = _getChildren(node_id);
            $(childrenNodes).each(function () {
                fab_child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                if (fab_child_node_id.text == Parent_table_Greenbook) {
                    fab_greenbook_node_id = fab_child_node_id.nodeId
                    CommonRightView(fab_greenbook_node_id)
                    CurrentNodeId = fab_greenbook_node_id
                    localStorage.setItem('CurrentNodeId', CurrentNodeId)
                }
            });
        }
        if (table_id.includes("covered_obj_child") && TreeParentParam == "Add-On Products") {
            Assembly_id_value = $(ele).closest('tr').find('td:nth-child(4)').text();
            Covered_object_record_id = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(3) a:last').attr('id');
            Parent_table_Greenbook = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(8)').text();
            Fab_Id = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(12)').text();
            SerialNumber = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(6)').text();
            EquipmentId = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(5)').text();
            Equipment_serial_number = EquipmentId + '-' + SerialNumber
            localStorage.setItem("Covered_object_record_id", Covered_object_record_id)
            localStorage.setItem("AssemblyIdValue", Assembly_id_value)
            localStorage.setItem("EquipmentIdValue", EquipmentId)
            localStorage.setItem("SerialNumberValue", SerialNumber)
            localStorage.setItem("EquipmentSerialNumber", Equipment_serial_number)
            localStorage.setItem("AssemblyId", "Yes")
            CurrentNodeId = localStorage.getItem('CurrentNodeId')
            node_id = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true }]);
            $('#lefttreepan #commontreeview').treeview('expandNode', [1, { silent: true }]);
            if (TreeParentParam == "Add-On Products") {
                var childrenNodes = _getChildren(node_id);
                $(childrenNodes).each(function () {
                    fabnodes = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                    if (fabnodes.text == Fab_Id) {
                        fab_node_id = fabnodes.nodeId
                        fab_node = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(fab_node_id), { silent: true }]);
                        fab_status = "Active"
                        var childrenNodes = _getChildren(fab_node);
                        $(childrenNodes).each(function () {
                            child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [this.nodeId, { silent: true }]);
                            if (child_node_id.text == Parent_table_Greenbook) {
                                Greenbook_pm_events_node_id = child_node_id.nodeId
                                CommonRightView(Greenbook_pm_events_node_id)
                                CurrentNodeId = Greenbook_pm_events_node_id
                                localStorage.setItem('CurrentNodeId', CurrentNodeId)
                            }
                        });
                    }
                });
            }
        }
        //View from Assembly table ends...
        var record_id = table_id.split('_');
        var TableId = record_id[0] + '-' + record_id[1];
        localStorage.setItem('TableId_cancel_fun', TableId);
        if (TableId == "SYOBJR-00010" || TableId == "SYOBJR-00008" || TableId == "SYOBJR-00009" || TableId == "SYOBJR-98841" || TableId.includes("WithBundleParentTable")) {
            var RecordId = $(ele).closest('tr').find('td:nth-child(4)').text();
        }
        else {
            var RecordId = $(ele).closest('tr').find('td:nth-child(3)').text();
        }
        objn = RecordId.split('-')
        ObjectName = objn[0]
        if (TableId == "SYOBJR-98872") {
            ObjectName = "SAQRIT"
        }
        if (TableId == "SYOBJR-98873") {
            ObjectName = "SAQRIP"
        }

        if (TableId == "SYOBJR-00010" || TableId == "SYOBJR-00008" || TableId == "SYOBJR-98841" || TableId == "SYOBJR-98799") {
            var KeyId = $(ele).closest('tr').find('td:nth-child(4) a abbr').attr('id');
        }
        else if (TableId.includes("WithBundleParentTable")) {
            var KeyId = $(ele).closest('tr').attr('id');
        }
        else if (TableId == "table-covered") {
            var obj = $(ele).closest('tr').find('td:nth-child(3) a:last-child').attr('title');
        }
        else if (TableId == "table-Preventive") {
            var obj = $(ele).closest('tr').find('td:nth-child(3) a:last-child').attr('title');
        }
        else if (TableId == "table-equipment") {
            var obj = $(ele).closest('tr').find('td:nth-child(2) a:last-child').attr('title');
        }
        else if (TableId == "SYOBJR-98872") {
            var KeyId = $(ele).closest('tr').find('td:nth-child(4) a abbr').attr('id');
        }
        else if (TableId == "SYOBJR-00005") {
            var KeyId = $(ele).closest('tr').find('td:nth-child(4) > a > abbr').attr('id');
        }
        else {
            var KeyId = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
        }
        /*if (TableId == 'SYOBJR-95813') {
            data_type = $(ele).closest('tr').find('td:nth-child(6)').text();
            $(".Layout_tabs_cls_Id").css("display", "none");
            $(".Layout_qstn_Id").css("display", "block");
            $('#COMMON_TABS').find('#Layout_qstn_id').addClass('active');
            if (data_type == 'TABLE') {
                $('#COMMON_TABS').find('#Layout_qstn_tbl_col_id').show();
            }
            else {
                $('#COMMON_TABS').find('#Layout_qstn_tbl_col_id').hide();
            }
            $('#ADDNEW__SYOBJR_95813_SYOBJ_00454').hide();
        }*/
        $('.CommonTreeDetail').css('display', 'block');
        $('.Detail, .Related').css('display', 'none');
        localStorage.setItem('TreeParamRecordId', RecordId);
        //11642 start
        /*if (TableId == 'SYOBJR-95812' || 'SYOBJR-95813' || 'SYOBJR-95814') {
            if (TableId == 'SYOBJR-95813') {
                $('#COMMON_TABS').css("display", "block");
                $('#Layout_qstn_id').css('display', 'block');
                $('#Layout_Rules_id').css('display', 'block');

            }
            Subbaner('', KeyId, ObjectName)
        }*/
        if (TableId == 'SYOBJR-98799') {
            $('#TREE_div').css('display', 'block');
            localStorage.setItem("bktolist", "yes");
            localStorage.setItem("showrefresh", "no");
            localStorage.setItem("CurrentRecordId", KeyId);
            $('#div_CTR_related_list').css('display', 'none');
            tool_breadcrumb();
            //commented to check the secondary banner
            //Subbaner(CurrentNodeId, KeyId, 'SAQDOC');
            downloadExcelConfiguration(KeyId, ObjectName)


        }

        else if (TableId == 'SYOBJR-00014') {
            $('#TREE_div').css('display', 'block');
            localStorage.setItem("CurrentRecordId", KeyId);
            tool_breadcrumb();
            Subbaner("Approvers", CurrentRecordId, KeyId, 'ACACSA');
        }
        else if (TableId == 'SYOBJR-00010') {
            $('#TREE_div').css('display', 'block');
            localStorage.setItem("CurrentRecordId", KeyId);
        }
        else if (TableId == 'SYOBJR-00015') {
            $('#TREE_div').css('display', 'block');
            localStorage.setItem("CurrentRecordId", KeyId);
            tool_breadcrumb();
            Subbaner("Tracked Fields", CurrentRecordId, KeyId, 'ACAPTF');
        }
        else if (TableId == 'SYOBJR-00026') {
            $('#TREE_div').css('display', 'block');
            localStorage.setItem("CurrentRecordId", KeyId);
            tool_breadcrumb();
            //Subbaner("Tracked Fields",CurrentRecordId, KeyId, 'ACAPTF');
        }
        /*else if (TableId == 'SYOBJR-98798') {
            $('.fixed-table-body').css('display','none');
            localStorage.setItem("CurrentRecordId",KeyId);
            tool_breadcrumb();
            //Subbaner("Tracked Fields",CurrentRecordId, KeyId, 'ACAPTF');
        }*/
        else if (TableId == 'SYOBJR-98871') {
            // $('.fixed-table-body').css('display','none');
            localStorage.setItem("CurrentRecordId", KeyId);
            tool_breadcrumb();
            //Subbaner("Tracked Fields",CurrentRecordId, KeyId, 'ACAPTF');
        }
        var [TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam] = [localStorage.getItem('CommonTreeParam'), localStorage.getItem('CommonTreeParentParam'), localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam')];
        //11642 end 
        if (ProductId == '271' || ProductId == '2240' || ProductId == '273' || ProductId == '610' || ProductId == '710') {
            x = localStorage.getItem('CurrentNodeId')
            if (TableId == "SYOBJR-00008" || TableId == "SYOBJR-98872" || TableId == "SYOBJR-00010" || TableId == "SYOBJR-98841" || TableId == "SYOBJR-98799") {
                var RecordId = $(ele).closest('tr').find('td:nth-child(4) abbr').attr('id');
            }
            else if (TableId.includes("WithBundleParentTable")) {
                var RecordId = $(ele).attr('id');
            }
            else if (TableId == "table-covered") {
                var RecordId = $(ele).closest('tr').find('td:nth-child(3) a:last-child').attr('id');
            }
            else if (TableId == "table-Preventive") {
                var RecordId = $(ele).closest('tr').find('td:nth-child(3) a:last-child').attr('id');
            }

            else if (TableId == "table-equipment") {
                var RecordId = $(ele).closest('tr').find('td:nth-child(2) a:last-child').attr('id');
            }
            else if (TableId == "SYOBJR-00005") {
                var RecordId = $(ele).closest('tr').find('td:nth-child(4) > a > abbr').attr('id');
            }
            else {
                var RecordId = $(ele).closest('tr').find('td:nth-child(3) abbr').attr('id');
                if (RecordId == undefined) {

                    var RecordId = $(ele).closest('tr').find('td:nth-child(3)')[0].innerText;
                }
            }
            AllTreeParams = JSON.parse(AllTreeParams)
            AllTreeParams = JSON.stringify(AllTreeParams)
            if (TableId == "SYOBJR-00008" || TableId == "SYOBJR-00010" || TableId == "SYOBJR-98841" || TableId == "SYOBJR-98799") {
                var obj = $(ele).closest('tr').find('td:nth-child(4) abbr').attr('title');
            }
            else if (TableId.includes("WithBundleParentTable")) {
                var obj = $(ele).text();
            }
            else if (TableId == "table-covered") {
                var obj = $(ele).closest('tr').find('td:nth-child(3) a:last-child').attr('title');
            }
            else if (TableId == "table-Preventive") {
                var obj = $(ele).closest('tr').find('td:nth-child(3) a:last-child').attr('title');
            }
            else if (TableId == "table-equipment") {
                var obj = $(ele).closest('tr').find('td:nth-child(2) a:last-child').attr('title');
            }
            else if (TableId == "SYOBJR-98872") {
                var obj = $(ele).closest('tr').find('td:nth-child(2) a:last-child').attr('title');
            }
            else {
                var obj = $(ele).closest('tr').find('td:nth-child(3) abbr').attr('title');
            }
            if (obj) {
                objn = obj.split('-')
                ObjectName = objn[0]
                if (TableId == "SYOBJR-98873") {
                    ObjectName = "SAQRIP"
                }
                if (TableId == "SYOBJR-00005") {
                    ObjectName = "SAQSPT"
                }
                if (TableId == "SYOBJR-98859") {
                    ObjectName = "SAQSGB"
                }
                node = $('#commontreeview').treeview('getNode', parseInt(x));
                //$('#commontreeview').treeview('expandNode', [ x, {silent: true } ]);
                var childrenNodes = _getChildren(node);
                $(childrenNodes).each(function (ele) {
                    //console.log(ele)
                    y = $('#commontreeview').treeview('getNode', this.nodeId);
                    if (y.id == RecordId) {
                        nodeId = y.nodeId
                        $('#commontreeview').treeview('selectNode', [parseInt(nodeId), { silent: true }]);
                        CommonRightView(nodeId)
                        if (nodeId != '' && nodeId != null) {
                            TreeParentParam = $('#commontreeview').treeview('getParent', nodeId).text;
                            TreeParentNodeId = $('#commontreeview').treeview('getParent', nodeId).nodeId;
                            TreeParentNodeRecId = $('#commontreeview').treeview('getParent', nodeId).id;
                        }
                        if (TreeParentNodeId != '' && TreeParentNodeId != null) {
                            TreeSuperParentParam = $('#commontreeview').treeview('getParent', TreeParentNodeId).text;
                            TreeSuperParentId = $('#commontreeview').treeview('getParent', TreeParentNodeId).nodeId;
                            TreeSuperParentRecId = $('#commontreeview').treeview('getParent', TreeParentNodeId).id;
                        }
                        if (TreeSuperParentId != '' && TreeSuperParentId != null) {
                            TreeTopSuperParentParam = $('#commontreeview').treeview('getParent', TreeSuperParentId).text;
                            TreeTopSuperParentId = $('#commontreeview').treeview('getParent', TreeSuperParentId).nodeId;
                            TreeTopSuperParentRecId = $('#commontreeview').treeview('getParent', TreeSuperParentId).id;
                        }
                        if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null) {
                            TreeSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).text;
                            TreeSuperTopParentId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
                            TreeSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).id;
                        }
                        localStorage.setItem('CommonParentNodeRecId', TreeParentNodeRecId);
                        localStorage.setItem('CommonTreeSuperParentRecId', TreeSuperParentRecId);
                        localStorage.setItem('CommonTopSuperParentRecId', TreeTopSuperParentRecId);
                        localStorage.setItem('CommonSuperTopParentParam', TreeSuperTopParentParam);
                    }
                });
            }
            $('.CommonTreeDetail').css('display', 'block');
            if (TableId != 'table-covered' && TableId != 'covered-obj' && TableId != 'table-ContractCovered' && TableId != 'table-equipment' && TableId != 'table-ContractEquipment' && TableId != 'SYOBJR-00005' && TableId != 'SYOBJR-91822' && TableId != 'SYOBJR-00010' && TableId != 'table-assemblies') {
                loadDetails(RecordId, ObjectName, AllTreeParams)
            }
            else if (TableId == 'table-equipment') {
                if (TreeSuperParentParam == "Sending Equipment") {
                    localStorage.setItem("CurrentRecordId", eqp);
                    subTabDetails('Equipment Details', 'Detail', 'SAQSSE', eqp)
                }
                else {
                    localStorage.setItem("CurrentRecordId", eqp);
                    subTabDetails('Equipment Details', 'Detail', 'SAQFBL', eqp)
                }

            }
            else if (TableId == 'covered-obj') {
                localStorage.setItem("CurrentRecordId", coveredobjectchild);
                AssemblyIdValue = $(ele).closest('td').next('td').text();
                localStorage.setItem("AssemblyIdValue", AssemblyIdValue);
                setTimeout(function () {
                    subTabDetails('Assembly Details', 'Detail', 'SAQSCA', coveredobjectchild);
                }, 1000);
            }
            else if (TableId == 'table-ContractEquipment') {
                localStorage.setItem("CurrentRecordId", eqp);
                subTabDetails('Equipment Details', 'Detail', 'CTCFBL', '')
            } else if (TableId == 'SYOBJR-00005') {
                localStorage.setItem("CurrentRecordId", KeyId);
                subTabDetails('Spare Part Details', 'Detail', 'SAQSPT', '')
            } else if (TableId == 'SYOBJR-00010') {
                localStorage.setItem("CurrentRecordId", KeyId);
                subTabDetails('Spare Part Details', 'Detail', 'SAQIFP', KeyId)
            } else if (TableId == 'SYOBJR-00009') {
                localStorage.setItem("CurrentRecordId", cov1);
                subTabDetails('Equipment Details', 'Detail', 'SAQICO', cov1)
            } else if (TableId == 'SYOBJR-91822') {
                localStorage.setItem("CurrentRecordId", itm);
                subTabDetails('Equipment Details', 'Detail', 'CTCICO', '')
            } else if (TableId == 'table-covered') {
                localStorage.setItem("CurrentRecordId", cov);
                //$('#div_CTR_Covered_Objects').css('display', 'none');
                $('#div_CTR_related_list').css('display', 'none');
                subTabDetails('Equipment Details', 'Detail', 'SAQSCO', cov);
            } else if (TableId == 'table-ContractCovered') {
                localStorage.setItem("CurrentRecordId", contract_cov);
                subTabDetails('Equipment Details', 'Detail', 'CTCSCO', '');
            } else if (TableId == 'table-assemblies') {
                //localStorage.setItem("CurrentRecordId", cov);
                $('#div_CTR_related_list').css('display', 'none');
                subTabDetails('Equipment Details', 'Detail', 'SAQSCO', '');
            }



            if (TableId == 'table-covered') {
                //tool_breadcrumb();
                //$('div#header_label').append('<li><a onclick="breadCrumb_redirection(this)"><abbr title="Tools">Tools</abbr></a><span class="angle_symbol"><img src="/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>');
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().removeClass('active');
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().removeClass('active');
                //Rec = $('.dropdown-item.cur_sty').attr('id');

                $('#div_CTR_Covered_Objects').css('display', 'none');
                //localStorage.setItem("CurrentRecordId", Rec);
                //INC08634400-M
                var equp_index = $(ele).closest('table').find('[data-field="EQUIPMENT_ID"]').index()+1;
                var equpserial_index = $(ele).closest('table').find('[data-field="SERIAL_NO"]').index()+1;
                ToolEquipment = $(ele).closest('tr').find('td:nth-child('+equp_index+')').text();
                ToolSerial = $(ele).closest('tr').find('td:nth-child('+equpserial_index+')').text();
                //INC08634400-M
                localStorage.setItem('ToolEquipment', ToolEquipment);
                localStorage.setItem('ToolSerial', ToolSerial);
                //commented to check the secondary banner
                //Subbaner(CurrentNodeId, 'QTQSCOT', 'SAQSCO');

            }
            else if (TableId == 'SYOBJR-98788') {
                setTimeout(function () {
                    $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "none");
                    //$('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                }, 2000);

            }
            else if (TableId == 'covered-obj') {
                var EquipmentIdValue = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(6)').text();//A055S000P01-20381
                var Assembly_id_value = $(ele).closest('tr').find('td:nth-child(5)').text();
                localStorage.setItem("EquipmentIdValue", EquipmentIdValue)
                localStorage.setItem("AssemblyIdValue", Assembly_id_value)
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                $('#div_CTR_Covered_Objects').css('display', 'none');
                $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Assembly Details')").parent().addClass('active');
                $('div#COMMON_TABS').find("li a:contains('Assembly Entitlements')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "block");
                ////commented to check the secondary banner
                //Subbaner(CurrentNodeId,coveredobjectchild, 'QTQSCA');
            }
            else if (TableId == 'table-events') {
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Events')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Got Code')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Kit')").parent().css("display", "none");
                $('#ADDNEW__SYOBJR_00011_SYOBJ_00974').css('display', 'none');
                $('div#COMMON_TABS').find("li a:contains('Kit Details')").parent().css("display", "block").addClass('active');
                $('div#COMMON_TABS').find("li a:contains('BoM')").parent().css("display", "block");
                Subbaner('Kit Details', CurrentNodeId, CurrentRecordId, 'SAQSKP');
            }
            else if (TableId == 'SYOBJR-98825') {
                ObjectName = "CTCTIP"
                var display = $(ele).closest('tr').find('td:nth-child(4)').text();
                var res = display.split('-');
                var bread = res[0]
                chainsteps_breadcrumb(bread);
            }

            else if (TableId == 'SYOBJR-98806') {
                ObjectName = "SAQTIP"
                localStorage.setItem("CurrentRecordId", transaction_record_id);
                tool_breadcrumb();
                localStorage.setItem("page_type", "OBJECT PAGE LAYOUT")
                Subbaner('Accounts', CurrentNodeId, transaction_record_id, 'SAQTIP');

            }
            else if (TableId == 'SYOBJR-00643') {
                ObjectName = "SAQDLT"
                localStorage.setItem("CurrentRecordId", transaction_record_id);
                tool_breadcrumb();
                localStorage.setItem("page_type", "OBJECT PAGE LAYOUT")
                Subbaner('', CurrentNodeId, transaction_record_id, 'SAQDLT');
            }
            else if (TableId == 'SYOBJR-98870') {//9646 code starts..ends..
                Subbaner(subTabText, CurrentNodeId, transaction_record_id, "SAQSPT");
            }
            else if (TableId == 'SYOBJR-00024' || TableId == 'SYOBJR-98825') {
                if (TableId == 'SYOBJR-98825') {
                    if (TableId == 'SYOBJR-98825') {
                        ObjectName = "CTCTIP"
                    }
                    breadCrumb_Reset();
                    var role = $(ele).closest('tr').find('td:nth-child(6)').text();
                    $('div#COMMON_TABS').find("li a:contains('Involved Parties')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Opportunity')").parent().css("display", "none");
                    $(".common_quote_information ").hide();
                    $(".involvedparties_Details ").show();
                    $(".involvedparties_Details ").addClass('active');
                    Saletype = localStorage.getItem('saletype')
                    if (role == 'SOURCE ACCOUNT') {
                        $('div#COMMON_TABS').find("li a:contains('Source Fab Location')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
                        if (Saletype == "NEW" || Saletype == "CONTRACT RENEWAL") {
                            $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().css("display", "none");
                        }
                        else {
                            $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().css("display", "block");
                        }
                    }
                    else {
                        $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Source Fab Location')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                        $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().css("display", "none");
                    }


                    if (ObjectName == 'CTCTIP') {
                        Subbaner('Detail', CurrentNodeId, transaction_record_id, 'CTCTIP');
                    }
                    // else{
                    // 	Subbaner('Detail',CurrentNodeId, transaction_record_id, 'SAQTIP');
                    // }
                }
                localStorage.setItem("CurrentRecordId", transaction_record_id);
                subTabText = localStorage.getItem('currentSubTab');
                chainsteps_breadcrumb(subTabText);
                if (ObjectName == 'CTCTIP') {
                    chainsteps_breadcrumb(role);
                }
                tool_breadcrumb();
            }
            else if (TableId == 'SYOBJR-98857' || TableId == 'SYOBJR-98858' || TableId == 'SYOBJR-00028') {
                if (TableId == 'SYOBJR-98857') {
                    Subbaner('Source Fab Location Details', CurrentNodeId, sourcefab, 'SAQSCF');
                }
                else if (TableId == 'SYOBJR-98858') {
                    Subbaner('Equipment details', CurrentNodeId, sourcefab, 'SAQSTE');
                }
                else {
                    Subbaner('Tool Relocation Matrix details', CurrentNodeId, sourcefab, 'SAQSTE');
                }
            }
            else if (TableId == 'table-ContractCovered') {
                tool_breadcrumb();
                //$('div#header_label').append('<li><a onclick="breadCrumb_redirection(this)"><abbr title="Tools">Tools</abbr></a><span class="angle_symbol"><img src="/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>');
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
                $('div#COMMON_TABS').find("li a:contains('Equipment Assemblies')").parent().removeClass('active');
                $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().removeClass('active');


                //Rec = $('.dropdown-item.cur_sty').attr('id');

                //localStorage.setItem("CurrentRecordId", Rec);
                ////commented to check the secondary banner
                //Subbaner(CurrentNodeId, contract_cov, 'CTCSCO');

            }
            else if (TableId == 'table-equipment') {
                if (TreeSuperParentParam == "Sending Equipment") {
                    tool_breadcrumb();
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                    $('#div_CTR_Equipments').css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');

                    localStorage.setItem("CurrentRecordIdEQUIP", eqp);

                    setTimeout(function () {
                        $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                    }, 100);
                    Pmevents_breadcrumb(fab_equipment_serial_number);
                    //commented to check the secondary banner
                    setTimeout(function () {
                        Subbaner("Equipment Details", CurrentNodeId, eqp, 'SAQSSE');
                    }, 3500);
                }
                else {
                    tool_breadcrumb();
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                    $('#div_CTR_Equipments').css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');



                    localStorage.setItem("CurrentRecordIdEQUIP", eqp);

                    setTimeout(function () {
                        $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
                        $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "none");
                    }, 100);
                    if (TreeSuperParentParam != "Fab Locations") {
                        Pmevents_breadcrumb(fab_equipment_serial_number);
                    }
                    //commented to check the secondary banner
                    setTimeout(function () {
                        Subbaner("Equipment Details", CurrentNodeId, eqp, 'SAQFEQ');
                    }, 3500);
                }
            }
            else if (TableId == 'table-ContractEquipment') {
                tool_breadcrumb();
                $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                $('#div_CTR_Equipments').css("display", "none");
                $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');

                localStorage.setItem("CurrentRecordIdEQUIP", eqp);

            }
            else {
                if (TableId == "SYOBJR-00005") {
                    tool_breadcrumb();
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Delivery Schedules')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Forecast Summary')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().addClass('active');
                    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                }
                else if (TableId == "SYOBJR-00009") {
                    localStorage.setItem("RecordId", line)
                    ObjectName = "SAQICO"
                    //tool_breadcrumb();
                    chainsteps_breadcrumb(line);
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                    setTimeout(function () {
                        $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
                    }, 1);


                    //commented to check the secondary banner
                    //Subbaner(CurrentNodeId, 'SAQICOJ', 'SAQICO');
                }
                else if (TableId == "SYOBJR-91822") {
                    tool_breadcrumb();
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Equipment Details')").parent().addClass('active');
                    setTimeout(function () {
                        $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
                    }, 1);


                    ////commented to check the secondary banner
                    //Subbaner(CurrentNodeId, itm, 'CTCICO');
                }
                else if (TableId == "SYOBJR-00010") {
                    tool_breadcrumb();
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "none");
                    $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Spare Part Details')").parent().addClass('active');
                }
                else if (TableId == "SYOBJR-00026") {
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "block");
                    $('div#COMMON_TABS').find("li a:contains('Details')").parent().addClass('active');
                    $('div#COMMON_TABS').find("li a:contains('Tracked Values')").parent().css("display", "none");

                }
            }

        }
        //11642 start
        else if ((CurrentTab == 'CM Class') && (TreeParam == 'Items' || TreeParam == 'CM Classes' || TreeParam == 'Simple Materials' || TreeParam == 'Variant Material' || TreeParam == 'Inherited Materials' || TreeParam == 'Added Related Materials')) {
            x = localStorage.getItem('CurrentNodeId')
            var RecordId = $(ele).closest('tr').find('td:nth-child(3) abbr').attr('id');
            node = $('#commontreeview').treeview('getNode', parseInt(x));
            var childrenNodes = _getChildren(node);
            $(childrenNodes).each(function (ele) {
                y = $('#commontreeview').treeview('getNode', this.nodeId);
                if (y.id == RecordId) {
                    nodeId = y.nodeId
                    x = localStorage.setItem('CurrentNodeId', parseInt(nodeId))
                    $('#commontreeview').treeview('selectNode', [parseInt(nodeId), { silent: true }]);
                    Common_enable_disable();
                }
            });
        }
        //11642 end 
        else if ((CurrentTab == 'Attribute') && (TreeParam == 'Material Attributes' || TreeParam == 'Attribute Languages'
        )) {
            x = localStorage.getItem('CurrentNodeId')
            var RecordId = $(ele).closest('tr').find('td:nth-child(3) abbr').attr('id');
            node = $('#commontreeview').treeview('getNode', parseInt(x));
            var childrenNodes = _getChildren(node);
            $(childrenNodes).each(function (ele) {
                y = $('#commontreeview').treeview('getNode', this.nodeId);
                if (y.id == RecordId) {
                    nodeId = y.nodeId
                    x = localStorage.setItem('CurrentNodeId', parseInt(nodeId))
                    $('#commontreeview').treeview('selectNode', [parseInt(nodeId), { silent: true }]);
                    Common_enable_disable();
                }
            });
        }
        else {
            // -------- A043S001P01-7590 Start --------
            var [TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam] = [localStorage.getItem('CommonTreeParam'), localStorage.getItem('CommonTreeParentParam'), localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam')];
            // -------- A043S001P01-7590 End --------

            if (TableId == 'SYOBJR-92122' && TreeParam != '' && TreeParentParam != '' && TreeSuperParentParam == 'Account Quotas' && currenttab == 'Account') {
                TableId = 'SYOBJR-92128'
            }
            RecordId = RecordId.trim();
            try {
                cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': RecordId, 'TableId': TableId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'NEWVAL': '', 'MODE': 'VIEW', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                    var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                    localStorage.setItem('Lookupobjd', data5)
                    $('#header_label').parent().css('display', 'block');
                    if (document.getElementById("TREE_div")) {
                        document.getElementById("TREE_div").innerHTML = datas;
                        // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                        popover()
                        $(".CommonTreeDetail").addClass("tree_second_child");
                        $('#sub_child_content_banner, #sub_content_banner').css("display", "none");
                        // 9620 start
                        if (currenttab != 'Award Levels' && TreeParam != 'Used in Revision') {       // 9620 end
                            var node = $('#commontreeview').treeview('getNode', data4);
                            var TreeTopSuperParentRecId = TreeTopSuperParentId = TreeTopSuperParentParam = TreeSuperParentRecId = TreeSuperParentId = TreeSuperParentParam = TreeParentNodeRecId = TreeParentNodeId = TreeParentParam = CurrentNodeId = TreeParam = '';
                            CurrentNodeId = node.nodeId
                            var node_text_var = node.text;

                            if (typeof (node_text_var) != 'function' && node_text_var.includes("<span")) {
                                TreeParam = node_text_var.split(">").pop();
                            }
                            else {
                                TreeParam = node_text_var
                            }
                            if (TreeParam.includes("<img")) {
                                TreeParam = TreeParam.split(">")
                                TreeParam = TreeParam[TreeParam.length - 1]
                            } else {
                                TreeParam = TreeParam
                            }
                            if (TreeParam.includes("-")) {

                                if (!TreeParam.includes('- BASE') && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving')) {
                                    TreeParam = TreeParam.split("-")[0].trim()
                                }
                            } else {
                                TreeParam = TreeParam
                            }
                            //A043S001P01-12976 - Start
                            CurrentRecordId = node.id;
                            localStorage.setItem("CurrentRecordId", CurrentRecordId)
                            //A043S001P01-12976 - End
                            localStorage.setItem("CurrentNodeId", CurrentNodeId);
                            if (TableId != "SYOBJR-93178" && TableId != "SYOBJR-93179" && TableId != "SYOBJR-93174" && TableId != "SYOBJR-93177" && TableId != "B47B8FD3-B23F-42BC-81B9-59AEC02BD46D" && TableId != "SYOBJR-94463" && TableId != "SYOBJR-92131" && TableId != "SYOBJR-92135" && TableId != "SYOBJR-95862" && TableId != "SYOBJR-93175" && TableId != "SYOBJR-93176" && TableId != "SYOBJR-93155" && TableId != "SYOBJR-91533" && TableId != "SYOBJR-93171" && TableId != "SYOBJR-93136" && TableId != "SYOBJR-93134") {
                                try {
                                    $('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), { silent: true }]);
                                    if (CurrentNodeId != '' && CurrentNodeId != null) {
                                        TreeParentParam = $('#commontreeview').treeview('getParent', CurrentNodeId).text;
                                        if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("<img")) {
                                            //TreeParentParam = TreeParentParam.split(">")[1];
                                            TreeParentParam = TreeParentParam.split(">")
                                            TreeParentParam = TreeParentParam[TreeParentParam.length - 1];
                                        }
                                        if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("-")) {
                                            if (!TreeParentParam.includes('- BASE')) {
                                                TreeParentParam = TreeParentParam.split("-")[0].trim()
                                            }
                                        }
                                        TreeParentNodeId = $('#commontreeview').treeview('getParent', CurrentNodeId).nodeId;
                                        TreeParentNodeRecId = $('#commontreeview').treeview('getParent', CurrentNodeId).id;
                                    }
                                    if (TreeParentNodeId != '' && TreeParentNodeId != null) {
                                        TreeSuperParentParam = $('#commontreeview').treeview('getParent', TreeParentNodeId).text;
                                        if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("<img")) {
                                            //TreeSuperParentParam = TreeSuperParentParam.split(">")[1];
                                            TreeSuperParentParam = TreeSuperParentParam.split(">")
                                            TreeSuperParentParam = TreeSuperParentParam[TreeSuperParentParam.length - 1];
                                        }
                                        if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("-")) {
                                            if (!TreeSuperParentParam.includes('- BASE')) {
                                                TreeSuperParentParam = TreeSuperParentParam.split("-")[0].trim()
                                            }
                                        }
                                        TreeSuperParentId = $('#commontreeview').treeview('getParent', TreeParentNodeId).nodeId;
                                        TreeSuperParentRecId = $('#commontreeview').treeview('getParent', TreeParentNodeId).id;
                                    }
                                    if (TreeSuperParentId != '' && TreeSuperParentId != null) {
                                        TreeTopSuperParentParam = $('#commontreeview').treeview('getParent', TreeSuperParentId).text;
                                        if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
                                            //	TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")[1];
                                            TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")
                                            TreeTopSuperParentParam = TreeTopSuperParentParam[TreeTopSuperParentParam.length - 1];
                                        }
                                        if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("-")) {
                                            if (!TreeTopSuperParentParam.includes('- BASE')) {
                                                TreeTopSuperParentParam = TreeTopSuperParentParam.split("-")[0].trim()
                                            }
                                        }
                                        TreeTopSuperParentId = $('#commontreeview').treeview('getParent', TreeSuperParentId).nodeId;
                                        TreeTopSuperParentRecId = $('#commontreeview').treeview('getParent', TreeSuperParentId).id;
                                    }
                                    if (TreeSuperParentId === undefined) {
                                        TreeSuperParentParam = ''
                                    }
                                    if (TreeTopSuperParentId === undefined) {
                                        TreeTopSuperParentParam = ''
                                    }
                                    localStorage.setItem('CommonTreeParam', TreeParam);
                                    localStorage.setItem('CommonTreeParentParam', TreeParentParam);
                                    localStorage.setItem('CommonNodeTreeSuperParentParam', TreeSuperParentParam);
                                    localStorage.setItem('CommonTopSuperParentParam', TreeTopSuperParentParam);
                                    localStorage.setItem('CommonParentNodeRecId', TreeParentNodeRecId);
                                    localStorage.setItem('CommonTreeSuperParentRecId', TreeSuperParentRecId);
                                    localStorage.setItem('CommonTopSuperParentRecId', TreeTopSuperParentRecId);
                                    try {
                                        cpq.server.executeScript("SYULODTREE", { 'LOAD': 'GlobalSet', 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam, 'TreeFirstSuperTopParentParam': TreeFirstSuperTopParentParam }, function (dataset) {
                                            // A043S001P01-12265 Start
                                            if (TableId.trim() == 'SYOBJR-95862') {

                                            }
                                            else if (TableId != 'SYOBJR-95802' && TableId != 'SYOBJR-95801' && TableId != "SYOBJR-95860" && TableId != "SYOBJR-95870" && TableId != "SYOBJR-95984" && TableId != "SYOBJR-95983" && TableId != "SYOBJR-95871" && TableId != "SYOBJR-93178" && TableId != "SYOBJR-93134" && TableId != "SYOBJR-95803" && TableId != "SYOBR-95862" && TableId != "SYOBJR-94463" && TableId != "SYOBJR-95872") {


                                                Common_enable_disable();

                                            }
                                            else {
                                                //commented to check the secondary banner
                                                //Subbaner(CurrentNodeId, KeyId, ObjectName);
                                            }
                                            // // A043S001P01-12265 End
                                        });
                                    }
                                    catch (e) {
                                        console.log(e);
                                    }
                                    if (TreeParentParam == "Award Levels" && currenttab == 'Program' && TableId != 'SYOBJR-93178' && TableId != "SYOBJR-93179") {
                                        RecName = 'div_CTR_Award_Groups';
                                        loadRelatedList('SYOBJR-93199', RecName);
                                        $("div[id='" + RecName + "']").closest('.Related').css('display', 'none');
                                        $("div[id='" + RecName + "']").closest('.Related').addClass("tree_second_child");
                                        $("div[id='" + RecName + "']").closest('.Related').removeClass("tree_first_child tree_third_child tree_forth_child");
                                        $("#COMMON_TABS").css("display", "block");
                                        $('.common_Award_Levels_Lvl1_Prog_Tab_Detail').css('display', 'block');
                                    }


                                    if (TreeParentParam == "Account Quotas") {
                                        $("div[id='div_CTR_Account_Quotas']").closest('.Related').css('display', 'block');
                                        $("div[id='div_CTR_Account_Quotas']").closest('.Related').addClass("tree_second_child");
                                        $("div[id='div_CTR_Account_Quotas']").closest('.Related').removeClass("tree_first_child tree_third_child tree_forth_child tree_fifth_child");
                                    }

                                }
                                catch (err) {
                                    console.log(err);
                                }
                            }
                        }
                    }
                });
            }
            catch (e) {
                console.log(e);
            }
        }
    }
    if (table_id.includes('covered_obj_child') && (AllTreeParam['TreeParam'] == 'Product Offerings') || (AllTreeParam['TreeParentLevel0'] == 'Product Offerings') || (AllTreeParam['TreeParentLevel1'] == 'Product Offerings') || (AllTreeParam['TreeParentLevel2'] == 'Product Offerings') || (AllTreeParam['TreeParentLevel3'] == 'Product Offerings')) {
        //INC08634400-M
        var equp_index = $(ele).closest('table').find('[data-field= "ASSEMBLY_ID" ]').index()+1; //A055S000P01-20381
        var Assembly_id_value = $(ele).closest('tr').find('td:nth-child('+equp_index+')').text();
        //INC08634400-M
        localStorage.setItem("AssemblyIdValue", Assembly_id_value)
    }
}

function Commontree_edit_RL(ele) {
    table_id = $(ele).closest('table').attr('id');
    MODE = $(ele).text();
    record_id = table_id.split('_');
    TableId = record_id[0] + '-' + record_id[1];
    localStorage.setItem('TableId_cancel_fun', TableId);
    RecordId = $(ele).closest('tr').find('td:nth-child(3)').text();
    objn = RecordId.split('-')
    ObjectName = objn[0]
    currentSubTab = localStorage.getItem('currentSubTab'); //INC08642678-M
    var KeyId = $(ele).closest('tr').find('td:nth-child(3) a abbr').attr('id');
    $('.CommonTreeDetail').css('display', 'block');
    $('.Detail,.Related').css('display', 'none');
    localStorage.setItem('TreeParamRecordId', RecordId);
    $('#ADDNEW__SYOBJR_95800_SYOBJ_00458').hide();
    var [TreeParam, TreeParentParam, TreeSuperParentParam, TreeTopSuperParentParam] = [localStorage.getItem('CommonTreeParam'), localStorage.getItem('CommonTreeParentParam'), localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam')];
    //A043S001P01-11642 starts
    // commented the if condition beacuse it is not highlighting the current subnode while editing the editing - start
    cmnodeid = ""
    //if ((CurrentTab == 'CM Class') && (TreeParam == 'Items' || TreeParam == 'CM Classes' || TreeParam == 'Simple Materials' || TreeParam == 'Variant Material' || TreeParam == 'Inherited Materials' || TreeParam == 'Added Related Materials')) {
    x = localStorage.getItem('CurrentNodeId')
    var Cm_rec_id = $(ele).closest('tr').find('td:nth-child(3) abbr').attr('id');
    node = $('#commontreeview').treeview('getNode', parseInt(x));
    var childrenNodes = _getChildren(node);
    $(childrenNodes).each(function (ele) {
        y = $('#commontreeview').treeview('getNode', this.nodeId);
        if (y.id == Cm_rec_id) {
            cmnodeid = y.nodeId
            x = localStorage.setItem('CurrentNodeId', parseInt(cmnodeid))
            $('#commontreeview').treeview('selectNode', [parseInt(cmnodeid), { silent: true }]);
        }
    });
    //} //A043S001P01-11642 end // commented the if condition beacuse it is not highlighting the current subnode while editing the editing - start
    if (TreeParam == "Billing Plan") {
        TableId = "SYOBJR-98804";
        ObjName = "QTQIBP";
    }
    try {
        var btn = $('#seginnerbnr > button').attr('id');
        if (btn.includes('ADDNEW_')) {
            $('#' + btn).hide();
        }
    }
    catch (e) {
        console.log(e);
    }
    //INC08642678-M
    try {
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': RecordId, 'TableId': TableId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'NEWVAL': '|', 'MODE': MODE, 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1,'SubtabName':currentSubTab }, function (dataset) {
    //INC08642678-M
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                $(".CommonTreeDetail").addClass("tree_second_child");
                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                popover()
                $("#div_CTR_related_list").hide();
                $('#sub_child_content_banner, #sub_content_banner').css("display", "none");
                var SECTION_EDIT = data3;
                if (String(SECTION_EDIT) != '') {
                    //A055S000P01-3396 commented the below line to reduce the gap between secondary panel and basic information sectional edit
                    //$("." + SECTION_EDIT).css({ "margin-top": "10px", "box-shadow": "1px 0px 8px -1px grey", "padding-bottom": "40px", "padding": "10px", "border-radius": "4px" })
                    //A043S001P01-6728--HIDING SECTION LEVEL BUTTONS IN EDIT MODE WHILE COLLAPSING THE SECTION BANNER--START
                    //JIRA ID A043S001P01-6722 CHANGED THE BUTTON ORDER FROM SAVE AND CANCEL TO CANCEL AND SAVE -CODE START
                    //commented to hide section save and cancel in overall edit from grid
                    //$("." + SECTION_EDIT).append('<div class="g4 sec_' + SECTION_EDIT + ' collapse in except_sec removeHorLine iconhvr sec_edit_sty"><button id="" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="CommontreeCancel(this)">CANCEL</button><button id="" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="CommontreeSAVE(this)">SAVE</button></div>')
                    //JIRA ID A043S001P01-6722 CHANGED THE BUTTON ORDER FROM SAVE AND CANCEL TO CANCEL AND SAVE -CODE END
                    //A043S001P01-6728--HIDING SECTION LEVEL BUTTONS IN EDIT MODE WHILE COLLAPSING THE SECTION BANNER--END
                    //JIRA ID A055S000P01-2811 start show save and cancel in secandary banner on overall edit from grid
                    $('.HideAddNew').remove();
                    if (AllTreeParam['TreeParam'] == "Quote Information") {
                        $("#seginnerbnr").append('<button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="QuoteinformationSave(this)">SAVE</button><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="QuoteinformationCancel(this)">CANCEL</button>')
                    }
                    else if (AllTreeParam['TreeParam'] == "Approval Chain Information") {
                        $("#seginnerbnr").append('<button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="ApprovalinformationSave(this)">SAVE</button><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="ApprovalinformationCancel(this)">CANCEL</button>')
                    }

                    else {
                        $("#seginnerbnr").append('<button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="CommontreeSAVE(this)">SAVE</button><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="CommontreeCancel(this)">CANCEL</button>')
                    }

                    //JIRA ID A055S000P01-2811 end
					
					//JIRA ID A055S000P01-20393 start
                    if(TableId === 'SYOBJR-98881' && currentSubTab === 'Periods' && MODE === 'EDIT'){
                        $('#seginnerbnr #PeriodsInlineEdit').hide()
                    }
                    //JIRA ID A055S000P01-20393 end
                    // 19572 - start
                    if(CommonTreeParam =='Quote Items' && currentSubTab =='Annualized Items' && MODE =='EDIT')
                    { 
                        $("#anual_pick").css('display','none')
                    }
                    else
                    {
                        $("#anual_pick").css('display','block')
                    }
                    // 19572 - end
                       
                
                }
                //A043S001P01-11642 start // commented the if condition beacuse it is not highlighting the current subnode while editing the editing - start
                //if ((CurrentTab == 'CM Class') && (TreeParam == 'Items' || TreeParam == 'CM Classes' || TreeParam == 'Simple Materials' || TreeParam == 'Variant Material' || TreeParam == 'Inherited Materials' || TreeParam == 'Added Related Materials')) {
                var data4 = cmnodeid;
                //} //A043S001P01-11642 end // commented the if condition beacuse it is not highlighting the current subnode while editing the editing - start
                var node = $('#commontreeview').treeview('getNode', data4);
                var CurrentNodeId = TreeParentParam = TreeParentNodeId = TreeParentNodeRecId = TreeSuperParentParam = TreeSuperParentId = TreeSuperParentRecId = TreeTopSuperParentParam = TreeTopSuperParentId = TreeTopSuperParentRecId = TreeParam = '';
                CurrentNodeId = node.nodeId
                var node_text_var = node.text;

                if (typeof (node_text_var) != 'function' && node_text_var.includes("<span")) {
                    TreeParam = node_text_var.split(">").pop();
                }
                else {
                    TreeParam = node_text_var
                }
                if (typeof TreeParam === 'string') {
                    if (TreeParam.includes("<img")) {
                        TreeParam = TreeParam.split(">")
                        TreeParam = TreeParam[TreeParam.length - 1]
                    } else {
                        TreeParam = TreeParam
                    }
                    if (TreeParam.includes("-")) {

                        if (!TreeParam.includes('- BASE') && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving')) {
                            TreeParam = TreeParam.split("-")[0].trim()
                        }
                    } else {
                        TreeParam = TreeParam
                    }
                }
                var childrenNodes = _getChildren(node);
                if (childrenNodes.length > 0) {
                    child = 'true';
                } else {
                    child = 'false';
                }
                localStorage.setItem('Mtrlchildavailable', child);
                localStorage.setItem("CurrentNodeId", CurrentNodeId);
                try {
                    $('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), { silent: true }]);
                    if (CurrentNodeId != '' && CurrentNodeId != null) {
                        TreeParentParam = $('#commontreeview').treeview('getParent', CurrentNodeId).text;
                        if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("<img")) {
                            //TreeParentParam = TreeParentParam.split(">")[1];
                            TreeParentParam = TreeParentParam.split(">")
                            TreeParentParam = TreeParentParam[TreeParentParam.length - 1]
                        }
                        if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("-")) {
                            if (!TreeParentParam.includes('- BASE')) {
                                TreeParentParam = TreeParentParam.split("-")[0].trim()
                            }
                        }
                        TreeParentNodeId = $('#commontreeview').treeview('getParent', CurrentNodeId).nodeId;
                        TreeParentNodeRecId = $('#commontreeview').treeview('getParent', CurrentNodeId).id;
                    }
                    if (TreeParentNodeId != '' && TreeParentNodeId != null) {
                        TreeSuperParentParam = $('#commontreeview').treeview('getParent', TreeParentNodeId).text;
                        if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("<img")) {
                            //TreeSuperParentParam = TreeSuperParentParam.split(">")[1];
                            TreeSuperParentParam = TreeSuperParentParam.split(">")
                            TreeSuperParentParam = TreeSuperParentParam[TreeSuperParentParam.length - 1]
                        }
                        if (TreeSuperParentParam != '' && TreeTreeSuperParentParamParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("-")) {
                            if (!TreeSuperParentParam.includes('- BASE')) {
                                TreeSuperParentParam = TreeSuperParentParam.split("-")[0].trim()
                            }
                        }
                        TreeSuperParentId = $('#commontreeview').treeview('getParent', TreeParentNodeId).nodeId;
                        TreeSuperParentRecId = $('#commontreeview').treeview('getParent', TreeParentNodeId).id;
                    }
                    if (TreeSuperParentId != '' && TreeSuperParentId != null) {
                        TreeTopSuperParentParam = $('#commontreeview').treeview('getParent', TreeSuperParentId).text;
                        if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
                            //TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")[1];
                            TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")
                            TreeTopSuperParentParam = TreeTopSuperParentParam[TreeTopSuperParentParam.length - 1];
                        }
                        if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("-")) {
                            if (!TreeTopSuperParentParam.includes('- BASE')) {
                                TreeTopSuperParentParam = TreeTopSuperParentParam.split("-")[0].trim()
                            }
                        }
                        TreeTopSuperParentId = $('#commontreeview').treeview('getParent', TreeSuperParentId).nodeId;
                        TreeTopSuperParentRecId = $('#commontreeview').treeview('getParent', TreeSuperParentId).id;
                    }
                    if (TreeSuperParentId === undefined) {
                        TreeSuperParentParam = ''
                    }
                    if (TreeTopSuperParentId === undefined) {
                        TreeTopSuperParentParam = ''
                    }
                    //if (document.getElementById("header_label")) {
                    //document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
                    //document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
                    //document.getElementById('content_banner').style = 'display:block;margin-top: 10px;'
                    //}
                    localStorage.setItem('CommonTreeParam', TreeParam);
                    localStorage.setItem('CommonTreeParentParam', TreeParentParam);
                    localStorage.setItem('CommonNodeTreeSuperParentParam', TreeSuperParentParam);
                    localStorage.setItem('CommonTopSuperParentParam', TreeTopSuperParentParam);
                    localStorage.setItem('CommonParentNodeRecId', TreeParentNodeRecId);
                    localStorage.setItem('CommonTreeSuperParentRecId', TreeSuperParentRecId);
                    localStorage.setItem('CommonTopSuperParentRecId', TreeTopSuperParentRecId);
                    CurrentNodeId = localStorage.getItem('CurrentNodeId');
                    //A055S000P01-3392 - start breadcrumb in relatedlist edit mode
                    localStorage.setItem('key_id', MODE);//for subanner in edit mode
                    dict['TreeParam'] = $('#commontreeview').treeview('getNode', CurrentNodeId).text;
                    if (TreeParam != '' && TreeParam != undefined && (typeof TreeParam === 'string' || TreeParam instanceof String) && TreeParam.includes("<img")) {
                        //TreeParam = TreeParam.split(">")[1];
                        TreeParam = TreeParam.split(">")
                        TreeParam = TreeParam[TreeParam.length - 1];
                    }
                    if (TreeParam.includes("-")) {

                        if (!TreeParam.includes('- BASE') && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving')) {
                            TreeParam = TreeParam.split("-")[0].trim()
                        }
                    }
                    AllTreeParam = maintreeparamfunction(parseInt(CurrentNodeId), 0);
                    AllTreeParams = JSON.stringify(AllTreeParam);
                    //A055S000P01-3392 - end breadcrumb in relatedlist edit mode
                    //11285 start
                    if (CurrentNodeId != 0) {
                        //commented to check the secondary banner
                        Subbaner('', CurrentNodeId, KeyId, ObjectName);
                        $("#seginnerbnr").append('<button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="CommontreeSAVE(this)">SAVE</button><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="CommontreeCancel(this)">CANCEL</button>')
                    }//11285 end
                    onFieldChanges();
                    //A055S000P01-3392 - start breadcrumb in relatedlist edit mode
                    breadCrumb_Reset();
                    //A055S000P01-3392 - end breadcrumb in relatedlist edit mode
                }
                catch (err) {
                    console.log(err);
                }
            }
        });
    }
    catch (e) {
        console.log(e);
    }
}

function CommonEDIT(ele) {
    // To remove cloapse while sectional edit - Start
    $(ele).closest('#ctr_drop').closest('.dyn_main_head').removeAttr('data-toggle');
    $(ele).closest('#ctr_drop').closest('.dyn_main_head').removeAttr('data-target');
    // To remove cloapse while sectional edit - End

    var [SECTION_EDIT, RecordId, TreeParam, TableId, MODE, Rel_list_Id] = [$(ele).attr('id'), $("#TREE_div table tbody tr td input").val(), '', localStorage.getItem('CommonParentNodeRecId'), $(ele).text(), localStorage.getItem('Rel_List_Rec_ID')];
    localStorage.setItem('SECTION_LEVEL_EDIT_ID', SECTION_EDIT);
    var [TreeParam, TreeParentParam, TreeSuperParentParam, TopSuperParentParam, TreeTopSuperParentParam] = [AllTreeParam['TreeParam'], AllTreeParam['TreeParentLevel0'], localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam')];

    if (localStorage.getItem('currentSubTab') == "Equipment Details") {
        RecordId = $('#QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID').val();
    }
    obj = RecordId.split('-')

    ObjName = obj[0]
    // A043S001P01-7285 START

    if (TableId != '') {
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    var can_fun_tabId = localStorage.getItem('TableId_cancel_fun');

    if (can_fun_tabId) {
        TableId = can_fun_tabId;
    }
    if (TableId == '' || TableId == 'undefined' || TableId == null || TableId == undefined) {
        TableId = Rel_list_Id
        localStorage.setItem('TableId_cancel_fun', TableId);
    }

    if (TreeFirstSuperTopParentParam == 'Program Participant Quotas' && currenttab == 'Participant') {
        TableId = 'SYOBJR-90033'
        localStorage.setItem('TableId_cancel_fun', TableId);
    }// A043S001P01-8665 Start
    else if (TreeParentParam == "Sub Categories" || TreeSuperParentParam == "Sub Categories" || TopSuperParentParam == "Sub Categories" || TreeTopSuperParentParam == "Sub Categories") {
        TableId = 'SYOBJR-30009'
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    // A043S001P01-8665 End
    // A043S001P01-7285 END
    else if (TreeParentParam == "Tabs" && currenttab == "Page") {
        TableId = 'SYOBJR-95982'
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    else if (TreeParentParam == "Assigned Members" && currenttab == "Profile") {
        TableId = 'SYOBJR-95800'
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    else if (TreeParentParam == "Trees" && currenttab == "Page") {
        TableId = 'SYOBJR-95981'
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    else if (TreeParentParam == "Sections" && currenttab == "Page") {
        TableId = 'SYOBJR-95980'
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    else if (TreeSuperParentParam == "Constraints" && currenttab == "Object") {
        TableId = 'SYOBJR-95825'
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    try {
        SECTION_TEXT = $("div#container." + SECTION_EDIT).find('label').children().text()

        if (SECTION_TEXT == "EDITPROGRAM PARTICIPANT SPLIT INFORMATION") {
            spli_bind = 0
            var strdate = document.getElementById('ACCPRGLVL_QUOTA_BEGDTE').value;
            var ENDDATE = document.getElementById('ACCPRGLVL_QUOTA_ENDDTE').value;
            $('#VIEW_POP_DIV_ID').removeAttr('onclick')
            cpq.server.executeScript("SYPOPPORGM", { 'startdate': strdate, 'ENDDATE': ENDDATE }, function (datas) {
                var [data, data1, data2, data3, data4, data5] = [datas[0], datas[1], datas[2], datas[3], datas[4], datas[5]];
                localStorage.setItem('splitList', data2)
                localStorage.setItem('splitListid', data3)
                if (data == 'true') {
                    $('#cont_viewPupupModal').hide();
                }
                else {
                    $('#cont_viewPupupModal').show();
                    if (document.getElementById('VIEW_POP_DIV_ID')) {
                        document.getElementById('VIEW_POP_DIV_ID').innerHTML = data1;
                    }
                    try {
                        $('table#coppart_popup_model').after(data4);
                        setTimeout(function () {
                            start_val = 0
                            table_row_cnt = $('table#coppart_popup_model tbody').find('tr').length
                            $('#coppart_popup_model_totalItemCount').text(table_row_cnt)
                            var all_tr = document.querySelectorAll("table#coppart_popup_model_ass tbody.coppart_body tr");
                            counter_value = $('#coppart_popup_model_PageCountValue').val()
                            if (table_row_cnt < counter_value) {
                                $("span#coppart_popup_model_NumberofItem").html("1 - " + table_row_cnt + " of")
                            } else {
                                $("span#coppart_popup_model_NumberofItem").html("1 - " + counter_value + " of")
                            }
                            if (table_row_cnt > counter_value) {
                                for (i = start_val; i < counter_value; i++) {
                                    all_tr[i].removeAttribute("style");
                                }
                            }
                            else {
                                for (i = start_val; i < table_row_cnt; i++) {
                                    try {
                                        all_tr[i].removeAttribute("style");
                                    } catch (e) {

                                    }
                                }
                            }


                            $("input.form-control.splitclass").each(function () {
                                spli_bind += parseInt($(this).val())
                            });

                            if ((spli_bind) && (spli_bind < 100) && (!(spli_bind >= 100)) && (spli_bind != 0) && (spli_bind != '')) {
                                $('#coppart_Add').removeAttr('disabled');
                                $('.fa-check-circle-o').css('display', 'none');
                                $('.fa-exclamation-triangle').css({ "display": "inline-block", "color": "red" });

                            } else if ((spli_bind == 0) || (spli_bind = 100)) {
                                $('#coppart_Add').attr('disabled', 'true');
                                $('.fa-check-circle-o').css('display', 'inline-block');
                                $('.fa-exclamation-triangle').css('display', 'none');
                                $('#coppaq_save').removeAttr('disabled');
                            }

                        }, 500);

                        MAX = localStorage.getItem('MAXIMISED')
                        if (MAX) {
                            $('#restore_back').css('cssText', 'display : none !important');
                            $('#restore').css('cssText', 'display : block !important');
                            $('#restore').parent().parent().parent().parent().parent().parent().css('cssText', 'margin-top:5% !important;width:99% !important');
                            $('#restore').parent().parent().parent().parent().parent().css('cssText', 'height:130% !important');
                            $('table#coppart_popup_model tbody').css('cssText', 'max-height:50vh !important')
                        }


                    } catch (err) {
                        console.log(err);
                    }
                    if (data5 == 'NO RECORDS') {
                        document.getElementById('prg_0').innerHTML = '<div class="col-md-12 noRecord">No Records to Display</div>'
                    }

                }
            });
        }
        else {
            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': RecordId, 'TableId': TableId, 'TreeParam': TreeParam, 'ObjName': ObjName, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'NEWVAL': '', 'MODE': MODE, 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': SECTION_EDIT }, function (dataset) {
                var [datas, date_field, data2, data3, data4, data5, data6] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[10]];
                var node = '';
                localStorage.setItem('Lookupobjd', data5);
                CurrentNodeId = localStorage.getItem("CurrentNodeId");

                node = $('#commontreeview').treeview('getNode', data4);

                var data = data1 = TreeParam = CurrentTab = CurrentRecordId = CurrentNodeId = TreeParentParam = TreeParentNodeId = TreeParentNodeRecId = TreeSuperParentParam = TreeSuperParentId = TreeSuperParentRecId = TreeTopSuperParentParam = TreeTopSuperParentId = TreeTopSuperParentRecId = TreeSuperTopParentParam = TreeSuperTopParentRecId = TreeSuperTopParentId = TreeFirstSuperTopParentParam = TreeFirstSuperTopParentId = TreeFirstSuperTopParentRecId = '';

                CurrentNodeId = node.nodeId
                CurrentRecordId = node.id;
                //CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
                CurrentTab = $("ul#carttabs_head li.active a span").text();
                var node_text_var = node.text;

                if (typeof (node_text_var) != 'function' && node_text_var.includes("<span")) {
                    TreeParam = node_text_var.split(">").pop();
                }
                else {
                    TreeParam = node_text_var
                }
                if (typeof TreeParam === 'string') {
                    if (TreeParam.includes("<img")) {
                        TreeParam = TreeParam.split(">")
                        TreeParam = TreeParam[TreeParam.length - 1];
                    } else {
                        TreeParam = TreeParam
                    }
                    if (TreeParam.includes("-")) {

                        if (!TreeParam.includes('- BASE') && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving')) {
                            TreeParam = TreeParam.split("-")[0].trim()
                        }
                    } else {
                        TreeParam = TreeParam
                    }
                }
                localStorage.setItem("CurrentNodeId", CurrentNodeId);
                data1 = localStorage.getItem('CommonTreedatasetnew');
                data = data1.split(',');

                if (CurrentNodeId != '' && CurrentNodeId != null) {
                    TreeParentParam = $('#commontreeview').treeview('getParent', CurrentNodeId).text;
                    if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("<img")) {
                        //TreeParentParam = TreeParentParam.split(">")[1];
                        TreeParentParam = TreeParentParam.split(">")
                        TreeParentParam = TreeParentParam[TreeParentParam.length - 1];
                    }
                    if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("-")) {
                        if (!TreeParentParam.includes('- BASE')) {
                            TreeParentParam = TreeParentParam.split("-")[0].trim()
                        }
                    }
                    TreeParentNodeId = $('#commontreeview').treeview('getParent', CurrentNodeId).nodeId;
                    TreeParentNodeRecId = $('#commontreeview').treeview('getParent', CurrentNodeId).id;
                }
                if (TreeParentNodeId != '' && TreeParentNodeId != null) {
                    TreeSuperParentParam = $('#commontreeview').treeview('getParent', TreeParentNodeId).text;
                    if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("<img")) {
                        //TreeSuperParentParam = TreeSuperParentParam.split(">")[1];
                        TreeSuperParentParam = TreeSuperParentParam.split(">")
                        TreeSuperParentParam = TreeSuperParentParam[TreeSuperParentParam.length - 1];
                    }
                    if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("-")) {
                        if (!TreeSuperParentParam.includes('- BASE')) {
                            TreeSuperParentParam = TreeSuperParentParam.split("-")[0].trim()
                        }
                    }
                    TreeSuperParentId = $('#commontreeview').treeview('getParent', TreeParentNodeId).nodeId;
                    TreeSuperParentRecId = $('#commontreeview').treeview('getParent', TreeParentNodeId).id;
                }
                if (TreeSuperParentId != '' && TreeSuperParentId != null) {
                    TreeTopSuperParentParam = $('#commontreeview').treeview('getParent', TreeSuperParentId).text;
                    if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
                        //	TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")[1];
                        TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")
                        TreeTopSuperParentParam = TreeTopSuperParentParam[TreeTopSuperParentParam.length - 1];
                    }
                    if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("-")) {
                        if (!TreeTopSuperParentParam.includes('- BASE')) {
                            TreeTopSuperParentParam = TreeTopSuperParentParam.split("-")[0].trim()
                        }
                    }
                    TreeTopSuperParentId = $('#commontreeview').treeview('getParent', TreeSuperParentId).nodeId;
                    TreeTopSuperParentRecId = $('#commontreeview').treeview('getParent', TreeSuperParentId).id;
                }
                if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null) {
                    TreeSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).text;
                    if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeSuperTopParentParam.includes("<img")) {
                        //TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")[1];
                        TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")
                        TreeSuperTopParentParam = TreeSuperTopParentParam[TreeSuperTopParentParam.length - 1];
                    }
                    if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeSuperTopParentParam.includes("-")) {
                        if (!TreeSuperTopParentParam.includes('- BASE')) {
                            TreeSuperTopParentParam = TreeSuperTopParentParam.split("-")[0].trim()
                        }
                    }
                    TreeSuperTopParentId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
                    TreeSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).id;
                }
                if (TreeSuperTopParentId != '' && TreeSuperTopParentId != null) {
                    TreeFirstSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).text;
                    if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeFirstSuperTopParentParam.includes("<img")) {
                        //	TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")[1];

                        TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")
                        TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam[TreeFirstSuperTopParentParam.length - 1];
                    }
                    if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeSuperTopParentParam.includes("-")) {
                        if (!TreeFirstSuperTopParentParam.includes('- BASE')) {
                            TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split("-")[0].trim()
                        }
                    }
                    TreeFirstSuperTopParentId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).nodeId;
                    TreeFirstSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).id;
                }
                if (TreeSuperParentId === undefined) {
                    TreeSuperParentParam = ''
                }
                if (TreeTopSuperParentId === undefined) {
                    TreeTopSuperParentParam = ''
                }
                if (TreeSuperTopParentRecId === undefined) {
                    TreeSuperTopParentParam = ''
                }
                if (TreeFirstSuperTopParentRecId === undefined) {
                    TreeFirstSuperTopParentParam = ''
                }
                var childrenNodes = _getChildren(node);
                if (childrenNodes.length > 0) {
                    child = 'true';
                } else {
                    child = 'false';
                }

                localStorage.setItem('CommonTreeParam', TreeParam);
                localStorage.setItem('CommonTreeParentParam', TreeParentParam);
                localStorage.setItem('CommonNodeTreeSuperParentParam', TreeSuperParentParam);
                localStorage.setItem('CommonTopSuperParentParam', TreeTopSuperParentParam);
                localStorage.setItem('CommonTreeSuperTopParentParam', TreeSuperTopParentParam); //Accounts Tab 
                localStorage.setItem('CommonTreeFirstSuperTopParentParam', TreeFirstSuperTopParentParam); //Accounts Tab


                localStorage.setItem('CommonParentNodeRecId', TreeParentNodeRecId);
                localStorage.setItem('CommonTreeSuperParentRecId', TreeSuperParentRecId);
                localStorage.setItem('CommonTopSuperParentRecId', TreeTopSuperParentRecId);
                if ((((CurrentTab == 'Business Unit' || CurrentTab == 'Sales Area' || CurrentTab == 'Sales Territory' || CurrentTab == 'Region' || CurrentTab == 'Account' || CurrentTab == 'Sales Org') && ProductId == '777')) || ((CurrentTab == 'Quota Category' || CurrentTab == 'Quota Subcategory' || CurrentTab == 'Business Unit' || CurrentTab == 'Sales Area' || CurrentTab == 'Sales Territory' || CurrentTab == 'Account' || CurrentTab == 'Participant') && ProductId == '614') || (ProductId == '776' && (CurrentTab != 'Profile' && CurrentTab != 'App') || CurrentTab == 'Material')) {
                    localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
                    localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
                    localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
                    localStorage.setItem('CommonTopSuperParentParam', AllTreeParam['TreeParentLevel2']);
                    localStorage.setItem('CommonTreeSuperTopParentParam', AllTreeParam['TreeParentLevel3']); //Accounts Tab 
                    localStorage.setItem('CommonTreeFirstSuperTopParentParam', AllTreeParam['TreeParentLevel4']);
                }

                if ((jQuery.inArray(TreeParentParam, data) !== -1) && TreeParam != '') {
                    //if (document.getElementById("header_label")) {
                    //document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
                    //document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
                    //document.getElementById('content_banner').style = 'display:block;margin-top: 10px;'
                    //}
                }

                else if (((jQuery.inArray(TreeSuperParentParam, data) !== -1) && (jQuery.inArray(TreeParentParam, data) !== -1) && TreeParam != '')) {
                    if (document.getElementById("header_label")) {
                        //document.getElementById("header_label").innerHTML = TreeSuperParentParam.toUpperCase();
                        //document.getElementById("banner_label").innerHTML = TreeParentParam.toUpperCase();
                        //document.getElementById("sub_banner_label").innerHTML = TreeParam.toUpperCase();
                        //$('#content_banner, #sub_content_banner').css('cssText','display:block;margin-top: 10px;');
                    }
                }
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    //$(".CommonTreeDetail").addClass("tree_second_child");
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                }
                $("." + SECTION_EDIT).addClass("SEC_EDIT_ARROW")
                $("." + SECTION_EDIT).css({ "margin-top": "10px", "box-shadow": "1px 0px 8px -1px grey", "padding-bottom": "40px", "padding": "10px", "border-radius": "4px" })
                //A043S001P01-6728--HIDING SECTION LEVEL BUTTONS IN EDIT MODE WHILE COLLAPSING THE SECTION BANNER--START
                //JIRA ID A043S001P01-6722 CHANGED THE BUTTON ORDER FROM SAVE AND CANCEL TO CANCEL AND SAVE -CODE START
                //$("." + SECTION_EDIT).append('<div  class="g4 sec_' + SECTION_EDIT + ' collapse in except_sec removeHorLine iconhvr sec_edit_sty"><button id="" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="CommontreeCancel(this)">CANCEL</button><button id="" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="CommontreeSAVE(this)">SAVE</button></div>');



                $("." + SECTION_EDIT).append(data6);

                //JIRA ID A043S001P01-6722 CHANGED THE BUTTON ORDER FROM SAVE AND CANCEL TO CANCEL AND SAVE -CODE END
                //A043S001P01-6728--HIDING SECTION LEVEL BUTTONS IN EDIT MODE WHILE COLLAPSING THE SECTION BANNER--END
                //onFieldChanges()
                // Added to hide the FPM INFORMATION section in QTQITM details page based on quote type -  start
                if (CurrentTab == 'Quotes') {
                    //var getopptype = $( "#QSTN_SYSEFL_QT_00723 option:selected" ).text();
                    var getopptype = localStorage.getItem("getopptype");
                }
                else if (CurrentTab == "Contracts") {
                    var getopptype = $("#QSTN_SYSEFL_QT_016912 option:selected").text();
                }
                if (getopptype == "ZTBC - TOOL BASED") {
                    $('.CC119201-572D-41BB-8C53-5C063EEAAD4F').css('display', 'none');
                    //$(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display','none');
                }
                else {
                    $('.CC119201-572D-41BB-8C53-5C063EEAAD4F').css('display', 'block');
                }
                // Added to hide the FPM INFORMATION section in QTQITM details page based on quote type -  end
            });
        }
    }
    catch (e) {
        console.log(e);
    }
}
function onchangeFunction(ele) {
    //console.log('wwwwww')
    val = $("#IDLING_PERM").val();
    pre_val = $("#HOT_IDLE_NOTICE").val();
    id_val = $("#COLD_IDLE_NOTICE").val();
    hot_val = $("#HOT_IDLE").val();
    hotfee_val = $("#HOT_IDLE_FEE").val();
    cold_val = $("#COLD_IDLE").val();
    coldfee_val = $("#COLD_IDLE_FEE").val();
    if (cold_val) {
        if (cold_val == "NO") {
            $('#COLD_IDLE_EXCP').closest('tr').hide();
            $('#COLD_IDLE_FEE').closest('tr').hide();
            $('#COLD_IDLE_FEE_EXCP').closest('tr').hide();
            $('#COLD_IDLE').closest('tr').show();
        }
        else {
            $('#COLD_IDLE_EXCP').closest('tr').hide();
            $('#COLD_IDLE_FEE').closest('tr').show();
            $('#COLD_IDLE_FEE_EXCP').closest('tr').hide();
            $('#COLD_IDLE').closest('tr').show();
            if (coldfee_val == "MANUAL INPUT") {
                $('#COLD_IDLE_FEE_EXCP').closest('tr').show();
                $('#COLD_IDLE_FEE').closest('tr').show();
                $('#COLD_IDLE_EXCP').closest('tr').show();
                $('#COLD_IDLE').closest('tr').show();
            }
            else if (coldfee_val != "MANUAL INPUT") {
                $('#COLD_IDLE_FEE_EXCP').closest('tr').hide();
                $('#COLD_IDLE_FEE').closest('tr').show();
                $('#COLD_IDLE_EXCP').closest('tr').hide();
                $('#COLD_IDLE').closest('tr').show();
            }
        }
    }
    else if (hot_val) {
        if (hot_val == "NO") {
            $('#HOT_IDLE_FEE_EXCP').closest('tr').hide();
            $('#HOT_IDLE_FEE').closest('tr').hide();
            $('#HOT_IDLE_EXCP').closest('tr').hide();
            $('#HOT_IDLE').closest('tr').show();
        }
        else {
            $('#HOT_IDLE_FEE_EXCP').closest('tr').hide();
            $('#HOT_IDLE_FEE').closest('tr').show();
            $('#HOT_IDLE_EXCP').closest('tr').hide();
            $('#HOT_IDLE').closest('tr').show();
            if (hotfee_val == "EXCEPTION") {
                $('#HOT_IDLE_FEE_EXCP').closest('tr').show();
                $('#HOT_IDLE_FEE').closest('tr').show();
                $('#HOT_IDLE_EXCP').closest('tr').show();
                $('#HOT_IDLE').closest('tr').show();
            }
            else if (hotfee_val != "EXCEPTION") {
                $('#HOT_IDLE_FEE_EXCP').closest('tr').hide();
                $('#HOT_IDLE_FEE').closest('tr').show();
                $('#HOT_IDLE_EXCP').closest('tr').hide();
                $('#HOT_IDLE').closest('tr').show();
            }
        }
    }

    else if (val) {
        if (val == "PERCENTAGE OF TOOLS") {
            $('#HOT_IDLE_NOTICE').closest('tr').show();
            $('#HOT_IDLE_NOTICE_EXCP').closest('tr').show();
            $('#COLD_IDLE_NOTICE').closest('tr').show();
            $('#COLD_IDLE_NOTICE_EXCP').closest('tr').show();
            $('#IDLING_NOTES').closest('tr').show();
            $('#IDLING_PERM').closest('tr').show();
            $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
            $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            if (id_val == "EXCEPTION" && pre_val == "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
            else if (id_val != "EXCEPTION" && pre_val != "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
            else if (id_val != "EXCEPTION" && pre_val == "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
            else if (id_val == "EXCEPTION" && pre_val != "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
        }
        else if (val == "PERCENTAGE OF FIXED BILLING") {
            $('#IDLING_PERM').closest('tr').show();
            $('#HOT_IDLE_NOTICE').closest('tr').show();
            $('#HOT_IDLE_NOTICE_EXCP').closest('tr').show();
            $('#COLD_IDLE_NOTICE').closest('tr').show();
            $('#COLD_IDLE_NOTICE_EXCP').closest('tr').show();
            $('#IDLING_NOTES').closest('tr').show();
            $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
            $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            if (id_val == "EXCEPTION" && pre_val == "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
            else if (id_val != "EXCEPTION" && pre_val != "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
            else if (id_val != "EXCEPTION" && pre_val == "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
            else if (id_val == "EXCEPTION" && pre_val != "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
        }
        else if (val == "NOT PERMITTED") {
            $('#IDLING_PERM').closest('tr').show();
            $('#HOT_IDLE_NOTICE').closest('tr').hide();
            $('#HOT_IDLE_NOTICE_EXCP').closest('tr').hide();
            $('#COLD_IDLE_NOTICE').closest('tr').hide();
            $('#COLD_IDLE_NOTICE_EXCP').closest('tr').hide();
            $('#IDLING_NOTES').closest('tr').hide();
            $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'none')
            $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'none')
        }
        //else if(val.includes("Select")){
        else {
            $('#IDLING_PERM').closest('tr').show();
            $('#HOT_IDLE_NOTICE').closest('tr').show();
            $('#HOT_IDLE_NOTICE_EXCP').closest('tr').hide();
            $('#COLD_IDLE_NOTICE').closest('tr').show();
            $('#COLD_IDLE_NOTICE_EXCP').closest('tr').hide();
            $('#IDLING_NOTES').closest('tr').show();
            $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
            $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            if (id_val == "EXCEPTION" && pre_val == "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
            else if (id_val != "EXCEPTION" && pre_val != "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
            else if (id_val != "EXCEPTION" && pre_val == "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
            else if (id_val == "EXCEPTION" && pre_val != "EXCEPTION") {
                $('#HOT_IDLE_NOTICE_EXCP').closest('tr').hide();
                $('#HOT_IDLE_NOTICE').closest('tr').show();
                $('#IDLING_PERM').closest('tr').show();
                $('#COLD_IDLE_NOTICE').closest('tr').show();
                $('#COLD_IDLE_NOTICE_EXCP').closest('tr').show();
                $('#IDLING_NOTES').closest('tr').show();
                $(".13AECCC6-B6B4-4F89-BC06-D72EDB907BF2").css('display', 'block')
                $(".FE223959-D338-454D-B9D6-57992F50ACF1").css('display', 'block')
            }
        }
    }

}

function customer_value_EDIT(ele) {
    var fablocatedict = [];
    $('.fabvaldrives-toggle').removeAttr('data-toggle');
    $('#ctr_drop').css('display', 'none');
    $('#fabvaldrives').find(':input(:disabled)').prop('disabled', false);
    $('#fabvaldrives tbody  tr td select option').css('background-color', 'lightYellow');
    $('#fabnotify').addClass('header_section_div  header_section_div_pad_bt10');
    $('#fabvaldrives  tbody tr td select').addClass('light_yellow'); $('.disabled_edit_drivers ').prop('disabled', true).removeClass('light_yellow');
    $('select').on('change', function () {
        var valuedrivchage = this.value;
        var valuedesc = $(this).closest('tr').find('td:nth-child(1)').text();
        var concate_data = valuedesc + '-' + valuedrivchage;
        if (!fablocatedict.includes(concate_data)) { fablocatedict.push(concate_data) };
        getfablocatedict = JSON.stringify(fablocatedict);
        localStorage.setItem('getfablocatedict', getfablocatedict);
    });
    $(".fabvaldrives .bootstrap-table").append('<div class="g4 sec_fabvaldrives collapse in except_sec removeHorLine iconhvr sec_edit_sty"><button id="fablocate_cancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="fablocatecancel(this)">CANCEL</button><button id="fablocate_save" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="fablocatesave(this)">SAVE</button></div>');
}

function product_value_EDIT(ele) {
    if (AllTreeParam['TreeParentLevel1'] == "Product Offerings") {
        table_id = "servicecostvaldrives"
    }
    else if (AllTreeParam['TreeParentLevel2'] == "Product Offerings") {
        table_id = "csservicecostfabvaldrives"
    }
    else if (AllTreeParam['TreeParentLevel3'] == "Product Offerings") {
        table_id = "csserviceGreencostvaldrives"
    }
    var fablocatedict = [];
    $('.fabvaldrives-toggle').removeAttr('data-toggle');
    $('#ctr_drop').css('display', 'none');
    $('#servicecostvaldrives').find(':input(:disabled)').prop('disabled', false);
    $('#servicecostvaldrives tbody  tr td select option').css('background-color', 'lightYellow');
    $('#fabnotify').addClass('header_section_div header_section_div_pad_bt10 padtop10');
    $('#' + table_id + '  tbody tr td select').addClass('light_yellow');
    $('.disabled_edit_drivers ').prop('disabled', true).removeClass('light_yellow');
    // $('#fabcostlocate_save').css('display','block');
    // $('#fabcostlocate_cancel').css('display','block');
    $('select').on('change', function () {
        var valuedrivchage = this.value;
        var valuedesc = $(this).closest('tr').find('td:nth-child(1)').text();
        var concate_data = valuedesc + '=' + valuedrivchage;
        if (!fablocatedict.includes(concate_data)) {
            fablocatedict.push(concate_data)
        };
        getfablocatedict = JSON.stringify(fablocatedict);
        localStorage.setItem('getfablocatedict', getfablocatedict);
    });
    $(".fabvaldrives .bootstrap-table").append('<div class="g4 sec_fabvaldrives collapse in except_sec removeHorLine iconhvr sec_edit_sty"><button id="fabcostlocate_cancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="fabcostlocatecancel(this)">CANCEL</button><button id="fabcostlocate_save" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="fabcostlocatesave(this)">SAVE</button></div>');
}

function QuoteinformationEDIT(ele) {
    // To remove cloapse while sectional edit - Start
    $(ele).closest('#ctr_drop').closest('.dyn_main_head').removeAttr('data-toggle');
    $(ele).closest('#ctr_drop').closest('.dyn_main_head').removeAttr('data-target');
    // To remove cloapse while sectional edit - End
    localStorage.setItem('AddNew', 'false')
    var [SECTION_EDIT, RecordId, TreeParam, TableId, MODE, Rel_list_Id] = [$(ele).attr('id'), $("#key_field_id").val(), '', localStorage.getItem('CommonParentNodeRecId'), $(ele).text(), localStorage.getItem('Rel_List_Rec_ID')];
    localStorage.setItem('SECTION_LEVEL_EDIT_ID', SECTION_EDIT);
    var [TreeParam, TreeParentParam, TreeSuperParentParam, TopSuperParentParam, TreeTopSuperParentParam] = [localStorage.getItem('CommonTreeParam'), localStorage.getItem('CommonTreeParentParam'), localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam')];
    obj = RecordId.split('-')

    ObjName = obj[0]
    // A043S001P01-7285 START
    if (TableId != '') {
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    var can_fun_tabId = localStorage.getItem('TableId_cancel_fun');

    if (can_fun_tabId) {
        TableId = can_fun_tabId;
    }
    if (TableId == '' || TableId == 'undefined' || TableId == null || TableId == undefined) {
        TableId = Rel_list_Id
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (TableId == 'SYOBJR-98804') {
        ObjName = 'QTQIBP'
        TreeParam = 'Billing Plan'
    }
    var sub_tbname = localStorage.getItem('subatab_name')
    try {
        SECTION_TEXT = $("div#container." + SECTION_EDIT).find('label').children().text()
        localStorage.setItem("SECTION_TEXT", SECTION_TEXT)

        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': RecordId, 'TableId': TableId, 'TreeParam': TreeParam, 'ObjName': ObjName, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'NEWVAL': '', 'MODE': MODE, 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': SECTION_EDIT, 'SubtabName': sub_tbname }, function (dataset) {
            var [datas, date_field, data2, data3, data4, data5, data6] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[10]];
            var node = '';
            localStorage.setItem('Lookupobjd', data5);
            CurrentNodeId = localStorage.getItem("CurrentNodeId");
            node = $('#commontreeview').treeview('getNode', data4);
            var data = data1 = TreeParam = CurrentTab = CurrentRecordId = CurrentNodeId = TreeParentParam = TreeParentNodeId = TreeParentNodeRecId = TreeSuperParentParam = TreeSuperParentId = TreeSuperParentRecId = TreeTopSuperParentParam = TreeTopSuperParentId = TreeTopSuperParentRecId = TreeSuperTopParentParam = TreeSuperTopParentRecId = TreeSuperTopParentId = TreeFirstSuperTopParentParam = TreeFirstSuperTopParentId = TreeFirstSuperTopParentRecId = '';

            CurrentNodeId = node.nodeId
            CurrentRecordId = node.id;
            //CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
            CurrentTab = $("ul#carttabs_head li.active a span").text();
            var node_text_var = node.text;

            if (typeof (node_text_var) != 'function' && node_text_var.includes("<span")) {
                TreeParam = node_text_var.split(">").pop();
            }
            else {
                TreeParam = node_text_var
            }
            if (data4 && typeof TreeParam === 'string') {
                if (TreeParam.includes("<img")) {
                    TreeParam = TreeParam.split(">")
                    TreeParam = TreeParam[TreeParam.length - 1];
                } else {
                    TreeParam = TreeParam
                }
                if (TreeParam.includes("-")) {

                    if (!TreeParam.includes('- BASE') && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving')) {
                        TreeParam = TreeParam.split("-")[0].trim()
                    }
                } else {
                    TreeParam = TreeParam
                }
            };


            localStorage.setItem("CurrentNodeId", CurrentNodeId);
            data1 = localStorage.getItem('CommonTreedatasetnew');
            data = data1.split(',');
            if (CurrentNodeId != '' && CurrentNodeId != null) {
                TreeParentParam = $('#commontreeview').treeview('getParent', CurrentNodeId).text;
                if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("<img")) {
                    //	TreeParentParam = TreeParentParam.split(">")[1];
                    TreeParentParam = TreeParentParam.split(">")
                    TreeParentParam = TreeParentParam[TreeParentParam.length - 1];
                }
                if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("-")) {
                    if (!TreeParentParam.includes('- BASE')) {
                        TreeParentParam = TreeParentParam.split("-")[0].trim()
                    }
                }
                TreeParentNodeId = $('#commontreeview').treeview('getParent', CurrentNodeId).nodeId;
                TreeParentNodeRecId = $('#commontreeview').treeview('getParent', CurrentNodeId).id;
            }
            if (TreeParentNodeId != '' && TreeParentNodeId != null) {
                TreeSuperParentParam = $('#commontreeview').treeview('getParent', TreeParentNodeId).text;
                if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("<img")) {

                    //	TreeSuperParentParam = TreeSuperParentParam.split(">")[1];
                    TreeSuperParentParam = TreeSuperParentParam.split(">")
                    TreeSuperParentParam = TreeSuperParentParam[TreeSuperParentParam.length - 1];
                }
                if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("-")) {
                    if (!TreeSuperParentParam.includes('- BASE')) {
                        TreeSuperParentParam = TreeSuperParentParam.split("-")[0].trim()
                    }
                }
                TreeSuperParentId = $('#commontreeview').treeview('getParent', TreeParentNodeId).nodeId;
                TreeSuperParentRecId = $('#commontreeview').treeview('getParent', TreeParentNodeId).id;
            }
            if (TreeSuperParentId != '' && TreeSuperParentId != null) {
                TreeTopSuperParentParam = $('#commontreeview').treeview('getParent', TreeSuperParentId).text;
                if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
                    //	TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")[1];
                    TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")
                    TreeTopSuperParentParam = TreeTopSuperParentParam[TreeTopSuperParentParam.length - 1];
                }
                if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("-")) {
                    if (!TreeTopSuperParentParam.includes('- BASE')) {
                        TreeTopSuperParentParam = TreeTopSuperParentParam.split("-")[0].trim()
                    }
                }
                TreeTopSuperParentId = $('#commontreeview').treeview('getParent', TreeSuperParentId).nodeId;
                TreeTopSuperParentRecId = $('#commontreeview').treeview('getParent', TreeSuperParentId).id;
            }
            if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null) {
                TreeSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).text;
                if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
                    //TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")[1];
                    TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")
                    TreeSuperTopParentParam = TreeSuperTopParentParam[TreeSuperTopParentParam.length - 1];
                }
                if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeSuperTopParentParam.includes("-")) {
                    if (!TreeSuperTopParentParam.includes('- BASE')) {
                        TreeSuperTopParentParam = TreeSuperTopParentParam.split("-")[0].trim()
                    }
                }
                TreeSuperTopParentId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
                TreeSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).id;
            }
            if (TreeSuperTopParentId != '' && TreeSuperTopParentId != null) {
                TreeFirstSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).text;
                if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
                    //	TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")[1];
                    TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")
                    TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam[TreeFirstSuperTopParentParam.length - 1];
                }
                if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeFirstSuperTopParentParam.includes("-")) {
                    if (!TreeFirstSuperTopParentParam.includes('- BASE')) {
                        TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split("-")[0].trim()
                    }
                }
                TreeFirstSuperTopParentId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).nodeId;
                TreeFirstSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).id;
            }
            if (TreeSuperParentId === undefined) {
                TreeSuperParentParam = ''
            }
            if (TreeTopSuperParentId === undefined) {
                TreeTopSuperParentParam = ''
            }
            if (TreeSuperTopParentRecId === undefined) {
                TreeSuperTopParentParam = ''
            }
            if (TreeFirstSuperTopParentRecId === undefined) {
                TreeFirstSuperTopParentParam = ''
            }
            var childrenNodes = _getChildren(node);
            if (childrenNodes.length > 0) {
                child = 'true';
            } else {
                child = 'false';
            }

            localStorage.setItem('CommonTreeParam', TreeParam);
            localStorage.setItem('CommonTreeParentParam', TreeParentParam);
            localStorage.setItem('CommonNodeTreeSuperParentParam', TreeSuperParentParam);
            localStorage.setItem('CommonTopSuperParentParam', TreeTopSuperParentParam);
            localStorage.setItem('CommonTreeSuperTopParentParam', TreeSuperTopParentParam); //Accounts Tab 
            localStorage.setItem('CommonTreeFirstSuperTopParentParam', TreeFirstSuperTopParentParam); //Accounts Tab


            localStorage.setItem('CommonParentNodeRecId', TreeParentNodeRecId);
            localStorage.setItem('CommonTreeSuperParentRecId', TreeSuperParentRecId);
            localStorage.setItem('CommonTopSuperParentRecId', TreeTopSuperParentRecId);


            if ((jQuery.inArray(TreeParentParam, data) !== -1) && TreeParam != '') {
                //if (document.getElementById("header_label")) {
                //document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
                //document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
                //document.getElementById('content_banner').style = 'display:block;margin-top: 10px;'
                //}
            }

            else if (((jQuery.inArray(TreeSuperParentParam, data) !== -1) && (jQuery.inArray(TreeParentParam, data) !== -1) && TreeParam != '')) {
                if (document.getElementById("header_label")) {
                    //document.getElementById("header_label").innerHTML = TreeSuperParentParam.toUpperCase();
                    //document.getElementById("banner_label").innerHTML = TreeParentParam.toUpperCase();
                    //document.getElementById("sub_banner_label").innerHTML = TreeParam.toUpperCase();
                    //$('#content_banner, #sub_content_banner').css('cssText','display:block;margin-top: 10px;');
                }
            }
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                if (MODE == 'EDIT') { // to display yellow background while sectional edit
                    $('#CANCELLATION_PERIOD').attr('onchange', 'cancellationPeriodChange()');
                    // if($('#CANCELLATION_PERIOD').val()!="MANUAL INPUT" ){
                    // 	$('#CANCELLATION_PERIOD_NOTPER').closest('tr').css('display','none');
                    // }

                    $('#sec_' + SECTION_EDIT + ' > table > tbody > tr').each(function () {
                        try {
                            if ($(this).find('td.float_r_bor_bot > div > a > i').attr('class').includes('fa-pencil')) {

                                $(this).find('td:nth-child(3) > input,select,textarea').addClass('light_yellow wid_90');

                            }
                        }
                        catch (e) {
                            console.log('No class found');
                        }
                    });

                }
                //$(".CommonTreeDetail").addClass("tree_second_child");
                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                popover()

            }


            $("." + SECTION_EDIT).addClass("SEC_EDIT_ARROW")
            $("." + SECTION_EDIT).css({ "margin-top": "10px", "box-shadow": "1px 0px 8px -1px grey", "padding-bottom": "40px", "padding": "10px", "border-radius": "4px" })
            //A043S001P01-6728--HIDING SECTION LEVEL BUTTONS IN EDIT MODE WHILE COLLAPSING THE SECTION BANNER--START
            //JIRA ID A043S001P01-6722 CHANGED THE BUTTON ORDER FROM SAVE AND CANCEL TO CANCEL AND SAVE -CODE START


            $("." + SECTION_EDIT).append(data6);
            onchangeFunction()
        });
    }
    catch (e) {
        console.log(e);
    }
}
function cancellationPeriodChange() {
    // if($('#CANCELLATION_PERIOD').val()=="MANUAL INPUT"){
    //    $('#CANCELLATION_PERIOD_NOTPER').closest('tr').removeAttr('style');
    // }
    // else{
    //      $('#CANCELLATION_PERIOD_NOTPER').closest('tr').css('display','none');
    // }
}
function legalsowEDIT(ele) {
    // To remove cloapse while sectional edit - Start
    var get_saqtrvfield = localStorage.getItem('rev_field');
    $(ele).closest('#ctr_drop').closest('.dyn_main_head').removeAttr('data-toggle');
    $(ele).closest('#ctr_drop').closest('.dyn_main_head').removeAttr('data-target');
    // To remove cloapse while sectional edit - End
    localStorage.setItem('AddNew', 'false')
    var [SECTION_EDIT, RecordId, TreeParam, TableId, MODE, Rel_list_Id] = [$(ele).attr('id'), get_saqtrvfield, '', localStorage.getItem('CommonParentNodeRecId'), $(ele).text(), localStorage.getItem('Rel_List_Rec_ID')];
    localStorage.setItem('SECTION_LEVEL_EDIT_ID', SECTION_EDIT);
    var [TreeParam, TreeParentParam, TreeSuperParentParam, TopSuperParentParam, TreeTopSuperParentParam] = [localStorage.getItem('CommonTreeParam'), localStorage.getItem('CommonTreeParentParam'), localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam')];
    obj = RecordId.split('-')

    ObjName = obj[0]
    // A043S001P01-7285 START
    if (TableId != '') {
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    var can_fun_tabId = localStorage.getItem('TableId_cancel_fun');

    if (can_fun_tabId) {
        TableId = can_fun_tabId;
    }
    if (TableId == '' || TableId == 'undefined' || TableId == null || TableId == undefined) {
        TableId = Rel_list_Id
        localStorage.setItem('TableId_cancel_fun', TableId);
    }

    var sub_tbname = localStorage.getItem('subatab_name')
    try {
        SECTION_TEXT = $("div#container." + SECTION_EDIT).find('label').children().text()
        localStorage.setItem("SECTION_TEXT", SECTION_TEXT)

        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': RecordId, 'TableId': TableId, 'TreeParam': TreeParam, 'ObjName': ObjName, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'NEWVAL': '', 'MODE': MODE, 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': SECTION_EDIT, 'SubtabName': sub_tbname, 'LEGALSOW': 'LEGAL_SOW' }, function (dataset) {
            var [datas, date_field, data2, data3, data4, data5, data6] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[10]];
            var node = '';
            localStorage.setItem('Lookupobjd', data5);
            CurrentNodeId = localStorage.getItem("CurrentNodeId");
            //A055S000P01-20972 - Start - M
            if(localStorage.getItem('currentSubTab')=="Legal SoW"){
                data4=0;
            }
            //A055S000P01-20972 - End - M
            node = $('#commontreeview').treeview('getNode', data4);
            var data = data1 = TreeParam = CurrentTab = CurrentRecordId = CurrentNodeId = TreeParentParam = TreeParentNodeId = TreeParentNodeRecId = TreeSuperParentParam = TreeSuperParentId = TreeSuperParentRecId = TreeTopSuperParentParam = TreeTopSuperParentId = TreeTopSuperParentRecId = TreeSuperTopParentParam = TreeSuperTopParentRecId = TreeSuperTopParentId = TreeFirstSuperTopParentParam = TreeFirstSuperTopParentId = TreeFirstSuperTopParentRecId = '';

            CurrentNodeId = node.nodeId
            CurrentRecordId = node.id;
            //CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
            CurrentTab = $("ul#carttabs_head li.active a span").text();
            var node_text_var = node.text;
            if (typeof (node_text_var) != 'function' && node_text_var.includes("<span")) {
                TreeParam = node_text_var.split(">").pop();
            }
            else {
                TreeParam = node_text_var
            }
            if (data4) {
                if (TreeParam.includes("<img")) {
                    TreeParam = TreeParam.split(">")
                    TreeParam = TreeParam[TreeParam.length - 1];
                } else {
                    TreeParam = TreeParam
                }
                if (TreeParam.includes("-")) {

                    if (!TreeParam.includes('- BASE') && TreeParam != 'Add-On Products' && !TreeParam.includes('Sending') && !TreeParam.includes('Receiving')) {
                        TreeParam = TreeParam.split("-")[0].trim()
                    }
                } else {
                    TreeParam = TreeParam
                }
            };

            localStorage.setItem("CurrentNodeId", CurrentNodeId);
            data1 = localStorage.getItem('CommonTreedatasetnew');
            data = data1.split(',');
            if (CurrentNodeId != '' && CurrentNodeId != null) {
                TreeParentParam = $('#commontreeview').treeview('getParent', CurrentNodeId).text;
                if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("<img")) {
                    //	TreeParentParam = TreeParentParam.split(">")[1];
                    TreeParentParam = TreeParentParam.split(">")
                    TreeParentParam = TreeParentParam[TreeParentParam.length - 1];
                }
                if (TreeParentParam != '' && TreeParentParam != undefined && (typeof TreeParentParam === 'string' || TreeParentParam instanceof String) && TreeParentParam.includes("-")) {
                    if (!TreeParentParam.includes('- BASE')) {
                        TreeParentParam = TreeParentParam.split("-")[0].trim()
                    }
                }
                TreeParentNodeId = $('#commontreeview').treeview('getParent', CurrentNodeId).nodeId;
                TreeParentNodeRecId = $('#commontreeview').treeview('getParent', CurrentNodeId).id;
            }
            if (TreeParentNodeId != '' && TreeParentNodeId != null) {
                TreeSuperParentParam = $('#commontreeview').treeview('getParent', TreeParentNodeId).text;
                if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("<img")) {
                    TreeSuperParentParam = TreeSuperParentParam.split(">")
                    TreeSuperParentParam = TreeSuperParentParam[TreeSuperParentParam.length - 1];
                    //	TreeSuperParentParam = TreeSuperParentParam.split(">")[1];

                }
                if (TreeSuperParentParam != '' && TreeSuperParentParam != undefined && (typeof TreeSuperParentParam === 'string' || TreeSuperParentParam instanceof String) && TreeSuperParentParam.includes("-")) {
                    if (!TreeSuperParentParam.includes('- BASE')) {
                        TreeSuperParentParam = TreeSuperParentParam.split("-")[0].trim()
                    }
                }
                TreeSuperParentId = $('#commontreeview').treeview('getParent', TreeParentNodeId).nodeId;
                TreeSuperParentRecId = $('#commontreeview').treeview('getParent', TreeParentNodeId).id;
            }
            if (TreeSuperParentId != '' && TreeSuperParentId != null) {
                TreeTopSuperParentParam = $('#commontreeview').treeview('getParent', TreeSuperParentId).text;
                if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
                    //	TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")[1];
                    TreeTopSuperParentParam = TreeTopSuperParentParam.split(">")
                    TreeTopSuperParentParam = TreeTopSuperParentParam[TreeTopSuperParentParam.length - 1];
                }
                if (TreeTopSuperParentParam != '' && TreeTopSuperParentParam != undefined && (typeof TreeTopSuperParentParam === 'string' || TreeTopSuperParentParam instanceof String) && TreeTopSuperParentParam.includes("-")) {
                    if (!TreeTopSuperParentParam.includes('- BASE')) {
                        TreeTopSuperParentParam = TreeTopSuperParentParam.split("-")[0].trim()
                    }
                }
                TreeTopSuperParentId = $('#commontreeview').treeview('getParent', TreeSuperParentId).nodeId;
                TreeTopSuperParentRecId = $('#commontreeview').treeview('getParent', TreeSuperParentId).id;
            }
            if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null) {
                TreeSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).text;
                if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
                    //TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")[1];
                    TreeSuperTopParentParam = TreeSuperTopParentParam.split(">")
                    TreeSuperTopParentParam = TreeSuperTopParentParam[TreeSuperTopParentParam.length - 1];
                }
                if (TreeSuperTopParentParam != '' && TreeSuperTopParentParam != undefined && (typeof TreeSuperTopParentParam === 'string' || TreeSuperTopParentParam instanceof String) && TreeSuperTopParentParam.includes("-")) {
                    if (!TreeSuperTopParentParam.includes('- BASE')) {
                        TreeSuperTopParentParam = TreeSuperTopParentParam.split("-")[0].trim()
                    }
                }
                TreeSuperTopParentId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
                TreeSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeTopSuperParentId).id;
            }
            if (TreeSuperTopParentId != '' && TreeSuperTopParentId != null) {
                TreeFirstSuperTopParentParam = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).text;
                if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeTopSuperParentParam.includes("<img")) {
                    //	TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")[1];
                    TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split(">")
                    TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam[TreeFirstSuperTopParentParam.length - 1];
                }
                if (TreeFirstSuperTopParentParam != '' && TreeFirstSuperTopParentParam != undefined && (typeof TreeFirstSuperTopParentParam === 'string' || TreeFirstSuperTopParentParam instanceof String) && TreeFirstSuperTopParentParam.includes("-")) {
                    if (!TreeFirstSuperTopParentParam.includes('- BASE')) {
                        TreeFirstSuperTopParentParam = TreeFirstSuperTopParentParam.split("-")[0].trim()
                    }
                }
                TreeFirstSuperTopParentId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).nodeId;
                TreeFirstSuperTopParentRecId = $('#commontreeview').treeview('getParent', TreeSuperTopParentId).id;
            }
            if (TreeSuperParentId === undefined) {
                TreeSuperParentParam = ''
            }
            if (TreeTopSuperParentId === undefined) {
                TreeTopSuperParentParam = ''
            }
            if (TreeSuperTopParentRecId === undefined) {
                TreeSuperTopParentParam = ''
            }
            if (TreeFirstSuperTopParentRecId === undefined) {
                TreeFirstSuperTopParentParam = ''
            }
            var childrenNodes = _getChildren(node);
            if (childrenNodes.length > 0) {
                child = 'true';
            } else {
                child = 'false';
            }

            localStorage.setItem('CommonTreeParam', TreeParam);
            localStorage.setItem('CommonTreeParentParam', TreeParentParam);
            localStorage.setItem('CommonNodeTreeSuperParentParam', TreeSuperParentParam);
            localStorage.setItem('CommonTopSuperParentParam', TreeTopSuperParentParam);
            localStorage.setItem('CommonTreeSuperTopParentParam', TreeSuperTopParentParam); //Accounts Tab 
            localStorage.setItem('CommonTreeFirstSuperTopParentParam', TreeFirstSuperTopParentParam); //Accounts Tab


            localStorage.setItem('CommonParentNodeRecId', TreeParentNodeRecId);
            localStorage.setItem('CommonTreeSuperParentRecId', TreeSuperParentRecId);
            localStorage.setItem('CommonTopSuperParentRecId', TreeTopSuperParentRecId);


            if ((jQuery.inArray(TreeParentParam, data) !== -1) && TreeParam != '') {
            }

            else if (((jQuery.inArray(TreeSuperParentParam, data) !== -1) && (jQuery.inArray(TreeParentParam, data) !== -1) && TreeParam != '')) {
                if (document.getElementById("header_label")) {
                    //document.getElementById("header_label").innerHTML = TreeSuperParentParam.toUpperCase();
                    //document.getElementById("banner_label").innerHTML = TreeParentParam.toUpperCase();
                    //document.getElementById("sub_banner_label").innerHTML = TreeParam.toUpperCase();
                    //$('#content_banner, #sub_content_banner').css('cssText','display:block;margin-top: 10px;');
                }
            }
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                if (MODE == 'EDIT') { // to display yellow background while sectional edit
                    $('#sec_' + SECTION_EDIT + ' > table > tbody > tr').each(function () {
                        try {
                            if ($(this).find('td.float_r_bor_bot > div > a > i').attr('class').includes('fa-pencil')) {
                                $(this).find('td:nth-child(3) > input,select,textarea').addClass('light_yellow wid_90');
                            }
                        }
                        catch (e) {
                            console.log('No class found');
                        }
                    });
                }
                //$(".CommonTreeDetail").addClass("tree_second_child");
                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                popover()

            }


            $("." + SECTION_EDIT).addClass("SEC_EDIT_ARROW")
            $("." + SECTION_EDIT).css({ "margin-top": "10px", "box-shadow": "1px 0px 8px -1px grey", "padding-bottom": "40px", "padding": "10px", "border-radius": "4px" })
            //A043S001P01-6728--HIDING SECTION LEVEL BUTTONS IN EDIT MODE WHILE COLLAPSING THE SECTION BANNER--START
            //JIRA ID A043S001P01-6722 CHANGED THE BUTTON ORDER FROM SAVE AND CANCEL TO CANCEL AND SAVE -CODE START


            $("." + SECTION_EDIT).append(data6);

            // if (AllTreeParam['TreeParam']=="Quote Information"){
            // 	$("." + SECTION_EDIT).append('<div  class="g4 sec_' + SECTION_EDIT + ' collapse in except_sec removeHorLine iconhvr sec_edit_sty"><button id="" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="QuoteinformationCancel(this)">CANCEL</button><button id="" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="QuoteinformationSave(this)">SAVE</button></div>');	

            // }
            // else if (AllTreeParam['TreeParam'] =="Approval Chain Information"){
            // $("." + SECTION_EDIT).append('<div  class="g4 sec_' + SECTION_EDIT + ' collapse in except_sec removeHorLine iconhvr sec_edit_sty"><button id="" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="ApprovalinformationCancel(this)">CANCEL</button><button id="" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="ApprovalinformationSave(this)">SAVE</button></div>');	

            // }



            //JIRA ID A043S001P01-6722 CHANGED THE BUTTON ORDER FROM SAVE AND CANCEL TO CANCEL AND SAVE -CODE END
            //A043S001P01-6728--HIDING SECTION LEVEL BUTTONS IN EDIT MODE WHILE COLLAPSING THE SECTION BANNER--END
            //onFieldChanges()
            onchangeFunction()
        });
    }
    catch (e) {
        console.log(e);
    }
}

function CommontreeCancel() {
    $('#cust_notifi_warning').css('display', 'none');
    //JIRA ID A055S000P01-2811 start
    $("[id='hidesavecancel']").removeClass("disp_blk").addClass("disp_none");
    //JIRA ID A055S000P01-2811 end
    //JIRA ID A055S000P01-10547 start
    var legal_sow = $('#COMMON_TABS ul li.active').text().trim()
    if (legal_sow == 'Legal SoW') {
        record_id_can = localStorage.getItem('rev_field');
    }
    else {
        record_id_can = $('table > tbody > tr:nth-child(1) > td:nth-child(3) > input').val()
    }
    //JIRA ID A055S000P01-10547 end

    //AllTreeParam = maintreeparamfunction(parseInt(CurrentNodeId), 0);
    //AllTreeParams = JSON.stringify(AllTreeParam);
    //localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    //localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    //localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    //localStorage.setItem('CommonTopSuperParentParam', AllTreeParam['TreeParentLevel2']);
    var [RecordId, TableId, TreeParam, TreeParentParam, TreeSuperParentParam, TopSuperParentParam, TreeTopSuperParentParam, tabId_cancel_fun, Rel_list_Id] = [record_id_can, localStorage.getItem('CommonParentNodeRecId'), AllTreeParam['TreeParam'], AllTreeParam['TreeParentLevel0'], , localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam'), localStorage.getItem('CommonTreeTopSuperParentParam'), localStorage.getItem('TableId_cancel_fun'), localStorage.getItem('Rel_List_Rec_ID')];
    Obj = RecordId.split('-')
    ObjName = Obj[0]
    if (tabId_cancel_fun) {
        TableId = tabId_cancel_fun;
    }
    if (TableId == 'undefined' || TableId == undefined || TableId == null) {
        TableId = Rel_list_Id;
    }

    if (TreeFirstSuperTopParentParam == 'Program Participant Quotas' && currenttab == 'Participant') {
        TableId = 'SYOBJR-90033'
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    //A043S001P01-11642 start
    if (TreeSuperParentParam == 'Personalizations' && currenttab == 'CM Class') {
        TableId = 'SYOBJR-95811'//PERSONALIZATION ATTRIBUTES
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (TreeTopSuperParentParam == 'Personalizations' && currenttab == 'CM Class') {
        TableId = 'SYOBJR-95869		'//PERSONALIZATION ATTR VAL
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (TreeSuperTopParentParam == 'Rules' && currenttab == 'CM Class') {
        TableId = 'SYOBJR-95803'//RULE ACTIONS
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    //A043S001P01-11642 End
    if (TreeParentParam == 'Assigned Members' && currenttab == 'Profile') {
        TableId = 'SYOBJR-95800'
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    // A043S001P01-12253 Start
    if (localStorage.CommonTreeSuperParentRecId == "SYOBJR-94458") {
        TableId = 'SYOBJR-95816'//PERSONALIZATION
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    curretRecIdsplit = RecordId.split('-')
    if (curretRecIdsplit[0] == "ACAPTF") {
        TableId = "SYOBJR-95860"
    }
    curretRecIdsplit = RecordId.split('-')
    if (curretRecIdsplit[0] == "ACAPFV") {
        TableId = "SYOBJR-95870"
    }
    if (curretRecIdsplit[0] == "SYOBJC") {
        TableId = "SYOBJR-95825"
    }
    if (currenttab == "CM Class") {
        ObjName = undefined;
    }
    // A043S001P01-12253 end
    CurrentNodeId = node.nodeId;
    localStorage.setItem("CurrentNodeId", CurrentNodeId)



    // AllTreeParam = maintreeparamfunction(parseInt(CurrentNodeId), 0);
    // AllTreeParams = JSON.stringify(AllTreeParam);
    localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    localStorage.setItem('CommonTopSuperParentParam', AllTreeParam['TreeParentLevel2']);
    try {
        if (legal_sow == 'Legal SoW') {
            Common_Tabs('', 'DetailLegalSow')
        }
        else {
            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': RecordId, 'TableId': TableId, 'TreeParam': TreeParam, 'ObjName': ObjName, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'NEWVAL': '', 'MODE': 'CANCEL', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                localStorage.setItem('Lookupobjd', data5)
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                    $("#div_CTR_related_list").hide();
                    if (TreeParentParam == 'Object Level Permissions') {
                        $('.BTN_MA_ALL_REFRESH').click();
                    }
                    //Added for hiding values based on picklist values selection in section cancel - start
                    //Added for hiding values based on picklist values selection in section cancel - end
                    // Added to hide the FPM INFORMATION section in QTQITM details page based on quote type -  start
                    if (CurrentTab == "Quotes") {
                        //var getopptype = $( "#QSTN_SYSEFL_QT_00723 option:selected" ).text();
                        var getopptype = localStorage.getItem("getopptype");
                    }
                    else if (CurrentTab == "Contracts") {
                        var getopptype = $("#QSTN_SYSEFL_QT_016912 option:selected").text();
                    }
                    if (getopptype == "ZTBC - TOOL BASED") {
                        $('.CC119201-572D-41BB-8C53-5C063EEAAD4F').css('display', 'none');
                        //$(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display','none');
                    }
                    else {
                        $('.CC119201-572D-41BB-8C53-5C063EEAAD4F').css('display', 'block');
                    }
                    // Added to hide the FPM INFORMATION section in QTQITM details page based on quote type -  end
                }
            });
        }
    }
    catch (e) {
        console.log(e);
    }
}
function ApprovalinformationCancel() {
    $('#cust_notifi_warning').css('display', 'none');
    //JIRA ID A055S000P01-2811 start
    $("[id='hidesavecancel']").removeClass("disp_blk").addClass("disp_none");
    //JIRA ID A055S000P01-2811 end
    var [RecordId, TableId, TreeParam, TreeParentParam, TreeSuperParentParam, TopSuperParentParam, TreeTopSuperParentParam, tabId_cancel_fun, Rel_list_Id] = [$("#APPROVAL_CHAIN_RECORD_ID").val(), localStorage.getItem('CommonParentNodeRecId'), localStorage.getItem('CommonTreeParam'), localStorage.getItem('CommonTreeParentParam'), localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam'), localStorage.getItem('CommonTreeTopSuperParentParam'), localStorage.getItem('TableId_cancel_fun'), localStorage.getItem('Rel_List_Rec_ID')];
    Obj = RecordId.split('-')
    ObjName = Obj[0]
    if (tabId_cancel_fun) {
        TableId = tabId_cancel_fun;
    }
    if (TableId == 'undefined' || TableId == undefined || TableId == null) {
        TableId = Rel_list_Id;
    }
    try {
        rec_id = $(".product_txt_to_top").text();
        cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'Approval_Chain_INFO', 'RECORD_ID': rec_id }, function (data0) {
            if (data0 != '') {
                //$('.CommonTreeDetail').css('display', 'none');
                $('.container_banner_inner_sec').css("display", "none")
                $('#TREE_div').html(data0);
                $(".CommonTreeDetail").css("display", "block");
                //$('.HideAddNew').remove();
                // $('#HideSavecancel').remove()
                // $("#div_CTR_Opportunity").closest('.Related').css("display", "block");
                // $('[data-toggle="popover"]').popover();
            }
        });
    }
    catch (e) {
        console.log(e);
    }
}

function QuoteinformationCancel() {
    $(".emp_notifiy").css('display', 'none');
    $("#PageAlert ").css('display', 'none');
    $('#cust_notifi_warning').css('display', 'none');
    //JIRA ID A055S000P01-2811 start
    $("[id='hidesavecancel']").removeClass("disp_blk").addClass("disp_none");
    //JIRA ID A055S000P01-2811 end
    var [RecordId, TableId, TreeParam, TreeParentParam, TreeSuperParentParam, TopSuperParentParam, TreeTopSuperParentParam, tabId_cancel_fun, Rel_list_Id] = [$("#QUOTE_REVISION_RECORD_ID").val(), localStorage.getItem('CommonParentNodeRecId'), localStorage.getItem('CommonTreeParam'), localStorage.getItem('CommonTreeParentParam'), localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam'), localStorage.getItem('CommonTreeTopSuperParentParam'), localStorage.getItem('TableId_cancel_fun'), localStorage.getItem('Rel_List_Rec_ID')];
    Obj = RecordId.split('-')
    ObjName = Obj[0]
    if (tabId_cancel_fun) {
        TableId = tabId_cancel_fun;
    }
    if (TableId == 'undefined' || TableId == undefined || TableId == null) {
        TableId = Rel_list_Id;
    }
    var sub_tbname = localStorage.getItem('subatab_name')
    if (sub_tbname == 'Idling Attributes') {
        try {
            cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'QUOTE_ATTR', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal }, function (data0) {
                if (data0 != '') {
                    $("#div_CTR_related_list").hide();
                    $('.container_banner_inner_sec').css("display", "none")
                    $('#TREE_div').html(data0[0]);
                    $(".CommonTreeDetail").css("display", "block");
                    //$('.HideAddNew').remove();
                    // $('#HideSavecancel').remove()
                    // $("#div_CTR_Opportunity").closest('.Related').css("display", "block");
                    // $('[data-toggle="popover"]').popover();
                    onchangeFunction()
                }
            });
        }
        catch (e) {
            console.log(e);
        }
    }
    else {
        try {
            cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'QUOTE_INFO', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal }, function (data0) {
                if (data0 != '') {
                    $("#div_CTR_related_list").hide();
                    $('.container_banner_inner_sec').css("display", "none")
                    $('#TREE_div').html(data0);
                    // if($('#CANCELLATION_PERIOD').val()!="MANUAL INPUT"){
                    //     $('#CANCELLATION_PERIOD_NOTPER').closest('div').parent('div').parent('div').css('display','none');
                    // }
                    $(".CommonTreeDetail").css("display", "block");
                    //$('.HideAddNew').remove();
                    // $('#HideSavecancel').remove()
                    // $("#div_CTR_Opportunity").closest('.Related').css("display", "block");
                    // $('[data-toggle="popover"]').popover();
                }
            });
        }
        catch (e) {
            console.log(e);
        }
    }
}

function QuoteinformationSave() {
    valid_from = Date.parse($("#CONTRACT_VALID_FROM").val())
    Valid_to = Date.parse($("#CONTRACT_VALID_TO").val())
    // cancellation_period = $("#CANCELLATION_PERIOD").val()


    if (Valid_to < valid_from) {
        $(".emp_notifiy").css('display', 'block');
        $("#PageAlert ").css('display', 'block');
        $("#alertnotify").html("CONTRACT VALID TO DATE SHOULD NOT LESS THAN CONTRACT VALID FROM DATE");
    }
    // else if (cancellation_period > 180){
    // 	$(".emp_notifiy").css('display','block');
    // 	$("#PageAlert ").css('display','block');
    // 	$("#alertnotify").html("CANCELLATION PERIOD SHOULD NOT GREATER THAN 180");
    // }
    else {
        var [RecordId, dict_new] = [$("#QUOTE_REVISION_RECORD_ID").val(), {}];
        //JIRA ID A055S000P01-2811 start
        $("[id='hidesavecancel']").removeClass("disp_blk").addClass("disp_none");
        //JIRA ID A055S000P01-2811 end
        obj = RecordId.split('-')
        ObjName = obj[0]




        // Added to stay page in same node if we click on save in sectional edit - start
        CurrentNodeId = node.nodeId;
        localStorage.setItem("CurrentNodeId", CurrentNodeId)
        // Added to stay page in same node if we click on save in sectional edit - end
        $("#TREE_div #container table tbody tr td select").each(function () {
            currentid = $(this).attr('id')
            if (currentid != 'FirstMESSAGE_HEADERVALUE' && currentid != 'options1_MESSAGE_HEADERVALUE' && currentid != 'FirstMESSAGE_BODYVALUE' && currentid != 'options1_MESSAGE_BODYVALUE') {
                dict_new[$(this).attr('id')] = $(this).children(":selected").val();
            }
            if (currentid == 'options1_MESSAGE_HEADERVALUE') {
                fec = ''
                $('select#options1_MESSAGE_HEADERVALUE option').each(function () {
                    fec += $(this).val()
                    fec += ','
                });
                fec = fec.slice(0, -1)
                dict_new["MESSAGE_HEADERVALUE"] = fec
            }
            else if (currentid == 'options1_MESSAGE_BODYVALUE') {
                fec = ''
                $('select#options1_MESSAGE_BODYVALUE option').each(function () {
                    fec += $(this).val()
                    fec += ','
                });
                fec = fec.slice(0, -1)
                dict_new["MESSAGE_BODYVALUE"] = fec
            }
        });
        $("#TREE_div #container table tbody tr td input:not(.popup)").each(function () {
            if ($(this).attr('type') == 'CHECKBOX') {
                dict_new[$(this).attr('id')] = String($(this).prop("checked"));
            } else {
                id_val = $(this).attr('id');
                dict_new[$(this).attr('id')] = $('#TREE_div #container table tbody tr td input#' + id_val).val();
            }
        });
        $("#TREE_div #container textarea").each(function () {
            id_val = $(this).attr('id');
            dict_new[$(this).attr('id')] = $('#TREE_div #container table tbody tr td textarea#' + id_val).val();
        })
        dict_new['RECORDID'] = RecordId;

        if (TreeFirstSuperTopParentParam == 'Program Participant Quotas' && currenttab == 'Participant') {
            TableId = 'SYOBJR-90033'
        }

        var sub_tbname = localStorage.getItem('subatab_name')


        var [TableId, TreeParam, TreeParentParam, TreeSuperParentParam, TopSuperParentParam, TreeTopSuperParentParam] = [localStorage.getItem('TableId_cancel_fun'), AllTreeParam['TreeParam'], localStorage.getItem('CommonTreeParentParam'), localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam')];
        sub_tab_name = localStorage.getItem("currentSubTab")
        if (sub_tbname == "Idling Attributes") {
            try {
                SECTION_TEXT = localStorage.getItem("SECTION_TEXT")
                cpq.server.executeScript("SYSECTSAVE", { 'RECORD': JSON.stringify(dict_new), 'TableId': TableId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TopSuperParentParam': TopSuperParentParam, 'SECTION_TEXT': SECTION_TEXT, 'subtab_name': sub_tab_name }, function (data) {
                    if (data[1] == "") {

                        $('#cust_notifi_warning').css('display', 'none');
                        // commenting to avoid jumping issue while clicking save in section level - start
                        //CommonLeftView()// to update the tree for approval trip after changing payterm
                        // commenting to avoid jumping issue while clicking save in section level - end
                        try {
                            cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'QUOTE_ATTR', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal }, function (data0) {

                                if (data0 != '') {
                                    //contract valid date from and to updated in primary highlight panel	
                                    var valid_from = new Date(data0[6]);
                                    var dd = String(valid_from.getDate()).padStart(2, '0');
                                    var mm = String(valid_from.getMonth() + 1).padStart(2, '0');
                                    var yyyy = valid_from.getFullYear();
                                    valid_from = mm + '/' + dd + '/' + yyyy;
                                    var valid_to = new Date(data0[7]);
                                    var dd = String(valid_to.getDate()).padStart(2, '0');
                                    var mm = String(valid_to.getMonth() + 1).padStart(2, '0');
                                    var yyyy = valid_to.getFullYear();
                                    valid_to = mm + '/' + dd + '/' + yyyy;
                                    $('.order_mgmt_date_text').text(valid_from);
                                    $('.segment_revision_text').text(valid_to);
                                    //$('.CommonTreeDetail').css('display', 'none');
                                    $('.container_banner_inner_sec').css("display", "none")
                                    //$('.order_mgmt_date_text').text(data0[6]);
                                    //$('.segment_revision_text').text(data0[7]);
                                    $('#TREE_div').html(data0);
                                    $("#div_CTR_related_list").hide();
                                    $(".CommonTreeDetail").css("display", "block");
                                    //$('.HideAddNew').remove();
                                    // $('#HideSavecancel').remove()
                                    // $("#div_CTR_Opportunity").closest('.Related').css("display", "block");
                                    // $('[data-toggle="popover"]').popover();
                                    if (currenttab == "Quotes" && SECTION_TEXT == ' EDITBASIC INFORMATION') {
                                        //QuoteStatus();
                                        dynamic_status();
                                    }
                                    // calling subbaner function update subanner after save the section - start
                                    Subbaner("Details", CurrentNodeId, CurrentRecordId, ObjName);
                                    // calling subbaner function update subanner after save the section - end
                                    onchangeFunction()
                                    primary_banner()
                                }
                            });
                        } catch (err) {
                            console.log(err);
                        }
                    }
                });
            } catch (e) {
                console.log(e);
            }
        }
        else {
            try {
                SECTION_TEXT = localStorage.getItem("SECTION_TEXT")
                sub_tab_name = localStorage.getItem("currentSubTab")
                cpq.server.executeScript("SYSECTSAVE", { 'RECORD': JSON.stringify(dict_new), 'TableId': TableId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TopSuperParentParam': TopSuperParentParam, 'SECTION_TEXT': SECTION_TEXT, 'subtab_name': sub_tab_name }, function (data) {
                    if (data[1] == "") {

                        $('#cust_notifi_warning').css('display', 'none');
                        // commenting to avoid jumping issue while clicking save in section level - start
                        //CommonLeftView()// to update the tree for approval trip after changing payterm
                        // commenting to avoid jumping issue while clicking save in section level - end
                        try {
                            cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'QUOTE_INFO', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal }, function (data0) {

                                if (data0 != '') {
                                    //contract valid date from and to updated in primary highlight panel
                                    $('#TREE_div').html(data0);
                                    // if($('#CANCELLATION_PERIOD').val()!="MANUAL INPUT"){
                                    // 	$('#CANCELLATION_PERIOD_NOTPER').closest('div').parent('div').parent('div').css('display','none');
                                    // }
                                    $("#div_CTR_related_list").hide();
                                    $(".CommonTreeDetail").css("display", "block");
                                    //$('.HideAddNew').remove();
                                    // $('#HideSavecancel').remove()
                                    // $("#div_CTR_Opportunity").closest('.Related').css("display", "block");
                                    // $('[data-toggle="popover"]').popover();
                                    if (currenttab == "Quotes" && SECTION_TEXT == ' EDITBASIC INFORMATION') {
                                        //QuoteStatus();
                                        dynamic_status();
                                    }
                                    // calling subbaner function update subanner after save the section - start
                                    Subbaner("Details", CurrentNodeId, CurrentRecordId, ObjName);
                                    primary_banner()
                                    // calling subbaner function update subanner after save the section - end
                                }
                            });
                        } catch (err) {
                            console.log(err);
                        }
                    }
                });
            } catch (e) {
                console.log(e);
            }
        }
    }

}

function ApprovalinformationSave() {
    var [RecordId, dict_new] = [$("#APPROVAL_CHAIN_RECORD_ID").val(), {}];
    //JIRA ID A055S000P01-2811 start
    $("[id='hidesavecancel']").removeClass("disp_blk").addClass("disp_none");
    //JIRA ID A055S000P01-2811 end
    obj = RecordId.split('-')
    ObjName = obj[0]




    // Added to stay page in same node if we click on save in sectional edit - start
    CurrentNodeId = node.nodeId;
    localStorage.setItem("CurrentNodeId", CurrentNodeId)
    // Added to stay page in same node if we click on save in sectional edit - end
    $("#TREE_div #container table tbody tr td select").each(function () {
        currentid = $(this).attr('id')
        if (currentid != 'FirstMESSAGE_HEADERVALUE' && currentid != 'options1_MESSAGE_HEADERVALUE' && currentid != 'FirstMESSAGE_BODYVALUE' && currentid != 'options1_MESSAGE_BODYVALUE') {
            dict_new[$(this).attr('id')] = $(this).children(":selected").val();
        }
        if (currentid == 'options1_MESSAGE_HEADERVALUE') {
            fec = ''
            $('select#options1_MESSAGE_HEADERVALUE option').each(function () {
                fec += $(this).val()
                fec += ','
            });
            fec = fec.slice(0, -1)
            dict_new["MESSAGE_HEADERVALUE"] = fec
        }
        else if (currentid == 'options1_MESSAGE_BODYVALUE') {
            fec = ''
            $('select#options1_MESSAGE_BODYVALUE option').each(function () {
                fec += $(this).val()
                fec += ','
            });
            fec = fec.slice(0, -1)
            dict_new["MESSAGE_BODYVALUE"] = fec
        }
    });
    $("#TREE_div #container table tbody tr td input:not(.popup)").each(function () {
        if ($(this).attr('type') == 'CHECKBOX') {
            dict_new[$(this).attr('id')] = String($(this).prop("checked"));
        } else {
            id_val = $(this).attr('id');
            dict_new[$(this).attr('id')] = $('#TREE_div #container table tbody tr td input#' + id_val).val();
        }
    });
    $("#TREE_div #container textarea").each(function () {
        id_val = $(this).attr('id');
        dict_new[$(this).attr('id')] = $('#TREE_div #container table tbody tr td textarea#' + id_val).val();
    })
    dict_new['RECORDID'] = RecordId;

    if (TreeFirstSuperTopParentParam == 'Program Participant Quotas' && currenttab == 'Participant') {
        TableId = 'SYOBJR-90033'
    }


    var [TableId, TreeParam, TreeParentParam, TreeSuperParentParam, TopSuperParentParam, TreeTopSuperParentParam] = [localStorage.getItem('TableId_cancel_fun'), AllTreeParam['TreeParam'], localStorage.getItem('CommonTreeParentParam'), localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam')];
    try {
        sub_tab_name = localStorage.getItem("currentSubTab")
        cpq.server.executeScript("SYSECTSAVE", { 'RECORD': JSON.stringify(dict_new), 'TableId': TableId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TopSuperParentParam': TopSuperParentParam, 'subtab_name': sub_tab_name }, function (data) {
            if (data[1] == "") {

                $('#cust_notifi_warning').css('display', 'none');
                try {
                    rec_id = $(".product_txt_to_top").text();
                    cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'Approval_Chain_INFO', 'RECORD_ID': rec_id }, function (data0) {
                        if (data0 != '') {
                            //$('.CommonTreeDetail').css('display', 'none');
                            $('.container_banner_inner_sec').css("display", "none")
                            $('#TREE_div').html(data0);
                            $(".CommonTreeDetail").css("display", "block");
                            //$('.HideAddNew').remove();
                            // $('#HideSavecancel').remove()
                            // $("#div_CTR_Opportunity").closest('.Related').css("display", "block");
                            // $('[data-toggle="popover"]').popover();
                        }
                    });
                } catch (err) {
                    console.log(err);
                }
            }
        });
    } catch (e) {
        console.log(e);
    }
}


function CommontreeSAVE() {
    var [RecordId, dict_new] = [$("#TREE_div table tbody tr td input").val(), {}];
    //JIRA ID A055S000P01-2811 start
    $("[id='hidesavecancel']").removeClass("disp_blk").addClass("disp_none");
    //JIRA ID A055S000P01-2811 end
    obj = RecordId.split('-')
    ObjName = obj[0]
    // A043S001P01-12265 Start
    if (ObjName == "ACAPTF") {
        TableId = "SYOBJR-95860"
        localStorage.setItem('TableId_cancel_fun', TableId)
    }
    if (ObjName == "SAQTRV") {
        TableId = "SYOBJR-98869"
        localStorage.setItem('TableId_cancel_fun', TableId)
    }
    if (ObjName == "ACAPFV") {
        TableId = "SYOBJR-95870"
        localStorage.setItem('TableId_cancel_fun', TableId)
    }
    // A043S001P01-12265 End
    // A043S001P01-11642 Start
    if (ObjName == "CMCRAC") {
        TableId = "SYOBJR-95803"
        localStorage.setItem('TableId_cancel_fun', TableId)
    }
    if (ObjName == "CMCPAT") {
        TableId = "SYOBJR-95811"
        localStorage.setItem('TableId_cancel_fun', TableId)
    }
    if (ObjName == "CMCVVP") {
        TableId = "SYOBJR-95869"
        localStorage.setItem('TableId_cancel_fun', TableId)
    }
    if (ObjName == "CMCLSE") {
        TableId = "SYOBJR-95814"
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (ObjName == "CMCMQU") {
        TableId = "SYOBJR-95813"
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (ObjName == "CMCLTB") {
        TableId = "SYOBJR-95812"
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (ObjName == "CMCMAT") {
        TableId = "SYOBJR-90006"
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    // A043S001P01-11642 End
    //A043S001P01-13851 START
    if (ObjName == "SYTABS") {
        TableId = "SYOBJR-95982"
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (ObjName == "SYTREE") {
        TableId = "SYOBJR-95981"
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (ObjName == "SAQTIP") {
        TableId = "SYOBJR-98798"
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (ObjName == "SYSECT") {
        TableId = "SYOBJR-95980"
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (ObjName == "ACACSA") {
        TableId = "SYOBJR-00014"
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (ObjName == "ACACSS") {
        TableId = "SYOBJR-00016"
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    if (ObjName == "SAQSCO") {
        TableId = "SYOBJR-98791"
        localStorage.setItem('TableId_cancel_fun', TableId)
    }
    //Send the correct Table id for Quote item details...
    if (ObjName == "QTQITM") {
        TableId = "SYOBJR-00008"
        localStorage.setItem('TableId_cancel_fun', TableId);
    }
    //Send the correct Table id for Quote item details...
    //A043S001P01-13851 END
    // Added to stay page in same node if we click on save in sectional edit - start


    CurrentNodeId = node.nodeId;
    localStorage.setItem("CurrentNodeId", CurrentNodeId)

    // Added to stay page in same node if we click on save in sectional edit - end
    $("#TREE_div #container table tbody tr td select").each(function () {
        currentid = $(this).attr('id')
        if (currentid != 'FirstMESSAGE_HEADERVALUE' && currentid != 'options1_MESSAGE_HEADERVALUE' && currentid != 'FirstMESSAGE_BODYVALUE' && currentid != 'options1_MESSAGE_BODYVALUE') {
            dict_new[$(this).attr('id')] = $(this).children(":selected").val();
        }
        if (currentid == 'options1_MESSAGE_HEADERVALUE') {
            fec = ''
            $('select#options1_MESSAGE_HEADERVALUE option').each(function () {
                fec += $(this).val()
                fec += ','
            });
            fec = fec.slice(0, -1)
            dict_new["MESSAGE_HEADERVALUE"] = fec
        }
        else if (currentid == 'options1_MESSAGE_BODYVALUE') {
            fec = ''
            $('select#options1_MESSAGE_BODYVALUE option').each(function () {
                fec += $(this).val()
                fec += ','
            });
            fec = fec.slice(0, -1)
            dict_new["MESSAGE_BODYVALUE"] = fec
        }
    });
    $("#TREE_div #container table tbody tr td input:not(.popup)").each(function () {
        if ($(this).attr('type') == 'CHECKBOX') {
            dict_new[$(this).attr('id')] = String($(this).prop("checked"));
        } else {
            id_val = $(this).attr('id');
            dict_new[$(this).attr('id')] = $('#TREE_div #container table tbody tr td input#' + id_val).val();
        }
    });
    $("#TREE_div #container textarea").each(function () {
        id_val = $(this).attr('id');
        dict_new[$(this).attr('id')] = $('#TREE_div #container table tbody tr td textarea#' + id_val).val();
    })
    dict_new['RECORDID'] = RecordId;

    if (TreeFirstSuperTopParentParam == 'Program Participant Quotas' && currenttab == 'Participant') {
        TableId = 'SYOBJR-90033'
    }
    AllTreeParam = maintreeparamfunction(parseInt(CurrentNodeId), 0);
    AllTreeParams = JSON.stringify(AllTreeParam);
    localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    localStorage.setItem('CommonTopSuperParentParam', AllTreeParam['TreeParentLevel2']);
    sub_tab_name = localStorage.getItem("currentSubTab")
    var [TableId, TreeParam, TreeParentParam, TreeSuperParentParam, TopSuperParentParam, TreeTopSuperParentParam] = [localStorage.getItem('TableId_cancel_fun'), localStorage.getItem('CommonTreeParam'), localStorage.getItem('CommonTreeParentParam'), localStorage.getItem('CommonNodeTreeSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam'), localStorage.getItem('CommonTopSuperParentParam')];
    try {
        cpq.server.executeScript("SYSECTSAVE", { 'RECORD': JSON.stringify(dict_new), 'TableId': TableId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TopSuperParentParam': TopSuperParentParam, 'subtab_name': sub_tab_name }, function (data) {
            if (data[1] == "") {

                $('#cust_notifi_warning').css('display', 'none');

                if (data[3] != "" && TableId == "SYOBJR-93121") {

                    $('#alert_msg').css('display', 'block');
                    $('#alert_msg div label').text("! ERROR:CPQ Administrator must set visible permission to system admin app");

                }

                else if (data[6] != "" && TreeParam == "Billing Matrix") {
                    $('#cust_notifi_warning').css('display', 'block');

                    $('#cust_notifi_warning div label').html('<img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/warning1.svg" alt="Info"> Warning: Selected Billing Date is greater than Contract Start Date.Please select valid Billing Date');



                }
                else if (data[7] != "" && TreeParam == "Billing Matrix") {
                    $('#cust_notifi_warning').css('display', 'block');

                    $('#cust_notifi_warning div label').html('<img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/warning1.svg" alt="Info"> Warning: Please proceed with valid Billing Day before saving');
                }


                else {
                    if (currenttab == "CM Class") {
                        ObjName = undefined;
                    }
                    try {
						// A055S000P01-20393 Start - M
                        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': RecordId, 'TableId': TableId, 'TreeParam': TreeParam, 'ObjName': ObjName, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'NEWVAL': '', 'MODE': 'VIEW', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1, 'SubtabName': sub_tab_name }, function (dataset) {
						// A055S000P01-20393 End - M

                            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];

                            localStorage.setItem('Lookupobjd', data5)
                            if (document.getElementById("TREE_div")) {
                                document.getElementById("TREE_div").innerHTML = datas;
                                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                                popover()
                                // commented because of issue: while clicking on save in edit mode it is redirecting to Related list -  start
                                //CommonLeftView()
                                // commented because of issue: while clicking on save in edit mode it is redirecting to Related list -  end
                            }
                            //A055S000P01-9435 To update the primary panel after saving the record value in section edit code starts...
                            primary_banner()
                            //A055S000P01-10547
                            var legal_sow = $('#COMMON_TABS ul li.active').text().trim()
                            if (legal_sow == 'Legal SoW' && data[1] == "") {
                                Common_Tabs('', 'DetailLegalSow')
                                $('#Newrevision1').css('display', 'none')
                            }
                            //A055S000P01-9435 To update the primary panel after saving the record value in section edit code ends...
                            //if(TreeParentParam == 'Tabs'){
                            //	CommonLeftView()

                            //}
                            if (localStorage.getItem('CommonNodeTreeSuperParentParam') == "Quote Items" || localStorage.getItem('CommonTopSuperParentParam') == "Quote Items" || localStorage.getItem('CommonTreeParentParam') == "Quote Items") {
                                localStorage.setItem("add_new_functionality", "TRUE");
                                //localStorage.setItem("SaveSalesPrice","yes");
                                $("[id='qtn_save'] span").click();
                            }
                            if (TreeParentParam == "Indexes" || TreeParentParam == "Assigned Members") {
                                localStorage.setItem("add_new_functionality", "TRUE");
                            }
                            $('.BTN_MA_ALL_REFRESH').click();
                            if (ObjName == "SAQTIP") {
                                var trans_rec_id = localStorage.getItem('involvedparties_details')
                                Subbaner('Detail', CurrentNodeId, trans_rec_id, ObjName);
                            }
                            // for loading left tree view in ascending order under Approval Chain Steps node - start
                            if (TreeParentParam == 'Approval Chain Steps' && ObjName == 'ACACST') {
                                CommonLeftView();
                            }
                            if (TreeParam == 'Customer Information') {
                                localStorage.setItem("left_tree_refresh", "yes")
                                localStorage.setItem("add_new_functionality", "TRUE")
                                CommonLeftView();
                            }
                            // for loading left tree view in ascending order under Approval Chain Steps node - end
                            //$("#BTN_MA_ALL_REFRESH").click();
                            // Billing Matrix Dynamic Tab - Start
                            if (TreeParam == 'Billing') {
                                CommonLeftView();
                            }
                            if (TreeParam == 'Revisions') {
                                CommonLeftView();
                                var get_currentnode = node.nodeId
                                CommonRightView(get_currentnode);
                            }
                            // Billing Matrix Dynamic Tab - End
                            //Added for hiding values based on picklist values selection in section save - start
                            if ((TreeParentParam == 'Approval Chain Steps' || TreeSuperParentParam == 'Approval Chain Steps') && ObjName == 'ACACSA') {

                                onFieldChanges()
                            }
                            //Added for hiding values based on picklist values selection in section save - end
                            // Added to hide the FPM INFORMATION section in QTQITM details page based on quote type -  start
                            if (CurrentTab == "Quotes") {
                                //var getopptype = $( "#QSTN_SYSEFL_QT_00723 option:selected" ).text();
                                var getopptype = localStorage.getItem("getopptype");
                            }
                            else if (CurrentTab == "Contracts") {
                                var getopptype = $("#QSTN_SYSEFL_QT_016912 option:selected").text();
                            }
                            if (getopptype == "ZTBC - TOOL BASED") {
                                $('.CC119201-572D-41BB-8C53-5C063EEAAD4F').css('display', 'none');
                                //$(".85FDCC0D-DCC0-4428-921E-F6D6DCED4B4C").css('display','none');
                            }
                            else {
                                $('.CC119201-572D-41BB-8C53-5C063EEAAD4F').css('display', 'block');
                            }
                            // Added to hide the FPM INFORMATION section in QTQITM details page based on quote type -  end	

                        });
                    } catch (err) {
                        console.log(err);
                    }
                }
            }
            else {
                $('#alert_msg').css('display', 'block');
                $('#alert_msg div label').text(data[1]);
                //A055S000P01-10547
                $("[id='hidesavecancel']").removeClass("disp_none").addClass("disp_blk");
            }
        });
    } catch (e) {
        console.log(e);
    }
}

function CommonTree_lookup_popup(elem) {
    popup_value = $(elem).siblings('input').attr('id');
    localStorage.setItem('selected_popup_id', popup_value);
    var value1 = $(elem).attr('id');
    var value_split = value1.split("|");
    if (value_split[0] == "") {
        value_split[0] = "SYTABS"
    }
    var [value, table, look_up_id, input_val, pop_id, assoc, keyData, price_mod_id] = [value_split[0], value_split[1], $(elem).closest('td').children('input:first').attr('id'), [], [], {}, '', ''];
    if (value_split[1] == 'SAQSTE' && value_split[0] == 'MAFBLC') {
        look_up_id = 'FABLOCATION_ID'
        Current_object_name = 'SAQSTE'
        localStorage.setItem('Lookupobjd', Current_object_name)
    }
    else if (value_split[1] == 'SAQICO' && value_split[0] == 'PRTXCL') {
        look_up_id = 'SRVTAXCLA_DESCRIPTION'
        Current_object_name = 'SAQICO'
        localStorage.setItem('Lookupobjd', Current_object_name)
    }
    localStorage.setItem("look_up_id", look_up_id);
    $("#VIEW_DIV_ID #container input:not(.popup)").each(function () {
        if ($(this).attr('type') == 'CHECKBOX' && $(this).closest('div').attr('id') != 'checkboxes') {
            input_val.push($(this).prop('checked'));
            pop_id.push($(this).attr('id'));
        } else if ($(this).attr('type') != 'checkbox') {
            input_val.push($(this).val());
            pop_id.push($(this).attr('id'));
        }
    });
    $("#VIEW_DIV_ID #container select:not(#select_id)").each(function () {
        input_val.push($(this).children("option:selected").text());
        pop_id.push($(this).attr('id'));
    });
    current_tab_name = $('#carttabs_head li.active a span').text();
    //Get the Tested Object Name code starts..
    if (current_tab_name == 'Approval Chain') {
        Tested_object_name = $('#TSTOBJ_LABEL').val();
        Trackedfield_Tested_object_name = $('#TRKOBJ_NAME').val();
        chain_mappings_approval_object = $('#APROBJ_LABEL').val();
    }
    //To get the classification id from UI
    else if (current_tab_name == 'Quotes' && value_split[0] == 'PRTXCL' && look_up_id == 'SRVTAXCLA_DESCRIPTION') {
        Tested_object_name = $('#SRVTAXCAT_ID').val();
        Trackedfield_Tested_object_name = ''
        chain_mappings_approval_object = ''
    }
    //To get the classification id from UI	
    else {
        Tested_object_name = ''
        Trackedfield_Tested_object_name = ''
        chain_mappings_approval_object = ''
    }
    //Get the Tested Object Name code ends..
    for (var i = 0; i < pop_id.length; i++) {
        assoc[pop_id[i]] = input_val[i];
    }
    localStorage.setItem("assoc_array_value_view", JSON.stringify((assoc)));
    [table, keyData, price_mod_id] = [localStorage.getItem('cont_table_id'), localStorage.getItem('keyData'), ''];
    if (document.getElementById('PRICEMODEL_ID_VALUE')) {
        price_mod_id = document.getElementById('PRICEMODEL_ID_VALUE').value
    }// A043S001P01-12265 Start
    if (document.getElementById('TRKOBJ_NAME')) {
        price_mod_id = document.getElementById('TRKOBJ_NAME').value
    }// A043S001P01-12265 End
    //A043S001P01-11642 Start
    if (look_up_id == 'ATTRIBUTE_NAME' || look_up_id == 'ATTVAL_VALUECODE') {
        var price_mod_id = document.getElementById('ATTRIBUTE_NAME').value
    }
    //A043S001P01-11642 End

    try {
        cpq.server.executeScript("SYCTLKPPUP", { 'TABLEID': value, 'OPER': 'CommonTreeView', 'ATTRIBUTE_NAME': '', 'ATTRIBUTE_VALUE': '', 'GSCONTLOOKUP': '', 'TABLENAME': table, 'PRICE_MOD_ID': price_mod_id, 'KEYDATA': keyData, 'ARRAYVAL': '', 'LOOKUP_ID': look_up_id, 'MAPPINGSAPPROVALOBJECT': chain_mappings_approval_object, 'TESTEDOBJECT': Tested_object_name, 'TRACKEDTESTEDOBJECT': Trackedfield_Tested_object_name }, function (dataset) {
            var [datas, data1, data2, data3] = [dataset[0], dataset[1], dataset[2], dataset[3]];
            if (document.getElementById('VIEW_DIV_ID')) {
                document.getElementById('VIEW_DIV_ID').innerHTML = datas;
                //To bring the lookup popup in front of the Bulk edit popup code starts..
                $('#cont_viewModalSection').css('z-index', '99999')
                //To bring the lookup popup in front of the Bulk edit popup code starts..
            }
            try {
                //A055S000P01-3627 -- start
                if (dataset[6] != "") {
                    $('#' + dataset[2]).attr('data-pagination', 'false');
                    localStorage.setItem('lookup_ids', [table, dataset[2], look_up_id]);
                    $('#popup_footer').html(dataset[6]);
                    total_rec = $('#TotalRecAppCount').text();
                    localStorage.setItem('total_lookup_records', total_rec);
                }
                $('#' + data2).bootstrapTable({ data: data1 });
                //A055S000P01-3627 -- end
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({ data: data1 });
                }, 5000);
            }
            finally { }
            eval(data3);
        });
    } catch (e) {
        console.log(e);
    }
}
function CommonTreePlaceHolder(value, row) {
    ids = row.ids
    return '<a id = "' + ids + '" class="cur_sty" onclick="CommonTree_lookup_popup_onchange(this)">' + value + '</a>';
}
function CommonTreeBackOnclick() {
    $('#cont_viewModalSection').modal('hide');
}
function commonrealtedhyperlink(value, row) {
    active_subtab = $('#COMMON_TABS ul li.active').text().trim();
    if (node.text == "Revisions" || active_subtab == "Annualized Items" || active_subtab == "Items" || node.text.includes('Sales Team')) {
        return value
    }
    else {
        return '<a href="#" onclick="Commonteree_view_RL(this)">' + value + '</a>'
    }
}
function offeringdescriptionhyperlink(value, row) {
    if (node.text == "Revisions") {
        return value
    }
    else {
        return '<a href="#" onclick="">' + value + '</a>'
    }
}
function CommonTree_lookup_popup_onchange(ele) {
    var id_value = $(ele).attr('id');
    var value1 = id_value.split('|');
    var [Apiname, getobj] = [localStorage.getItem("look_up_id"), localStorage.getItem('Lookupobjd')];

    try {
        cpq.server.executeScript("SYPARCEFMA", { 'API_Name': Apiname, 'API_Value': value1[0], 'Object': getobj, 'ACTION': 'UICALL' }, function (dataset) {
            var lookup_clear_fields = [];
            $.each(dataset, function (key, values) {
                lookup_clear_fields.push(values['API_NAME']);
                if (values != '') {
                    $('#TREE_div #container #' + values['API_NAME']).val(values['FORMULA_RESULT']);
                }
                //Binding the value choosed from the lookup popup in the bulk edit code starts..
                if ((value1[1] == 'FAB_LOCATION_RECORD_ID' && Apiname == 'FABLOCATION_ID' && getobj == 'SAQSTE') || (value1[1] == 'TAX_CLASSIFICATION_RECORD_ID' && Apiname == 'SRVTAXCLA_DESCRIPTION' && getobj == 'SAQICO')) {
                    $('#RL_EDIT_DIV_ID #container #' + values['API_NAME']).val(values['FORMULA_RESULT']);
                }
                //Binding the value choosed from the lookup popup in the bulk edit code ends..
            });
            if (localStorage.getItem("CommonTreeParam") == "Receiving Equipment") {
                document.getElementById('FABLOCATION_ID').value = dataset[2]['FORMULA_RESULT']
            }
            localStorage.setItem('lookup_clear_fields', lookup_clear_fields);//to use the API_NAME when clearselection()
            $('#cont_viewModalSection').modal('hide');
            if (getobj == "ACACSA") {
                onFieldChanges();
            }
        });
    } catch (e) {
        console.log(e);
    }
}

//clears the selected value in fablocation popup (Tool relocation)-start
function CommonTree_clear_selection() {
    var popup_id = localStorage.getItem('selected_popup_id');
    $('#cont_viewModalSection').modal('hide');
    $('#' + popup_id).val('');
    var fields = localStorage.getItem('lookup_clear_fields');
    fields = fields.split(',');
    for (let i = 0; i < fields.length; i++) {
        $('#RL_EDIT_DIV_ID #container #' + fields[i]).val('');
    }
}
//clears the selected value in fablocation popup (Tool relocation)-end

/* JIRA-ID : A043S001P01-7076 - Current User Name - Tooltip 'Begin' */
// 8505 jira for Function Activeuser
function activeUser() {
    $('.iconhvr label').each(function (index) {

        var label_txt = $(this).text();
        if (label_txt == 'Last Modified By' || label_txt == 'Added By') {
            var addedby = $(this).closest('.iconhvr').children('div:nth-child(2)').children('input').val();
            var lastmodify = $(this).closest('.iconhvr').children('td:nth-child(3)').children('input').val();
            $(this).closest('.iconhvr').children('div:nth-child(2)').children('input').attr('title', addedby);
            $(this).closest('.iconhvr').children('td:nth-child(3)').children('input').attr('title', lastmodify);
        }
    });
}

function popover() {
    try {
        $('[data-toggle="popover"]').popover();
        $("[data-toggle='popover']").popover({ trigger: 'focus' });
    } catch (err) {
        console.log('error', err);
    }
}

function splitchange(ele) {
    try {
        var [sum, updatesplit] = [0, []];
        var checktrue = "";
        $(".splitclass").each(function () {
            updatesplit.push($(this).val());
            sum += Number($(this).val());
        });

        /*$("#coppart_popup_model tbody tr").each(function () {
            var currentRow = $(this);
            if (currentRow.find("td:nth-child(5)").find("input").val() == "" && checktrue == "") {
                checktrue = 'false';
            }

        });*/

        $("#coppart_popup_model tbody tr td input[id^='Particpantget']").each(function () {
            var value = $(this).val()
            if (!(value)) {
                checktrue = 'false';
                return false;
            }
        });


        if (sum != 100) {
            $('#VIEW_POP_DIV_ID').removeAttr('onclick')
            $('#VIEW_POPUP_MODAL_SECTION .fa-exclamation-triangle').css("display", "");
            $('#VIEW_POPUP_MODAL_SECTION .fa-check-circle-o').css("display", "none");
            $('#VIEW_POPUP_MODAL_SECTION .fa-exclamation-triangle').css("color", "red");
            if (updatesplit.length == 1 && sum == 0) {
                var today = new Date();
                var dd = today.getDate();
                var mm = today.getMonth() + 1; //January is 0!
                var yyyy = today.getFullYear();
                if (dd < 10) {
                    dd = '0' + dd;
                }
                if (mm < 10) {
                    mm = '0' + mm;
                }
                var today = mm + '/' + dd + '/' + yyyy;
                var expireDate = new Date();
                var numOfYears = 1;
                expireDate.setFullYear(expireDate.getFullYear() + numOfYears);
                expireDate.setDate(expireDate.getDate() - 1);
                var date = expireDate.getDate();
                var month = expireDate.getMonth() + 1;
                var year = expireDate.getFullYear();
                $(".datenddate2").val(month + "/" + date + "/" + year);
                $(".datenddate1").val(today);
                $('#VIEW_POPUP_MODAL_SECTION #coppaq_save').removeAttr("disabled");
                $('#VIEW_POPUP_MODAL_SECTION #coppart_Add').removeAttr("disabled");

                if (updatesplit[0] == '') {
                    $('#VIEW_POPUP_MODAL_SECTION #coppaq_save').attr("disabled", "true");
                    $('#VIEW_POPUP_MODAL_SECTION #coppart_Add').attr("disabled", "true");
                }
            }
            else {
                $('#VIEW_POPUP_MODAL_SECTION #coppart_Add').removeAttr("disabled");
                $('#VIEW_POPUP_MODAL_SECTION #coppaq_save').attr("disabled", true);
                var today = new Date();
                var dd = today.getDate();
                var mm = today.getMonth() + 1; //January is 0!
                var yyyy = today.getFullYear();
                if (dd < 10) {
                    dd = '0' + dd;
                }
                if (mm < 10) {
                    mm = '0' + mm;
                }
                var today = mm + '/' + dd + '/' + yyyy;
                var expireDate = new Date();
                var numOfYears = 1;
                expireDate.setFullYear(expireDate.getFullYear() + numOfYears);
                expireDate.setDate(expireDate.getDate() - 1);
                var date = expireDate.getDate();
                var month = expireDate.getMonth() + 1;
                var year = expireDate.getFullYear();
                $(".datenddate1").val(today);
            }
            if (sum > 100) {
                $('#VIEW_POPUP_MODAL_SECTION #coppart_Add').attr("disabled", true);
            }
            if (checktrue == 'false') {
                $('#VIEW_POPUP_MODAL_SECTION .fa-exclamation-triangle').css("display", "inline-block");
                $('#VIEW_POPUP_MODAL_SECTION .fa-check-circle-o').css("display", "none");
                $('#VIEW_POPUP_MODAL_SECTION .fa-exclamation-triangle').css("color", "red");

                $('#VIEW_POPUP_MODAL_SECTION #coppaq_save').attr("disabled", true);
                $('#VIEW_POPUP_MODAL_SECTION #coppart_Add').attr("disabled", true);
            }

        }
        else {
            $('#VIEW_POPUP_MODAL_SECTION .fa-exclamation-triangle').css("display", "none");
            $('#VIEW_POPUP_MODAL_SECTION .fa-check-circle-o').css("display", "");
            $('#VIEW_POPUP_MODAL_SECTION .fa-check-circle-o').css("color", "#0d8a0d");
            var [getsplitdate, data1] = [localStorage.getItem('splitList'), localStorage.getItem('CommonTreedatasetnew')];
            var splitdate = getsplitdate.split(',');
            if (JSON.stringify(updatesplit) != JSON.stringify(splitdate)) {
                var today = new Date();
                var dd = today.getDate();
                var mm = today.getMonth() + 1; //January is 0!
                var yyyy = today.getFullYear();
                if (dd < 10) {
                    dd = '0' + dd;
                }
                if (mm < 10) {
                    mm = '0' + mm;
                }
                var today = mm + '/' + dd + '/' + yyyy;
                $(".datenddate1").val(today);
                //$('#VIEW_POP_DIV_ID').attr('onclick', 'Program_Assign_Refresh()')
                $('#VIEW_POPUP_MODAL_SECTION #coppart_Add').attr("disabled", true);
            }
        }
        // REFRESHING THE POPUP GRID
        //Program_Assign_Refresh()

    }
    catch (e) {
        console.log(e);
    }
}

// RAMESH A043S001P01-7656  ADD NEW ROW FOUNTION START
var Particpantid_list = ParticipantName_list = [];



// RAMESH A043S001P01-7656  SEARCH KEY WORD BOLD  START 
function boldString(str, find) {
    var re = new RegExp(find, 'g');
    return str.replace(re, '<b>' + find + '</b>');
}

// RAMESH A043S001P01-7656  SEARCH KEY WORD BOLD  START 

// RAMESH A043S001P01-7656  SEARCH AUTOCOMPLETE FUNTION START 
function autocomplete(inp, arr) {
    var currentFocus;
    inp.addEventListener("input", function (e) {
        var getsetid = "Particpantid";
        var a, b, i, val = this.value;
        closeAllLists();
        if (!val) { return false; }
        currentFocus = -1;
        a = document.createElement("ul");
        a.setAttribute("id", getsetid + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        this.parentNode.appendChild(a);
        for (i = 0; i < arr.length; i++) {
            if (arr[i].indexOf(val) != -1) {
                b = document.createElement("li");
                b.innerHTML = boldString(arr[i], val);
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                b.addEventListener("click", function (e) {
                    //CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
                    CurrentTab = $("ul#carttabs_head li.active a span").text();

                    inp.value = this.getElementsByTagName("input")[0].value;
                    if (CurrentTab == 'Participant') {
                        //localStorage.setItem('AUTOCOMPLETE_PARTICIPANT','TRUE');
                        inp_val = inp.value
                        try {
                            cpq.server.executeScript("SYPOPUPMOD", {
                                'REC_ID': '',
                                'ACTION': 'PARTICIPANT_ID',
                                'PER_PAGE_FROM': '',
                                'PER_PAGE_TO': '',
                                'participant_id': inp_val,
                            }, function (datas) {
                                data3 = datas[2]


                            });
                        } catch (err) {
                            console.log(err)
                        }
                    }
                    var intval = Particpantid_list.indexOf(inp.value)
                    var ParticipantName = ParticipantName_list[intval]

                    var createid = '#' + inp.id
                    $(createid).val(inp.value)
                    var [sum, updatesplit] = [0, []];
                    var checktrue = "";
                    $(".splitclass").each(function () {
                        updatesplit.push($(this).val());
                        sum += Number($(this).val());
                    });

                    $("#coppart_popup_model tbody tr").each(function () {
                        var currentRow = $(this);
                        if (currentRow.find("td:eq(2)").find("input").val() == "" && checktrue == "") {
                            checktrue = 'false';

                        }

                    });

                    if (checktrue == "" && sum == 100) {
                        $('#VIEW_POPUP_MODAL_SECTION #coppaq_save').removeAttr("disabled");
                        $('#VIEW_POPUP_MODAL_SECTION #coppart_Add').attr("disabled", true);
                    }
                    else if (checktrue == "" && sum != 100) {
                        $('#VIEW_POPUP_MODAL_SECTION #coppart_Add').removeAttr("disabled");
                        $('#VIEW_POPUP_MODAL_SECTION #coppaq_save').attr("disabled", true);
                    }


                    if (CurrentTab == 'Program') {
                        if (ParticipantName != '' || ParticipantName != 'undefined' || ParticipantName != null) {
                            $(createid).closest('tr').children('td:nth-child(6)').text(ParticipantName)
                            split_val = $(createid).closest('tr').find("td:nth-child(10) input").val()
                            sum = 0
                            $(".splitclass").each(function () {
                                sum += Number($(this).val());
                            });
                            if ((split_val) && (sum != 100) && (!(sum > 100))) {
                                $("#coppart_Add").removeAttr("disabled");
                            } else {
                                $("#coppart_Add").attr("disabled", "true");
                            }
                            if (inp.value == "0000000000") {
                                var lastChar = createid[createid.length - 1];
                                var createcheckid = '#checkboxhouse' + lastChar
                                $(createcheckid).prop("checked", true);

                            }

                            else {
                                var lastChar = createid[createid.length - 1];
                                var createcheckid = '#checkboxhouse' + lastChar
                                $(createcheckid).prop("checked", false);
                            }


                        }

                        else {
                            $(createid).closest('tr').children('td:nth-child(4)').text('')
                            var lastChar = createid[createid.length - 1];
                            var createcheckid = '#checkboxhouse' + lastChar
                            $(createcheckid).prop("checked", false);
                        }

                    } else if (CurrentTab == 'Participant') {
                        if (ParticipantName != '' || ParticipantName != 'undefined' || ParticipantName != null) {
                            $(createid).closest('tr').children('td:nth-child(8)').text(ParticipantName)
                        }

                        else {
                            $(createid).closest('tr').children('td:nth-child(8)').text('')
                        }
                        setTimeout(function () {
                            if (data3 != null && data3 != '' && data3 == 'True') {
                                $(createid).parent().next().next().children().prop('checked', true);
                            }
                            else {
                                $(createid).parent().next().next().children().prop('checked', false);
                            }

                        }, 2000)


                    }
                    closeAllLists();
                });
                a.appendChild(b);
                //localStorage.setItem('AUTOCOMPLETE_PARTICIPANT','');
            }
        }
    });
    inp.addEventListener("keydown", function (e) {
        var getsetid = "Particpantid";
        var x = document.getElementById(getsetid + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(x);
        } else if (e.keyCode == 38) {

            currentFocus--;
            addActive(x);
        } else if (e.keyCode == 13) {
            e.preventDefault();
            if (currentFocus > -1) {
                if (x) x[currentFocus].click();
            }
        }
    });
    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }
    function closeAllLists(elmnt) {
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}

function chckbx_clck() {
    $('#VIEW_POP_DIV_ID').removeAttr('onclick')
    try {
        setTimeout(function () {
            cpq.server.executeScript("SYPOPUPMOD", {
                'REC_ID': '',
                'ACTION': 'PRODUCT_LOAD',
                'PER_PAGE_FROM': '',
                'PER_PAGE_TO': ''

            }, function (datas) {
                data = datas[0]
                data1 = datas[1]
                data2 = datas[2]
                data3 = datas[3]
                data4 = datas[4]
                data5 = datas[5]
                data6 = datas[6]
                data7 = datas[7]
                data8 = datas[8]
                data9 = datas[9]
                data10 = datas[10]


                if (data == 'true') {
                    $('#cont_viewPupupModal').hide();
                    //localStorage.setItem("COMM_END_DATE_REQUIRED","FALSE");
                }
                else {
                    //localStorage.setItem("COMM_END_DATE_REQUIRED","TRUE");
                    //$('#datePick9670').find('.req-field').css('display','block');
                    $('#cont_viewPupupModal').show();
                    if (document.getElementById('VIEW_POP_DIV_ID')) {
                        document.getElementById('VIEW_POP_DIV_ID').innerHTML = data1;
                        try {
                            $('#' + data2).bootstrapTable({
                                data: data3,
                            });

                            if (document.getElementById('SELECT_DIV')) {
                                var s = document.getElementById("SELECT_DIV");

                                if (document.getElementsByClassName('bs-checkbox')) {
                                    var h = document.getElementsByClassName("bs-checkbox")[0].children[0]

                                    h.insertAdjacentElement("beforebegin", s);
                                }
                            }

                            MAX = localStorage.getItem('MAXIMISED')
                            if (MAX) {
                                $('#restore').css('cssText', 'display : none !important');
                                $('#restore_back').css('cssText', 'display : block !important');
                                $('#restore').parent().parent().parent().parent().parent().parent().css('cssText', 'margin-top:5% !important;width:99% !important');
                                $('#restore').parent().parent().parent().parent().parent().css('cssText', 'height:130% !important');
                                $('table#coppart_popup_model tbody').css('cssText', 'max-height:50vh !important')
                            }

                        } catch (err) {
                            setTimeout(function () {
                                $('#' + data2).bootstrapTable({
                                    data: data3,
                                });
                                if (document.getElementById('SELECT_DIV')) {
                                    var s = document.getElementById("SELECT_DIV");

                                    if (document.getElementsByClassName('bs-checkbox')) {
                                        var h = document.getElementsByClassName("bs-checkbox")[0].children[0]

                                        h.insertAdjacentElement("beforebegin", s);
                                    }
                                }

                            }, 5000);
                            MAX = localStorage.getItem('MAXIMISED')
                            if (MAX) {
                                $('#restore').css('cssText', 'display : none !important');
                                $('#restore_back').css('cssText', 'display : block !important');
                                $('#restore').parent().parent().parent().parent().parent().parent().css('cssText', 'margin-top:5% !important;width:99% !important');
                                $('#restore').parent().parent().parent().parent().parent().css('cssText', 'height:130% !important');
                                $('table#coppart_popup_model tbody').css('cssText', 'max-height:50vh !important')
                            }
                        }

                        finally {
                            $('#' + data2).after(data5);
                            try {
                                eval(data6); eval(datas[7]); eval(data10);
                            } catch (err) {
                                console.log(err);
                            }
                        }
                        //$('#' + data2).after(data5);
                        setTimeout(function () {
                            if (data2) {
                                $("table#coppart_popup_model").colResizable({ disable: true });
                                $("table#" + data2).colResizable({ disable: true });
                                //$("table#" + data2).colResizable({ liveDrag: true });
                            }

                        }, 3000);
                        $("table#coppart_popup_model").colResizable({ disable: true });
                    }

                }
            });
        }, 1000);
    } catch (e) {
    }
}

function selectedval(ele) {
    val = $(ele).attr('id');
    var list = [];
    var value = ['SYSEFL_PB_00431', 'SYSEFL_PB_01919'];
    value.forEach((k, i) => { if (val == 'SYSEFL_PB_01935') { $('.options_' + k).text('') }; console.log(k) });
    $(".options_" + val + " option:selected").each(function () {
        if ((localStorage.getItem('selected_items_' + val) + '').indexOf($(this).text()) <= 0 || $(this).text() == "PRICEBOOK") {
            $("#options1_" + val).append('<option value="' + $(this).text() + '">' + $(this).text() + '</option>' + "\n");
            list.push($(this).text());
        }
    });
    $(".options_" + val + " option").filter(function () {
        return $.inArray(this.value, list) !== -1
    }).remove();
    value.forEach((k, i) => {
        if (val == 'SYSEFL_PB_01935') {
            $("#options1_SYSEFL_PB_01935 option").each(function () {
                if ($('#options1_' + k + ' option[value="' + $(this).val() + '"]').length == 0 && $(this).val() != '') {
                    $('.options_' + k).append('<option value="' + $(this).val() + '">' + $(this).val() + '</option>' + "\n")
                    $(".options1_" + k + " option").filter(function () {
                        return ($(this).val().trim() == "" && $(this).text().trim() == "");
                    }).remove();
                    $(".options_" + val + " option").filter(function () {
                        return ($(this).val().trim() == "" && $(this).text().trim() == "");
                    }).remove();
                }
            });
        }
    });
    localStorage.setItem('selected_items_' + val, $("#options1_" + val).text().trim().split("\n"));
    $(".options_" + val + " option").filter(function () {
        return ($(this).val().trim() == "" && $(this).text().trim() == "");
    }).remove();
    $("#options1_" + val + " option").filter(function () {
        return ($(this).val().trim() == "" && $(this).text().trim() == "");
    }).remove();
}

function unselectedval(ele) {
    val = $(ele).attr('id');
    var value = ['SYSEFL_PB_00431', 'SYSEFL_PB_01919'];
    value.forEach((k, i) => { if (val == 'SYSEFL_PB_01935') { }; console.log(k) });
    $("#options1_" + val + " option:selected").each(function () {
        if (val == 'SYSEFL_PB_01935') {
            value.forEach((k, i) => {
                $("#options1_" + val + " option:selected").each(function () {
                    $("#options1_" + k + " option[value=\"" + $(this).text() + "\"]").remove();
                    $(".options_" + k + " option[value=\"" + $(this).text() + "\"]").remove();
                });
            });
        }
        //$(".options1").remove( '<option value="'+$(this).text()+'">'+$(this).text()+'</option>');
        $("#options1_" + val + " option[value=\"" + $(this).text() + "\"]").remove();
        $(".options_" + val).append('<option value="' + $(this).text() + '">' + $(this).text() + '</option>' + "\n");
        //$('#my-select').multiselect('refresh');
        /*$.each($(".options1").text().trim().split("/n"),function(){
            console.log(value);items =value + ","
        });
    localStorage.setItem('selected_items',items);*/
    });

    $(".options_" + val + " option").filter(function () {
        return ($(this).val().trim() == "" && $(this).text().trim() == "");
    }).remove();

    $("#options1_" + val + " option").filter(function () {
        return ($(this).val().trim() == "" && $(this).text().trim() == "");
    }).remove();
    localStorage.setItem('selected_items_' + val, $("#options1_" + val).text().trim().split("\n"));
}
function topselect(ele) {
    val = $(ele).attr('id');
    $("#options1_" + val + " option:selected:first-child").prop("selected", false);
    before = $("#options1_" + val + " option:selected:first").prev();
    $("#options1_" + val + " option:selected").detach().insertBefore(before);
}
function btmselect(ele) {
    val = $(ele).attr('id');
    var op = $("#options1_" + val + " option:selected");
    op.last().next().after(op);
    // $("#options1_"+val+" option:selected:last-child").prop("selected", false);
    // after = $("#options1_"+val+" option:selected:last").next();
    // $("#options1_"+val+" option:selected").detach().insertAfter(after);
}

function chckbx_clck_SAVE() {
    $('#VIEW_POP_DIV_ID').removeAttr('onclick')
    try {
        cpq.server.executeScript("SYPOPUPMOD", {
            'REC_ID': '',
            'ACTION': 'PRODUCT_LOAD',
            'PER_PAGE_FROM': '',
            'PER_PAGE_TO': ''

        }, function (datas) {
            data = datas[0]
            data1 = datas[1]
            data2 = datas[2]
            data3 = datas[3]
            data4 = datas[4]
            data5 = datas[5]
            data6 = datas[6]
            data7 = datas[7]
            data8 = datas[8]
            data9 = datas[9]
            data10 = datas[10]


            if (data == 'true') {
                $('#cont_viewPupupModal').hide();
                //localStorage.setItem("COMM_END_DATE_REQUIRED","FALSE");
            }
            else {
                //localStorage.setItem("COMM_END_DATE_REQUIRED","TRUE");
                //$('#datePick9670').find('.req-field').css('display','block');
                $('#cont_viewPupupModal').show();
                if (document.getElementById('VIEW_POP_DIV_ID')) {
                    document.getElementById('VIEW_POP_DIV_ID').innerHTML = data1;
                    try {
                        $('#' + data2).bootstrapTable({
                            data: data3,
                        });

                        if (document.getElementById('SELECT_DIV')) {
                            var s = document.getElementById("SELECT_DIV");

                            if (document.getElementsByClassName('bs-checkbox')) {
                                var h = document.getElementsByClassName("bs-checkbox")[0].children[0]

                                h.insertAdjacentElement("beforebegin", s);
                            }
                        }

                    } catch (err) {
                        setTimeout(function () {
                            $('#' + data2).bootstrapTable({
                                data: data3,
                            });
                            if (document.getElementById('SELECT_DIV')) {
                                var s = document.getElementById("SELECT_DIV");

                                if (document.getElementsByClassName('bs-checkbox')) {
                                    var h = document.getElementsByClassName("bs-checkbox")[0].children[0]

                                    h.insertAdjacentElement("beforebegin", s);
                                }
                            }

                        }, 5000);
                    }

                    finally {
                        $('#' + data2).after(data5);
                        try {
                            eval(data6); eval(datas[7]); eval(data10);
                        } catch (err) {
                            console.log(err);
                        }
                    }
                    //$('#' + data2).after(data5);
                    setTimeout(function () {
                        if (data2) {
                            $("table#" + data2).colResizable({ disable: true });
                            $("table#" + data2).colResizable({ liveDrag: true });
                        }

                    }, 2000);
                }
            }
        });
    } catch (e) {
        console.log(e);
    }

}

function No_Records() {
    setTimeout(function () {
        Rec = localStorage.getItem('NO_RECORDS')

        localStorage.setItem('NO_RECORDS', '')
        if (Rec != 'FALSE') {
            $('#VIEW_POP_DIV_ID').removeAttr('onclick');

            $('.noRecord').remove();
            $('.tab-content').css('display', 'none');
            $('#ass_icon1').css('display', 'none');
            $('#ass_icon2').css('display', 'none');
            //$('#assignment_tab').css('padding','7px 10px')	
            $('.tab-content').before("<div class='noRecord mrg_tp10'>No Records to Display</div>")
        } else {
            $('.noRecord').remove();
            //$('#assignment_tab').css('padding','2px 10px')
            $('.tab-content').css('display', 'block');
        }
    }, 200)

}




function cont_DeleteAss(ele) {
    $('#VIEW_POP_DIV_ID').removeAttr('onclick');
    DISABLE_SAVE = false
    localStorage.setItem('PARTI_DELETE_EXEC', 'TRUE')
    participantId = $(ele).attr('id');
    //Participant_ID_dict = Participant_Name_dict = Participant_Split_Percentage_Dict = House_Participant_Dict = {}
    $('#coppart_popup_model_ass tbody tr td:nth-child(7) input').each(function () {
        Participant_ID_dict[$(this).attr('id')] = $(this).val()
        Participant_Name_dict[$(this).attr('id')] = $(this).parent().next().text()
        Participant_Split_Percentage_Dict[$(this).closest('tr').find('.copart_split').attr('id')] = $(this).closest('tr').find('.copart_split').val()
        House_Participant_Dict[$(this).attr('id')] = $(this).parent().next().next().children().is(":checked")
    });

    cpq.server.executeScript("SYPOPUPMOD", {
        'REC_ID': participantId,
        'ACTION': 'PARTICIPANT_DELETE',
        'PER_PAGE_FROM': '',
        'PER_PAGE_TO': '',

    }, function (datas) {
        data0 = datas[0]
        data1 = datas[1]

        $('#' + data0).bootstrapTable('removeAll');
        $('#' + data0).bootstrapTable({ data: data1 });
        $('#coppart_popup_model_ass').bootstrapTable('load', data1);

        var val = 0;

        Particpantid_list_Loc_str_Parsed = JSON.parse(localStorage.getItem("Particpantid_list_Loc_str"));
        for (var key in Participant_ID_dict) {
            var value = Participant_ID_dict[key];
            if (document.getElementById(key)) {
                autocomplete(document.getElementById(key), Particpantid_list_Loc_str_Parsed);
            }
            $('#' + key).val(value)
        }
        for (var key in Participant_Name_dict) {
            var value = Participant_Name_dict[key];
            $('#' + key).parent().next().text(value)
        }
        for (var key in House_Participant_Dict) {
            var value = House_Participant_Dict[key];
            if (value == true) {
                $('#' + key).parent().next().next().children().prop('checked', true)
            } else {
                $('#' + key).parent().next().next().children().prop('checked', false)
            }
        }

        // SPLIT PERCENTAGE CALCULATION ISSUE.

        /*for (var key in Participant_Split_Percentage_Dict){
            var value = Participant_Split_Percentage_Dict[key];
            console.log('key***key',key);
            console.log('value***value',value);
            $('#'+key).val(value)
        }*/

        //console.log("val",val)
        start_val = document.getElementById('coppart_popup_model_ass_NumberofItem').split(' ')[0]
        table_row_cnt = $('table#coppart_popup_model_ass tbody').find('tr').length
        $('#coppart_popup_model_ass_totalItemCount').text(table_row_cnt)
        counter_value = $('#coppart_popup_model_ass_PageCountValue').val()
        var all_tr = document.querySelectorAll("table#coppart_popup_model_ass tbody.coppart_body tr");
        if (table_row_cnt > counter_value) {
            for (i = start_val; i < counter_value; i++) {
                all_tr[i].removeAttribute("style");
            }
        }
        else {
            for (i = start_val; i < table_row_cnt; i++) {
                all_tr[i].removeAttribute("style");
            }
        }

        $(".copart_split").each(function () {
            val += Number($(this).val());
        });

        $('#coppart_popup_model_ass tbody tr td:nth-child(7) input').each(function () {
            Participant_ID = $(this).val()
            if (Participant_ID != '' && Participant_ID != null && Participant_ID != undefined) {
                DISABLE_SAVE = false
            } else {
                DISABLE_SAVE = true
            }
        });

        copart_split_val = val
        if (copart_split_val > 100) {
            $('#coppart_Add_pop').css('display', 'none');
            $('#coppart_Save_pop').css('display', 'none');
            $('#ass_icon1').css('display', 'none')
            $('#ass_icon2').css('display', 'block')
        } else if ((copart_split_val) < 100 && (DISABLE_SAVE == false)) {
            $('#coppart_Add_pop').css('display', 'block');
            $('#coppart_Save_pop').css('display', 'none');
            $('#ass_icon1').css('display', 'none')
            $('#ass_icon2').css('display', 'block')
        } else if ((copart_split_val == 100) && (DISABLE_SAVE == false)) {
            $('#coppart_Add_pop').css('display', 'none');
            $('#coppart_Save_pop').css('display', 'block');
            $('#ass_icon1').css('display', 'block')
            $('#ass_icon2').css('display', 'none')
        } else if ((copart_split_val == 100) && (DISABLE_SAVE == true)) {
            $('#coppart_Add_pop').css('display', 'none');
            $('#coppart_Save_pop').css('display', 'none');
            $('#ass_icon1').css('display', 'none')
            $('#ass_icon2').css('display', 'block')
        } else {
            $('#coppart_Add_pop').css('display', 'none');
            $('#coppart_Save_pop').css('display', 'none');
            $('#ass_icon1').css('display', 'none')
            $('#ass_icon2').css('display', 'block')
        }

    });
}

function assignment_pagination_change(table_id) {
    //table_id = "coppart_popup_model_ass"

    start_val = parseInt(document.getElementById(table_id + "_NumberofItem").innerHTML.split('-')[0].trim())
    table_row_cnt = $("table#" + table_id + " tbody").find('tr').length
    counter_value = $('#' + table_id + '_PageCountValue').val()
    $('#' + table_id + '_totalItemCount').text(table_row_cnt)
    current_tab_name = $('#carttabs_head li.active a span').text();

    $('table tbody.coppart_body tr').css('display', 'none');
    var all_tr = document.querySelectorAll("table#" + table_id + " tbody tr");

    NumberofItem = document.getElementById(table_id + "_NumberofItem").innerHTML

    a = NumberofItem.split(' ')[0]
    b = NumberofItem.split(' ')[2]

    if (!(a == '') && !(b == '')) {
        updated_count = parseInt(a) + parseInt(parseInt(counter_value) - 1)

        if (updated_count > table_row_cnt) {
            updated_count = table_row_cnt
        }

        document.getElementById(table_id + "_NumberofItem").innerHTML = a + " - " + updated_count + " of "
        if (table_row_cnt > counter_value) {
            for (i = start_val - 1; i < updated_count; i++) {
                all_tr[i].removeAttribute("style");
            }
        }
        else {
            for (i = start_val; i < table_row_cnt; i++) {
                all_tr[i].removeAttribute("style");
            }
        }
    }

}
function assignment_pagination_first(table_id) {
    //table_id = "coppart_popup_model_ass"

    current_tab_name = $('#carttabs_head li.active a span').text();
    var totalItemCount = document.getElementById(table_id + "_totalItemCount").innerHTML;
    var page_count = document.getElementById(table_id + "_page_count").innerHTML;
    var PerPage = $("#" + table_id + "_PageCountValue").val();
    total_rows_count = $('table#' + table_id + ' tbody').find('tr').length
    if (parseInt(page_count) > 1) {
        var a = 1;
        var b = parseInt(a) * parseInt(PerPage);
        document.getElementById(table_id + "_page_count").innerHTML = parseInt(1);
        document.getElementById(table_id + "_NumberofItem").innerHTML = a + ' - ' + b + ' of ';
        document.getElementsByName(table_id + "_totalItemCount").innerHTML = total_rows_count
        $('table#' + table_id + ' tbody tr').css('display', 'none');
        var all_tr = document.querySelectorAll("table#" + table_id + " tbody tr");

        for (i = 0; i < PerPage; i++) {
            all_tr[i].removeAttribute("style");
        }
    }
}
function assignment_pagination_last(table_id) {

    //table_id = "coppart_popup_model_ass"
    current_tab_name = $('#carttabs_head li.active a span').text();
    total_rows_count = $('table#' + table_id + ' tbody').find('tr').length
    var totalItemCount = document.getElementById(table_id + "_totalItemCount").innerHTML;
    var page_count = document.getElementById(table_id + "_page_count").innerHTML;
    var PerPage = $("#" + table_id + "_PageCountValue").val();
    var page_count = parseInt(totalItemCount) / parseInt(PerPage);
    if (page_count.toString().indexOf('.') != -1) {
        page_count = parseInt(page_count) + 1;
    }
    if (parseInt(page_count) > 1) {
        var Firstrecord = ((parseInt(page_count) - 1) * parseInt(PerPage)) + 1
    } else {
        Firstrecord = 1
    }
    var Lastrecord = parseInt(PerPage) * parseInt(page_count)
    document.getElementById(table_id + "_page_count").innerHTML = page_count;
    document.getElementById(table_id + "_NumberofItem").innerHTML = Firstrecord + ' - ' + total_rows_count + ' of ';

    $('table#' + table_id + ' tbody tr').css('display', 'none');
    var all_tr = document.querySelectorAll("table#" + table_id + " tbody tr");

    for (i = Firstrecord - 1; i < total_rows_count; i++) {
        all_tr[i].removeAttribute("style");
    }

}
function assignment_pagination_previous(table_id) {

    //table_id = 'coppart_popup_model_ass'
    current_tab_name = $('#carttabs_head li.active a span').text();
    totalItemCount = document.getElementById(table_id + "_totalItemCount").innerHTML
    page_count = document.getElementById(table_id + "_page_count").innerHTML
    PerPage = $("#" + table_id + "_PageCountValue").val();

    if (parseInt(page_count) > 1) {
        $('table#' + table_id + ' tbody tr').css('display', 'none');
        var all_tr = document.querySelectorAll("table#" + table_id + "  tbody tr");

        page_count = parseInt(page_count) - 1
        b = parseInt(page_count) * parseInt(PerPage)
        if (parseInt(page_count) == 1) {
            a = 1
        } else {
            a = ((page_count - 1) * parseInt(PerPage)) + 1
        }

        document.getElementById(table_id + "_page_count").innerHTML = parseInt(page_count)
        document.getElementById(table_id + "_NumberofItem").innerHTML = a + ' - ' + b + ' of '

        for (i = a - 1; i < b; i++) {
            all_tr[i].removeAttribute("style");
        }

    }
}
function assignment_pagination_Next(table_id) {
    current_tab_name = $('#carttabs_head li.active a span').text();
    totalItemCount = document.getElementById(table_id + "_totalItemCount").innerHTML
    page_count = document.getElementById(table_id + "_page_count").innerHTML
    PerPage = $("#" + table_id + "_PageCountValue").val();
    NumberofItem = document.getElementById(table_id + "_NumberofItem").innerHTML
    a1 = page_count * PerPage
    a = a1 + 1
    c = parseInt(page_count) + 1
    b = c * parseInt(PerPage)

    validation = parseInt(totalItemCount) / parseInt(PerPage)
    validation_1 = parseInt(validation) + 1
    if (page_count < validation_1) {
        $('table#' + table_id + ' tbody tr').css('display', 'none');
        var all_tr = document.querySelectorAll("table#" + table_id + " tbody tr");

        document.getElementById(table_id + "_page_count").innerHTML = parseInt(page_count) + 1
        if (b > totalItemCount) {
            if (document.getElementById(table_id + "_NumberofItem")) {
                document.getElementById(table_id + "_NumberofItem").innerHTML = a + ' - ' + totalItemCount + ' of '
            }
            for (i = a - 1; i < totalItemCount; i++) {
                all_tr[i].removeAttribute("style");
            }
        } else {
            if (document.getElementById(table_id + "_NumberofItem")) {
                document.getElementById(table_id + "_NumberofItem").innerHTML = a + ' - ' + b + ' of '
            }

            for (i = a - 1; i < b; i++) {
                all_tr[i].removeAttribute("style");
            }
        }
    }
}

// JANARTHANI PARTICIPANT POPUP ENDS.

function breadCrumb_redirection(ele) {
    $(".involvedparties_Details").click();
}


function tree_breadCrumb_redirection(leftNode, parent_node) {
    var left_text = $(leftNode).text();
    var left_parent_text = $(leftNode).closest('li').prev('li').text();
    var first_text = $("#header_label  ul li:nth-child(1)").text();
    TreeParentParam = localStorage.getItem('CommonTreeParentParam');
    CurrentNodeId = localStorage.getItem('CurrentNodeId')
    var parent_found = false;
    $('ul.list-group li.list-group-item.node-commontreeview').each(function (index) {
        var nodeText = $(this).text();
        if (nodeText == first_text && first_text == left_text) {
            $(this).trigger('click');
        }
        else {
            if (nodeText == left_parent_text) {
                parent_found = true;
            }
            if (nodeText == left_text && parent_found == true) {
                $(this).trigger('click');
            }
        }
        if (TreeParam == "Quote Information") {
            if (nodeText == "Quote Information") {
                CommonRightView(0);
            }
        }
    });

    if (localStorage.getItem('CommonTreeParam') == left_text) {
        CommonRightView(CurrentNodeId);
    }
    if (Action == 'ADD NEW') {
        $('ul.breadcrumb').append('<li><a onclick="breadCrumb_redirection(this)"><abbr title="ADD NEW">ADD NEW</abbr></a><span class="angle_symbol"><img src="/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>');
    }

}


function Common_Tabs(ele, Name) {
    $('#Newrevision1').hide()
    $('#Completesowbtn').hide()
    TreeParam = localStorage.getItem('CommonTreeParam');
    TreeParentParam = localStorage.getItem('CommonTreeParentParam');
    TreeSuperParentParam = localStorage.getItem('CommonNodeTreeSuperParentParam');
    CurrentRecordId = node.id;
    ObjName = node.objname;
    SubNode_text = $(ele).text().trim();
    //currentTabName = $('div#attributesContainer .row.tabsfiled .tabsmenu ul#carttabs_head li.active').text().trim();
    current_tab_name = $('#carttabs_head li.active a span').text();

    /*var getnotifymsg = localStorage.getItem('getbannermessage');
    if (getnotifymsg == "bannerNotify"){
    	
        var getdata = localStorage.getItem('getbannerdetail');
        $(".emp_notifiy").css('display','block');
                                            $(".emp_notifiy").html(getdata)
    }*/

    if (Name == 'Prc_Mthd_Factors' || Name == 'Prc_Mthd_Entries') {
        if (Name == 'Prc_Mthd_Factors') {
            localStorage.setItem('Load_action', 'FCTR_VIEW');
        }
        else {
            $('#Prc_Mthd_Entries').css('display', 'block');
            localStorage.setItem('Load_action', '');
        }
        subtabs_load();
    }
    $('#' + localStorage.getItem('cont_table_id')).remove(); //to remove add new button in subaner after subtab change in involved parties
    $('#COMMON_TABS').css('display', 'block')
    if (Name == 'Detail') {
        common_Detail_Subtab()
    } else if (Name == 'Related') {
        common_Related_Subtab()
    } else if (Name == 'Sub_category_Detail' || Name == 'Sub_category_Related') {
        if (Name == 'Sub_category_Detail') {
            $('.CommonTreeDetail').css("display", "block")
            $("#div_CTR_Sub_Categories").closest('.Related').css("display", "none")
            Common_enable_disable();
        }
        else if (Name == 'Sub_category_Related') {
            $('.CommonTreeDetail').css("display", "none")
            $("#div_CTR_Sub_Categories").closest('.Related').css("display", "block")
            RecName = 'div_CTR_Sub_Categories'
            loadRelatedList("SYOBJR-30009", RecName);
        }

    } else if (Name == 'Service Fab Details') {
        fab_details();
        ObjName = 'SAQSFB';
        $('.CommonTreeDetail').css('display', 'block');
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
        setTimeout(function () {
            Subbaner("Details", CurrentNodeId, CurrentRecordId, 'SAQSFB');
        }, 4000);
        //$('table#table_covered_obj_parent').css('display', 'none');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            //commented to check the secondary banner
            //Subbaner(CurrentNodeId,CurrentRecordId,'SAQSFB');
            //onFieldChanges();
        });

    }
    else if (Name == 'SegRevPricebookset Enteries') {
        $('.CommonTreeDetail').css("display", "none")
        $("#div_CTR_Segment_Pricebook_Entries").closest('.Related').css("display", "block")
    }

    else if (Name == 'SegRevPricebookset Details') {
        $('.CommonTreeDetail').css("display", "block")
        $("#div_CTR_Segment_Pricebook_Entries").closest('.Related').css("display", "none")
    }
    else if (Name == 'SegRevApprCond Details') {
        $('.CommonTreeDetail').css("display", "block")
        $("#div_CTR_Approval_Processes").closest('.Related').css("display", "none")
    }
    else if (Name == 'SegRevApprCond Workflow Rules') {
        $('.CommonTreeDetail').css("display", "none")
        $("#div_CTR_Approval_Processes").closest('.Related').css("display", "block")
    }
    else if (Name == 'DetailAppLevel') {
        $('.CommonTreeDetail').css("display", "block");
        $("#div_CTR_Tab_Field_Settings").closest('.Related').css('display', 'none');
    }
    else if (Name == 'RelatedAppLevel') {
        $('.CommonTreeDetail').css("display", "none");
        $("#div_CTR_Tab_Field_Settings").closest('.Related').css('display', 'block');
    }
    else if (Name == 'DetailSecLevel') {
        $('.CommonTreeDetail').css("display", "block");
        $("#div_CTR_Section_Field_Settings").closest('.Related').css('display', 'none');
    }
    else if (Name == 'RelatedSecLevel') {
        $('.CommonTreeDetail').css("display", "none");
        $("#div_CTR_Section_Field_Settings").closest('.Related').css('display', 'block');
    }
    else if (Name == 'DetailTabLevel') {
        $('.CommonTreeDetail').css("display", "block");
        $("#div_CTR_Section_Field_Settings").closest('.Related').css('display', 'none');
    }
    else if (Name == 'RelatedTabLevel') {
        $('.CommonTreeDetail').css("display", "none");
        $("#div_CTR_Section_Field_Settings").closest('.Related').css('display', 'block');
    }
    else if (Name == 'DetailObjLevel') {
        $('.CommonTreeDetail').css("display", "block");
        $("#div_CTR_Field_Settings").closest('.Related').css('display', 'none');
    }
    else if (Name == 'RelatedObjLevel') {
        $('.CommonTreeDetail').css("display", "none");
        $("#div_CTR_Field_Settings").closest('.Related').css('display', 'block');
    }
    else if (Name == 'SegRevApprRule Details') {
        $('.CommonTreeDetail').css("display", "block")
        $("#div_CTR_Segment_Pricebook_Entries").closest('.Related').css("display", "none")
    }
    else if (Name == 'SegRevApprRule Approvers') {
        $('.CommonTreeDetail').css("display", "none")
        $('.container_banner_inner_sec').hide()
        $("#div_CTR_Segment_Pricebook_Entries").closest('.Related').css("display", "block")
    }
    else if (Name == 'SegRevApprRule violations') {
        $('.CommonTreeDetail').css("display", "block")
        $("#div_CTR_Segment_Pricebook_Entries").closest('.Related').css("display", "none")
    }
    else if (Name == 'SegRevApprRuleLvl Details') {
        $('.CommonTreeDetail').css("display", "block")
        $("#div_CTR_Segment_Pricebook_Entries").closest('.Related').css("display", "none")
    }
    else if (Name == 'SegRevApprRuleLvl Approvers') {
        $('.CommonTreeDetail').css("display", "none")
        $('.container_banner_inner_sec').hide()
        $("#div_CTR_Segment_Pricebook_Entries").closest('.Related').css("display", "block")
    }
    // A043S001P01-10455 End
    // A043S001P01-10899 Start
    else if (Name == 'ApprovalChain detail') {
        $('.CommonTreeDetail').css("display", "block")
        $("#div_CTR_Approval_Chain_Steps").closest('.Related').css("display", "none")
        $("#div_CTR_Segment_Pricebook_Entries").closest('.Related').css("display", "none");
    }
    else if (Name == 'Approvalchain steps') {
        $('.CommonTreeDetail').css("display", "none")
        $('.container_banner_inner_sec').hide()
        $("#div_CTR_Approval_Chain_Steps").closest('.Related').css("display", "block")
    }
    else if (Name == 'Approvalchain violations') {
        $('.CommonTreeDetail').css("display", "none")
        $('.container_banner_inner_sec').hide()
        $("#div_CTR_Approval_Chain_Steps").closest('.Related').css("display", "none")
        $("#div_CTR_Segment_Pricebook_Entries").closest('.Related').css("display", "block");
    }
    else if (Name == 'Quote_Information') {
        breadCrumb_Reset();
        $('.Detail').css("display", "none")
        $('#div_CTR_quote_prevw').css("display", "none")
        $("#div_CTR_related_list").closest('.Related').css("display", "none");
        //$("#div_CTR_Opportunity").closest('.Related').css("display", "none");
        //$('#div_CTR_Involved_Parties').css("display", "none")
        $('.3CB361DE-C513-4CA6-97A8-59C8D4F82D52').css("display", "none")
        $('.4A378C65-AFF4-44EC-A334-24DF86398F90').css("display", "none")
        //$("#div_CTR_Source_Fab_Locations").closest('.Related').css("display", "none");
        localStorage.setItem('subatab_name', 'Details')
        localStorage.setItem('currentSubTabtriggerpopup', "Details");
        keyDataVal = localStorage.getItem('keyDataVal')
        quote_id = $(".segment_part_number_text").text()
        cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'QUOTE_INFO', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal }, function (data0) {
            if (data0 != '') {
                //$('.CommonTreeDetail').css('display', 'none');
                $('.container_banner_inner_sec').css("display", "none")
                $('#TREE_div').html(data0);
                // if($('#CANCELLATION_PERIOD').val()!="MANUAL INPUT"){
                // 	$('#CANCELLATION_PERIOD_NOTPER').closest('div').parent('div').parent('div').css('display','none');
                // }
                $(".CommonTreeDetail").css("display", "block");
                $("#TREE_div").css("display", "block");
                $("#div_CTR_related_list").hide();
                var rev_field = $('#key_field_id').val();
                localStorage.setItem('rev_field', rev_field);
                var getopptype = $("#DOCTYP_ID").val();
                localStorage.setItem("getopptype", getopptype)
                //QuoteStatus()
                dynamic_status();
                //$('.HideAddNew').remove();
                // $('#HideSavecancel').remove()
                // $("#div_CTR_Opportunity").closest('.Related').css("display", "block");
                // $('[data-toggle="popover"]').popover();
            }
        });

    }
    else if (Name == 'Contract_Information') {
        breadCrumb_Reset();
        $('.Detail').css("display", "none")
        $('#div_CTR_quote_prevw').css("display", "none")
        $("#div_CTR_related_list").closest('.Related').css("display", "none");
        //$("#div_CTR_Opportunity").closest('.Related').css("display", "none");
        //$('#div_CTR_Involved_Parties').css("display", "none")
        $('.3CB361DE-C513-4CA6-97A8-59C8D4F82D52').css("display", "none")
        $('.4A378C65-AFF4-44EC-A334-24DF86398F90').css("display", "none")
        //$("#div_CTR_Source_Fab_Locations").closest('.Related').css("display", "none");
        keyDataVal = localStorage.getItem('keyDataVal')
        quote_id = $(".segment_part_number_text").text()
        cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'CONTRACT_INFO', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal }, function (data0) {
            if (data0 != '') {
                //$('.CommonTreeDetail').css('display', 'none');
                $('.container_banner_inner_sec').css("display", "none")
                $('#TREE_div').html(data0);
                $(".CommonTreeDetail").css("display", "block");
                $("#TREE_div").css("display", "block");
                $("#div_CTR_related_list").hide();
                //$('.HideAddNew').remove();
                // $('#HideSavecancel').remove()
                // $("#div_CTR_Opportunity").closest('.Related').css("display", "block");
                // $('[data-toggle="popover"]').popover();
            }
        });

    }
    else if (Name == 'Equipment Entitlements') {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
        // && (CommonNodeTreeSuperParentParam == 'Comprehensive Services' || CommonNodeTreeSuperParentParam == 'Complementary Products')
        if (CurrentTab == "Quote" || CurrentTab == "Quotes") {
            ObjName = 'SAQTSE';
        }
        else {
            ObjName = 'CTCTSE';
        }
        /*var getnotifymsg = localStorage.getItem('getbannermessage');
        if (getnotifymsg == "bannerNotify"){
        	
            var getdata = localStorage.getItem('getbannerdetail');
            $(".emp_notifiy").css('display','block');
            $(".emp_notifiy").html(getdata)
        }*/
        $('.CommonTreeDetail').css('display', 'block');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data12, data13, data14, data15, data16, data17, data18, data19, data20, data21, data22, data23, data24, data25, data26, data27, data28, data29, data30, data31, data32, data33, data34, data35, data36, data37, data38, data39] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[6], dataset[7], dataset[8], dataset[9], dataset[10], dataset[11], dataset[12], dataset[13], dataset[14], dataset[15], dataset[16], dataset[17], dataset[18], dataset[19], dataset[20], dataset[21], dataset[22], dataset[23], dataset[24], dataset[25], dataset[26], dataset[27], dataset[28], dataset[29], dataset[30], dataset[31], dataset[32], dataset[33], dataset[34], dataset[35], dataset[36], dataset[37], dataset[38], dataset[39]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                //document.getElementById("TREE_div").innerHTML = datas;
                document.getElementById('TREE_div').innerHTML = data7



                $.each(data8, function (k, v) {


                    $.each(v, function (index2, value2) {
                        ctid = 'sec_' + index2
                        //Hide the section , if the section does not nave attributes to show code starts....
                        if (data38.includes(ctid)) {

                            $('#' + ctid).css('display', 'none');
                            $('#' + index2).css('display', 'none');
                        }
                        //Hide the section , if the section does not nave attributes to show code ends...


                        $('#' + index2).bootstrapTable({
                            data: value2
                        });
                        $("#" + index2 + "  tbody tr td:nth-child(2)").css('text-align', 'left');
                        $("#" + index2 + "  tbody tr td:nth-child(2)").each(function () { var ent_desc = $(this).text(); $(this).html(ent_desc); });
                        $("#" + index2 + "  tbody tr td:nth-child(3)").each(function () { var ent_val = $(this).text(); $(this).html(ent_val); });
                        $("#" + index2 + "  tbody tr td:nth-child(4)").each(function () { var data_typrval = $(this).text(); $(this).html(data_typrval); });
                        $("#" + index2 + "  tbody tr td:nth-child(1)").each(function () { var ent_val_im = $(this).text(); $(this).html(ent_val_im); });
                        $("#" + index2 + "  tbody tr td:nth-child(6)").each(function () { var factcurr = $(this).text(); $(this).html(factcurr); });
                        $("#" + index2 + "  tbody tr td:nth-child(5)").each(function () { var ent_val_cf = $(this).text(); $(this).html(ent_val_cf); });
                        $("#" + index2 + "  tbody tr td:nth-child(7)").each(function () { var ent_val_imp = $(this).text(); $(this).html(ent_val_imp); });
                        $("#" + index2 + "  tbody tr td:nth-child(8)").each(function () { var ent_val_primp = $(this).text(); $(this).html(ent_val_primp); });
                        if (data15 === undefined || data15 == null) { data15 = "" }
                        if (data16 === undefined || data16 == null) { data16 = "" }
                        if (data17 === undefined || data17 == null) { data17 = "" }
                        if (data18 === undefined || data18 == null) { data18 = "" }
                        if (data19 === undefined || data19 == null) { data19 = "" }
                        if (data20 === undefined || data20 == null) { data20 = "" }
                        if (data21 === undefined || data21 == null) { data21 = "" }
                        if (data23 === undefined || data23 == null) { data23 = "" }
                        if (data24 === undefined || data24 == null) { data24 = "" }
                        if (data22 === undefined || data22 == null) { data22 = "" }
                        if (data26 === undefined || data26 == null) { data22 = "" }
                        if (data27 === undefined || data27 == null) { data27 = "" }
                        if (data28 === undefined || data28 == null) { data28 = "" }
                        if (data29 === undefined || data29 == null) { data29 = "" }
                        if (data30 === undefined || data30 == null) { data30 = "" }
                        if (data31 === undefined || data31 == null) { data31 = "" }
                        if (data32 === undefined || data32 == null) { data32 = "" }
                        if (data33 === undefined || data33 == null) { data33 = "" }
                        if (data34 === undefined || data34 == null) { data34 = "" }
                        if (data35 === undefined || data35 == null) { data35 = "" }
                        if (data36 === undefined || data36 == null) { data36 = "" }
                        var deinstall = $('#INSTALLATION_LABOR_Z_07').val();
                        if (index2 == '2F6D3B86-2B8E-4C0B-80F5-C2926BD322C9' && deinstall == 'Included') {
                            $("#\\32 F6D3B86-2B8E-4C0B-80F5-C2926BD322C9 tbody  tr:nth-child(2)").after('<tr data-index="5" id="labtype" class="hovergreyent"><td style=""></td><td style="text-align: left;">T3 Labor Type</td><td style=""><select class="form-control cust_hover remove_yellow no_border_bg" style="" id="T3_LABOR_TYPE" type="text" data-content="T3_LABOR_TYPE" onclick="editent_bt(this)" disabled=""><option id = "PSE" value="PSE">PSE</option><option id="CE" value="CE" selected="">CE</option></select></td><td style=""><input class="form-control cust_hover_lock" style="" id="T3_LABOR_TYPE_dt" type="text" disabled="" value="' + data26 + '"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover_lock" style="" id="T3_LABOR_TYPE" type="text" disabled="" value="USD"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T3_LABOR_TYPE_calc" type="number" value="' + data36 + '" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T3_LABOR_TYPE_imt" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T3_LABOR_TYPE_primp" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td></tr>')
                            $("#\\32 F6D3B86-2B8E-4C0B-80F5-C2926BD322C9 tbody  tr:nth-child(2)").after('<tr data-index="5" id="labtype1" class="hovergreyent"><td style=""></td><td style="text-align: left;">T3 Labor</td><td style=""><select class="form-control cust_hover remove_yellow no_border_bg" style="" id="T3_LABOR" type="text" data-content="T3_LABOR" onclick="editent_bt(this)" disabled=""><option id="Excluded" value="Excluded">Excluded</option><option id="Included" value="Included" selected="">Included</option></select></td><td style=""><input class="form-control cust_hover_lock" style="" id="T3_LABOR_dt" type="text" disabled="" value="' + data28 + '"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover_lock" style="" id="T3_LABOR" type="text" disabled="" value=""><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover_lock" style="" id="T3_LABOR_calc" type="number" value="' + data35 + '" disabled="disabled"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T3_LABOR_imt" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T3_LABOR_primp" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td></tr>')
                            $("#\\32 F6D3B86-2B8E-4C0B-80F5-C2926BD322C9 tbody  tr:nth-child(2)").after('<tr data-index="5" id="labtype2" class="hovergreyent"><td style=""></td><td style="text-align: left;">T2 Labor Type</td><td style=""><select class="form-control cust_hover remove_yellow no_border_bg" style="" id="T2_LABOR_TYPE" type="text" data-content="T2_LABOR_TYPE" onclick="editent_bt(this)" disabled=""><option id="PSE" value="PSE">PSE</option><option id="CE" value="CE" selected="">CE</option></select></td><td style=""><input class="form-control cust_hover_lock" style="" id="T2_LABOR_TYPE_dt" type="text" disabled="" value="' + data22 + '"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover_lock" style="" id="T2_LABOR_TYPE" type="text" disabled="" value="USD"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T2_LABOR_TYPE_calc" type="number" value="' + data34 + '" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T2_LABOR_TYPE_imt" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T2_LABOR_TYPE_primp" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td></tr>')
                            $("#\\32 F6D3B86-2B8E-4C0B-80F5-C2926BD322C9 tbody  tr:nth-child(2)").after('<tr data-index="5" id="labtype3" class="hovergreyent"><td style=""></td><td style="text-align: left;">T2 Labor</td><td style=""><select class="form-control cust_hover remove_yellow no_border_bg" style="" id="T2_LABOR" type="text" data-content="T2_LABOR" onclick="editent_bt(this)" disabled=""><option id="Excluded" value="Excluded">Excluded</option><option id="Included" value="Included" selected="">Included</option></select></td><td style=""><input class="form-control cust_hover_lock" style="" id="T2_LABOR_dt" type="text" disabled="" value="' + data23 + '"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover_lock" style="" id="T2_LABOR" type="text" disabled="" value=""><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover_lock" style="" id="T2_LABOR_calc" type="number" value="' + data33 + '" disabled="disabled"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T2_LABOR_imt" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T2_LABOR_primp" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td></tr>')
                            $("#\\32 F6D3B86-2B8E-4C0B-80F5-C2926BD322C9 tbody  tr:nth-child(2)").after('<tr data-index="5" id="labtype4" class="hovergreyent"><td style=""></td><td style="text-align: left;">T0/T1 Labor Type</td><td style=""><select class="form-control cust_hover remove_yellow no_border_bg" style="" id="T0_T1_LABOR_TYPE" type="text" data-content="T0_T1_LABOR_TYPE" onclick="editent_bt(this)" disabled=""><option id="Technician_or_3rd_Party" value="Technician or 3rd Party">Technician or 3rd Party</option><option id="CE" value="CE" selected="">CE</option></select></td><td style=""><input class="form-control cust_hover_lock" style="" id="T0_T1_LABOR_TYPE_dt" type="text" disabled="" value="' + data29 + '"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover_lock" style="" id="T0_T1_LABOR_TYPE" type="text" disabled="" value="USD"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T0_T1_LABOR_TYPE_calc" type="number" value="' + data32 + '" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T0_T1_LABOR_TYPE_imt" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T0_T1_LABOR_TYPE_primp" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td></tr>')
                            $("#\\32 F6D3B86-2B8E-4C0B-80F5-C2926BD322C9 tbody  tr:nth-child(2)").after('<tr data-index="4" id="labtype5" class="hovergreyent"><td style=""></td><td style="text-align: left;">T0/T1 Labor</td><td style=""><select class="form-control cust_hover remove_yellow no_border_bg" style="" id="T0_T1_LABOR" type="text" data-content="T0_T1 Labor" onclick="editent_bt(this)" disabled=""><option value="Excluded">Excluded</option><option id="Included" value="Included" selected="">Included</option></select></td><td style=""><input class="form-control cust_hover_lock" style="" id="T0_T1_LABOR_dt" type="text" disabled="" value="' + data21 + '"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover_lock" style="" id="T0_T1_LABOR" type="text" disabled="" value=""><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover_lock" style="" id="T0_T1_LABOR_calc" type="number" value="' + data31 + '" disabled="disabled"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T0_T1_LABOR_imt" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="T0_T1_LABOR_primp" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td></tr>')
                            $("#\\32 F6D3B86-2B8E-4C0B-80F5-C2926BD322C9 tbody  tr:nth-child(2)").after('<tr data-index="3" id="labtype6" class="hovergreyent"><td style=""></td><td style="text-align: left;">Labor Type</td><td style=""><select class="form-control cust_hover remove_yellow no_border_bg" style="" id="LABOR_TYPE" type="text" data-content="labor Type" onclick="editent_bt(this)" disabled=""><option id="Technician_or_3rd_Party" value="Technician or 3rd Party">Technician or 3rd Party</option><option id="CE" value="CE" selected="">CE</option></select></td><td style=""><input class="form-control cust_hover_lock" style="" id="LABOR_TYPE_dt" type="text" disabled="" value="NUMBER"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover_lock" style="" id="LABOR_TYPE" type="text" disabled="" value="USD"><i class="fa fa-lock cust_hover_lock_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="LABOR_TYPE_calc" type="number" value="' + data30 + '" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="LABOR_TYPE_imt" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td><td style=""><input class="form-control cust_hover" style="" id="LABOR_TYPE_primp" type="text" value="" disabled=""><i class="fa fa-pencil cust_hover_icon" aria-hidden="true" style="display: none;"></i></td></tr>')

                            $('#labtype').dblclick(function () {
                                $('#LABOR_TYPE').removeAttr('disabled'); $('#T0_T1_LABOR').removeAttr('disabled'); $('#T0_T1_LABOR_TYPE').removeAttr('disabled'); $('#T2_LABOR').removeAttr('disabled'); $('#T2_LABOR_TYPE').removeAttr('disabled'); $('#T3_LABOR').removeAttr('disabled'); $('#T3_LABOR_TYPE').removeAttr('disabled'); $('#T3_LABOR_TYPE_calc').removeAttr('disabled'); $('#T2_LABOR_TYPE_calc').removeAttr('disabled'); $('#T0_T1_LABOR_TYPE_calc').removeAttr('disabled'); $('#LABOR_TYPE_calc').removeAttr('disabled'); $('#entsave').css('display', 'block');
                                $('#entcancel').css('display', 'block');
                            });

                            $('#labtype1').dblclick(function () {
                                $('#LABOR_TYPE').removeAttr('disabled');
                                $('#T0_T1_LABOR').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE').removeAttr('disabled');
                                $('#T2_LABOR').removeAttr('disabled');
                                $('#T2_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR').removeAttr('disabled');
                                $('#T3_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T2_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#LABOR_TYPE_calc').removeAttr('disabled');
                                $('#entsave').css('display', 'block');
                                $('#entcancel').css('display', 'block');

                            });
                            $('#labtype2').dblclick(function () {
                                $('#LABOR_TYPE').removeAttr('disabled');
                                $('#T0_T1_LABOR').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE').removeAttr('disabled');
                                $('#T2_LABOR').removeAttr('disabled');
                                $('#T2_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR').removeAttr('disabled');
                                $('#T3_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T2_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#LABOR_TYPE_calc').removeAttr('disabled');
                                $('#entsave').css('display', 'block');
                                $('#entcancel').css('display', 'block');

                            });

                            $('#labtype3').dblclick(function () {
                                $('#LABOR_TYPE').removeAttr('disabled');
                                $('#T0_T1_LABOR').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE').removeAttr('disabled');
                                $('#T2_LABOR').removeAttr('disabled');
                                $('#T2_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR').removeAttr('disabled');
                                $('#T3_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T2_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#LABOR_TYPE_calc').removeAttr('disabled');
                                $('#entsave').css('display', 'block');
                                $('#entcancel').css('display', 'block');

                            });

                            $('#labtype4').dblclick(function () {
                                $('#LABOR_TYPE').removeAttr('disabled');
                                $('#T0_T1_LABOR').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE').removeAttr('disabled');
                                $('#T2_LABOR').removeAttr('disabled');
                                $('#T2_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR').removeAttr('disabled');
                                $('#T3_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T2_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#LABOR_TYPE_calc').removeAttr('disabled');
                                $('#entsave').css('display', 'block');
                                $('#entcancel').css('display', 'block');
                            });
                            $('#labtype5').dblclick(function () {
                                $('#LABOR_TYPE').removeAttr('disabled');
                                $('#T0_T1_LABOR').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE').removeAttr('disabled');
                                $('#T2_LABOR').removeAttr('disabled');
                                $('#T2_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR').removeAttr('disabled');
                                $('#T3_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T2_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#LABOR_TYPE_calc').removeAttr('disabled');
                                $('#entsave').css('display', 'block');
                                $('#entcancel').css('display', 'block');
                            });
                            $('#labtype6').dblclick(function () {
                                $('#LABOR_TYPE').removeAttr('disabled');
                                $('#T0_T1_LABOR').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE').removeAttr('disabled');
                                $('#T2_LABOR').removeAttr('disabled');
                                $('#T2_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR').removeAttr('disabled');
                                $('#T3_LABOR_TYPE').removeAttr('disabled');
                                $('#T3_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T2_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#T0_T1_LABOR_TYPE_calc').removeAttr('disabled');
                                $('#LABOR_TYPE_calc').removeAttr('disabled');
                                $('#entsave').css('display', 'block');
                                $('#entcancel').css('display', 'block');
                            });
                        }

                    });

                });

                if (data39 != "" && data39 != undefined) {
                    arr_list = data39

                    for (const [key, value] of Object.entries(arr_list)) {
                        if (value != "") {
                            defaultText = value
                        }
                        else {
                            defaultText = 'Select Below'
                        }
                        $("#" + key).CreateMultiCheckBox({ width: '230px', defaultText: defaultText, height: '250px', attr_id: key });
                        $('#' + key).closest('td').attr('title', defaultText);
                    };

                }

                $.each(data11, function (index, value) {

                    $("#" + value).closest('tr').css('display', 'none');
                });
                if (data13 != '' && data13 != null) {
                    $.each(data13, function (index, value) {
                        $('#' + value).css('color', '#0060B1');
                    });
                }
                try {
                    eval(data9)
                    eval(data37)
                    if ($('#approve_status').text() == "APPROVALS") { eval(data9) }
                    var getdataprevent = eval(data10)

                } catch { console.log('error---') }
                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                popover()
            }
            onFieldChanges();
        });

    } else if (Name == 'Equipment Details' && (CommonTopSuperParentParam == 'Comprehensive Services' || TreeSuperTopParentParam == 'Complementary Products' || CommonTopSuperParentParam == 'Complementary Products' || CommonTopSuperParentParam == 'Product Offerings') && currenttab.indexOf('Quotes') != -1) {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
        equipment_serialnumber = localStorage.getItem("coveredobject_equipment_serial_number")
        if (AllTreeParam['TreeParentLevel1'] == "Sending Equipment") {
            ObjName = 'SAQSSE';
        }
        else {
            ObjName = 'SAQSCO';
        }
        $("div_CTR_related_list").css("display", "none");
        $('.CommonTreeDetail').css('display', 'block');
        $('#div_CTR_related_list').css('display', 'none');
        $('table#table_covered_obj_parent').css('display', 'none');
        /*var getnotifymsg = localStorage.getItem('getbannermessage');
        if (getnotifymsg == "bannerNotify"){
        	
            var getdata = localStorage.getItem('getbannerdetail');
            $(".emp_notifiy").css('display','block');
            $(".emp_notifiy").html(getdata)
        }*/
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
            $('div#COMMON_TABS').find("li a:contains('Equipment Entitlements')").parent().css("display", "block");
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            breadCrumb_Reset();
            Pmevents_breadcrumb(equipment_serialnumber)
            var nobreadCrumb_Reset = true
            onFieldChanges();
            if (TreeParam == 'Z0007_AG' || TreeParam == 'Z0007') {
                $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "block");
            }
            else {
                $(".BCF901C7-ACD1-42F0-B3DD-E78A3D1AA134").css("display", "none");
            }
        });
        try {
            cpq.server.executeScript("CQCRUDOPTN", {
                'Opertion': 'GET',
                'ActionType': 'SHOW_PRICING_BENCHMARKING_NOTIFICATION',
                'NodeType': 'QUOTE LEVEL NOTIFICATION'
            }, function (data) {
                if (data != "") {

                    if (data[0] != "" || data[1] != "") {

                        $(".emp_notifiy").css('display', 'block');
                        $("#PageAlert ").css('display', 'block');
                        $("#alertnotify").html(data);
                    }
                }

            });
        }
        catch { console.log('===error price bench mark notification') }
    } else if (Name == 'Equipment Details' && CommonNodeTreeSuperParentParam == 'Comprehensive Services' && currenttab.indexOf('Contracts') != -1) {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
        Values = localStorage.getItem("EquipmentSerialNumber")

        ObjName = 'CTCSCO';
        $('#div_CTR_related_list').hide();
        $('.CommonTreeDetail').css('display', 'block');
        //$('table#table_covered_obj_parent').css('display', 'none');
        //$('#div_CTR_related_list').css('display', 'none');
        /*var getnotifymsg = localStorage.getItem('getbannermessage');
        if (getnotifymsg == "bannerNotify"){
        	
            var getdata = localStorage.getItem('getbannerdetail');
            $(".emp_notifiy").css('display','block');
            $(".emp_notifiy").html(getdata)
        }*/
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            $('#div_CTR_related_list').hide();
            $("#TREE_div").show();
            breadCrumb_Reset();
            //Pmevents_breadcrumb(Values)
            onFieldChanges();
        });
    }//A055S000P01-17070 code starts.. ends...
    else if (Name == 'Sending_Account_Details' && TreeParam == 'Customer Information') {
        CurrentRecordId = localStorage.getItem('account_details_hyperlink')
        Values = localStorage.getItem("EquipmentSerialNumber")

        ObjName = 'SAQTIP';
        $('.CommonTreeDetail').css('display', 'block');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            $('#div_CTR_related_list').hide();
            $("#TREE_div").show();
            breadCrumb_Reset();
            account_id = localStorage.getItem("account_id")
            fts_breadcrumb(account_id)
        });
    } else if (Name == 'Sending_Fab_Location_Details' && TreeParam == 'Customer Information') {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
        Values = localStorage.getItem("EquipmentSerialNumber")

        ObjName = 'SAQSAF';
        $('.CommonTreeDetail').css('display', 'block');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            $('#div_CTR_related_list').hide();
            $("#TREE_div").show();
            breadCrumb_Reset();
            account_id = localStorage.getItem("account_id")
            fts_breadcrumb(account_id)
            tool_breadcrumb()
        });
    }
    else if (Name == 'Receiving_Fab_Location_Details' && TreeParam == 'Customer Information') {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
        ObjName = 'SAQFBL';
        $('.CommonTreeDetail').css('display', 'block');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            $('#div_CTR_related_list').hide();
            $("#TREE_div").show();
            breadCrumb_Reset();
            account_id = localStorage.getItem("account_id")
            fts_breadcrumb(account_id)
            tool_breadcrumb()
        });
    }
    else if (Name == 'Equipment Details' && currenttab == "Contracts" && CommonNodeTreeSuperParentParam == 'Comprehensive Services') {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");

        ObjName = 'CTCSCO';
        $('.CommonTreeDetail').css('display', 'block');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            onFieldChanges();
        });
    }
    else if (Name == 'Spare Part Details') {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");

        ObjName = 'SAQSPT';
        $('.CommonTreeDetail').css('display', 'block');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            onFieldChanges();
        });
    }
    else if (Name == 'Equipment_Details' && currenttab.indexOf('Quotes') != -1) {
        /*var getnotifymsg = localStorage.getItem('getbannermessage');
            if (getnotifymsg == "bannerNotify"){
            	
                var getdata = localStorage.getItem('getbannerdetail');
                $(".emp_notifiy").css('display','block');
                $(".emp_notifiy").html(getdata)
            }*/
        CurrentRecordId = localStorage.getItem("CurrentRecordId");

        ObjName = 'SAQICO';
        $('.CommonTreeDetail').css('display', 'block');
        $("#div_CTR_related_list").css('display', 'none');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {

            var [datas, data1, data2, data3, data4, data5, data7] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[7]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            onFieldChanges();
        });
    }
    else if (Name == 'Offerings_Assembly_Details' && currenttab.indexOf('Quotes') != -1) {
        Values = localStorage.getItem("EquipmentSerialNumber")
        Assembly_Id = localStorage.getItem("AssemblyIdValue")
        CurrentRecordId = localStorage.getItem("CurrentRecordId");

        ObjName = 'SAQSCA';
        $('.CommonTreeDetail').css('display', 'block');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {

            var [datas, data1, data2, data3, data4, data5, data7] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[7]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            onFieldChanges();
            //Calling the breadcrumb functionality
            breadCrumb_Reset();
            Pmevents_breadcrumb(Values);
            Pmevents_breadcrumb(Assembly_Id);
            $("#div_CTR_related_list").css("display", "none");
            //Calling the breadcrumb functionality
            //commented to check the secondary banner
            //Subbaner(CurrentNodeId, CurrentRecordId, ObjName);
        });
    }
    else if (Name == 'Equipment_Details' && currenttab == "Contracts") {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");

        ObjName = 'CTCICO';
        $('.CommonTreeDetail').css('display', 'block');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            onFieldChanges();
        });
    }
    else if (Name == 'Spare_parts_details') {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");

        ObjName = 'SAQIFP';
        $('.CommonTreeDetail').css('display', 'block');
        /*var getnotifymsg = localStorage.getItem('getbannermessage');
        if (getnotifymsg == "bannerNotify"){
        	
            var getdata = localStorage.getItem('getbannerdetail');
            $(".emp_notifiy").css('display','block');
            $(".emp_notifiy").html(getdata)
        }*/
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            Subbaner('Spare Part Details', CurrentNodeId, CurrentRecordId, 'SAQIFP');
        });
    }
    else if (Name == 'addon_details') {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");

        ObjName = 'SAQSGB';
        $('.CommonTreeDetail').css('display', 'block');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            if (document.getElementById("TREE_div")) {
                document.getElementById("TREE_div").innerHTML = datas;
                popover()
            }
            // Subbaner('Spare Part Details',CurrentNodeId, CurrentRecordId, 'SAQIFP');
        });
    }
    else if (Name == 'Equipment Details' && TreeSuperParentParam != "Product Offerings" && currenttab.indexOf('Quotes') != -1) {
        //CurrentRecordId = localStorage.getItem("CurrentRecordId");
        if (TreeSuperParentParam == "Sending Equipment") {
            CurrentRecordId = localStorage.getItem("CurrentRecordIdEQUIP")

            ObjName = 'SAQSSE';
            $("#div_CTR_related_list").css("display", "none");
            $('.CommonTreeDetail').css('display', 'block');
            /*var getnotifymsg = localStorage.getItem('getbannermessage');
            if (getnotifymsg == "bannerNotify"){
            	
                var getdata = localStorage.getItem('getbannerdetail');
                $(".emp_notifiy").css('display','block');
                $(".emp_notifiy").html(getdata)
            }*/
            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                var [datas, data1, data2, data3, data4, data5, data7] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[7]];
                localStorage.setItem('Lookupobjd', data5)
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                }
                onFieldChanges();
            });
            //commented to check the secondary banner
            //Subbaner(CurrentNodeId, CurrentRecordId, "SAQFEQ")
        }
        else {
            CurrentRecordId = localStorage.getItem("CurrentRecordIdEQUIP")

            ObjName = 'SAQFEQ';
            $("#div_CTR_related_list").css("display", "none");
            $('.CommonTreeDetail').css('display', 'block');
            /*var getnotifymsg = localStorage.getItem('getbannermessage');
            if (getnotifymsg == "bannerNotify"){
            	
                var getdata = localStorage.getItem('getbannerdetail');
                $(".emp_notifiy").css('display','block');
                $(".emp_notifiy").html(getdata)
            }*/
            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                var [datas, data1, data2, data3, data4, data5, data7] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5], dataset[7]];
                localStorage.setItem('Lookupobjd', data5)
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                }
                onFieldChanges();
            });
        }
    }
    else if (Name == 'Equipment Details' && CurrentTab == "Contracts") {
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
        $("#div_CTR_related_list").css("display", "none")
        ObjName = 'CTCFEQ';
        $('.CommonTreeDetail').css('display', 'block');
        cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'ObjName': ObjName, 'AllTreeParams': AllTreeParams, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
            var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
            localStorage.setItem('Lookupobjd', data5)
            //commented to check the secondary banner
            //Subbaner(CurrentNodeId, CurrentRecordId, data5);
            if (document.getElementById("TREE_div")) {

                document.getElementById("TREE_div").innerHTML = datas;
                // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                popover()
            }
            onFieldChanges();
        });
    }




    else if (Name == 'DetailOpportunity') {
        breadCrumb_Reset();
        $('.Detail').css("display", "none")
        $('.container_banner_inner_sec').css("display", "none")
        $('#conta2936').css("display", "none")
        $('#div_CTR_related_list').css("display", "none")
        //$("#div_CTR_Source_Fab_Locations").closest('.Related').css("display", "none");
        $('#conta2002').css("display", "none")
        $('#conta2939').css("display", "block")
        $('#conta2511').css("display", "block")
        //$("#div_CTR_Value_driver").closest('.Related').css("display", "none");
        //$("#div_CTR_Opportunity").css("display", "block");
        $('#container2511').css('cssText', 'margin-top : 0px !important');
        $('#container2939').css('cssText', 'margin-top : 0px !important');
        localStorage.setItem('currentSubTabtriggerpopup', "Opportunity");
        record_id = CurrentRecordId
        keyDataVal = localStorage.getItem('keyDataVal')
        quote_id = $(".segment_part_number_text").text()
        cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'OPPORTUNITY_VIEW', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal, 'AllTreeParam': AllTreeParam }, function (data0) {
            if (data0 != '') {
                $('.CommonTreeDetail').css('display', 'none');
                $('.container_banner_inner_sec').css("display", "none")
                $('#TREE_div').html(data0);
                $('.HideAddNew').remove();
                $('#HideSavecancel').remove()
                $("#TREE_div").closest('.Related').css("display", "block");
                $('[data-toggle="popover"]').popover();
            }
        });
        $("#TREE_div").css("display", "block");
        var subTabText = "Opportunity";
        chainsteps_breadcrumb(subTabText);
    }
    else if (Name == 'DetailLegalSow') {
        breadCrumb_Reset();
        //$('#Newrevision1').css('display','block')
        $('.Detail').css("display", "none")
        $('.container_banner_inner_sec').css("display", "none")
        $('#conta2936').css("display", "none")
        $('#div_CTR_related_list').css("display", "none")
        //$("#div_CTR_Source_Fab_Locations").closest('.Related').css("display", "none");
        $('#conta2002').css("display", "none")
        $('#conta2939').css("display", "block")
        $('#conta2511').css("display", "block")
        //$("#div_CTR_Value_driver").closest('.Related').css("display", "none");
        //$("#div_CTR_Opportunity").css("display", "block");
        $('#container2511').css('cssText', 'margin-top : 0px !important');
        $('#container2939').css('cssText', 'margin-top : 0px !important');
        localStorage.setItem('currentSubTab', "Legal SoW");
        localStorage.setItem('currentSubTabtriggerpopup', "Legal SoW");
        record_id = CurrentRecordId
        keyDataVal = localStorage.getItem('keyDataVal')
        quote_id = $(".segment_part_number_text").text()
        rev_status = $(".segment_revision_sale_id_text").text()
        cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'LEGALSOW_VIEW', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal, 'AllTreeParam': AllTreeParam }, function (data0) {
            if (data0 != '') {
                $('.CommonTreeDetail').css('display', 'none');
                $('.container_banner_inner_sec').css("display", "none")
                $('#TREE_div').html(data0);
                $('.HideAddNew').remove();
                $('#HideSavecancel').remove()
                $("#TREE_div").closest('.Related').css("display", "block");
                $('[data-toggle="popover"]').popover();
                dynamic_status();
            }
        });
        $("#TREE_div").css("display", "block");
        var subTabText = "Legal SoW";
        chainsteps_breadcrumb(subTabText);
        //QuoteStatus()
    }
    else if (Name == 'Detail_clean_booking_list') {
        breadCrumb_Reset();
        $('.Detail').css("display", "none")
        $('.container_banner_inner_sec').css("display", "none")
        $('#div_CTR_related_list').css("display", "none")
        record_id = CurrentRecordId
        keyDataVal = localStorage.getItem('keyDataVal')
        quote_id = $(".segment_part_number_text").text()
        localStorage.setItem('currentSubTabtriggerpopup', "Clean Booking Checklist");
        cpq.server.executeScript("CQPREVWDTL", { 'ACTION': 'CBC_VIEW', 'QUOTE_ID': quote_id, 'QT_REC_ID': keyDataVal, 'AllTreeParam': AllTreeParam }, function (data0) {
            if (data0 != '') {
                $('.CommonTreeDetail').css('display', 'none');
                $('.container_banner_inner_sec').css("display", "none")
                $('#TREE_div').html(data0);
                $("#cbc_notes").append('<div class="note_CBC"><p>NOTE:Credit limit check is performed by SAP, whereby completion of the contract booking is based on the adequate customer credit limits or GC&C exception approval. <br>Always review special or unusual circumstances with the AGS Revenue Manager (Kenneth Ho)</p><p>Service Contract Specialist Review:</p></div>');
                $('.HideAddNew').remove();
                $('#HideSavecancel').remove()
                $("#TREE_div").closest('.Related').css("display", "block");
                $('[data-toggle="popover"]').popover();
            }
        });
        $("#TREE_div").css("display", "block");
        var subTabText = "Clean Booking Checklist";
        chainsteps_breadcrumb(subTabText);
    }

    else if (Name == 'Involved_Parties') {
        breadCrumb_Reset();
        $('.Detail').css("display", "none")
        $('.container_banner_inner_sec').css("display", "none");
        $('#TREE_div').css("display", "none")
        $('#conta2939').css("display", "none")
        $("#div_CTR_related_list").css("display", "block")
        $("#div_CTR_Involved_Parties").closest('.Related').css("display", "block");
        localStorage.setItem('currentSubTab', "Involved Parties");

        if (TreeParam == "Contract Information") {
            RecId = "SYOBJR-98825";
            RecName = "div_CTR_Involved_Parties"
        }
        loadRelatedList(RecId, RecName)

        $('.Involved_Parties').css("display", "block");
        $('.common_opportunity').css('display', 'block');
        $('.common_legalsow').css('display', 'block');
        localStorage.setItem("page_type", "OBJECT PAGE LISTGRID")
        if (TreeParam != "Contract Information") {
            Subbaner('Involved Parties', CurrentNodeId, CurrentRecordId, 'SAQTIP');
        }
        var subTabText = "Involved Parties";
        localStorage.setItem('currentSubTab', subTabText);
        breadCrumb_Reset();
        chainsteps_breadcrumb(subTabText);
    }
    else if (Name == 'SourceFabLocation') {
        breadCrumb_Reset();
        localStorage.setItem("page_type", "OBJECT PAGE LISTGRID")
        localStorage.setItem('srcfab_details', 'false');
        $('.Detail').css("display", "none")
        $('.involvedparties_Details ').show();
        $('.SourceFabLocation').show();
        $('#div_CTR_Tool_Relocation_Matrix').closest('.Related').css("display", "none")
        $("#div_CTR_Source_Fab_Locations").css("display", "block");
        $('#div_CTR_Involved_Parties').css("display", "none")
        $("#div_CTR_Value_driver").closest('.Related').css("display", "none");
        $("#div_CTR_Opportunity").css("display", "none");
        $('#TREE_div').css('display', 'none');
        $('#div_CTR_Equipments').css('display', 'none');
        $('#div_CTR_Involved_Parties_Equipments').css('display', 'none');
        $('#ADDNEW__SYOBJR_98858_SYOBJ_01034').hide()
        $('div#COMMON_TABS').find("li a:contains('Source Fab Locations')").parent().css("display", "block");
        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
        var sale_type = localStorage.getItem("saletype");
        if (sale_type == "NEW" || Saletype == "CONTRACT RENEWAL") {
            $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().css("display", "none");
        }
        else {
            $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().css("display", "block");
        }
        RecId = 'SYOBJR-98857';
        RecName = "div_CTR_Source_Fab_Locations"
        loadRelatedList(RecId, RecName)
        $('.container_banner_inner_sec').css("display", "none");
        $("#div_CTR_Source_Fab_Locations").closest('.Related').css("display", "block");
        //CurrentRecordId = $('#QSTN_SYSEFL_QT_00001').attr('title');
        CurrentRecordId = localStorage.getItem("masterquoteRecId");
        Subbaner('Source Fab Location', CurrentNodeId, RecId, 'SAQSCF');
        ObjectName = "SAQSCF";
        subTabText = localStorage.getItem('currentSubTab');
        chainsteps_breadcrumb(subTabText);
        subtab = localStorage.getItem('sourcefab');
        //chainsteps_breadcrumb(subtab);
        localStorage.setItem('CurrentRecordId', subtab);
        tool_breadcrumb();
    }

    else if (Name == 'Approvalstep_Approvers') {
        $(".SegmentQuerybuilderclass").css("display", "none");
        $('.CommonTreeDetail, .Related').css("display", "none");
        $("#div_CTR_Approvers").closest('.Related').css("display", "block");
        $('#ApprovalChainStepDetail').removeClass('active');
        $('#ApprovalChainStepRelated').removeClass('active');
        $('#ApprovalChainStepTrackedField').removeClass('active');
        $('#ApprovalChainStepRel').addClass('active');
        $('#ApprovalChainStepEmail').removeClass('active');
        $('.ApprovalsDetail').css('display', "none");
        ObjName = "ACACSA";
        CurrentRecordId = "SYOBJR-95816";
        CurrentNodeId = localStorage.getItem("CurrentNodeId");
        //# A043S001P01-12254 Start 
        if (TreeParentParam != 'Approval History') {
            try {
                cpq.server.executeScript("SYSUBANNER", { 'ObjName': ObjName, 'CurrentRecordId': CurrentRecordId, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                    //console.log("dataset-----> ",dataset);
                    if (dataset != '') {
                        if (document.getElementById("seginnerbnr")) {
                            $("#seginnerbnr").css("display", "block");
                            document.getElementById('seginnerbnr').innerHTML = dataset[0];
                        }
                        if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                            $(".container_banner_inner_sec").css("display", "none");
                        } else {
                            $(".container_banner_inner_sec").css("display", "block");
                        }
                    }
                });
            } catch (e) {
                console.log(e);
            }
        }//# A043S001P01-12254 Start 
    }
    else if (Name == 'Approvalstep_TrackedField') {
        $(".SegmentQuerybuilderclass").css("display", "none");
        $('.CommonTreeDetail, .Related').css("display", "none");
        $("#div_CTR_Tracked_Fields").closest('.Related').css("display", "block");
        $('#ApprovalChainStepDetail').removeClass('active');
        $('#ApprovalChainStepRelated').removeClass('active');
        $('#ApprovalChainStepTrackedField').addClass('active');
        $('#ApprovalChainStepRel').removeClass('active');
        $('.ApprovalsDetail').css('display', "none");
        ObjName = "ACAPTF";
        CurrentRecordId = "SYOBJR-95860";
        CurrentNodeId = localStorage.getItem("CurrentNodeId");
        //# A043S001P01-12254 Start 
        if (TreeParentParam != 'Approval History') {
            try {
                cpq.server.executeScript("SYSUBANNER", { 'ObjName': ObjName, 'CurrentRecordId': CurrentRecordId, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                    //console.log("dataset-----> ",dataset);
                    if (dataset != '') {
                        if (document.getElementById("seginnerbnr")) {
                            $("#seginnerbnr").css("display", "block");
                            document.getElementById('seginnerbnr').innerHTML = dataset[0];
                        }
                        if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                            $(".container_banner_inner_sec").css("display", "none");
                        } else {
                            $(".container_banner_inner_sec").css("display", "block");
                        }
                    }
                });
            } catch (e) {
                console.log(e);
            }
        }//# A043S001P01-12254 Start 
    }
    //equipment for inv-par
    else if (Name == 'Equipment') {
        breadCrumb_Reset();
        localStorage.setItem("page_type", "OBJECT PAGE LISTGRID")
        localStorage.setItem('eqp_details', 'false');
        $('.involvedparties_Details ').show();
        $('#div_CTR_Involved_Parties_Equipments').css('display', 'block');
        $('#div_CTR_Tool_Relocation_Matrix').closest('.Related').css("display", "none");
        $("#div_CTR_Source_Fab_Locations").closest('.Related').css("display", "none");
        $('div#COMMON_TABS').find("li a:contains('Source Fab Locations')").parent().css("display", "block");
        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
        var sale_type = localStorage.getItem("saletype");
        if (sale_type == "NEW" || Saletype == "CONTRACT RENEWAL") {
            $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().css("display", "none");
        }
        else {
            $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().css("display", "block");
        }
        RecId = 'SYOBJR-98858';
        RecName = "div_CTR_Involved_Parties_Equipments"
        loadRelatedList(RecId, RecName)
        $('.container_banner_inner_sec').css("display", "none");
        $('#div_CTR_Involved_Parties_Equipments').closest('.Related').css("display", "block")
        $('#div_CTR_Equipments').css('display', 'block');
        $('#TREE_div').css('display', 'none');
        //CurrentRecordId = $('#QSTN_SYSEFL_QT_00001').attr('title');
        CurrentRecordId = localStorage.getItem("masterquoteRecId");
        Subbaner('Equipment', CurrentNodeId, RecId, 'SAQSTE')
        $('#ADDNEW__SYOBJR_98858_SYOBJ_01034').show()
        ObjectName = "SAQSTE";
        subTabText = localStorage.getItem('currentSubTab');
        chainsteps_breadcrumb(subTabText);
        subtab = localStorage.getItem('sourcefab');
        localStorage.setItem('CurrentRecordId', subtab);
        tool_breadcrumb();
    }
    //A043S001P01-13245 start
    //
    else if (Name == 'ToolRelocationMatrix') {
        breadCrumb_Reset();
        localStorage.setItem('eqp_details', 'true');
        localStorage.setItem('toolmatrix_details', 'false');
        ObjectName = "SAQSTE";
        $('.involvedparties_Details ').show();
        $('#div_CTR_Tool_Relocation_Matrix').css('display', 'block');
        $('#div_CTR_Involved_Parties_Equipments').css('display', 'none');
        $("#div_CTR_Source_Fab_Locations").closest('.Related').css("display", "none");
        $('div#COMMON_TABS').find("li a:contains('Source Fab Locations')").parent().css("display", "block");
        $('div#COMMON_TABS').find("li a:contains('Equipment')").parent().css("display", "block");
        $('div#COMMON_TABS').find("li a:contains('Tool Relocation Matrix')").parent().css("display", "block");
        RecId = 'SYOBJR-00028';
        RecName = "div_CTR_Tool_Relocation_Matrix"
        loadRelatedList(RecId, RecName)
        $('#div_CTR_Tool_Relocation_Matrix').closest('.Related').css("display", "block")
        $('#div_CTR_Involved_Parties_Equipments').closest('.Related').css("display", "none")
        $('#div_CTR_Equipments').css('display', 'none');
        $('#TREE_div').css('display', 'none');
        $('.container_banner_inner_sec').css("display", "none");
        $('#ADDNEW__SYOBJR_98858_SYOBJ_01034').hide()
        //CurrentRecordId = $('#QSTN_SYSEFL_QT_00001').attr('title');
        CurrentRecordId = localStorage.getItem("masterquoteRecId");
        subTabText = localStorage.getItem('currentSubTab');
        chainsteps_breadcrumb(subTabText);
        subtab = localStorage.getItem('sourcefab');
        localStorage.setItem('CurrentRecordId', subtab);
        tool_breadcrumb();
        Subbaner('Tool Relocation Matrix', CurrentNodeId, RecId, 'SAQSTE');
    }
    //
    else if (Name == 'Transactions') {
        $(".SegmentQuerybuilderclass").css("display", "none");
        $('.CommonTreeDetail, .Related').css("display", "none");
        $("#div_CTR_Approval_Transactions").closest('.Related').css("display", "block");
        $('#ApprovalChainStepDetail').removeClass('active');
        $('#ApprovalChainStepRelated').removeClass('active');
        $('#ApprovalChainStepTrackedField').removeClass('active');
        $('#ApprovalChainStepRel').removeClass('active');
        $('#ApprovalTransactions').addClass('active');
        $('#ApprovalDetail').removeClass('active');
        $('#ApprovalTrackedValues').removeClass('active');
        $(".ApprovalChainStep").css("display", "none");
        ObjName = "ACAPTX";
        CurrentRecordId = "SYOBJR-95983";
        CurrentNodeId = localStorage.getItem("CurrentNodeId");
        //# A043S001P01-12254 Start 
        if (TreeParentParam != 'Approval Chain Steps') {
            try {
                cpq.server.executeScript("SYSUBANNER", { 'ObjName': ObjName, 'CurrentRecordId': CurrentRecordId, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                    //console.log("dataset-----> ",dataset);
                    if (dataset != '') {
                        if (document.getElementById("seginnerbnr")) {
                            $("#seginnerbnr").css("display", "block");
                            document.getElementById('seginnerbnr').innerHTML = dataset[0];
                        }
                        if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                            $(".container_banner_inner_sec").css("display", "none");
                        } else {
                            $(".container_banner_inner_sec").css("display", "block");
                        }
                    }
                });
            } catch (e) {
                console.log(e);
            }
        }
    }
    else if (Name == 'Values') {
        $(".SegmentQuerybuilderclass").css("display", "none");
        $('.CommonTreeDetail, .Related').css("display", "none");
        $("#div_CTR_Tracked_Values").closest('.Related').css("display", "block");
        $('#ApprovalChainStepDetail').removeClass('active');
        $('#ApprovalChainStepRelated').removeClass('active');
        $('#ApprovalChainStepTrackedField').removeClass('active');
        $('#ApprovalChainStepRel').removeClass('active');
        $('#ApprovalTransactions').removeClass('active');
        $('#ApprovalTrackedValues').addClass('active');
        $('#ApprovalDetail').removeClass('active');
        $(".ApprovalChainStep").css("display", "none");
        ObjName = "ACAPFV";
        CurrentRecordId = "SYOBJR-95984";
        CurrentNodeId = localStorage.getItem("CurrentNodeId");
        //# A043S001P01-12254 Start 
        if (TreeParentParam != 'Approval Chain Steps') {
            try {
                cpq.server.executeScript("SYSUBANNER", { 'ObjName': ObjName, 'CurrentRecordId': CurrentRecordId, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                    //console.log("dataset-----> ",dataset);
                    if (dataset != '') {
                        if (document.getElementById("seginnerbnr")) {
                            $("#seginnerbnr").css("display", "block");
                            document.getElementById('seginnerbnr').innerHTML = dataset[0];
                        }
                        if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                            $(".container_banner_inner_sec").css("display", "none");
                        } else {
                            $(".container_banner_inner_sec").css("display", "block");
                        }
                    }
                });
            } catch (e) {
                console.log(e);
            }
        }
    }
    //A043S001P01-13245 end
    //A043S001P01-13010 start
    else if (Name == 'TrackedValues') {
        $(".SegmentQuerybuilderclass").css("display", "none");
        $('.CommonTreeDetail, .Related').css("display", "none");
        $("#div_CTR_Tracked_Values").closest('.Related').css("display", "block");
        $('#ApprovalTrackedValues').addClass('active');
        $('#ApprovalTrackedFieldDetail').removeClass('active');
        $('#ApprovalChainStepDetail').css('display', 'none');
        $('#ApprovalChainStepRelated').css('display', 'none');
        $('#ApprovalChainStepTrackedField').css('display', 'none');
        $('#ApprovalChainStepRel').css('display', 'none');
        ObjName = "ACAPFV";
        CurrentRecordId = "SYOBJR-95870";
        CurrentNodeId = localStorage.getItem("CurrentNodeId");
        //# A043S001P01-12254 Start 
        if (TreeParentParam != 'Approval History') {
            try {
                cpq.server.executeScript("SYSUBANNER", { 'ObjName': ObjName, 'CurrentRecordId': CurrentRecordId, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                    //console.log("dataset-----> ",dataset);
                    if (dataset != '') {
                        if (document.getElementById("seginnerbnr")) {
                            $("#seginnerbnr").css("display", "block");
                            document.getElementById('seginnerbnr').innerHTML = dataset[0];
                        }
                        if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                            $(".container_banner_inner_sec").css("display", "none");
                        } else {
                            $(".container_banner_inner_sec").css("display", "block");
                        }
                    }
                });
            } catch (e) {
                console.log(e);
            }
        }//# A043S001P01-12254 Start 
    }
    //A043S001P01-13010 end
    //A043S001P01-13006 start
    else if (Name == 'Snapshots') {
        $(".SegmentQuerybuilderclass").css("display", "none");
        $('.CommonTreeDetail, .Related').css("display", "none");
        $("#div_CTR_Snapshots").closest('.Related').css("display", "block");
        $('#ApprovalChainStepDetail').css('display', 'none');
        $('#ApprovalChainStepRelated').css('display', 'none');
        $('#ApprovalChainStepTrackedField').css('display', 'none');
        $('#ApprovalChainStepRel').css('display', 'none');
        $('#ApprovalTrackedFieldDetail').css('display', 'none');
        $('#ApprovalTrackedValues').css('display', 'none');
        ObjName = "ACAPSS";
        CurrentRecordId = "SYOBJR-95871";
        CurrentNodeId = localStorage.getItem("CurrentNodeId");
        if (TreeParentParam != 'Tracked Objects') {
            try {
                cpq.server.executeScript("SYSUBANNER", { 'ObjName': ObjName, 'CurrentRecordId': CurrentRecordId, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                    //console.log("dataset-----> ",dataset);
                    if (dataset != '') {
                        if (document.getElementById("seginnerbnr")) {
                            $("#seginnerbnr").css("display", "block");
                            document.getElementById('seginnerbnr').innerHTML = dataset[0];
                        }
                        if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                            $(".container_banner_inner_sec").css("display", "none");
                        } else {
                            $(".container_banner_inner_sec").css("display", "block");
                        }
                    }
                });
            } catch (e) {
                console.log(e);
            }
        }
    }
    //A043S001P01-13006 end
    else if (Name == 'Approvalstep_Email') {
        $(".SegmentQuerybuilderclass").css("display", "none");
        $('.CommonTreeDetail, .Related').css("display", "none");
        $('#ApprovalChainStepEmail').addClass('active');
        $('#ApprovalChainStepDetail').removeClass('active');
        $('#ApprovalChainStepRelated').removeClass('active');
        $('#ApprovalChainStepTrackedField').removeClass('active');
        $('#ApprovalChainStepRel').removeClass('active');
        CurrentRecordId = localStorage.getItem("CurrentRecordId");
        try {
            cpq.server.executeScript("ACACSEMLBD", { 'Action': 'EmailContent', 'CurrentRecordId': CurrentRecordId }, function (dataset) {
                //console.log("dataset-----> ",dataset);
                if (dataset != '') {
                    if (document.getElementById("TREE_div")) {
                        $(".CommonTreeDetail").css("display", "block");
                        document.getElementById('TREE_div').innerHTML = dataset[0];
                        eval(dataset[1])
                    }
                }
            });
        } catch (e) {
            console.log(e);
        }
    }
    else if (Name == 'EmailTemplate detail') {
        $('#dyn10686').closest('.Detail ').show();
        $('#ban10687').closest('.Detail ').show();
        $('#ban10688').closest('.Detail ').show();
        $('#ban10689').closest('.Detail ').show();
        $('#drop10690').closest('.Detail').show();
        $('#ban10692').closest('.Detail ').show();

        $('#dyn10984').closest('.Detail ').hide();
        $('#ban10691').closest('.Detail ').hide();

        $('#dyn10432').closest('.Detail ').show();
        $('#ban10433').closest('.Detail ').show();
        $('#ban10434').closest('.Detail ').show();
        $('#ban10435').closest('.Detail ').show();
        $('#ban10436').closest('.Detail ').show();
    }
    else if (Name == 'EmailTemplate Body') {
        $('#dyn10686').closest('.Detail ').hide();
        $('#ban10687').closest('.Detail ').hide();
        $('#ban10688').closest('.Detail ').hide();
        $('#ban10689').closest('.Detail ').hide();
        $('#drop10690').closest('.Detail').hide();
        $('#ban10692').closest('.Detail ').hide();

        $('#dyn10984').closest('.Detail ').show();
        $('#ban10691').closest('.Detail ').show();

        $('#dyn10432').closest('.Detail ').hide();
        $('#ban10433').closest('.Detail ').hide();
        $('#ban10434').closest('.Detail ').hide();
        $('#ban10435').closest('.Detail ').hide();
        $('#ban10436').closest('.Detail ').hide();
    }
    else if (Name == 'Modal Details') {
        $('.SYSECT-SE-00131').show()
        $('.SYSECT-SE-00132').show()
        $('.SYSECT-SE-00133').show()
        $('.SYSECT-SE-00134').hide()
        $('.SYSECT-SE-00135').hide()
    }
    else if (Name == 'Metal Details') {
        $('.SYSECT-SE-00131').hide()
        $('.SYSECT-SE-00132').hide()
        $('.SYSECT-SE-00133').hide()
        $('.SYSECT-SE-00134').show()
        $('.SYSECT-SE-00135').show()
    }

    if (Name == 'Attribute_Details') {
        Common_enable_disable();
        $('.CommonTreeDetail').css('display', 'block');
        $('#div_CTR_Attribute_Values').closest('.Related').css('display', 'none');
        $('#div_CRT_Attribute_Value_Dependencies').closest('.Related').css('display', 'none');
        $('#ADDNEW__SYOBJR_95802_SYOBJ_00451').remove()
    }
    else if (Name == 'Attribute_Values') {
        $('.CommonTreeDetail').css('display', 'none');
        $('#div_CTR_Attribute_Values').closest('.Related').css('display', 'block');
        $('#div_CTR_Attribute_Value_Dependencies').closest('.Related').css('display', 'none');
        $('#ADDNEW__SYOBJR_95802_SYOBJ_00451').remove()
        $('#seginnerbnr').append('<button id="CMAssignValues__SYOBJR_95817_SYOBJ_00192" onclick="" class="btnconfig CMAssignValues" data-toggle="modal">ASSIGN VALUE</button>');
        try {
            currentrecordIdVal = localStorage.getItem('CurrentRecordId')
            recID = $(".CommonTreeDetail #TREE_div>#container table tr td input").val()
            cpq.server.executeScript("SYSUBANNER", { 'ObjName': 'CMCMAV', 'CurrentRecordId': 'SYOBJR-95801|' + currentrecordIdVal + '|' + recID, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam, 'SubBannerText': SubNode_text }, function (dataset) {
                if (dataset != '') {
                    if (document.getElementById("seginnerbnr")) {
                        $("#seginnerbnr").css("display", "block");
                        document.getElementById('seginnerbnr').innerHTML = dataset[0];
                    }
                    if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                        $(".container_banner_inner_sec").css("display", "none");
                    } else {
                        $(".container_banner_inner_sec").css("display", "block");
                    }
                }
            });
        } catch (e) {
            console.log(e);
        }
    }
    else if (Name == 'Attribute_Dependency_Rule') {
        $('.CommonTreeDetail').css('display', 'none');
        $('#div_CTR_Attribute_Values').closest('.Related').css('display', 'none');
        $('#div_CTR_Attribute_Value_Dependencies').closest('.Related').css('display', 'block');
        $('#ADDNEW__SYOBJR_95802_SYOBJ_00451').remove()
        $('#seginnerbnr').append('<button id="ADDNEW__SYOBJR_95802_SYOBJ_00451" onclick="cont_openaddnew(this, \'div_CTR_Attribute_Value_Dependencies\')" class="btnconfig addNewRel HideAddNew">ADD NEW</button>')
        try {
            currentrecordIdVal = localStorage.getItem('CurrentRecordId')
            recID = $(".CommonTreeDetail #TREE_div>#container table tr td input").val()
            cpq.server.executeScript("SYSUBANNER", { 'ObjName': 'CMCAVD', 'CurrentRecordId': 'SYOBJR-95802|' + currentrecordIdVal + '|' + recID, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam, 'SubBannerText': SubNode_text }, function (dataset) {
                //console.log("dataset-----> ",dataset);
                if (dataset != '') {
                    if (document.getElementById("seginnerbnr")) {
                        $("#seginnerbnr").css("display", "block");
                        document.getElementById('seginnerbnr').innerHTML = dataset[0];
                    }
                    if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                        $(".container_banner_inner_sec").css("display", "none");
                    } else {
                        $(".container_banner_inner_sec").css("display", "block");
                    }
                }
            });
        } catch (e) {
            console.log(e);
        }

    }
    else if (Name == 'Attribute_Value_Dependency_Rule') {
        $('.CommonTreeDetail').css('display', 'none');
        $(".Attribute_Value_Subtab").css("display", "block");
        $('#div_CTR_Attribute_Value_Dependencies').closest('.Related').css('display', 'block');
        $('#Attribute_Value_Details_id').removeClass('active');
        $('[id^="UnAssignValue__CMCMAV"]').css("display", "none");
        try {
            currentrecordIdVal = localStorage.getItem('CurrentRecordId')
            recID = $(".CommonTreeDetail #TREE_div>#container table tr td input").val()
            cpq.server.executeScript("SYSUBANNER", { 'ObjName': 'CMCAVD', 'CurrentRecordId': 'SYOBJR-95802|' + currentrecordIdVal + '|' + recID, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam, 'SubBannerText': SubNode_text }, function (dataset) {
                //console.log("dataset-----> ",dataset);
                if (dataset != '') {
                    if (document.getElementById("seginnerbnr")) {
                        $("#seginnerbnr").css("display", "block");
                        document.getElementById('seginnerbnr').innerHTML = dataset[0];
                    }
                    if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                        $(".container_banner_inner_sec").css("display", "none");
                    } else {
                        $(".container_banner_inner_sec").css("display", "block");
                    }
                }
            });
        } catch (e) {
            console.log(e);
        }
    }
    else if (Name == 'Attribute_classes_details') {
        Common_enable_disable();
        $('#div_CTR_Attributes').closest('.Related').css('display', 'none');
    }
    else if (Name == 'Attributes_attr') {
        $('.CommonTreeDetail').css('display', 'none')
        $('#div_CTR_Attributes').closest('.Related').css('display', 'block');
        try {
            currentrecordIdVal = localStorage.getItem('CurrentRecordId')
            recID = $(".CommonTreeDetail #TREE_div>#container table tr td input").val()
            cpq.server.executeScript("SYSUBANNER", { 'ObjName': "CMCMAT", 'CurrentRecordId': 'SYOBJR-90006|' + currentrecordIdVal + '|' + recID, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam, 'SubBannerText': SubNode_text }, function (dataset) {
                //console.log("dataset-----> ",dataset);
                if (dataset != '') {
                    if (document.getElementById("seginnerbnr")) {
                        $("#seginnerbnr").css("display", "block");
                        document.getElementById('seginnerbnr').innerHTML = dataset[0];
                    }
                    $(".container_banner_inner_sec").css("display", "none");
                }
            });
        } catch (e) {
            console.log(e);
        }
    }
    else if (Name == 'Rule_Details') {
        Common_enable_disable();
        $('#div_CTR_Rule_Actions').closest('.Related').css('display', 'none');
        $('#div_CTR_Rule_Actions').closest('.Related').css('display', 'none');
        setTimeout(function () {
            $('#ADDNEW__SYOBJR_95803_SYOBJ_00455').css('display', 'none');
        }, 2000);
        //$('#ADDNEW__SYOBJR_95803_SYOBJ_00455').remove();
    }
    else if (Name == "Rule_Actions") {
        $('.CommonTreeDetail').css('display', 'none');
        $('#div_CTR_Rule_Actions').closest('.Related').css('display', 'block');
        $('#ADDNEW__SYOBJR_95803_SYOBJ_00455').remove();
        setTimeout(function () {
            $('#Rule_Details_Delete').css('display', 'none');
        }, 900);
        //$('#seginnerbnr').append('<button id="ADDNEW__SYOBJR_95803_SYOBJ_00455" onclick="cont_openaddnew(this, \'div_CTR_Rule_Actions\')" class="btnconfig addNewRel HideAddNew">ADD NEW</button>');
        try {
            currentrecordIdVal = localStorage.getItem('CurrentRecordId')
            recID = $(".CommonTreeDetail #TREE_div>#container table tr td input").val()
            cpq.server.executeScript("SYSUBANNER", { 'ObjName': 'CMCRAC', 'CurrentRecordId': 'SYOBJR-95803|' + currentrecordIdVal + '|' + recID, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                if (dataset != '') {
                    if (document.getElementById("seginnerbnr")) {
                        $("#seginnerbnr").css("display", "block");
                        document.getElementById('seginnerbnr').innerHTML = dataset[0];
                    }
                    if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                        $(".container_banner_inner_sec").css("display", "none");
                    } else {
                        $(".container_banner_inner_sec").css("display", "block");
                    }
                }
            });
        } catch (e) {
            console.log(e);
        }
    }
    else if (Name == 'Layout_tabs') {
        $('.CommonTreeDetail').css('display', 'none')
        loadRelatedList('SYOBJR-95812', 'div_CTR_Tabs');
        $('#div_CTR_Tabs').closest('.Related').css('display', 'block');
        $('#div_CTR_Sections').closest('.Related').css('display', 'none');
        $('#div_CTR_Questions').closest('.Related').css('display', 'none');
        $('#div_CTR_Preview').closest('.Related').css('display', 'none');
        try {
            currentrecordIdVal = localStorage.getItem('CurrentRecordId')
            recID = $(".CommonTreeDetail #TREE_div>#container table tr td input").val()
            cpq.server.executeScript("SYSUBANNER", { 'ObjName': 'CMCLTB', 'CurrentRecordId': 'SYOBJR-95812|' + currentrecordIdVal + '|' + recID, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                if (dataset != '') {
                    if (document.getElementById("seginnerbnr")) {
                        $("#seginnerbnr").css("display", "block");
                        document.getElementById('seginnerbnr').innerHTML = dataset[0];
                        $('#deletebtn_Tab').hide();
                        $('#BTL_CMCLTB').hide();
                    }
                    if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                        $(".container_banner_inner_sec").css("display", "none");
                    } else {
                        $(".container_banner_inner_sec").css("display", "block");
                    }
                }
            });
        } catch (e) {
            console.log(e);
        }
        $('.HideAddNew').remove();
        $('#HideSavecancel').remove()
        $('#seginnerbnr').append('<button id="ADDNEW__SYOBJR_95812_SYOBJ_00457" onclick="cont_openaddnew(this,\'div_CTR_Tabs\')" class="btnconfig addNewRel HideAddNew" style="display: block;">ADD NEW</button>')

    }
    else if (Name == 'Layout_sections') {
        $('.CommonTreeDetail').css('display', 'none')
        loadRelatedList('SYOBJR-95814', 'div_CTR_Sections');
        $('#div_CTR_Sections').closest('.Related').css('display', 'block');
        $('#div_CTR_Tabs').closest('.Related').css('display', 'none');
        $('#div_CTR_Questions').closest('.Related').css('display', 'none');
        $('#div_CTR_Preview').closest('.Related').css('display', 'none');
        try {
            currentrecordIdVal = localStorage.getItem('CurrentRecordId')
            recID = $(".CommonTreeDetail #TREE_div>#container table tr td input").val()
            cpq.server.executeScript("SYSUBANNER", { 'ObjName': 'CMCLSE', 'CurrentRecordId': 'SYOBJR-95814|' + currentrecordIdVal + '|' + recID, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                if (dataset != '') {
                    if (document.getElementById("seginnerbnr")) {
                        $("#seginnerbnr").css("display", "block");
                        document.getElementById('seginnerbnr').innerHTML = dataset[0];
                        $('#deletebtn_Section').hide();
                        $('#BTL_CMCLSE').hide();
                    }
                    if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                        $(".container_banner_inner_sec").css("display", "none");
                    } else {
                        $(".container_banner_inner_sec").css("display", "block");
                    }
                }
            });
        } catch (e) {
            console.log(e);
        }
        $('.HideAddNew').remove();
        $('#HideSavecancel').remove()
        $('#seginnerbnr').append('<button id="ADDNEW__SYOBJR_95814_SYOBJ_00456" onclick="cont_openaddnew(this,\'div_CTR_Sections\')" class="btnconfig addNewRel HideAddNew" style="display: block;">ADD NEW</button>')
    }
    else if (Name == 'Layout_questions') {
        $('.CommonTreeDetail').css('display', 'none')
        loadRelatedList('SYOBJR-95813', 'div_CTR_Questions');
        $('#div_CTR_Sections').closest('.Related').css('display', 'none');
        $('#div_CTR_Tabs').closest('.Related').css('display', 'none');
        $('#div_CTR_Questions').closest('.Related').css('display', 'block');
        $('#div_CTR_Preview').closest('.Related').css('display', 'none');
        try {
            currentrecordIdVal = localStorage.getItem('CurrentRecordId')
            recID = $(".CommonTreeDetail #TREE_div>#container table tr td input").val()
            cpq.server.executeScript("SYSUBANNER", { 'ObjName': 'CMCMQU', 'CurrentRecordId': 'SYOBJR-95813|' + currentrecordIdVal + '|' + recID, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                if (dataset != '') {
                    if (document.getElementById("seginnerbnr")) {
                        $("#seginnerbnr").css("display", "block");
                        document.getElementById('seginnerbnr').innerHTML = dataset[0];
                        $('#Question_BTL').hide();
                        $('#deletebtn_Question').hide();
                        $('#BTL_CMCMQU').hide();
                    }
                    if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                        $(".container_banner_inner_sec").css("display", "none");
                    } else {
                        $(".container_banner_inner_sec").css("display", "block");
                    }
                }
            });
        } catch (e) {
            console.log(e);
        }

        $('.HideAddNew').remove();
        $('#HideSavecancel').remove()
        //$('#seginnerbnr').append('<button id="ADDNEW__SYOBJR_95813_SYOBJ_00454" onclick="cont_openaddnew(this,\'div_CTR_Questions\')" class="btnconfig addNewRel HideAddNew" style="display: block;">ADD NEW</button>')
    }
    else if (Name == 'Page_Model') {
        $('#container13437 .container_banner_inner_sec').addClass('disp_none');
        /*record_id = CurrentRecordId
        keyDataVal = localStorage.getItem('keyDataVal')
        cpq.server.executeScript("CMPREVWDTL", { 'ACTION': 'MODEL_VIEW', 'REC_ID': record_id, 'CM_REC_ID': keyDataVal }, function (data) {
            if (data != '') {
                $('.CommonTreeDetail').css('display', 'none');
                $('#div_CTR_PageModel').closest('.Related').css('display', 'block');
                $('#div_CTR_PageModel').html(data);
            }
        });
        console.log("Page_Model-----!");*/
        $('.CommonTreeDetail').css('display', 'none');
        $('#div_CTR_PageModel').closest('.Related').css('display', 'block');
    }
    else if (Name == 'Layout_Preview' && ($('.segment_part_number_text').text() == 'SURFACEBOOK' || $('.segment_part_number_text').text() == 'LAPTOP')) {
        $('#conta12523 .container_banner_inner_sec').css('display', 'none');
        localStorage.setItem('IndexZeroAttr', '');
        record_id = CurrentRecordId
        keyDataVal = localStorage.getItem('keyDataVal')
        cpq.server.executeScript("CMPREVWDTL", { 'ACTION': 'TABS', 'REC_ID': record_id, 'CM_REC_ID': keyDataVal }, function (data) {
            data0 = data[0];
            data1 = data[1];
            data2 = data[2];
            localStorage.setItem('IndexZeroAttr', data2);
            if (data0 != '') {
                //console.log("datadata---->", data0);
                $('.CommonTreeDetail').css('display', 'none');
                $('#div_CTR_Sections').closest('.Related').css('display', 'none');
                $('#div_CTR_Tabs').closest('.Related').css('display', 'none');
                $('#div_CTR_Questions').closest('.Related').css('display', 'none');
                $('#div_CTR_PageModel').closest('.Related').css('display', 'none');
                $('#div_CTR_Preview').closest('.Related').css('display', 'block');
                $('#div_CTR_Preview').html(data0);
                eval(data1);
                try {
                    currentrecordIdVal = localStorage.getItem('CurrentRecordId')
                    recID = $(".CommonTreeDetail #TREE_div>#container table tr td input").val()
                    cpq.server.executeScript("SYSUBANNER", { 'ObjName': 'CMCMPL', 'CurrentRecordId': currentrecordIdVal, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                        if (dataset != '') {
                            if (document.getElementById("seginnerbnr")) {
                                $("#seginnerbnr").css("display", "block");
                                document.getElementById('seginnerbnr').innerHTML = dataset[0];
                                $('#deletebtn_Page').hide();
                            }
                        }
                    });
                } catch (e) {
                    console.log(e);
                }
                $('.HideAddNew').remove();
                $('#HideSavecancel').remove()
            }
        });
    }
    else if (Name == 'Layout_Preview' && ($('.segment_part_number_text').text() != 'SURFACEBOOK' || $('.segment_part_number_text').text() != 'LAPTOP')) {
        $('#conta12523 .container_banner_inner_sec').css('display', 'none');
        getPageModel = $('#X_PAGE_MODEL').val()
        $('.CommonTreeDetail').css('display', 'none');
        $('#div_CTR_PageModel').closest('.Related').css('display', 'none');
        $('#div_CTR_Preview').closest('.Related').css('display', 'block');
        keyDataVal = localStorage.getItem('keyDataVal')
        $('#div_CTR_Preview').html(getPageModel);
        keyDataVal = localStorage.getItem('keyDataVal');
        record_id = CurrentRecordId;
        attrname = ""
        Clkval = ""

        var ViewModel = function () {
            var self = this;

            self.subtabId = ko.observable();
            self.imagePath = ko.observable();
            self.ClassName = ko.observable();
            self.SapDescription = ko.observable();
            self.SapPartNumber = ko.observable();
            self.retrievedData = ko.observable();

            self.displayAttributeValue = function (dataset) {
                self.subtabId(dataset[0]);
                self.imagePath(dataset[1]);
                self.ClassName(dataset[2]);
                self.SapDescription(dataset[3]);
                self.SapPartNumber(dataset[4]);
                self.retrievedData(dataset[5]);
            };

            cpq.server.executeScript("CMPREVWDTL", {
                'ACTION': 'KNOCKOUT_DATA',
                'CM_REC_ID': keyDataVal,
                'REC_ID': record_id,
                'ATTR_NAME': attrname,
                'ATTR_VAL': Clkval
            }, function (dataset) {
                setTimeout(function () {
                    self.displayAttributeValue(dataset)
                }, 1500);
            });

            self.selected = ko.observable();

            self.SelectedAttributeValue = ko.computed(function () {
                var selectedAttribute = self.selected();
                if (selectedAttribute != undefined) {
                    cpq.server.executeScript("CMPREVWDTL", {
                        'ACTION': 'GETATTRIBUTE',
                        'CM_REC_ID': keyDataVal,
                        'REC_ID': record_id,
                        'ATTR_NAME': selectedAttribute.split('_')[0],
                        'ATTR_VAL': selectedAttribute.split('_')[1]
                    }, function (dataset) {
                        setTimeout(function () {
                            self.displayAttributeValue(dataset)
                        }, 1500);
                    });
                }
                return self.selected()

            });

        };
        ko.cleanNode(document.getElementById('div_CTR_Preview'));
        ko.applyBindings(new ViewModel(), document.getElementById('div_CTR_Preview'));
    }
    else if (Name == 'Layout_qstn_detail') {
        $('.CommonTreeDetail').css('display', 'block');
        $('.HideAddNew').hide();
        $('#Question_BTL').show();
        $('#div_CTR_Question_Table_Columns').closest('.Related').css('display', 'none');
    }
    else if (Name == 'Layout_qstn_tbl_col') {
        $('.CommonTreeDetail').css('display', 'none');
        loadRelatedList('SYOBJR-95872', 'div_CTR_Question_Table_Columns');
        $('#div_CTR_Question_Table_Columns').closest('.Related').css('display', 'block');
        try {
            currentrecordIdVal = localStorage.getItem('CurrentRecordId')
            recID = $(".CommonTreeDetail #TREE_div>#container table tr td input").val()
            cpq.server.executeScript("SYSUBANNER", { 'ObjName': 'CMQTCL', 'CurrentRecordId': 'SYOBJR-95872|' + currentrecordIdVal + '|' + recID, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
                if (dataset != '') {
                    if (document.getElementById("seginnerbnr")) {
                        $("#seginnerbnr").css("display", "block");
                        document.getElementById('seginnerbnr').innerHTML = dataset[0];
                    }
                    if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                        $(".container_banner_inner_sec").css("display", "none");
                    } else {
                        $(".container_banner_inner_sec").css("display", "block");
                    }
                }
            });
        } catch (e) {
            console.log(e);
        }
    }
    //QuoteStatus()
    dynamic_status();
}
function common_Detail_Subtab() {
    $('#seginnerbnr').css('display', 'block');
    $('#seginner_relbnr').css('display', 'none');
    //CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
    CurrentTab = $("ul#carttabs_head li.active a span").text();
    TreeParam = localStorage.getItem('CommonTreeParam');
    TreeParentParam = localStorage.getItem('CommonTreeParentParam');
    TreeSuperParentParam = localStorage.getItem('CommonNodeTreeSuperParentParam');
    TopSuperParentParam = localStorage.getItem('CommonTopSuperParentParam');
    //TreeSuperTopParentParam = localStorage.getItem('CommonTreeSuperTopParentParam');
    TreeFirstSuperTopParentParam = localStorage.getItem('CommonTreeFirstSuperTopParentParam');
    TreeFirstSuperTopParentParam12 = localStorage.getItem('common_TreeFirstSuperTopParentParam')

    $("#COMMON_TABS li").each(function () {
        $(this).css('display', 'none');
    });
    $('#COMMON_TABS').css('display', 'block');
    $('.CommonTreeDetail').css('display', 'block');
    $('#COMMON_TABS').find('li.active').removeClass('active');
    $('.Related').css('display', 'none')
    if (CurrentTab == "Approval Chain" || CurrentTab == "My Approvals Queue" || CurrentTab == "Team Approvals Queue") {
        //A043S001P01-13006 end
        CurrentRecordId = localStorage.getItem("CurrentRecordId")
        if (TreeParentParam == 'Approval Chain Steps') {
            $(".SegmentQuerybuilderclass").css("display", "none");
            ObjName = "ACACST";
            CurrentRecordId = localStorage.getItem("CurrentRecordId")
            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'TableId': TreeParentNodeRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                localStorage.setItem('Lookupobjd', data5)
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                }
            });
            $('.ApprovalChainStep').css('display', 'block');
            $('#ApprovalChainStepDetail').addClass('active');
            //$('.ApprovalQueue').css('display', 'block');
            //$('#ApprovalTrackedFieldDetail').addClass('active');			
            $('#ApprovalChainStepRelated').removeClass('active');
            $('#ApprovalChainStepRel').removeClass('active');
            $('#ApprovalChainStepTrackedField').removeClass('active');
            $('#ApprovalChainStepEmail').removeClass('active');
            $("#COMMON_TABS").css("display", "block");
            $('.ApprovalHistory').css('display', 'none');
            $('.ApprovalQueue').css('display', 'none');
            $('.ApprovalsDetail').css('display', 'none');
        }
        //A043S001P01-13010 start
        else if (TreeSuperParentParam == "Tracked Objects") {
            $('.ApprovalQueue').css('display', 'block');
            $('#ApprovalTrackedFieldDetail').addClass('active');
            $('#ApprovalTrackedValues').removeClass('active');
            $('.ApprovalHistory').css('display', 'none');
            $('.ApprovalsDetail').css('display', 'none');
            ObjName = "ACAPTF"
            CurrentRecordId = localStorage.getItem("CurrentRecordId")
            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'TableId': TreeParentNodeRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                localStorage.setItem('Lookupobjd', data5)
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                }
            });
        }
        //A043S001P01-13010 end	
        // A043S001P01-13006 start
        else if (TreeParentParam == "Approval History") {
            $('.ApprovalHistory').css('display', 'block');
            $('#ApprovalHistoryDetail').addClass('active');
            $('#ApprovalSnapshot').removeClass('active');
            $('.ApprovalQueue').css('display', 'none');
            $('.ApprovalsDetail').css('display', 'none');
            ObjName = "ACAPTX"
            CurrentRecordId = localStorage.getItem("CurrentRecordId")
            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'TableId': TreeParentNodeRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                localStorage.setItem('Lookupobjd', data5)
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                }
            });
        }
        // A043S001P01-13006 end
        //A043S001P01-13245 start
        else if (TreeParentParam == "Approvals") {
            $('.ApprovalsDetail').css('display', 'block');
            $('#ApprovalDetail').addClass('active');
            $('#ApprovalTransactions').removeClass('active');
            $('.ApprovalQueue').css('display', 'none');
            $('.ApprovalChainStep').css('display', 'none');
            $('#div_CTR_related_list').css('display', 'none');
            ObjName = "ACAPMA"
            CurrentRecordId = localStorage.getItem("CurrentRecordId")
            cpq.server.executeScript("SYULODTRND", { 'RECORD_ID': CurrentRecordId, 'TableId': TreeParentNodeRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'MODE': 'VIEW', 'NEWVAL': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '', 'SECTION_EDIT': '', 'Flag': 1 }, function (dataset) {
                var [datas, data1, data2, data3, data4, data5] = [dataset[0], dataset[1], dataset[2], dataset[3], dataset[4], dataset[5]];
                localStorage.setItem('Lookupobjd', data5)
                if (document.getElementById("TREE_div")) {
                    document.getElementById("TREE_div").innerHTML = datas;
                    // FUNCTION CALL TO ENABLE THE POPOVER AND TO CLOSE IT WHEN ANOTHER IS ACTIVE
                    popover()
                }
            });
        }
        //A043S001P01-13245 end		
    } // A043S001P01-12254  End

    $("#COMMON_TABS li").each(function () {
        if (($(this).css("display") == "block") && ($(this).children('a').text() == 'Detail') || ($(this).children('a').text() == 'Details') || ($(this).children('a').text() == 'Sales Territory')) {
            $(this).addClass('active')
        }
    });

    try {
        cpq.server.executeScript("SYSUBANNER", { 'ObjName': ObjName, 'CurrentRecordId': CurrentRecordId, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
            //console.log("dataset-----> ",dataset);
            if (dataset != '') {
                if (document.getElementById("seginnerbnr")) {
                    $("#seginnerbnr").css("display", "block");
                    document.getElementById('seginnerbnr').innerHTML = dataset[0];
                }
                if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                    $(".container_banner_inner_sec").css("display", "none");
                } else {
                    $(".container_banner_inner_sec").css("display", "block");
                }
            }
        });
    } catch (e) {
        console.log(e);
    }

}
function common_Related_Subtab() {
    ObjName = CurrentRecordId = TreeParentNodeRecId = TreeSuperParentRecId = TreeTopSuperParentRecId = TreeSuperTopParentRecId = TreeFirstSuperTopParentRecId = GrandTreeFirstSuperTopParentRecId = Grand_GrandTreeFirstSuperTopParentRecId = TreeParam = TreeParentParam = TreeSuperParentParam = TreeTopSuperParentParam = TreeSuperTopParentParam = ""

    $('#seginnerbnr').css('display', 'block');
    $('#seginner_relbnr').css('display', 'none');
    //CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
    CurrentTab = $("ul#carttabs_head li.active a span").text();
    TreeParam = localStorage.getItem('CommonTreeParam');
    TreeParentParam = localStorage.getItem('CommonTreeParentParam');
    TreeSuperParentParam = localStorage.getItem('CommonNodeTreeSuperParentParam');
    TopSuperParentParam = localStorage.getItem('CommonTopSuperParentParam');
    TreeSuperTopParentParam = localStorage.getItem('CommonTreeSuperTopParentParam');
    TreeFirstSuperTopParentParam12 = localStorage.getItem('common_TreeFirstSuperTopParentParam')
    TreeParentNodeRecId = localStorage.getItem('CommonParentNodeRecId');

    $("#COMMON_TABS li").each(function () {
        $(this).css('display', 'none');
    });

    $('#COMMON_TABS').css('display', 'block');
    $('.Related').css('display', 'none');
    $('.CommonTreeDetail').css('display', 'none');


    if (CurrentTab == "Approval Chain" || CurrentTab == "Approver" || CurrentTab == "My Approvals Queue") {
        if (TreeParentParam == 'Approval Chain Steps' || TreeParentParam == 'Approval History') {
            $(".SegmentQuerybuilderclass").css("display", "block");
            if (currenttab == 'Approver') {
                $('.ApproverChainStep').css('display', 'block');
                $('#ApproverDetail').removeClass('active');
                $('#ApproverRelated').addClass('active');
            } else {
                $('.ApprovalChainStep').css('display', 'block');
                $('#ApprovalChainStepDetail').removeClass('active');
                $('#ApprovalChainStepRelated').addClass('active');
                $('#ApprovalChainStepRel').removeClass('active');
                $('#ApprovalChainStepTrackedField').removeClass('active');
                $('.QBeditbtn').show()
            }
            $("#COMMON_TABS").css("display", "block");
            ObjName = "ACACST";
            CurrentRecordId = localStorage.getItem("CurrentRecordId")
        }

    }// A043S001P01-12254  End


    try {
        cpq.server.executeScript("SYSUBANNER", { 'ObjName': ObjName, 'CurrentRecordId': CurrentRecordId, 'TreeParentNodeRecId': TreeParentNodeRecId, 'TreeSuperParentRecId': TreeSuperParentRecId, 'TreeTopSuperParentRecId': TreeTopSuperParentRecId, 'TreeSuperTopParentRecId': TreeSuperTopParentRecId, 'TreeFirstSuperTopParentRecId': TreeFirstSuperTopParentRecId, 'GrandTreeFirstSuperTopParentRecId': GrandTreeFirstSuperTopParentRecId, 'Grand_GrandTreeFirstSuperTopParentRecId': Grand_GrandTreeFirstSuperTopParentRecId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam, 'TreeSuperTopParentParam': TreeSuperTopParentParam }, function (dataset) {
            //console.log("dataset-----> ",dataset);
            if (dataset != '') {
                if (document.getElementById("seginnerbnr")) {
                    $("#seginnerbnr").css("display", "block");
                    document.getElementById('seginnerbnr').innerHTML = dataset[0];
                }
                if (CurrentRecordId.startsWith("SYOBJR", 0) == true) {
                    $(".container_banner_inner_sec").css("display", "none");
                } else {
                    $(".container_banner_inner_sec").css("display", "block");
                }
                if (CurrentTab == "Approval Chain") {
                    if (TreeParentParam == 'Approval Chain Steps') {
                        $('.QBeditbtn').show()
                    }
                }
            }
        });
    } catch (e) {
        console.log(e);
    }
}


function maintreeparamfunction(CurrentNodeId, level) {
    try {
        Curlevel = level
        var cur_id = $('#commontreeview').treeview('getParent', CurrentNodeId).nodeId;

        if (cur_id != undefined) {
            cur_key = "TreeParentLevel" + Curlevel
            var bd_val = $('#commontreeview').treeview('getNode', cur_id).text;
            var bd_val_temp = ''
            if (bd_val.includes("<img") || bd_val.includes("<span")) {
                temp = $('#commontreeview').treeview('getNode', cur_id).text.split(">");
                dict[cur_key] = temp[temp.length - 1];
            } else {
                dict[cur_key] = $('#commontreeview').treeview('getNode', cur_id).text;
            }
            bd_val_temp = dict[cur_key]
            if (bd_val_temp.includes("-")) {
                // temp = $('#commontreeview').treeview('getNode', cur_id).text.split("-");
                if (!bd_val_temp.includes('- BASE') && bd_val_temp != 'Add-On Products' && !bd_val_temp.includes('Sending') && !bd_val_temp.includes('Receiving')) {
                    temp = bd_val_temp.split("-");
                    dict[cur_key] = temp[0].trim();
                }
            }


            Curlevel += 1
            maintreeparamfunction(cur_id, Curlevel)
        }
        return dict
    }
    catch (e) {
        console.log(e);
    };
}
//#A043S001P01-9934_START
function buttonState() {
    var test = $('#COMM_CONCESSION_FACTOR').val()
    if (test != '') {
        $('#saveButton').removeAttr('disabled')
    }
    else {
        $('#saveButton').attr('disabled', 'disabled')

    }
}
//#A043S001P01-9934_END




// hiding the vertical scrollbar when resizing the browser for RTE
function overflowYoff() {
    $(".tab-content").css("overflow-y", "hidden");
}
function overflowYon() {
    $(".tab-content").css("overflow-y", "auto");
}

// $('#PrincipalClasscheck').on('change', function () {

// });

function PrincipalClass_Check_change(ele) {
    if ($(ele).prop("checked") == true) {
        $("#mat12432").hide();
        $("#mat12434").hide();
        $("#dyn11020").hide();


    }
    else {
        $("#mat12432").show();
        $("#dyn11020").show();
        $("#mat12434").show();
    }

}
function cata_relatedOk() { // function name chagned
    var getempty = $(".product_txt_to_top_banner").text();
    getcurrentcancelid = $('.sec_edit_sty_btn').attr('id')
    localStorage.setItem('getcurrentcancelid', getcurrentcancelid)
    if (getempty == '') {
        $('#commontreeview').treeview('selectNode', [parseInt(0), { levels: 1, silent: true }]);

    }

    else {
        localStorage.setItem('RelatedEdit', '0')
        if (document.getElementById('BTN_SYACTI_PB_00017_CANCEL')) {
            document.getElementById('BTN_SYACTI_PB_00017_CANCEL').click();
            localStorage.setItem('RelatedEdit', '0');
        }
        if (document.getElementById('BTN_SYACTI_PB_00127_CANCEL')) {
            document.getElementById('BTN_SYACTI_PB_00127_CANCEL').click();
            localStorage.setItem('RelatedEdit', '0');
        }
        try {
            var SECTION_EDIT = localStorage.getItem("SECTION_EDIT")
            if (SECTION_EDIT != '') {
                sec_cancel_tab();
            }
            // if (SECTION_EDIT == ''){
            // sec_levelcancel_tab();
            // }
        }
        catch (e) {
            console.log(e);
        };
        sec_cancel_tab()
        CurrentNodeId = localStorage.getItem('EditCurrentNodeId');
        localStorage.setItem("CurrentNodeId", CurrentNodeId);
        Common_enable_disable();    // Changeed
        var node = $('#commontreeview').treeview('getNode', CurrentNodeId);
        var childrenNodes = _getChildren(node);
        if (childrenNodes.length == 0) {
            //prcmdl_viewedit();
            //MaterialLeftTreeView
        }
        // matriltreeview    -- Corresponding tree veiw ID

    }

}
function cata_relatedCancel() {
    $('#cata_related_edit').modal('hide'); // mtrlcmdl_related_edit  Template Id
    localStorage.setItem('RelatedEdit', '1');
    if (localStorage.getItem('CurrentNodeId') != '') {
        $('#commontreeview').treeview('selectNode', [parseInt(localStorage.getItem('CurrentNodeId')), { levels: 1, silent: true }]);
        var name = $('#commontreeview').treeview('getNode', parseInt(localStorage.getItem('CurrentNodeId'))).text;
        localStorage.setItem('TreeParam', name);
    }
    else {
        $('#commontreeview').treeview('selectNode', [parseInt(0), { levels: 1, silent: true }]);
        localStorage.setItem('TreeParam', '');
    }
    //Mtrl_tree_click();

}
function breadCrumb_Reset() {
    var unique_breadcrumb_list = [];
    for (var k in AllTreeParam) unique_breadcrumb_list.push(k);
    var build_breadcrumb = '<ul class="breadcrumb">'
    $(unique_breadcrumb_list.reverse()).each(function (index) {
        if (index != 0) {
            parent_node = AllTreeParam[unique_breadcrumb_list[index - 1]]
        }
        if (build_breadcrumb.includes(AllTreeParam[unique_breadcrumb_list[index]])) {
            build_breadcrumb += ''
        }
        else {
            build_breadcrumb += '<li><a onclick="tree_breadCrumb_redirection(this,parent_node)"><abbr title="' + AllTreeParam[unique_breadcrumb_list[index]] + '">'
            build_breadcrumb += AllTreeParam[unique_breadcrumb_list[index]];
            build_breadcrumb += '</abbr></a><span class="angle_symbol"><img src = "/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"/></span></li>'
        }
    });
    build_breadcrumb += '</ul>'
    if (TreeParam == "Quote Information") {
        parent_node = ""
    }
    $('div#header_label').html(build_breadcrumb);
    $('ul.breadcrumb > li > a').each(function (index) {
        var a = $(this).text();
        if (a.indexOf('function(e)') != -1) {
            $(this).parent('li').remove();
        }
    });
    var header_label_parent_height = $('div#header_label').parent().css('height');
    var breadcrumb_height = $('div#header_label ul.breadcrumb').css('height');
    var header_label_parent_height_split = header_label_convert_to_int = breadcrumb_height_split = breadcrumb_height_convert_to_int = header_label_parent_width_split = header_label_width_convert_to_int = breadcrumb_width_split = breadcrumb_width_convert_to_int = '';
    if (header_label_parent_height) {
        header_label_parent_height_split = header_label_parent_height.split('px');
        header_label_convert_to_int = parseInt(header_label_parent_height_split[0]);
    }
    if (breadcrumb_height) {
        breadcrumb_height_split = breadcrumb_height.split('px');
        breadcrumb_height_convert_to_int = parseInt(breadcrumb_height_split[0]);
    }
    var header_label_parent_width = $('div#header_label').parent().css('width');
    if (header_label_parent_width) {
        header_label_parent_width_split = header_label_parent_width.split('px');
        header_label_width_convert_to_int = parseInt(header_label_parent_width_split[0]) - 70;
    }
    var breadcrumb_width = $('div#header_label ul.breadcrumb').css('width');
    if (breadcrumb_width) {
        breadcrumb_width_split = breadcrumb_width.split('px');
        breadcrumb_width_convert_to_int = parseInt(breadcrumb_width_split[0]);
    }
    var breadcrumb_content_length = unique_breadcrumb_list.length;
    var set_width_for_breadcrumb = parseInt(header_label_parent_width_split[0] / breadcrumb_content_length);
    var set_width_for_breadcrumb_px = set_width_for_breadcrumb + 'px';
    var set_width_for_breadcrumb_level2 = set_width_for_breadcrumb - 20;
    set_width_for_breadcrumb_level2 = set_width_for_breadcrumb_level2 + 'px';
    if ((header_label_convert_to_int < breadcrumb_height_convert_to_int) || (breadcrumb_width_convert_to_int > header_label_width_convert_to_int)) {
        $('div#header_label ul.breadcrumb li').css('width', set_width_for_breadcrumb_px);
        $('span.angle_symbol').css('padding', '0 5px 0 0px');
        $('div#header_label').children('ul.breadcrumb').find('a').css('width', set_width_for_breadcrumb_level2);
        $('div#header_label').children('ul.breadcrumb').children('li:last-child').css('float', 'unset');
    }
}

//Equipment Nested grid starts..
function EquipmentTreeTable() {
    AllTreeParam = maintreeparamfunction(CurrentNodeId, 0);
    TreeParam = localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    TreeParentParam = localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    TreeSuperParentParam = localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    if (AllTreeParam['TreeParam'] != 'Customer Information') {
        breadCrumb_Reset();
    }
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Equipment Parent',
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': '',
            'TreeParam': TreeParam,
            'TreeParentParam': TreeParentParam,
            'TreeSuperParentParam': TreeSuperParentParam
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            if (document.getElementById("div_CTR_related_list")) {
                document.getElementById('div_CTR_related_list').innerHTML = datas;
                $('#div_CTR_related_list').css("display", "block");
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
            }
            if (data4 == "NORECORDS") {
                document.getElementById('div_CTR_related_list').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                $('#div_CTR_related_list').css("display", "block");
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
            }

            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.EQUIPMENT_ID || '';
						filterkeyData = row.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID || '';
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }
                        Equipment_child(filteredData,filterkeyData,$detail);
                    }
                });
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.EQUIPMENT_ID || '';
							filterkeyData = row.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            Equipment_child(filteredData,filterkeyData,$detail);
                        }
                    });
                }, 5000);
            }
            finally {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.EQUIPMENT_ID || '';
							filterkeyData = row.QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            Equipment_child(filteredData,filterkeyData,$detail);
                        }
                    });
                }, 5000);
            }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);

        });
        $(".JCLRgrip").mousedown(function () {

            $("thead.fullHeadFirst").css("cssText", "z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "none");

        });
        var arr_value = [];
        $(".JCLRgrip").mouseup(function () {

            var th_width_resize = [];
            $("#table_equipment_parent thead.fullHeadFirst tr th").each(function (index) {
                var wid = $(this).css("width");

                if (index == 0 || index == 1) {
                    th_width_resize.push("60px");
                } else {
                    th_width_resize.push(wid);
                }
            });


            $("thead.fullHeadFirst").css("cssText", "position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "table-header-group");

            var txt_alg = []
            $('table#table_equipment_parent thead.fullHeadSecond tr th').each(function (index) {
                var a = $(this).css('text-align');
                txt_alg.push(a);
            });

            $("#table_equipment_parent thead.fullHeadFirst tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });
            $("#table_equipment_parent thead.fullHeadSecond tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });



            $('div[id^=listBoxRelatedMutipleCheckBoxDrop_]').each(function (index) {

                var avoid_set = 0;
                var listdrop_disp = $(this).css('display');

                if (listdrop_disp == 'block') {
                    var cur_grid = $(this).attr('id');

                    var get_id = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').attr('id');

                    var insert_data = cur_grid + '|' + get_id;

                    if (arr_value.indexOf(insert_data) !== -1) {
                        delete arr_value[insert_data];
                        const index = arr_value.indexOf(insert_data);
                        if (index > -1) {
                            arr_value.splice(index, 1);
                        }

                        avoid_set = 1;
                    }
                    else {
                        arr_value.push(insert_data);
                    }

                    if (avoid_set == 0) {
                        var left_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left');

                        if (left_drop) {
                            left_drop = left_drop.split('px');
                            left_drop = parseInt(left_drop[0]) - 1;

                        }

                        left_drop = left_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left', left_drop);


                        var width_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').width();

                        width_drop = width_drop + 1;

                        width_drop = width_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').css('width', width_drop);
                    }

                }
            });


        });
    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_equipment_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}


function SendingEquipmentTreeTable() {
    breadCrumb_Reset();
    AllTreeParam = maintreeparamfunction(CurrentNodeId, 0);
    TreeParam = localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    TreeParentParam = localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    TreeSuperParentParam = localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Sending Equipment Parent',
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': '',
            'TreeParam': TreeParam,
            'TreeParentParam': TreeParentParam,
            'TreeSuperParentParam': TreeSuperParentParam
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            $("#div_CTR_related_list").css('display', 'block');
            if (document.getElementById("div_CTR_related_list")) {
                document.getElementById('div_CTR_related_list').innerHTML = datas;
                //$("#div_CTR_related_list").closest('.Related').css('display', 'block');
                $("#div_CTR_related_list").css('display', 'block');
            }
            if (data4 == "NORECORDS") {
                document.getElementById('div_CTR_related_list').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                //$("#div_CTR_related_list").closest('.Related').css('display', 'block');
                $("#div_CTR_related_list").css('display', 'block');
            }

            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.SND_EQUIPMENT_ID || '';
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }



                        Sending_Equipment_child(filteredData, $detail);
                    }
                });
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.SND_EQUIPMENT_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            Sending_Equipment_child(filteredData, $detail);
                        }
                    });
                }, 1000);
            }
            finally {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.SND_EQUIPMENT_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            Sending_Equipment_child(filteredData, $detail);
                        }
                    });
                }, 1000);
            }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);

        });
        $(".JCLRgrip").mousedown(function () {

            $("thead.fullHeadFirst").css("cssText", "z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "none");

        });
        var arr_value = [];
        $(".JCLRgrip").mouseup(function () {

            var th_width_resize = [];
            $("#table_equipment_parent thead.fullHeadFirst tr th").each(function (index) {
                var wid = $(this).css("width");

                if (index == 0 || index == 1) {
                    th_width_resize.push("60px");
                } else {
                    th_width_resize.push(wid);
                }
            });


            $("thead.fullHeadFirst").css("cssText", "position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "table-header-group");

            var txt_alg = []
            $('table#table_equipment_parent thead.fullHeadSecond tr th').each(function (index) {
                var a = $(this).css('text-align');
                txt_alg.push(a);
            });

            $("#table_equipment_parent thead.fullHeadFirst tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });
            $("#table_equipment_parent thead.fullHeadSecond tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });



            $('div[id^=listBoxRelatedMutipleCheckBoxDrop_]').each(function (index) {

                var avoid_set = 0;
                var listdrop_disp = $(this).css('display');

                if (listdrop_disp == 'block') {
                    var cur_grid = $(this).attr('id');

                    var get_id = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').attr('id');

                    var insert_data = cur_grid + '|' + get_id;

                    if (arr_value.indexOf(insert_data) !== -1) {
                        delete arr_value[insert_data];
                        const index = arr_value.indexOf(insert_data);
                        if (index > -1) {
                            arr_value.splice(index, 1);
                        }

                        avoid_set = 1;
                    }
                    else {
                        arr_value.push(insert_data);
                    }

                    if (avoid_set == 0) {
                        var left_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left');

                        if (left_drop) {
                            left_drop = left_drop.split('px');
                            left_drop = parseInt(left_drop[0]) - 1;

                        }

                        left_drop = left_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left', left_drop);


                        var width_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').width();

                        width_drop = width_drop + 1;

                        width_drop = width_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').css('width', width_drop);
                    }

                }
            });


        });
    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_sending_equipment_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}

function ContractEquipmentTreeTable() {
    AllTreeParam = maintreeparamfunction(CurrentNodeId, 0);
    TreeParam = localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    TreeParentParam = localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    TreeSuperParentParam = localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Contract Equipment Parent',
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': '',
            'TreeParam': TreeParam,
            'TreeParentParam': TreeParentParam,
            'TreeSuperParentParam': TreeSuperParentParam
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            if (document.getElementById("div_CTR_related_list")) {
                $("#div_CTR_related_list").css('display', 'block');
                document.getElementById('div_CTR_related_list').innerHTML = datas;
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
            }
            if (data4 == "NORECORDS") {
                document.getElementById('div_CTR_related_list').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
            }

            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.EQUIPMENT_ID || '';
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }



                        Contract_Equipment_child(filteredData, $detail);
                    }
                });
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.EQUIPMENT_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            Contract_Equipment_child(filteredData, $detail);
                        }
                    });
                }, 5000);
            }
            finally {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.EQUIPMENT_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            Contract_Equipment_child(filteredData, $detail);
                        }
                    });
                }, 5000);
            }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);

        });
        $(".JCLRgrip").mousedown(function () {

            $("thead.fullHeadFirst").css("cssText", "z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "none");

        });
        var arr_value = [];
        $(".JCLRgrip").mouseup(function () {

            var th_width_resize = [];
            $("#table_Contract_equipment_parent thead.fullHeadFirst tr th").each(function (index) {
                var wid = $(this).css("width");

                if (index == 0 || index == 1) {
                    th_width_resize.push("60px");
                } else {
                    th_width_resize.push(wid);
                }
            });


            $("thead.fullHeadFirst").css("cssText", "position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "table-header-group");

            var txt_alg = []
            $('table#table_equipment_parent thead.fullHeadSecond tr th').each(function (index) {
                var a = $(this).css('text-align');
                txt_alg.push(a);
            });

            $("#table_Contract_equipment_parent thead.fullHeadFirst tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });
            $("#table_Contract_equipment_parent thead.fullHeadSecond tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });



            $('div[id^=listBoxRelatedMutipleCheckBoxDrop_]').each(function (index) {

                var avoid_set = 0;
                var listdrop_disp = $(this).css('display');

                if (listdrop_disp == 'block') {
                    var cur_grid = $(this).attr('id');

                    var get_id = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').attr('id');

                    var insert_data = cur_grid + '|' + get_id;

                    if (arr_value.indexOf(insert_data) !== -1) {
                        delete arr_value[insert_data];
                        const index = arr_value.indexOf(insert_data);
                        if (index > -1) {
                            arr_value.splice(index, 1);
                        }

                        avoid_set = 1;
                    }
                    else {
                        arr_value.push(insert_data);
                    }

                    if (avoid_set == 0) {
                        var left_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left');

                        if (left_drop) {
                            left_drop = left_drop.split('px');
                            left_drop = parseInt(left_drop[0]) - 1;

                        }

                        left_drop = left_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left', left_drop);


                        var width_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').width();

                        width_drop = width_drop + 1;

                        width_drop = width_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').css('width', width_drop);
                    }

                }
            });


        });
    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_Contract_equipment_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}

function Equipment_child(filteredData,filterkeyData,$detail) {
    filteredData_1 = filteredData.split(">");
    filteredData_2 = filteredData_1[1].split("<");
    filteredData = filteredData_2[0];
	filterkeyData = filterkeyData.replace('SAQFEQ-', '')
    ChildEquipmentId = localStorage.setItem("ChildEquipmentId", filteredData)
    ChildEquipcpId = localStorage.setItem("ChildEquipcpId", filterkeyData)
	try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Equipment child',
            'ACTION': 'CHILDLOAD',
            'ATTRIBUTE_NAME': filteredData,
            'ATTRIBUTE_VALUE': '',
			'CPQ_TAB_ID': filterkeyData
        }, function (datachild) {

            datachld_table = datachild[0];
            datachld = datachild[1];
            datachld2 = datachild[2];
            datachld3 = datachild[3];
            datachld4 = datachild[4];
            datachld5 = datachild[5];
            datachld6 = datachild[6];
            datachld7 = datachild[7];
            datachld8 = datachild[8];
            datachld9 = datachild[9];
            datachld10 = datachild[10];
            datachld11 = datachild[11];
            if (datachld4 == "NORECORDS") {
                $detail.html('<div class="noRecDisp noRecDisp1">No Records to Display</div>')
            }
            else {
                $detail.html(datachld_table).find('table#' + datachld2).bootstrapTable({
                    data: datachld,
                });
            }
            $('#' + datachld2).after(datachld10);
            eval(datachld9);
            eval(datachld3);
            eval(datachld5);
            if (localStorage.getItem("currentSubTab") == 'Receiving Equipment' && AllTreeParam['TreeParam'] == 'Customer Information') {
                $('table#' + datachld2 + ' #CHAMBER').closest('tr').find('td:nth-child(3) input').removeAttr('disabled')
                $('table#' + datachld2 + ' #CHAMBER').closest('tr').find('td:nth-child(3) input').attr("onclick", "OnclickAssemblyEdit(this,'FTS')");
            }
        });
    } catch (e) {
        console.log(e);
    }
}
//Equipment Nested grid ends..
function Sending_Equipment_child(filteredData, $detail) {
    filteredData_1 = filteredData.split(">");
    filteredData_2 = filteredData_1[1].split("<");
    filteredData = filteredData_2[0];
    ChildEquipmentId = localStorage.setItem("ChildEquipmentId", filteredData)
    localStorage.setItem("Assembly_edit_mode", 'False')
    localStorage.setItem("Assembly_edit_mode_first", 'False')
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Sending Equipment child',
            'ACTION': 'CHILDLOAD',
            'ATTRIBUTE_NAME': filteredData,
            'ATTRIBUTE_VALUE': ''
        }, function (datachild) {

            datachld_table = datachild[0];
            datachld = datachild[1];
            datachld2 = datachild[2];
            datachld3 = datachild[3];
            datachld4 = datachild[4];
            datachld5 = datachild[5];
            datachld6 = datachild[6];
            datachld7 = datachild[7];
            datachld8 = datachild[8];
            datachld9 = datachild[9];
            datachld10 = datachild[10];
            datachld11 = datachild[11];
            datachld12 = datachild[12];
            if (datachld4 == "NORECORDS") {
                $detail.html('<div class="noRecDisp noRecDisp1">No Records to Display</div>')
            }
            else {
                $detail.html(datachld_table).find('table#' + datachld2).bootstrapTable({
                    data: datachld,
                });
            }
            localStorage.setItem('Assembly_table_id', datachld2)
            $('#' + datachld2).before(datachld12);
            $('#' + datachld2).after(datachld10);
            eval(datachld9);
            eval(datachld3);
            eval(datachld5);
        });
    } catch (e) {
        console.log(e);
    }
}
//Assembly grid edit in Sending Equipment starts ..
// function SendEqupAssemblyEdit() {
// 	$('.hyperlink').attr("disabled", "disabled");
// 	$('.hyperlink').addClass("disabledcolor");
// 	$("#assembly_edit ").css('display', 'none');
// 	$("#assembly_save ").css('display', 'block');
// 	$("#assembly_cancel ").css('display', 'block');
// 	localStorage.setItem("Assembly_edit_mode", 'True')
// 	localStorage.setItem("Assembly_edit_mode_first", 'True')
// 	localStorage.setItem("selected_list_assembly", '')
// 	localStorage.setItem("unselected_list_assembly", '')
// 	table_id = '#' + localStorage.getItem('Assembly_table_id')
// 	console.log('table_id', table_id)
// 	try {
// 		cpq.server.executeScript("CQASSMEDIT", {
// 			'ACTION': 'EDIT_ASSEMBLY',
// 			'Values': localStorage.getItem("ChildEquipmentId"),
// 			'TABNAME': 'Sending Equipment child',
// 		}, function (data) {
// 			data.forEach(function (ele) {
// 				$(table_id + ' #' + ele).closest('tr').find('td:nth-child(3) input').removeAttr('disabled')
// 				$(table_id + ' #' + ele).closest('tr').find('td:nth-child(3) input').attr("onclick", "OnclickAssemblyEdit(this)");


// 			});

// 		});

// 	} catch (e) {
// 		console.log(e);
// 	}

// 	//$(table_id+' #INCLUDED').removeAttr('disabled');

// }
//Assembly grid edit in Sending Equipment ends ...
function OnclickAssemblyEdit(ele, prod_type) {
    //console.log('ele--',ele)
    included_value = $(ele).prop("checked")
    selected_value = ''
    assembly_index = $(ele).closest('table').find('[data-field="ASSEMBLY_ID"]').index() + 1;
    selected_assembly = $(ele).closest('tr').find('td:nth-child(' + assembly_index + ')').text().trim()
    fab_index = ''
    selected_index = ''
    selected_fab = ''
    if (prod_type == 'FTS') {

        fab_index = $(ele).closest('table').find('[data-field="FABLOCATION_ID"]').index() + 1;
        if (localStorage.getItem("currentSubTab") == 'Equipment') {
            selected_index = $(ele).closest('table').find('[data-field="QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID"]').index() + 1;
            selected_equipment = localStorage.getItem("CoveredobjectchildEquipmentId")
        }
        else {
            selected_index = $(ele).closest('table').find('[data-field="QUOTE_FAB_LOCATION_EQUIPMENTS_RECORD_ID"]').index() + 1;
            selected_equipment = localStorage.getItem("ChildEquipmentId")
        }
        selected_fab = $(ele).closest('tr').find('td:nth-child(' + fab_index + ')').text().trim()
        selected_value = $(ele).closest('tr').find('td:nth-child(' + selected_index + ')').text().trim()
    }
    //A055S000P01-16760
    else if (prod_type == 'TKM') {
        selected_index = $(ele).closest('table').find('[data-field="QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID"]').index() + 1;
        if (localStorage.getItem("currentSubTab") == 'Equipment') {
            selected_equipment = localStorage.getItem("CoveredobjectchildEquipmentId")
        }
        if (localStorage.getItem("currentSubTab") == 'Events') {
            equipment_index = $(ele).closest('table').find('[data-field="EQUIPMENT_ID"]').index() + 1;
            selected_equipment = $(ele).closest('tr').find('td:nth-child(' + equipment_index + ')').text().trim()
            selected_value = $(ele).closest('tr').find('td:nth-child(' + selected_index + ')').text().trim()
        }
    }
    else {
        selected_index = $(ele).closest('table').find('[data-field="QUOTE_SERVICE_COVERED_OBJECT_ASSEMBLIES_RECORD_ID"]').index() + 1;
        if (localStorage.getItem("currentSubTab") == 'Equipment') {
            selected_equipment = localStorage.getItem("CoveredobjectchildEquipmentId")
            selected_value = $(ele).closest('tr').find('td:nth-child(' + selected_index + ')').text().trim()
        }

    }


    try {
        cpq.server.executeScript("CQASSMEDIT", {
            'ACTION': 'SAVE_ASSEMBLY',
            'selected_assembly': selected_assembly,
            'selected_fab': selected_fab,
            'equipment_id': selected_equipment,
            'included_value': included_value,
            'subtab': localStorage.getItem("currentSubTab"),
            'selected_value': selected_value,
            'prod_type': prod_type,
        }, function (data) {
            // localStorage.setItem("selected_list_assembly",'')
            // localStorage.setItem("unselected_list_assembly",'')
            //$("#MM_ALL_REFRESH").click();
            //$('#cont_viewModalSection').css('display', 'none');
            // localStorage.setItem("AddFab", "yes")
            /*localStorage.setItem("left_tree_refresh", "yes")
            CommonLeftView();
            $('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
            silent: true
            }]);
            $('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
                silent: true
            }]);
            loadRelatedList("SYOBJR-98789","div_CTR_related_list")*/
        });
        //subTabDetails(localStorage.getItem("currentSubTab"), 'Related', CurrentRecordId)
    } catch (e) {
        console.log(e);
    }

    // if (localStorage.getItem("Assembly_edit_mode_first") == 'True'){
    // 	var unselected_list =[]
    // 	var selected_list = []
    // 	localStorage.setItem("Assembly_edit_mode_first",'False')
    // }
    // else{
    // 	unselected_list = JSON.parse(localStorage.getItem("unselected_list_assembly") )
    // 	selected_list = JSON.parse(localStorage.getItem("selected_list_assembly") )

    // }


    // var sel_val = $(ele).closest('tr').find('td:nth-child(4)').text().trim()
    // if($(ele).prop("checked") == true){
    // 	if (localStorage.getItem("unselected_list_assembly") ){
    // 	    var arr_list = JSON.parse(localStorage.getItem("unselected_list_assembly") )
    // 		att_index = arr_list.indexOf(sel_val )
    // 		if(att_index !== -1) {
    // 			console.log('att_index',att_index)
    // 			arr_list.splice(att_index, 1);
    // 			unselected_list = arr_list
    // 		} 
    // 	}
    // 	selected_list.push(sel_val);
    // 	//console.log("Checkbox is checked.");
    // }
    // else if($(ele).prop("checked") == false){

    // 	if (localStorage.getItem("selected_list_assembly") ){
    // 	    var arr_list = JSON.parse(localStorage.getItem("selected_list_assembly") )
    // 		att_index = arr_list.indexOf(sel_val )
    // 		if(att_index !== -1) {
    // 			console.log('att_index',att_index)
    // 			arr_list.splice(att_index, 1);
    // 			selected_list = arr_list
    // 		} 
    // 	}
    // 	unselected_list.push(sel_val);
    // 	//console.log("Checkbox is unchecked.");
    // }
    // console.log('onlcik fn--',ele.id)
    // localStorage.setItem("selected_list_assembly",JSON.stringify(selected_list))
    // localStorage.setItem("unselected_list_assembly",JSON.stringify(unselected_list))

}
//Assembly grid save in Sending Equipment starts ...
function SendEqupAssemblySave() {
    $('.hyperlink').removeAttr("disabled");
    $('.hyperlink').removeClass("disabledcolor")
    localStorage.setItem("Assembly_edit_mode_first", 'False')
    localStorage.setItem("Assembly_edit_mode", 'False')
    var selectedAssemblies_list = [];
    var unselected_list_assembly = [];

    selectedAssemblies_list = localStorage.getItem("selected_list_assembly")
    unselected_list_assembly = localStorage.getItem("unselected_list_assembly")
    if (selectedAssemblies_list == '') {
        selectedAssemblies_list = []
    }

    else {
        selectedAssemblies_list = JSON.parse(localStorage.getItem("selected_list_assembly"))
    }
    if (unselected_list_assembly == '') {
        unselected_list_assembly = []
    }
    else {
        unselected_list_assembly = JSON.parse(localStorage.getItem("unselected_list_assembly"))
    }
    $("#assembly_edit ").css('display', 'block');
    $("#assembly_save ").css('display', 'none');
    $("#assembly_cancel ").css('display', 'none');

    //selectedFabs = JSON.parse(localStorage.getItem("selected_items"));
    var selectAll = false;
    var A_Keys = [];
    var A_Values = [];
    table_id = '#' + localStorage.getItem('Assembly_table_id');
    $(table_id + ' #INCLUDED').attr('disabled', 'disabled');
    /*$(table_id).find('[type="checkbox"]:checked').map(function () {
        if ($(this).attr('name') == 'btSelectAll'){
            selectAll = true;
        }
        var sel_val = $(this).closest('tr').find('td:nth-child(4)').text()
        if (sel_val != '') {
            selectedAssemblies_list.push(sel_val.trim());
        }
    });   
	
    /*$(table_id+' .filter-control').each(function () {
        values = this.firstElementChild.className;
        if (values.indexOf('control') !== -1 && values.indexOf('RelatedMutipleCheckBoxDrop_') === -1) {
            x = values.split(' ')[1];
            y = x.split("-").slice(-1)[0];
            xyz = $(table_id+' .' + x).val();
            if ($.inArray(y, A_Keys) === -1) {
                A_Keys.push(y);
                A_Values.push(xyz)
            };
        }
    });*/
    try {
        cpq.server.executeScript("CQASSMEDIT", {
            'ACTION': 'UPDATE_ASSEMBLY',
            'Values': JSON.stringify(selectedAssemblies_list),
            'unselected_list': JSON.stringify(unselected_list_assembly),
            'TABNAME': 'Sending Equipment child',
            'equipment_id': localStorage.getItem("ChildEquipmentId"),
        }, function (data) {
            localStorage.setItem("selected_list_assembly", '')
            localStorage.setItem("unselected_list_assembly", '')
            //$("#MM_ALL_REFRESH").click();
            //$('#cont_viewModalSection').css('display', 'none');
            // localStorage.setItem("AddFab", "yes")
            /*localStorage.setItem("left_tree_refresh", "yes")
            CommonLeftView();
            $('#commontreeview').treeview('revealNode', [parseInt(CurrentNodeId), {
            silent: true
            }]);
            $('#commontreeview').treeview('selectNode', [parseInt(CurrentNodeId), {
                silent: true
            }]);
            loadRelatedList("SYOBJR-98789","div_CTR_related_list")*/
        });

    } catch (e) {
        console.log(e);
    }

}

//Assembly grid save in Sending Equipment ends ...

function SendEqupAssemblyCancel() {
    $('.hyperlink').removeAttr("disabled");
    $('.hyperlink').removeClass("disabledcolor")
    localStorage.setItem("Assembly_edit_mode_first", 'False')
    localStorage.setItem("Assembly_edit_mode", 'False')
    $("#assembly_edit ").css('display', 'block');
    $("#assembly_save ").css('display', 'none');
    $("#assembly_cancel ").css('display', 'none');
    localStorage.setItem("selected_list_assembly", '')
    localStorage.setItem("unselected_list_assembly", '')
    cancel_table_id = '#' + localStorage.getItem('Assembly_table_id');
    $(cancel_table_id + ' #INCLUDED').attr('disabled', 'disabled');
    active_sub_tab = $('#COMMON_TABS ul li.active').attr('onclick')
    eval(active_sub_tab)
}


//Preventive Maintainence grid starts..
function PreventiveMaintainenceTreeTable() {
    $('#cancelButton').css('display', 'none');
    $('#saveButton').css('display', 'none');
    $('#ADDNEW__SYOBJR_00011_SYOBJ_00974').css('display', 'block');
    Assembly_Id = localStorage.getItem("AssemblyIdValue")
    Equipment_Id = localStorage.getItem("EquipmentIdValue")
    Values = localStorage.getItem("EquipmentSerialNumber")
    AllTreeParam = maintreeparamfunction(CurrentNodeId, 0);
    TreeParam = localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    TreeParentParam = localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    TreeSuperParentParam = localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Preventive Maintainence Parent',
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': '',
            'ASSEMBLYID': Assembly_Id,
            'EQUIPMENTID': Equipment_Id,
            'TreeParam': TreeParam,
            'TreeParentParam': TreeParentParam,
            'TreeSuperParentParam': TreeSuperParentParam
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            $('#div_CTR_related_list').css('display', 'none');
            if (data4 == "NORECORDS") {
                document.getElementById('TREE_div').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                $("#div_CTR_PM_Events").closest('.Related').css('display', 'block');
                breadCrumb_Reset();
                Pmevents_breadcrumb(Values);
                Pmevents_breadcrumb(Assembly_Id);
            }
            else if (document.getElementById("TREE_div")) {
                document.getElementById('TREE_div').innerHTML = datas;
                $("#TREE_div").closest('.Related').css('display', 'block');
                breadCrumb_Reset();
                Pmevents_breadcrumb(Values);
                Pmevents_breadcrumb(Assembly_Id);
            }
            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        //filteredData = row.PM_ID || ''+'-'+ row.KIT_ID || ''+'-'+ row.KIT_NUMBER || '';
                        filteredData = row.PM_ID || '';
                        filteredData1 = row.KIT_ID || '';
                        filteredData2 = row.KIT_NUMBER || '';
                        Assembly_Id_Value=row.ASSEMBLY_ID || '';
                        Equipment_Id_Value=row.EQUIPMENT_ID || '';
                        Assembly_Id = localStorage.setItem("AssemblyIdValue",Assembly_Id_Value);
                        Equipment_Id = localStorage.setItem("EquipmentIdValue",Equipment_Id_Value);
                        Kit_Id_Value=localStorage.setItem("KIT_ID",filteredData1);
                        Kit_Number_Value=localStorage.setItem("KIT_NUMBER",filteredData2);
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }
                        Preventive_Maintainence_child(filteredData, filteredData1, filteredData2, $detail);
                    }
                });
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            //filteredData = row.PM_ID || ''+'-'+ row.KIT_ID || ''+'-'+ row.KIT_NUMBER || '';
                            filteredData = row.PM_ID || '';
                            filteredData1 = row.KIT_ID || '';
                            filteredData2 = row.KIT_NUMBER || '';
                            Assembly_Id_Value=row.ASSEMBLY_ID || '';
                            Equipment_Id_Value=row.EQUIPMENT_ID || '';
                            Assembly_Id = localStorage.setItem("AssemblyIdValue",Assembly_Id_Value);
                            Equipment_Id = localStorage.setItem("EquipmentIdValue",Equipment_Id_Value);
                            Kit_Id_Value=localStorage.setItem("KIT_ID",filteredData1);
                            Kit_Number_Value=localStorage.setItem("KIT_NUMBER",filteredData2);
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            Preventive_Maintainence_child(filteredData, filteredData1, filteredData2, $detail);
                        }
                    });
                }, 5000);
            }
            finally {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            //filteredData = row.PM_ID || ''+'-'+ row.KIT_ID || ''+'-'+ row.KIT_NUMBER || '';
                            filteredData = row.PM_ID || '';
                            filteredData1 = row.KIT_ID || '';
                            filteredData2 = row.KIT_NUMBER || '';
                            Assembly_Id_Value=row.ASSEMBLY_ID || '';
                            Equipment_Id_Value=row.EQUIPMENT_ID || '';
                            Assembly_Id = localStorage.setItem("AssemblyIdValue",Assembly_Id_Value);
                            Equipment_Id = localStorage.setItem("EquipmentIdValue",Equipment_Id_Value);
                            Kit_Id_Value=localStorage.setItem("KIT_ID",filteredData1);
                            Kit_Number_Value=localStorage.setItem("KIT_NUMBER",filteredData2);
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            Preventive_Maintainence_child(filteredData, filteredData1, filteredData2, $detail);
                        }
                    });
                }, 5000);
            }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);

        });
        $(".JCLRgrip").mousedown(function () {

            $("thead.fullHeadFirst").css("cssText", "z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "none");

        });
        var arr_value = [];
        $(".JCLRgrip").mouseup(function () {

            var th_width_resize = [];
            $("#table_Preventive_Maintainence_parent thead.fullHeadFirst tr th").each(function (index) {
                var wid = $(this).css("width");

                if (index == 0 || index == 1) {
                    th_width_resize.push("60px");
                } else {
                    th_width_resize.push(wid);
                }
            });


            $("thead.fullHeadFirst").css("cssText", "position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "table-header-group");

            var txt_alg = []
            $('table#table_Preventive_Maintainence_parent thead.fullHeadSecond tr th').each(function (index) {
                var a = $(this).css('text-align');
                txt_alg.push(a);
            });

            $("#table_Preventive_Maintainence_parent thead.fullHeadFirst tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });
            $("#table_Preventive_Maintainence_parent thead.fullHeadSecond tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });



            $('div[id^=listBoxRelatedMutipleCheckBoxDrop_]').each(function (index) {

                var avoid_set = 0;
                var listdrop_disp = $(this).css('display');

                if (listdrop_disp == 'block') {
                    var cur_grid = $(this).attr('id');

                    var get_id = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').attr('id');

                    var insert_data = cur_grid + '|' + get_id;

                    if (arr_value.indexOf(insert_data) !== -1) {
                        delete arr_value[insert_data];
                        const index = arr_value.indexOf(insert_data);
                        if (index > -1) {
                            arr_value.splice(index, 1);
                        }

                        avoid_set = 1;
                    }
                    else {
                        arr_value.push(insert_data);
                    }

                    if (avoid_set == 0) {
                        var left_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left');

                        if (left_drop) {
                            left_drop = left_drop.split('px');
                            left_drop = parseInt(left_drop[0]) - 1;

                        }

                        left_drop = left_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left', left_drop);


                        var width_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').width();

                        width_drop = width_drop + 1;

                        width_drop = width_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').css('width', width_drop);
                    }

                }
            });
        });
    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_Preventive_Maintainence_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}

function Preventive_Maintainence_child(filteredData, filteredData1, filteredData2, $detail) {
    Assembly_Id = localStorage.getItem("AssemblyIdValue")
    Equipment_Id = localStorage.getItem("EquipmentIdValue")
    localStorage.setItem("PM_ID", filteredData)
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Preventive Maintainence child',
            'ACTION': 'CHILDLOAD',
            'ASSEMBLYID': Assembly_Id,
            'EQUIPMENTID': Equipment_Id,
            'ATTRIBUTE_NAME': filteredData,
            'KITID': filteredData1,
            'KITNUMBER': filteredData2,
            'ATTRIBUTE_VALUE': ''
        }, function (datachild) {

            datachld_table = datachild[0];
            datachld = datachild[1];
            datachld2 = datachild[2];
            datachld3 = datachild[3];
            datachld4 = datachild[4];
            datachld5 = datachild[5];
            datachld6 = datachild[6];
            datachld7 = datachild[7];
            datachld8 = datachild[8];
            datachld9 = datachild[9];
            datachld10 = datachild[10];
            datachld11 = datachild[11];
            if (datachld4 == "NORECORDS") {
                $detail.html('<div class="noRecDisp noRecDisp1">No Records to Display</div>')
            }
            else {
                $detail.html(datachld_table).find('table#' + datachld2).bootstrapTable({
                    data: datachld,
                });
            }
            $('#' + datachld2).after(datachld10);
            eval(datachld9);
            eval(datachld3);
            eval(datachld5);
        });
    } catch (e) {
        console.log(e);
    }
}
//Preventive Maintainence grid ends..
//Tool Assemblies Nested grid starts..
function AssembliesTreeTable() {
    var recid = localStorage.getItem("CurrentRecordId");

    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Assemblies Parent',
            'RECORD_ID': recid,
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': ''
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            if (document.getElementById("div_CTR_related_list")) {
                document.getElementById('div_CTR_related_list').innerHTML = datas;
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
                $("#div_CTR_related_list").css('display', 'block');
            }
            if (data4 == "NORECORDS") {
                document.getElementById('div_CTR_related_list').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
                $("#div_CTR_related_list").css('display', 'block');
            }

            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.EQUIPMENT_ID || '';
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }



                        Assemblies_child(filteredData, $detail);
                    }
                });
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.EQUIPMENT_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            Assemblies_child(filteredData, $detail);
                        }
                    });
                }, 5000);
            }
            // Hided Equipment assembly binding issue
            // finally {
            // 	setTimeout(function () {
            // 		$('#' + data2).bootstrapTable({
            // 			data: data1,
            // 			onExpandRow: function (index, row, $detail) {
            // 				filteredData = row.EQUIPMENT_ID || '';
            // 				if (filteredData == '') {
            // 					filteredData = row.REC_ID
            // 				}

            // 				Assemblies_child(filteredData, $detail);
            // 			}
            // 		});
            // 	}, 5000);
            // }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);

        });
        $(".JCLRgrip").mousedown(function () {

            $("thead.fullHeadFirst").css("cssText", "z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "none");

        });
        var arr_value = [];
        $(".JCLRgrip").mouseup(function () {

            var th_width_resize = [];
            $("#table_assemblies_parent thead.fullHeadFirst tr th").each(function (index) {
                var wid = $(this).css("width");

                if (index == 0 || index == 1) {
                    th_width_resize.push("60px");
                } else {
                    th_width_resize.push(wid);
                }
            });


            $("thead.fullHeadFirst").css("cssText", "position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "table-header-group");

            var txt_alg = []
            $('table#table_assemblies_parent thead.fullHeadSecond tr th').each(function (index) {
                var a = $(this).css('text-align');
                txt_alg.push(a);
            });

            $("#table_equipment_parent thead.fullHeadFirst tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });
            $("#table_assemblies_parent thead.fullHeadSecond tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });



            $('div[id^=listBoxRelatedMutipleCheckBoxDrop_]').each(function (index) {

                var avoid_set = 0;
                var listdrop_disp = $(this).css('display');

                if (listdrop_disp == 'block') {
                    var cur_grid = $(this).attr('id');

                    var get_id = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').attr('id');

                    var insert_data = cur_grid + '|' + get_id;

                    if (arr_value.indexOf(insert_data) !== -1) {
                        delete arr_value[insert_data];
                        const index = arr_value.indexOf(insert_data);
                        if (index > -1) {
                            arr_value.splice(index, 1);
                        }

                        avoid_set = 1;
                    }
                    else {
                        arr_value.push(insert_data);
                    }

                    if (avoid_set == 0) {
                        var left_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left');

                        if (left_drop) {
                            left_drop = left_drop.split('px');
                            left_drop = parseInt(left_drop[0]) - 1;

                        }

                        left_drop = left_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left', left_drop);


                        var width_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').width();

                        width_drop = width_drop + 1;

                        width_drop = width_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').css('width', width_drop);
                    }

                }
            });


        });
    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_assemblies_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}

function ContractAssembliesTreeTable() {
    var recid = localStorage.getItem("CurrentRecordId");

    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Contract Assemblies Parent',
            'RECORD_ID': recid,
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': ''
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            // if (document.getElementById("div_CTR_Assemblies")) {
            // 	document.getElementById('div_CTR_Assemblies').innerHTML = datas;
            // 	$("#div_CTR_Assemblies").closest('.Related').css('display', 'block');
            // }
            // if (data4 == "NORECORDS"){
            // 	document.getElementById('div_CTR_Assemblies').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
            // 	$("#div_CTR_Assemblies").closest('.Related').css('display', 'block');
            // }
            if (document.getElementById("div_CTR_related_list")) {
                document.getElementById('div_CTR_related_list').innerHTML = datas;
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
                $("#div_CTR_related_list").css('display', 'block');
            }
            if (data4 == "NORECORDS") {
                document.getElementById('div_CTR_related_list').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
                $("#div_CTR_related_list").css('display', 'block');
            }

            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.EQUIPMENT_ID || '';
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }



                        Assemblies_child(filteredData, $detail);
                    }
                });
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.EQUIPMENT_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            ContractAssemblies_child(filteredData, $detail);
                        }
                    });
                }, 5000);
            }
            finally {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.EQUIPMENT_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            ContractAssemblies_child(filteredData, $detail);
                        }
                    });
                }, 5000);
            }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);

        });
        $(".JCLRgrip").mousedown(function () {

            $("thead.fullHeadFirst").css("cssText", "z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "none");

        });
        var arr_value = [];
        $(".JCLRgrip").mouseup(function () {

            var th_width_resize = [];
            $("#table_assemblies_parent thead.fullHeadFirst tr th").each(function (index) {
                var wid = $(this).css("width");

                if (index == 0 || index == 1) {
                    th_width_resize.push("60px");
                } else {
                    th_width_resize.push(wid);
                }
            });


            $("thead.fullHeadFirst").css("cssText", "position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "table-header-group");

            var txt_alg = []
            $('table#table_assemblies_parent thead.fullHeadSecond tr th').each(function (index) {
                var a = $(this).css('text-align');
                txt_alg.push(a);
            });

            $("#table_equipment_parent thead.fullHeadFirst tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });
            $("#table_assemblies_parent thead.fullHeadSecond tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });



            $('div[id^=listBoxRelatedMutipleCheckBoxDrop_]').each(function (index) {

                var avoid_set = 0;
                var listdrop_disp = $(this).css('display');

                if (listdrop_disp == 'block') {
                    var cur_grid = $(this).attr('id');

                    var get_id = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').attr('id');

                    var insert_data = cur_grid + '|' + get_id;

                    if (arr_value.indexOf(insert_data) !== -1) {
                        delete arr_value[insert_data];
                        const index = arr_value.indexOf(insert_data);
                        if (index > -1) {
                            arr_value.splice(index, 1);
                        }

                        avoid_set = 1;
                    }
                    else {
                        arr_value.push(insert_data);
                    }

                    if (avoid_set == 0) {
                        var left_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left');

                        if (left_drop) {
                            left_drop = left_drop.split('px');
                            left_drop = parseInt(left_drop[0]) - 1;

                        }

                        left_drop = left_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left', left_drop);


                        var width_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').width();

                        width_drop = width_drop + 1;

                        width_drop = width_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').css('width', width_drop);
                    }

                }
            });


        });
    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_assemblies_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}

function Assemblies_child(filteredData, $detail) {
    var recid = localStorage.getItem("CurrentRecordId");
    localStorage.setItem('CoveredobjectchildEquipmentId', filteredData);
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Assemblies Child',
            'RECORD_ID': recid,
            'ACTION': 'CHILDLOAD',
            'ATTRIBUTE_NAME': filteredData,
            'ATTRIBUTE_VALUE': ''
        }, function (datachild) {

            datachld_table = datachild[0];
            datachld = datachild[1];
            datachld2 = datachild[2];
            datachld3 = datachild[3];
            datachld4 = datachild[4];
            datachld5 = datachild[5];
            datachld6 = datachild[6];
            datachld7 = datachild[7];
            datachld8 = datachild[8];
            datachld9 = datachild[9];
            datachld10 = datachild[10];
            datachld11 = datachild[11];
            if (datachld4 == "NORECORDS") {
                $detail.html('<div class="noRecDisp noRecDisp1">No Records to Display</div>')
            }
            else {
                $detail.html(datachld_table).find('table#' + datachld2).bootstrapTable({
                    data: datachld,
                });
            }
            $('#' + datachld2).after(datachld10);
            eval(datachld9);
            eval(datachld3);
            eval(datachld5);
        });
    } catch (e) {
        console.log(e);
    }
}

//fts Assembly nested grid...child table...

function fts_assemblies_child(filteredData, $detail) {
    filteredData_1 = filteredData.split(">");
    filteredData_2 = filteredData_1[1].split("<");
    filteredData = filteredData_2[0];
    var recid = localStorage.getItem("CurrentRecordId");
    localStorage.setItem('CoveredobjectchildEquipmentId', filteredData);
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Fts Assemblies Child',
            'RECORD_ID': recid,
            'ACTION': 'CHILDLOAD',
            'ATTRIBUTE_NAME': filteredData,
            'ATTRIBUTE_VALUE': ''
        }, function (datachild) {

            datachld_table = datachild[0];
            datachld = datachild[1];
            datachld2 = datachild[2];
            datachld3 = datachild[3];
            datachld4 = datachild[4];
            datachld5 = datachild[5];
            datachld6 = datachild[6];
            datachld7 = datachild[7];
            datachld8 = datachild[8];
            datachld9 = datachild[9];
            datachld10 = datachild[10];
            datachld11 = datachild[11];
            //INC08691509 M
			datachld12 = datachild[12];
			//INC08691509 M
            if (datachld4 == "NORECORDS") {
                $detail.html('<div class="noRecDisp noRecDisp1">No Records to Display</div>')
            }
            else {
                $detail.html(datachld_table).find('table#' + datachld2).bootstrapTable({
                    data: datachld,
                });
            }
            $('#' + datachld2).after(datachld10);
            eval(datachld9);
            eval(datachld3);
            eval(datachld5);
            // making included column as editable for non tool based in assembly grid A055S000P01-16760..
            $('table#' + datachld2).closest('tr').find('td:nth-child(3) input').removeAttr('disabled')
            $('table#' + datachld2).closest('tr').find('td:nth-child(3) input').attr("onclick", "OnclickAssemblyEdit(this,'TKM')");
            //INC08691509 M
			if (datachld12 == "DISABLE_INCLUDE_CHECK") {
                $("#table_covered_obj_parent #INCLUDED").attr("disabled", "disabled");
            }
            else {
                $("#table_covered_obj_parent #INCLUDED").removeAttr("disabled");
            }
			//INC08691509 M
        });
    } catch (e) {
        console.log(e);
    }
}




function CoveredObj_child(filteredData,filterkeyData,$detail) {
    filteredData_1 = filteredData.split(">");
    filteredData_2 = filteredData_1[1].split("<");
    filteredData = filteredData_2[0];
    var recid = localStorage.getItem("CurrentRecordId");
	filterkeyData = filterkeyData.replace('SAQSCO-', '')
    EquipmentId = localStorage.setItem("CoveredobjectchildEquipmentId", filteredData);
	EquipcpId = localStorage.setItem("CoveredobjectchildEquipmentcpId", filterkeyData)
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Covered Object Child',
            'RECORD_ID': recid,
            'ACTION': 'CHILDLOAD',
            'ATTRIBUTE_NAME': filteredData,
            'ATTRIBUTE_VALUE': '',
			'CPQ_TAB_ID': filterkeyData
			
        }, function (datachild) {

            datachld_table = datachild[0];
            datachld = datachild[1];
            datachld2 = datachild[2];
            datachld3 = datachild[3];
            datachld4 = datachild[4];
            datachld5 = datachild[5];
            datachld6 = datachild[6];
            datachld7 = datachild[7];
            datachld8 = datachild[8];
            datachld9 = datachild[9];
            datachld10 = datachild[10];
            datachld11 = datachild[11];
            if (datachld4 == "NORECORDS") {
                $detail.html('<div class="noRecDisp noRecDisp1">No Records to Display</div>')
            }
            else {
                $detail.html(datachld_table).find('table#' + datachld2).bootstrapTable({
                    data: datachld,
                });
            }
            $('#' + datachld2).after(datachld10);
            eval(datachld9);
            eval(datachld3);
            eval(datachld5);
            //adding editability for chamber based in assembly grid 
            //A055S000P01-20837 Start - M
            if (localStorage.getItem("currentSubTab") == 'Equipment' && AllTreeParam['TreeParentLevel1'] == 'Product Offerings' && (AllTreeParam['TreeParam'] == 'Z0007' || AllTreeParam['TreeParam'] == 'Z0006') && $('.quote_type_value abbr').text().toUpperCase() == 'CHAMBER BASED') {
            //A055S000P01-20837 End - M
                $('table#' + datachld2 + ' #CHAMBER').closest('tr').find('td:nth-child(3) input').removeAttr('disabled')
                $('table#' + datachld2 + ' #CHAMBER').closest('tr').find('td:nth-child(3) input').attr("onclick", "OnclickAssemblyEdit(this,'FTS')");
            }
            else if (localStorage.getItem("currentSubTab") == 'Equipment' && AllTreeParam['TreeParentLevel1'] == 'Product Offerings' && AllTreeParam['TreeParam'] == 'Z0090' && $('.quote_type_value abbr').text().toUpperCase() == 'CHAMBER BASED') {
                $('table#' + datachld2 + ' #INCLUDED').closest('tr').find('td:nth-child(3) input').removeAttr('disabled')
                $('table#' + datachld2 + ' #INCLUDED').closest('tr').find('td:nth-child(3) input').attr("onclick", "OnclickAssemblyEdit(this,'COMPLEMENTARY PRODUCTS')");
            }
        });
    } catch (e) {
        console.log(e);
    }
}
//A055S000P01-20982
function CoveredObjTreeTable(subTabName = "") {
    quote_type = $('.quote_type_value').text();
    quote_type = quote_type.toUpperCase();
    breadCrumb_Reset();
    var recid = localStorage.getItem("CurrentRecordId");
    var active_subtab = subTabName
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Covered Object Parent',
            'RECORD_ID': recid,
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': '',
            'active_subtab': active_subtab
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            data12 = dataset[12];
            if (data12 == "True") {
                $('div#COMMON_TABS').find("li a:contains('Add On Products')").parent().css("display", "block");
            }
            else {
                $('div#COMMON_TABS').find("li a:contains('Add On Products')").parent().css("display", "none");
            }
            if (document.getElementById("div_CTR_related_list")) {
                // document.getElementById('div_CTR_Covered_Objects').innerHTML = datas;
                // $("#div_CTR_Covered_Objects").closest('.Related').css('display', 'block');
                document.getElementById('div_CTR_related_list').innerHTML = datas;
                $("#div_CTR_related_list").css('display', 'block');
            }
            if (data4 == "NORECORDS") {
                // document.getElementById('div_CTR_Covered_Objects').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                // $("#div_CTR_Covered_Objects").closest('.Related').css('display', 'block');
                document.getElementById('div_CTR_related_list').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                $("#div_CTR_related_list").css('display', 'block');
            }

            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.EQUIPMENT_ID || '';
                        filterkeyData = row.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID || '';
						if (filteredData == '') {
                            filteredData = row.REC_ID
                        }
                        if (quote_type != 'TOOL BASED' && quote_type != 'CHAMBER BASED' && quote_type != '' && quote_type != 'LABOR BASED') {
                            fts_assemblies_child(filteredData, $detail);
                        }
                        else {
                            CoveredObj_child(filteredData,filterkeyData,$detail);
                        }
                    }
                });
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.EQUIPMENT_ID || '';
							filterkeyData = row.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            if (quote_type != 'TOOL BASED' && quote_type != 'CHAMBER BASED' && quote_type != '' && quote_type != 'LABOR BASED') {
                                fts_assemblies_child(filteredData, $detail);
                            }
                            else {
                                CoveredObj_child(filteredData,filterkeyData,$detail);
                            }
                        }
                    });
                }, 5000);
            }
            finally {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.EQUIPMENT_ID || '';
                            filterkeyData = row.QUOTE_SERVICE_COVERED_OBJECTS_RECORD_ID || '';
							if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            if (quote_type != 'TOOL BASED' && quote_type != 'CHAMBER BASED' && quote_type != '' && quote_type != 'LABOR BASED') {
                                fts_assemblies_child(filteredData, $detail);
                            }
                            else {
                                CoveredObj_child(filteredData,filterkeyData,$detail);
                            }
                        }
                    });
                }, 5000);
            }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);

        });
        $(".JCLRgrip").mousedown(function () {

            $("thead.fullHeadFirst").css("cssText", "z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "none");

        });
        var arr_value = [];
        $(".JCLRgrip").mouseup(function () {

            var th_width_resize = [];
            $("#table_covered_obj_parent thead.fullHeadFirst tr th").each(function (index) {
                var wid = $(this).css("width");

                if (index == 0 || index == 1) {
                    th_width_resize.push("60px");
                } else {
                    th_width_resize.push(wid);
                }
            });


            $("thead.fullHeadFirst").css("cssText", "position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "table-header-group");

            var txt_alg = []
            $('table#table_covered_obj_parent thead.fullHeadSecond tr th').each(function (index) {
                var a = $(this).css('text-align');
                txt_alg.push(a);
            });

            $("#table_covered_obj_parent thead.fullHeadFirst tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });
            $("#table_covered_obj_parent thead.fullHeadSecond tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });



            $('div[id^=listBoxRelatedMutipleCheckBoxDrop_]').each(function (index) {

                var avoid_set = 0;
                var listdrop_disp = $(this).css('display');

                if (listdrop_disp == 'block') {
                    var cur_grid = $(this).attr('id');

                    var get_id = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').attr('id');

                    var insert_data = cur_grid + '|' + get_id;

                    if (arr_value.indexOf(insert_data) !== -1) {
                        delete arr_value[insert_data];
                        const index = arr_value.indexOf(insert_data);
                        if (index > -1) {
                            arr_value.splice(index, 1);
                        }

                        avoid_set = 1;
                    }
                    else {
                        arr_value.push(insert_data);
                    }

                    if (avoid_set == 0) {
                        var left_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left');

                        if (left_drop) {
                            left_drop = left_drop.split('px');
                            left_drop = parseInt(left_drop[0]) - 1;

                        }

                        left_drop = left_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left', left_drop);


                        var width_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').width();

                        width_drop = width_drop + 1;

                        width_drop = width_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').css('width', width_drop);
                    }

                }
            });


        });
    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_covered_obj_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}
//A055S000P01-20982
function ContractCoveredObjTreeTable() {
    var recid = localStorage.getItem("CurrentRecordId");

    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Contract Covered Object Parent',
            'RECORD_ID': recid,
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': ''
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            // if (document.getElementById("div_CTR_Covered_Objects")) {
            // 	document.getElementById('div_CTR_Covered_Objects').innerHTML = datas;
            // 	$("#div_CTR_Covered_Objects").closest('.Related').css('display', 'block');
            // }
            // if (data4 == "NORECORDS"){
            // 	document.getElementById('div_CTR_Covered_Objects').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
            // 	$("#div_CTR_Covered_Objects").closest('.Related').css('display', 'block');
            // }
            if (document.getElementById("div_CTR_related_list")) {
                document.getElementById('div_CTR_related_list').innerHTML = datas;
                $("#div_CTR_related_list").css('display', 'block');
            }
            if (data4 == "NORECORDS") {
                document.getElementById('div_CTR_related_list').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                $("#div_CTR_related_list").css('display', 'block');
            }

            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.EQUIPMENT_ID || '';
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }



                        CoveredObj_child(filteredData, $detail);
                    }
                });
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.EQUIPMENT_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            CoveredObj_child(filteredData, $detail);
                        }
                    });
                }, 5000);
            }
            finally {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.EQUIPMENT_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            CoveredObj_child(filteredData, $detail);
                        }
                    });
                }, 5000);
            }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);

        });
        $(".JCLRgrip").mousedown(function () {

            $("thead.fullHeadFirst").css("cssText", "z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "none");

        });
        var arr_value = [];
        $(".JCLRgrip").mouseup(function () {

            var th_width_resize = [];
            $("#table_covered_obj_parent thead.fullHeadFirst tr th").each(function (index) {
                var wid = $(this).css("width");

                if (index == 0 || index == 1) {
                    th_width_resize.push("60px");
                } else {
                    th_width_resize.push(wid);
                }
            });


            $("thead.fullHeadFirst").css("cssText", "position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "table-header-group");

            var txt_alg = []
            $('table#table_covered_obj_parent thead.fullHeadSecond tr th').each(function (index) {
                var a = $(this).css('text-align');
                txt_alg.push(a);
            });

            $("#table_covered_obj_parent thead.fullHeadFirst tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });
            $("#table_covered_obj_parent thead.fullHeadSecond tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });



            $('div[id^=listBoxRelatedMutipleCheckBoxDrop_]').each(function (index) {

                var avoid_set = 0;
                var listdrop_disp = $(this).css('display');

                if (listdrop_disp == 'block') {
                    var cur_grid = $(this).attr('id');

                    var get_id = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').attr('id');

                    var insert_data = cur_grid + '|' + get_id;

                    if (arr_value.indexOf(insert_data) !== -1) {
                        delete arr_value[insert_data];
                        const index = arr_value.indexOf(insert_data);
                        if (index > -1) {
                            arr_value.splice(index, 1);
                        }

                        avoid_set = 1;
                    }
                    else {
                        arr_value.push(insert_data);
                    }

                    if (avoid_set == 0) {
                        var left_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left');

                        if (left_drop) {
                            left_drop = left_drop.split('px');
                            left_drop = parseInt(left_drop[0]) - 1;

                        }

                        left_drop = left_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left', left_drop);


                        var width_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').width();

                        width_drop = width_drop + 1;

                        width_drop = width_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').css('width', width_drop);
                    }

                }
            });


        });
    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_contract_covered_obj_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}



function tool_breadcrumb() {
    databind = ""
    var recid = localStorage.getItem("CurrentRecordId");
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'RECORD_ID': recid,
            'TABNAME': 'Tools',
            'ACTION': 'BREADCRUMB',
            'TABLENAME': ObjectName,
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': ''

        }, function (datachild) {

            data = datachild;
            if (ObjectName == 'SAQSCF') {
                $('ul.breadcrumb').append(data);
            }
            else if (data != databind) {
                $('ul.breadcrumb').append(data);
            }
            databind = data
            var eqp_details = localStorage.getItem('eqp_details');
            var srcfab_details = localStorage.getItem('srcfab_details');
            var toolmatrix_details = localStorage.getItem('toolmatrix_details');

            if (ObjectName == "SAQSTE" && eqp_details == "false") {
                chainsteps_breadcrumb("Equipment");
            }
            else if (ObjectName == "SAQSTE" && toolmatrix_details == "false") {
                chainsteps_breadcrumb("Tool Relocation Matrix");
                localStorage.setItem("toolmatrix_details", "true");
            }
            else if (ObjectName == "SAQSCF" && srcfab_details == "false") {
                chainsteps_breadcrumb("Sending Fab Locations");
            }
        });
    } catch (e) {
        console.log(e);
    }
}
function downloadExcelConfiguration(ele) {
    localStorage.setItem("showProgressBar", 1);
    $("div#progress-bar-model-text").text("DOWNLOADING QUOTE DOCUMENT");
    RecordId = ele.text
    ObjectName = 'SAQDOC'
    showProgressBar();
    cpq.server.executeScript('CQGNTDOCPF', { 'RECORD_ID': RecordId, 'ObjectName': 'SAQDOC', 'Language': 'EN' }, function (data) {
        value = data.size
        if (data.ErrorMsg) {
            alert("Sorry, something went wrong. CPQ is not able to create a XML file.\nError message: " + data.ErrorMsg);
            return;
        }
        var byteArray = new Uint8Array(data.File);
        if (window.navigator && window.navigator.msSaveBlob) {//if is IE
            navigator.msSaveBlob(new Blob([byteArray], { type: 'application/xml' }), data.FileName)
        } else {
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.href = window.URL.createObjectURL(new Blob([byteArray], { type: 'application/octet-stream' }));
            a.download = data.FileName;
            localStorage.setItem("showProgressBar", 0);
            $("#dynamic").css("width", "100%").attr("aria-valuenow", 100).text("100% Complete");
            $('#progress_bar_modal').modal('hide');
            a.click();
            a.remove();
        }
    });
}

/*function downloadExcelConfiguration(RecordId, ObjectName, Language = 'Ch'){
    localStorage.setItem("showProgressBar", 1);
    $("div#progress-bar-model-text").text("DOWNLOADING QUOTE DOCUMENT");
    ObjectName ='SAQDOC'
    showProgressBar();
    cpq.server.executeScript('CQGNTDOCPF',{'RECORD_ID': RecordId,'ObjectName': ObjectName, 'Language': Language }, function (data) {
    value = data.size
    if(data.ErrorMsg){
        alert("Sorry, something went wrong. CPQ is not able to create a XML file.\nError message: "+data.ErrorMsg);
            return;
        }
        var byteArray = new Uint8Array(data.File);
        if(window.navigator && window.navigator.msSaveBlob){//if is IE
        navigator.msSaveBlob( new Blob([byteArray], {type:'application/xml'}), data.FileName )
        } else {
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.href = window.URL.createObjectURL(new Blob([byteArray], { type: 'application/octet-stream' }));
            a.download = data.FileName;
            localStorage.setItem("showProgressBar", 0);			
            $("#dynamic").css("width", "100%").attr("aria-valuenow", 100).text("100% Complete");
            $('#progress_bar_modal').modal('hide');
            a.click();
            a.remove();
        } 
});
}*/

function bulkAddSpareParts() {
    $('#pageloader').css('cssText', 'display:none !important;');
    try {
        $('#pageloader').css('cssText', 'display:none !important;');
        cpq.server.executeScript("SGCTLPREVW", {
            'Preview': 'True',
            'ACTION': 'GETCOUNT'
        }, function (dataset) {
            var current_progress = 5;
            var current_progress1 = 20;
            localStorage.setItem('firsttime_cancel', 0);
            $('#progress_bar_modal .modal-dialog').css('cssText', 'width:550px !important');
            $("#dynamic").css("width", current_progress1 + "%").attr("aria-valuenow", current_progress).text(current_progress + "% Complete");
            list_of_prod = dataset[0];
            count_of_prod = dataset[1];
            if (count_of_prod > 0) {
                record_processed = 0;
                $('#progress_bar_modal').modal('show');
                localStorage.setItem('count_of_prod', count_of_prod);
                var i = 0;
                var showGallery = function () {
                    $('.overlay').css('display', 'none');
                    clicked_preview_cancel = localStorage.getItem('clicked_preview_cancel');
                    firsttime_cancel = localStorage.getItem('firsttime_cancel');
                    if (clicked_preview_cancel == 1 && firsttime_cancel == 0) {
                        localStorage.setItem('firsttime_cancel', 1);
                        $('#progress_bar_modal').modal('hide');
                        return false;
                    }
                    if (firsttime_cancel == 1) {
                        return false;
                    } else {
                        $('.overlay').css('display', 'none !important');
                        setTimeout(function () {
                            $('.overlay').css('display', 'none !important');
                        }, 100);
                        try {
                            cpq.server.executeScript("SGCTLPREVW", {
                                'Preview': 'True',
                                'ACTION': 'STARTINSERT',
                                'WHERE_CONDUCTION': list_of_prod[i]
                            }, function (dataset) {
                                record_processed += 1;
                                count_of_prod = localStorage.getItem('count_of_prod');
                                count = 100 / parseInt(count_of_prod);
                                process_count = Math.round((count * parseInt(record_processed)).toFixed(2));
                                $("#dynamic").css("width", process_count + "%").attr("aria-valuenow", process_count).text(process_count + "% Complete");
                                if (process_count == 100) {
                                    $('#progress_bar_modal').modal('hide');
                                } else {
                                    i++;
                                    if (i < count_of_prod) {
                                        setTimeout(function () {
                                            showGallery();
                                        }, 1000);
                                    }
                                }
                            });
                        } catch (e) {
                            console.log(e);
                        }
                    }
                };
                if (count_of_prod > 0) {
                    showGallery();
                }
            }
        });
    } catch (e) {
        console.log(e);
    }
}


var getselectedsapres = localStorage.getItem("selectedspares")


function showSparePartsBulkEdit(ele) {


    $('#SYOBJR_00005_7EAA11B4_82C9_400B_8E48_65497373A578').find(':input(:disabled)').prop('disabled', false);
    //$('#SYOBJR_00005_7EAA11B4_82C9_400B_8E48_65497373A578').find(':input(:disabled)').css('background-color','lightyellow');
    $('#SYOBJR_00005_7EAA11B4_82C9_400B_8E48_65497373A578  tbody  tr td input').css('background-color', 'lightyellow');
    // A055S000P01-3184 issue:1 start
    // var sparePartsBulkAddBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-add-modal-btn')
    // var sparePartsBulkEDITBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-edit-btn')
    // var sparePartsBulkSAVEBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-save-btn')
    // var sparePartsBulkCANCELBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-cancel-btn')
    // if (sparePartsBulkAddBtn.length == 1){
    // 	sparePartsBulkAddBtn.remove()
    // }
    // if (sparePartsBulkEDITBtn.length == 1){
    // 	sparePartsBulkEDITBtn.remove()
    // }
    $('#spare-parts-bulk-add-modal-btn').css('display', 'none');
    $('#spare-parts-bulk-edit-btn').css('display', 'none');
    $('#spare-parts-bulk-save-btn').css('display', 'block');
    $('#spare-parts-bulk-cancel-btn').css('display', 'block');
    // To show save & cancel button in SHP after clicking on BULK EDIT button - START
    //$('.secondary_highlight_panel').append('<button id="spare-parts-bulk-cancel-btn" onclick="showSparePartsBulkcancel(this)" class="btnconfig" >CANCEL</button>')
    //$('.secondary_highlight_panel').append('<button id="spare-parts-bulk-save-btn" onclick="showSparePartsBulksave(this)"  class="btnconfig" >SAVE</button>')
    // To show save & cancel button in SHP after clicking on BULK EDIT button - END
    //A055S000P01-3184 issue:1 end
}

function showSparePartsBulkcancel(ele) {


    //A055S000P01-3184 issue:1 start
    // var sparePartsBulkAddBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-add-modal-btn')
    // var sparePartsBulkEDITBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-edit-btn')
    // var sparePartsBulkSAVEBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-save-btn')
    // var sparePartsBulkCANCELBtn = $('.secondary_highlight_panel').find('button#spare-parts-bulk-cancel-btn')
    // if (sparePartsBulkSAVEBtn.length == 1){
    // 	sparePartsBulkSAVEBtn.remove()
    // }
    // if (sparePartsBulkCANCELBtn.length == 1){
    // 	sparePartsBulkCANCELBtn.remove()
    // }
    $('#spare-parts-bulk-save-btn').css('display', 'none');
    $('#spare-parts-bulk-cancel-btn').css('display', 'none');
    $('#spare-parts-bulk-edit-btn').css('display', 'none');
    $('#spare-parts-bulk-add-modal-btn').css('display', 'block');
    loadRelatedList('SYOBJR-00005', 'div_CTR_Spare_Parts')
    //$('.secondary_highlight_panel').append('<button id="spare-parts-bulk-add-modal-btn" onclick="showSparePartsBulkAddModal(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">BULK ADD</button>')
    //$('.secondary_highlight_panel').append('<button id="spare-parts-bulk-edit-btn" onclick="showSparePartsBulkEdit(this)"  class="btnconfig" >BULK EDIT</button>')
    //A055S000P01-3184 issue:1 end
}


function showSparePartsBulksave(ele) {


    var selectedparts = [];

    var selectAll = false;
    $('#SYOBJR_00005_7EAA11B4_82C9_400B_8E48_65497373A578').find('[type="checkbox"]:checked').map(function () {
        if ($(this).attr('name') == 'btSelectAll') {
            selectAll = true;
        }
        var sel_val = $(this).closest('tr').find('td:nth-child(2)').text()
        if (sel_val != '') {
            selectedparts.push(sel_val);
        }


    });
    var input_val = []
    var selectedons = [];
    var selectedcust_AQ = [];
    var selectedQT = [];
    var selectPN = [];
    $("#div_CTR_Spare_Parts #SYOBJR_00005_7EAA11B4_82C9_400B_8E48_65497373A578 tbody tr ").each(function () {

        var type = $(this).attr('type')
        if (type != 'checkbox') {

            input_val.push($(this).val())
            var sel_val_sche = $(this).find('td:nth-child(10)').find('input').val()
            selectedons.push(sel_val_sche);
        }

        var sel_val_CA = $(this).find('td:nth-child(9)').find('input').val()
        selectedcust_AQ.push(sel_val_CA);

        var sel_val_QT = $(this).find('td:nth-child(3)').text()
        selectedQT.push(sel_val_QT);

        var sel_val_PN = $(this).find('td:nth-child(4)').text()
        selectPN.push(sel_val_PN);

    });







    cpq.server.executeScript("CQSPBKEDIT", {
        'CUS_ANN': selectedcust_AQ,
        'SCH_MODE': selectedons,
        'GETQTID': selectedQT,
        'GET_PARTNUM': selectPN
    }, function (dataset) {

        $('#spare-parts-bulk-save-btn').css('display', 'none');
        $('#spare-parts-bulk-cancel-btn').css('display', 'none');
        $('#spare-parts-bulk-edit-btn').css('display', 'none');
        $('#spare-parts-bulk-add-modal-btn').css('display', 'block');
        loadRelatedList('SYOBJR-00005', 'div_CTR_Spare_Parts')
        //A055S000P01-3184 issue:1 start 
        //$('.secondary_highlight_panel').append('<button id="spare-parts-bulk-add-modal-btn" onclick="showSparePartsBulkAddModal(this)" class="btnconfig" data-target="#cont_viewModalSection" data-toggle="modal">BULK ADD</button>')
        //$('.secondary_highlight_panel').append('<button id="spare-parts-bulk-edit-btn" onclick="showSparePartsBulkEdit(this)"  class="btnconfig" >BULK EDIT</button>')
        //A055S000P01-3184 issue:1 end
    });


}


function tot_equp(eqp) {
    cpq.server.executeScript("CQTOTEQUP", { 'equp_id': eqp, 'Node': 'Equipment' }, function (dataset) {
        var dat1 = dataset[0];
        var dat2 = dataset[1];
    });
}



function fablocatecancel(ele) {

    $('.sec_fabvaldrives').css('display', 'none');
    $('#ctr_drop').css('display', 'block');
    $('#fabvaldrives  tbody tr td select').removeClass('light_yellow');
    $('#fabnotify').removeClass('header_section_div header_section_div_pad_bt10');
    activetab = $('#COMMON_TABS li.active').text().trim();
    var subtabName = localStorage.getItem("currentSubTab")

}

function fablocatesave(ele) {


    var getfablocatedict = JSON.parse(localStorage.getItem('getfablocatedict'));
    //recordid =  localStorage.getItem("CurrentRecordId");
    record_id = localStorage.getItem("CurrentRecordIdEQUIP")
    var subtabName = localStorage.getItem("currentSubTab")
    Driver_popup(subtabName);
    var getfabid = $("#seginnerbnr div.product_txt_div_child.secondary_highlight div.product_txt_to_top_child  abbr").text();
    cpq.server.executeScript("CQTFABVIEW", {
        'FabLocateDT': getfablocatedict,
        'ACTION': 'SAVE',
        'CurrentRecordId': record_id, 'getfabid': getfabid, 'subtab': subtabName


    }, function () {

        $('.sec_fabvaldrives').css('display', 'none');
        $('#ctr_drop').css('display', 'block');
        $('#fabvaldrives  tbody tr td select').removeClass('light_yellow');
        $('#fabnotify').removeClass('header_section_div header_section_div_pad_bt10');
        //A055S000P01-3629 - start
        //activetab = $('#COMMON_TABS li.active').text().trim();
        activetab = $('#COMMON_TABS ul li.active').text().trim();
        //A055S000P01-3629 - end

    });

}

function fabcostlocatecancel(ele) {
    $('.sec_fabvaldrives').css('display', 'none');
    $('#ctr_drop').css('display', 'block');
    var subtabName = localStorage.getItem("currentSubTab")
    var entdictcan = localStorage.getItem("ent_dict_cancel")

    localStorage.setItem('EDITENT_SEC', '');
    var EquipmentId = ''
    if (subtabName == 'Equipment Entitlements') {
        EquipmentId = localStorage.getItem("Ent_EquipmentId")
    }
    if (subtabName == "Entitlements" || subtabName == "Equipment Entitlements" || subtabName == "Assembly Entitlements") {
        var getenttableid = localStorage.getItem('getatbleid');
        var getcurrentrecord_id = localStorage.getItem('EntCurrentId');
        var currentObject = localStorage.getItem("CurrentObject");
        $('#' + getenttableid + '  tbody tr td select').removeClass('light_yellow');
        $('#entsave').css('display', 'none'); $('#entcancel').css('display', 'none');
        var getprevdatadict = localStorage.getItem("prventdict");
        TreeParam = localStorage.getItem('CommonTreeParam');
        TreeParentParam = localStorage.getItem('CommonTreeParentParam');
        TreeSuperParentParam = localStorage.getItem('CommonNodeTreeSuperParentParam');
        TopSuperParentParam = localStorage.getItem('CommonTopSuperParentParam');
        /*try{
            cpq.server.executeScript("CQCRUDOPTN", {
                        'Opertion': 'GET',
                        'ActionType': 'SHOW_PRICING_BENCHMARKING_NOTIFICATION',
                        'NodeType': 'QUOTE LEVEL NOTIFICATION'            
                    },function (data) {
                    if (data != ""){
                        console.log(data)
                    if (data[0] != "" || data[1] != "" ){
                console.log(data)
                    $(".emp_notifiy").css('display','block');
                    $("#PageAlert ").css('display','block');
                    $("#alertnotify").html(data);
                    }
                    }
                	
                });
            }
            catch{console.log('===error price bench mark notification')}*/
        //TreeSuperTopParentParam = localStorage.getItem('CommonTreeSuperTopParentParam');
        TreeFirstSuperTopParentParam = localStorage.getItem('CommonTreeFirstSuperTopParentParam');
        TreeFirstSuperTopParentParam12 = localStorage.getItem('common_TreeFirstSuperTopParentParam')
        //commented on 09-03-2021 to check performance tuning
        try {
            CurrentRecordId = localStorage.getItem('CurrentRecordId');
            cpq.server.executeScript("CQENTLMENT", {
                'ENT_CANCEL': 'CANCEL',
                'SectionRecordId': getenttableid,
                'getprevdict': getprevdatadict,
                'subtabName': subtabName,
                'EquipmentId': EquipmentId,
                'RECORD_ID': CurrentRecordId,

            }, function (datas) {

                //attrval = datas[0];
                //aatrid = datas[1];
                disallowlist = datas[0];
                allowlist = datas[1];
                readonlylist = datas[3];
                editlis = datas[4];
                subTabDetails(subtabName, 'Detail', currentObject, getcurrentrecord_id);
            });
        } catch (e) {
            console.log(e);
        }



    }
    else {
        //$('#fabcostlocate_cancel').css('display','none');
        //$('#fabcostlocate_save').css('display','none');
        $('#servicecostvaldrives  tbody tr td select').removeClass('light_yellow');
        $('#csservicecostfabvaldrives  tbody tr td select').removeClass('light_yellow');
        $('#csserviceGreencostvaldrives tbody tr td select').removeClass('light_yellow');
        $('#csserviceEquipcostvaldrives  tbody tr td select').removeClass('light_yellow');
        $('#servicecostvaldrives').parent().removeClass('header_section_div header_section_div_pad_bt10 padtop10');
        $('#csservicecostfabvaldrives').parent().removeClass('header_section_div header_section_div_pad_bt10 padtop10');
        $('#csserviceGreencostvaldrives').parent().removeClass('header_section_div header_section_div_pad_bt10 padtop10');
        $('#csserviceEquipcostvaldrives').parent().removeClass('header_section_div header_section_div_pad_bt10 padtop10');
        $('#fabnotify').removeClass('header_section_div header_section_div_pad_bt10');
    }
    $('#fabcostlocate_cancel').css('display', 'none');
    $('#fabcostlocate_save').css('display', 'none');

}

function fabcostlocatesave(ele) {
    //localStorage.setItem("rolldown","yes");
    var gettable_id_edit = ele.id
    if (localStorage.getItem("edit_call_flag") != 'true') {
        editent_bt(ele)
        localStorage.setItem("edit_call_flag", "true")
    }
    get_network = localStorage.getItem("EntPrevdict")
    var network_preventive = get_network.includes("_NET_WECLLB");
    var network_Corrective = get_network.includes("_NET_PRMAB");
    if (network_preventive == true || network_Corrective == true) {
        localStorage.setItem("realProgressBar", '1');
        realProgressBar(200);
        setTimeout(function () {
            localStorage.setItem("realProgressBar", 0);
            $("#progress_sscm_dynamic").css("width", "100%").attr("aria-valuenow", 100).text("100% Complete");
            $('#progress_bar_sscm_popup').modal('hide');
        }, 6000);
    }
    var getserlocatedict = JSON.parse(localStorage.getItem('getfablocatedict'));
    localStorage.setItem('EDITENT_SEC', '');
    var entdict = JSON.parse(localStorage.getItem('getentedict'));
    var getenttableid = localStorage.getItem('getatbleid');
    recordid = localStorage.getItem("CurrentRecordId");
    TreeParam = localStorage.getItem('CommonTreeParam');
    TreeParentParam = localStorage.getItem('CommonTreeParentParam');
    TreeSuperParentParam = localStorage.getItem('CommonNodeTreeSuperParentParam');
    TopSuperParentParam = localStorage.getItem('CommonTopSuperParentParam');
    //TreeSuperTopParentParam = localStorage.getItem('CommonTreeSuperTopParentParam');
    TreeFirstSuperTopParentParam = localStorage.getItem('CommonTreeFirstSuperTopParentParam');
    //record_id =localStorage.getItem("CurrentRecordIdEQUIP")
    var subtabName = localStorage.getItem("currentSubTab")
    var currentObject = localStorage.getItem("CurrentObject");
    var entdictsave = JSON.parse(localStorage.getItem('getdictentdata'));
    // A055S000P01-20560 - Starts - A
    var contract_start = $(".segment_revision_status_text").text();
    var milestone_1 = $("#AGS_"+TreeParam+"_PQB_MIL1BD").val();
    var milestone_2 = $("#AGS_"+TreeParam+"_PQB_MIL2BD").val();
    var milestone_3 = $("#AGS_"+TreeParam+"_PQB_MIL3BD").val();
    var milestone_1_class_name =  $("#AGS_"+TreeParam+"_PQB_MIL1BD").attr('class');
    var milestone_2_class_name =  $("#AGS_"+TreeParam+"_PQB_MIL2BD").attr('class');
    var milestone_3_class_name =  $("#AGS_"+TreeParam+"_PQB_MIL3BD").attr('class');
    if ((Date.parse(milestone_1) >= Date.parse(contract_start)) || (milestone_1 == ''|| milestone_1 == undefined ||!milestone_1_class_name.includes('light_yellow'))){
        milestone_validation_1 = 'Yes'
    }
    else{
        milestone_validation_1 = 'No'
    }
    if ((Date.parse(milestone_2) >= Date.parse(contract_start)) || (milestone_2 == ''|| milestone_2 == undefined ||!milestone_2_class_name.includes('light_yellow'))){
        milestone_validation_2 = 'Yes'
    }
    else{
        milestone_validation_2 = 'No'
    }
    if ((Date.parse(milestone_3) >= Date.parse(contract_start)) || (milestone_3 == ''|| milestone_3 == undefined ||!milestone_3_class_name.includes('light_yellow'))){
        milestone_validation_3 = 'Yes'
    }
    else{
        milestone_validation_3 = 'No'
    }
    if (milestone_validation_1 == 'Yes' && milestone_validation_2 == 'Yes' && milestone_validation_3 == 'Yes'){
    // A055S000P01-20560 - Ends - A
        if (subtabName == "Entitlements" || subtabName == "Equipment Entitlements" || subtabName == "Assembly Entitlements") {
            $('.CommonTreeDetail').css('display', 'block');
            var newdict = JSON.parse(localStorage.getItem("Entitlementdict"));
            var calc_factor = ''
            var priceimapct = ''
            var costimpact = ''
            var getmaualipval = ''
            var getCalc = $('#ADDL_PERF_GUARANTEE_91_1').val()
            if (getCalc) {
                if (getCalc.toUpperCase() == "MANUAL INPUT") {
                    calc_factor = $('#ADDL_PERF_GUARANTEE_91_1_calc').val()
                    costimpact = $('#ADDL_PERF_GUARANTEE_91_1_imt').val()
                    priceimapct = $('#ADDL_PERF_GUARANTEE_91_1_primp').val()
                    getmaualipval = $('#ADDL_PERF_GUARANTEE_91_1_T').val()
                    newdict.push('ADDL_PERF_GUARANTEE_91_1');
                }
            }

            var EquipmentId = ''
            if (subtabName == 'Equipment Entitlements') {
                EquipmentId = localStorage.getItem("Ent_EquipmentId")
            }
            var ent_dict_new = {};
            var ent_dict_cancel = {};
            $(".getentdata  tbody tr").each(function () {

                if ($(this).find('td:nth-child(5) select')) {

                    var getsecval = $(this).find('td:nth-child(2)').text();
                    var selectedvalue = $(this).find('td:nth-child(5) select').children(":selected").val();
                    //INC08760692 - Start - A
                    if ($(this).find('td:nth-child(5) select').children(":selected").val() == undefined){
                        var selectedvalue = $(this).find('td:nth-child(5) select').children(":selected").text()
                    }
                    //INC08760692 - End - A
                    var entselectedid = $(this).find('td:nth-child(5) select').children(":selected").attr('id');
                    //var getcurrency =  $(this).find('td:nth-child(5) input').val();
                    var getcalcfac = $(this).find('td:nth-child(7) input').val();
                    var getcostimpact = $(this).find('td:nth-child(8) ').text();
                    var getpriceimpact = $(this).find('td:nth-child(9) ').text();
                    if (entselectedid == "FIXED_PRICE") { entselectedid = 'FIXED PRICE' }

                    ent_dict_new[$(this).find('td:nth-child(5) select').attr('id')] = selectedvalue + '||' + entselectedid + '||' + 'DropDown' + '||' + getsecval + '||' + getcalcfac + '||' + getcostimpact + '||' + getpriceimpact;
                    ent_dict_cancel[$(this).find('td:nth-child(5) select').attr('id')] = selectedvalue;
                }


            });
            arr = []
            $(".getentdata  tbody tr").each(function () {

                if ($(this).find('td:nth-child(5) input') && !($(this).find('td:nth-child(5) input').attr('type') == 'checkbox')) {

                    var getsecval = $(this).find('td:nth-child(2)').text();
                    //var getcurrency =  $(this).find('td:nth-child(5) ').text();
                    var getcalcfac = $(this).find('td:nth-child(7) ').text();
                    var getcostimpact = $(this).find('td:nth-child(8) ').text();
                    var getpriceimpact = $(this).find('td:nth-child(9) ').text();
                    //var disallow_attr =  $(this).find('td:nth-child() input').is(":visible");
                    var ent_Val = $(this).find('td:nth-child(5) input').val();
                    // if (ent_Val == 0){
                    //ent_Val = ''
                    //}
                    ent_dict_new[$(this).find('td:nth-child(5) input').attr('id')] = ent_Val + '||' + $(this).find('td:nth-child(5) input').attr('id') + '||' + 'FreeInputNoMatching' + '||' + getsecval + '||' + getcalcfac + '||' + getcostimpact + '||' + getpriceimpact;
                    ent_dict_cancel[$(this).find('td:nth-child(5) input').attr('id')] = $(this).find('td:nth-child(5) input').val();

                }
                else if ($(this).find('td:nth-child(5) input').attr('type') == 'checkbox') {
                    var attr_id = $(this).find('td:nth-child(5) select').attr('id')
                    if ($(this).find('td:nth-child(5) input').attr('type') == 'checkbox') {
                        arr = []
                        $(this).find(".mulinput:checked").each(function () {
                            arr.push($(this).val());
                        });
                        var getsecval = $(this).find('td:nth-child(2)').text();
                        //var getcurrency =  $(this).find('td:nth-child(5) input').val();
                        var getcalcfac = $(this).find('td:nth-child(7) input').val();
                        var getcostimpact = $(this).find('td:nth-child(8) ').text();
                        var getpriceimpact = $(this).find('td:nth-child(9) ').text();
                        ent_dict_new[attr_id] = JSON.stringify(arr) + '||' + $(this).find('td:nth-child(5) input').attr('id') + '||' + 'Check Box' + '||' + getsecval + '||' + getcalcfac + '||' + getcostimpact + '||' + getpriceimpact;
                        ent_dict_cancel[attr_id] = arr
                    }

                }

            });



            localStorage.setItem('ent_dict_cancel', ent_dict_cancel);
            //localStorage.setItem("entitlement_save_flag",'True')

            scheduled_parts = $("#AGS_Z0108_TSC_SCPT").val();

            try {
                Entitlement_edit_value = localStorage.getItem("Entitlement_edit_value")
                localStorage.setItem("Entitlement_edit_value", "")
                Assembly_id_value = localStorage.getItem("AssemblyIdValue")
                EquipmentId = localStorage.getItem("EquipmentIdValue")
                CurrentRecordId = localStorage.getItem('CurrentRecordId');
                cpq.server.executeScript("CQENTLMENT", {
                    'attributeId': 'ADDL_PERF_GUARANTEE_91_1_calc',
                    'subtabName': subtabName,
                    'EquipmentId': EquipmentId,
                    'EntitlementType': 'Text',
                    'calc_factor': calc_factor, 'costimpact': costimpact, 'priceimapct': priceimapct, 'getmaualipval': getmaualipval,
                    'inputId': 'ADDL_PERF_GUARANTEE_91_1_T', 'ENT_IP_DICT': ent_dict_new, 'AssemblyId': Assembly_id_value, 'scheduled_parts': scheduled_parts, 'RECORD_ID': CurrentRecordId, 'Entitlement_edit_value': Entitlement_edit_value
                }, function (data) {
                    var getcurrentrecord_id = localStorage.getItem('EntCurrentId');
                    //subTabDetails(subtabName, 'Detail', currentObject, getcurrentrecord_id);
                    getprevdatadict = localStorage.getItem("prventdict");
                    localStorage.setItem("ent_dict_new", JSON.stringify(ent_dict_new))
                    try {
                        //entitlement_save_flag = localStorage.getItem("entitlement_save_flag");
                        cpq.server.executeScript("CQENTLMENT", {
                            'ACTION': 'SAVE',
                            'newdict': newdict,
                            'subtabName': subtabName,
                            'EquipmentId': EquipmentId, 'ENT_IP_DICT': ent_dict_new,
                            'getprevdict': getprevdatadict, 'AssemblyId': Assembly_id_value, 'scheduled_parts': scheduled_parts, 'RECORD_ID': CurrentRecordId
                        }, function (datas) {
                            //localStorage.setItem("add_new_functionality","TRUE");
                            //localStorage.setItem("save_flag",'false')	
                            //localStorage.setItem("entitlement_save_flag",'False')
                            // && (TreeParam == 'Z0091' || TreeParentParam == 'Z0091' || TreeSuperParentParam == 'Z0091')
                            if (subtabName != "Equipment Entitlements" && localStorage.getItem("CommonTreeParam") == 'Z0009' && datas[1].includes('AGS_Z0009_PQB_QTETYP')) {
                                localStorage.setItem("add_new_functionality", "TRUE");
                                // localStorage.setItem('left_tree_refresh','yes');
                                localStorage.setItem("add_new_functionality", "TRUE");
                                localStorage.setItem("EntRefresh", "YES");
                                //window.location.reload();
                                CommonLeftView();
                                //$("[id='qtn_save'] span").click();
                                //
                            }
                            //   subTabDetails(subtabName, 'Detail', currentObject, getcurrentrecord_id);
                            config_status = datas[0];
                            //A055S000P01-20941 - Start - M
                            oldconfig_status = data[23];
                            //attr_list = datas[1];
                            //INC08634400-Start-M
                            if ((config_status == "COMPLETE" || (config_status == "INCOMPLETE" && oldconfig_status == 'COMPLETE'  ) || (config_status == "INCOMPLETE" && oldconfig_status == 'ERROR'  ) || config_status == "ERROR" ) && dict["TreeParam"] != 'Add-On Products' && subtabName != 'Equipment Entitlements') {
                                localStorage.setItem("add_new_functionality", "TRUE");
                                localStorage.setItem("EntRefresh", "YES");
                                CommonLeftView();
                            }
                           
                            //A055S000P01-20941 - End - M
                            if (dict["TreeParam"] == 'Add-On Products' ) {
                                //localStorage.setItem("add_new_functionality", "TRUE");
                                subTabDetails('Entitlements', 'Detail', 'SAQSAO', CurrentRecordId);
                            }
                            //A055S000P01-20941 - Start - M
                            else if (subtabName == 'Equipment Entitlements' || (dict["TreeParentLevel2"] == 'Product Offerings' && subtabName == 'Entitlements' ) ) {
                                //localStorage.setItem("add_new_functionality", "TRUE");
                                subTabDetails(subtabName, 'Detail', 'SAQSGB', CurrentRecordId);
                            }
                            //A055S000P01-20941 - End - M
                            // (datas[1].includes('AGS_Z0046_TSC_NONCNS') || datas[1].includes('AGS_Z0009_TSC_NONCNS') || datas[1].includes('AGS_Z0046_TSC_CONSUM') || datas[1].includes('AGS_Z0009_TSC_CONSUM') || datas[1].includes('AGS_Z0091_TSC_NONCNS') || datas[1].includes('AGS_Z0091_TSC_CONSUM') || datas[1].includes('AGS_Z0035_TSC_NONCNS') || datas[1].includes('AGS_Z0035_TSC_CONSUM') || datas[1].includes('AGS_Z0004_TSC_NONCNS') || datas[1].includes('AGS_Z0004_TSC_CONSUM') || datas[1].includes('AGS_Z0007_TSC_NONCNS') || datas[1].includes('AGS_Z0007_TSC_CONSUM') || datas[1].includes('AGS_Z0092_TSC_NONCNS') || datas[1].includes('AGS_Z0092_TSC_CONSUM') || datas[1].includes('AGS_Z0092_TSC_CONADD') ||
                            //     datas[1].includes('AGS_Z0091_TSC_RPPNNW') || datas[1].includes('AGS_Z0092_TSC_RPPNNW') || datas[1].includes('AGS_Z0004_TSC_RPPNNW') || datas[1].includes('AGS_Z0006_TSC_RPPNNW') || datas[1].includes('AGS_Z0009_TSC_RPPNNW') || datas[1].includes('AGS_Z0007_TSC_RPPNNW') || datas[1].includes('AGS_Z0035_TSC_RPPNNW') || datas[1].includes('AGS_Z0046_TSC_RPPNNW') || datas[1].includes('AGS_Z0006_TSC_CONSUM') || datas[1].includes('AGS_Z0006_TSC_NONCNS'))
                            if (datas[1].toString().includes('TSC_RPPNNW') || datas[1].toString().includes('TSC_CONSUM') || datas[1].toString().includes('TSC_NONCNS') || datas[1].toString().includes('TSC_CONADD') && subtabName != 'Equipment Entitlements'){
                                if (dict['TreeParentLevel2'] == 'Product Offerings') {
                                    localStorage.setItem("entitlement_level_flag", "SAQSGE");
                                }
                                else if (dict['TreeParentLevel1'] == 'Product Offerings') {
                                    localStorage.setItem("entitlement_level_flag", "SAQTSE");
                                }
                                else {
                                    localStorage.setItem("entitlement_level_flag", "");
                                }
                                localStorage.setItem("add_new_functionality", "TRUE");
                                localStorage.setItem("EntRefresh", "YES");
                                if (subtabName != 'Assembly Entitlements' || subtabName != 'Equipment Entitlements') {
                                    active_chain_step = $('#COMMON_TABS ul li.active').attr('onclick');
                                    CommonLeftView();
                                    eval(active_chain_step);
                                }
                            }
                            else if (datas[1].includes("AGS_Z0035_NET_PRMALB") || datas[1].includes("AGS_Z0091_NET_PRMALB") || datas[1].includes("AGS_Z0092_NET_PRMALB") || datas[1].includes("AGS_Z0099_NET_PRMALB") || datas[1].includes("AGS_Z0004_NET_PRMALB") && subtabName != 'Equipment Entitlements') {
                                localStorage.setItem("add_new_functionality", "TRUE");
                                localStorage.setItem("EntRefresh", "YES");
                                CommonLeftView()
                            }
                            else {
                                localStorage.setItem("entitlement_level_flag", "");
                            }
                            //INC08634400-End-M
                            /*if (datas[1]){
                            const attr_list = datas[1];
                                let pattern = /_TSC_NONCNS|_TSC_CONSUM/i;
                                let text = "";
                                let flagconsume = "";
                                for (let i = 0; i < attr_list.length; i++) {
                                let result = attr_list[i].match(pattern);
                                console.log('22--',result);
                                flagconsume = 'pass'
                                }
                                
                                
                                if (flagconsume == "pass"){CommonLeftView();flagconsume = ''}
                            }*/

                            //if (att_list_cons.includes("_TSC_NONCNS","_TSC_CONSUM","_TSC_RPPNNW")){
                            //CommonLeftView();

                            // $('div#COMMON_TABS').find("li a:contains('Details')").parent().removeClass('active');
                            //$('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().addClass('active');
                            //$('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().click();
                            //}
                            //A055S000P01-20941 - Start - M
                            if (subtabName == 'Entitlements' && dict["TreeParentLevel1"] == 'Product Offerings'){
                                $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().click();
                            }
                            //A055S000P01-20941 - End - M

                        });
                    } catch (e) {
                        console.log(e);
                    }
                });
            }
            catch (e) {
                console.log(e);
            }
            $('#entsave').css('display', 'none');
            $('.sec_edit_sty').css('display', 'none');
            $('#entcancel').css('display', 'none'); $('.sec_edit_sty_btn').css('display', 'none');
            Entitlement_popup();
            var getcurrentrecord_id = localStorage.getItem('EntCurrentId');
            $('.CommonTreeDetail').css('display', 'block');
            $('#sc_' + getenttableid).removeClass('header_section_div header_section_div_pad_bt10');
            //subTabDetails(subtabName, 'Detail', currentObject, getcurrentrecord_id);
            // setTimeout(function () {
            // 	subTabDetails(subtabName, 'Detail', currentObject, getcurrentrecord_id);
            // }, 1000);
            //var getentfabvalue = localStorage.getItem('getfabvantage')
            //if(getentfabvalue == 'Excluded')
            //{
            //	localStorage.setItem('getbannerdetail','');
            //	$(".emp_notifiy").css('display','none');
            //	if (TreeParentParam == "Comprehensive Services" || TopSuperParentParam == "Comprehensive Services"){
            //	$('.CommonTreeDetail').css('display', 'block');
            //subTabDetails(subtabName, 'Detail', 'SAQSCO', getcurrentrecord_id);
            //}
            //}
            //else{$(".emp_notifiy").css('display','block');
            //getdata = '<div class="col-md-12" id="dirty-flag-warning"><div class="col-md-12 alert-warning"><label> <img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/warning1.svg" alt="Warning"> INFORMATION : 000001 : This quote requires manual pricing updates before finalization.</label></div></div>'
            //$(".emp_notifiy").html(getdata);
            //localStorage.setItem('getbannerdetail',getdata);
            //subTabDetails(subtabName, 'Detail', currentObject, getcurrentrecord_id);
            $('#' + getenttableid + '  tbody tr td select').removeClass('light_yellow').addClass('remove_yellow');
            $('#' + getenttableid + '  tbody tr td input').removeClass('light_yellow').addClass('remove_yellow');
            $('#fabcostlocate_cancel').css('display', 'none');
            $('#fabcostlocate_save').css('display', 'none');
            try {
                //var get_edit_table= $('#btn_ent').parent("div").attr("id");
                var gettableidedit = gettable_id_edit.slice(0, -7)
                $('#' + gettableidedit + '  tbody tr td select').removeClass('light_yellow').addClass('remove_yellow');
                $('#' + gettableidedit + '  tbody tr td input').removeClass('light_yellow').addClass('remove_yellow');
                $('#sc_' + gettableidedit).removeClass('header_section_div header_section_div_pad_bt10');
            }
            catch (e) {
                console.log(e);
            }
            // getprevdatadict = localStorage.getItem("prventdict");
            // localStorage.setItem("ent_dict_new",JSON.stringify(ent_dict_new))

            //localStorage.setItem("save_flag",'True')
            //if(AllTreeParam['TreeParentLevel1'] != 'Receiving Equipment' && subtabName != 'Equipment Entitlements'){

            // try {
            // 	//entitlement_save_flag = localStorage.getItem("entitlement_save_flag");
            // 	cpq.server.executeScript("CQENTLMENT", {
            // 		'ACTION': 'SAVE',
            // 		'newdict': newdict,
            // 		'subtabName': subtabName,
            // 		'EquipmentId':EquipmentId,'ENT_IP_DICT':ent_dict_new,
            // 		'getprevdict': getprevdatadict,				
            // 	}, function (datas) {
            // 		//localStorage.setItem("save_flag",'false')	
            // 		  //localStorage.setItem("entitlement_save_flag",'False')
            // 		  if (subtabName != "Equipment Entitlements" && (TreeParam == 'Z0091' || TreeParentParam == 'Z0091' || TreeSuperParentParam == 'Z0091')){
            // 			localStorage.setItem("add_new_functionality","TRUE");
            // 			localStorage.setItem("EntRefresh","YES");
            // 			$("[id='qtn_save'] span").click();
            // 			//subTabDetails(subtabName, 'Detail', currentObject, getcurrentrecord_id);
            // 		  }
            // 	});
            // } catch (e) {
            // 	console.log(e);
            // }
            //}

            localStorage.setItem("Entitlementdict", JSON.stringify([]))
            /*try{
                cpq.server.executeScript("CQCRUDOPTN", {
                            'Opertion': 'GET',
                            'ActionType': 'SHOW_PRICING_BENCHMARKING_NOTIFICATION',
                            'NodeType': 'QUOTE LEVEL NOTIFICATION'            
                        },function (data) {
                        if (data != ""){
                            console.log(data)
                        if (data[0] != "" || data[1] != "" ){
                    console.log(data)
                        $(".emp_notifiy").css('display','block');
                        $("#PageAlert ").css('display','block');
                        $("#alertnotify").html(data);
                        }
                        }
                        
                    });
                }
                catch{console.log('===error price bench mark notification')}*/

            //if (TreeParentParam == "Comprehensive Services" || TopSuperParentParam == "Comprehensive Services"){
            //subTabDetails(subtabName, 'Detail', currentObject, getcurrentrecord_id);
            //}
        }
        else {
            var getfabid = $("#seginnerbnr div.product_txt_div_child.secondary_highlight div.product_txt_to_top_child  abbr").text();
            cpq.server.executeScript("CQTFABVIEW", {
                'SerLocateDT': getserlocatedict,
                'ACTION': 'SAVECOST',
                'CurrentRecordId': recordid, 'getfabid': getfabid, 'subtab': subtabName


            }, function () {

                $('#fabcostlocate_cancel').css('display', 'none');
                $('#fabcostlocate_save').css('display', 'none');
                $('#servicecostvaldrives  tbody tr td select').removeClass('light_yellow');
                $('#csservicecostfabvaldrives  tbody tr td select').removeClass('light_yellow');
                $('#csserviceGreencostvaldrives tbody tr td select').removeClass('light_yellow');
                $('#csserviceEquipcostvaldrives  tbody tr td select').removeClass('light_yellow');
            });

        }
    }
    $(".disable_edit").prop("disabled", true);
    $(".MultiCheckBox").prop("disabled", true);
    $('.MultiCheckBox').removeClass('light_yellow').addClass('remove_yellow');

}


//Commented the below code because we have changed the hyperlink to key column.
/*function assembly_pmevents(ele){
    Assembly_id_value = $(ele).closest("td").text();
    Covered_object_record_id = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(3) a:last').attr('id');
    Parent_table_Greenbook = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(8)').text();
    SerialNumber = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(6)').text();
    EquipmentId = $(ele).closest("table").closest('tr').prev('tr').find('td:nth-child(5)').text();
    Equipment_serial_number = EquipmentId+'-'+SerialNumber
    localStorage.setItem("Covered_object_record_id",Covered_object_record_id)
    localStorage.setItem("AssemblyIdValue",Assembly_id_value)
    localStorage.setItem("EquipmentIdValue",EquipmentId)
    localStorage.setItem("SerialNumberValue",SerialNumber)
    localStorage.setItem("EquipmentSerialNumber",Equipment_serial_number)
    localStorage.setItem("AssemblyId","Yes")
    CurrentNodeId = localStorage.getItem('CurrentNodeId')
    node_id = $('#lefttreepan #commontreeview').treeview('getNode', [parseInt(CurrentNodeId), { silent: true } ]);
    $('#lefttreepan #commontreeview').treeview('expandNode', [ 1, {silent: true } ]);
    if(TreeParentParam == "Comprehensive Services"){
        var childrenNodes = _getChildren(node_id);
        $(childrenNodes).each(function(){
            child_node_id = $('#lefttreepan #commontreeview').treeview('getNode', [ this.nodeId, { silent: true } ]);
            if (child_node_id.text == Parent_table_Greenbook){
                    Greenbook_pm_events_node_id = child_node_id.nodeId
                    CommonRightView(Greenbook_pm_events_node_id)
                    CurrentNodeId = Greenbook_pm_events_node_id
                    localStorage.setItem('CurrentNodeId',CurrentNodeId)
                    setTimeout(function(){
                        Subbaner(CurrentNodeId, "", "QTQSAP")
                    },4500);
                }
                });
    }
    else{
        CommonRightView(CurrentNodeId)
        setTimeout(function(){    
            Subbaner(CurrentNodeId, "", "QTQSAP")
        },4500);
        }
    }*/

function Pmevents_breadcrumb(Values) {
    if (Values) {
        if (Values.includes('-')) {
            Action_Str = '<li><a onclick="Redirection_to_Tool_Details()" <abbr title="' + Values + '">' + Values + '</abbr></a><span class="angle_symbol"><img src="/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>'
            $('ul.breadcrumb').append(Action_Str);
        }
        else {
            Action_Str = '<li><a  <abbr title="' + Values + '">' + Values + '</abbr></a><span class="angle_symbol"><img src="/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>'
            $('ul.breadcrumb').append(Action_Str);
        }
    }

}
function chainsteps_breadcrumb(subTabText) {
    Action_Str = '<li><a onclick="Redirection_to_subtab(' + "'" + subTabText + "'" + ')" <abbr title="' + subTabText + '">' + subTabText + '</abbr></a><span class="angle_symbol"><img src="/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>'
    $('ul.breadcrumb').append(Action_Str);
}
function Redirection_to_subtab(breadcrumb_label) {
    if (TreeParam == "Quote Information" && breadcrumb_label == "Involved Parties") {
        subtab = Common_Tabs(this, "Involved_Parties")
    }
    else {
        active_chain_step = $('#COMMON_TABS ul li.active').attr('onclick')
        eval(active_chain_step)
    }
    //active_chain_step = eval($('#COMMON_TABS ul li.active').attr('onclick'))
    //chain_step_grid = localStorage.getItem('currentSubTab');
    //subTabDetails(chain_step_grid, 'Related','ACACHR', '8488EC73-F32A-47F2-9872-D762787D6E39')
}
//A055S000P01-1981 code starts..
function Redirection_to_Tool_Details() {
    CurrentNodeId = localStorage.getItem('CurrentNodeId')
    covered_object_record_id = localStorage.getItem("Covered_object_record_id").split('|')[0]
    CommonRightView(CurrentNodeId)
    setTimeout(function () {
        $('#' + covered_object_record_id).click();
    }, 1500);
}
//A055S000P01-1981 code ends...
function pending_grid() {
    try {
        cpq.server.executeScript("CQDOCUGENR", {
            'ACTION': 'COUNT',
        }, function (data) {
            var count = data;

        });
    } catch (e) {
        console.log(e);
    }
    if (data == 1) {
        setTimeout(function () {
            if (lang == 'English') {
                l = "EN"
            } else if (lang == "Chinese") {
                l = "ZH"
            }
            if ($('.noRecDisp').length && $('#SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1').length == 0) {
                $('.noRecDisp').css('display', 'none');
                $('#div_CTR_Quote_documents').append('<div class="bootstrap-table"><div class="fixed-table-toolbar"></div><div class="fixed-table-container" style="padding-bottom:0;"><div class="fixed-table-header" style="display:none"><table onmouseup="relatedmouseup(this)"></table></div><div class="fixed-table-body"><div class="fixed-table-loading" style="top:58.5px">Loading, please wait...</div><div class="JCLRgrips" style="width:1095.25px"><div class="JCLRgrip" style="left:61px;height:150px"><div class="JColResizer"></div></div><div class="JCLRgrip" style="left:121px;height:150px"><div class="JColResizer"></div></div><div class="JCLRgrip" style="left:191px;height:150px"><div class="JColResizer"></div></div><div class="JCLRgrip" style="left:311px;height:150px"><div class="JColResizer"></div></div><div class="JCLRgrip" style="left:511px;height:150px"><div class="JColResizer"></div></div><div class="JCLRgrip" style="left:711px;height:150px"><div class="JColResizer"></div></div><div class="JCLRgrip" style="left:912.25px;height:150px"><div class="JColResizer"></div></div><div class="JCLRgrip JCLRLastGrip" style="left:1113.5px;height:150px"></div></div><table id="SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1" data-pagination="false" data-filter-control="true" data-maintain-selected="true" data-locale="en-US" class="table table-hover JColResizer" onmouseup="relatedmouseup(this)"><thead><tr><th style="width:60px" data-field="ACTIONS"><div class="th-inner"><div class="action_col">ACTIONS</div><button class="searched_button" id="Act_SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1">Search</button></div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th class="bs-checkbox wth45" style="width:60px" data-field="SELECT"><div class="pad0brdbt">SELECT</div><div class="th-inner"><input name="btSelectAll" type="checkbox" class="custom"><span class="lbl"></span></div><div class="fht-cell"><div class="no-filter-control"></div></div></th><th title="Status" style="width:70px" data-field="STATUS"><div class="th-inner sortable both">Status</div><div class="fht-cell"><div class="filter-control"><input class="width100_vis form-control bootstrap-table-filter-control-STATUS"></div></div></th><th title="Key" style="width:120px" data-field="QUOTE_DOCUMENT_RECORD_ID"><div class="th-inner sortable both">Key</div><div class="fht-cell"><div class="filter-control"><input class="width100_vis form-control bootstrap-table-filter-control-QUOTE_DOCUMENT_RECORD_ID"></div></div></th><th title="Document ID" style="width:200px" data-field="DOCUMENT_ID"><div class="th-inner sortable both">Document ID</div><div class="fht-cell"><div class="filter-control"><input class="width100_vis form-control bootstrap-table-filter-control-DOCUMENT_ID"></div></div></th><th title="Document Name" style="width:200px" data-field="DOCUMENT_NAME"><div class="th-inner sortable both">Document Name</div><div class="fht-cell"><div class="filter-control"><input class="width100_vis form-control bootstrap-table-filter-control-DOCUMENT_NAME"></div></div></th><th title="Language ID" style="width:201.25px" data-field="LANGUAGE_ID"><div class="th-inner sortable both">Language ID</div><div class="fht-cell"><div class="filter-control"><input class="width100_vis form-control bootstrap-table-filter-control-LANGUAGE_ID"></div></div></th><th title="Language Name" style="width:201.25px" data-field="LANGUAGE_NAME"><div class="th-inner sortable both">Language Name</div><div class="fht-cell"><div class="filter-control"><input class="width100_vis form-control bootstrap-table-filter-control-LANGUAGE_NAME"></div></div></th></tr></thead><tbody onclick="Table_Onclick_Scroll(this)"><tr data-index="0"><td style="position:relative"><div class="btn-group dropdown"><div class="dropdown column-with-actions" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item" href="#">VIEW</a></li></ul></div></div></td><td class="bs-checkbox wth45"><input data-index="2" name="btSelectItem" type="checkbox" class="custom"><span class="lbl"></span><span class="lbl"></span><span class="lbl"></span></td><td><abbr title="<img title=Acquiring src=/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Cloud_Icon.svg>"><img title="Acquiring" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Cloud_Icon.svg"></abbr></td><td><abbr id="Pending" title="Pending">Pending</abbr></td><td><abbr></abbr></td><td><abbr id="F7423685-5271-4DF6-92CB-A1CF9567E41D"></abbr></td><td><abbr id="F7423685-5271-4DF6-92CB-A1CF9567E41D" title="' + l + '">' + l + '</abbr></td><td><abbr id="F7423685-5271-4DF6-92CB-A1CF9567E41D title = "' + lang + '">' + lang + '</abbr></td></tr></tbody></table><div class="col-md-12 brdr listContStyle padbthgt30"><div class="col-md-4 pager-numberofitem clear-padding"><span class="pager-number-of-items-item noofitem" id="SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1_NumberofItem">1 - 1 of</span><span class="pager-number-of-items-item fltltpad2mrg0" id="SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1_totalItemCount">1</span><div class="clear-padding fltltmrgtp3"><div class="pull-right veralmert"><select id="SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1_PageCountValue" class="form-control pagecunt"><option value="10" selected>10</option><option value="20">20</option><option value="50">50</option><option value="100">100</option><option value="200">200</option></select></div></div></div><div class="col-xs-8 col-md-4 clear-padding totcnt" data-bind="visible: totalItemCount"><div class="clear-padding col-xs-12 col-sm-6 col-md-12 brdr0"><ul class="pagination pagination"><li class="disabled"><a href="javascript:void(0)" onclick="FirstPageLoad_paginationChild(&quot;RelatedList&quot;,&quot;SYOBJR-98799&quot;,&quot;SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1&quot;)"><i class="fa fa-caret-left fnt14bold"></i><i class="fa fa-caret-left fnt14"></i></a></li><li class="disabled"><a href="javascript:void(0)" onclick="Previous12334Child(&quot;RelatedList&quot;,&quot;SYOBJR-98799&quot;,&quot;SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1&quot;)"><i class="fa fa-caret-left fnt14"></i>PREVIOUS</a></li><li class="disabled"><a href="javascript:void(0)" class="disabledPage" onclick="Next12334Child(&quot;RelatedList&quot;,&quot;SYOBJR-98799&quot;,&quot;SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1&quot;)">NEXT<i class="fa fa-caret-right fnt14"></i></a></li><li class="disabled"><a href="javascript:void(0)" onclick="LastPageLoad_paginationChild(&quot;RelatedList&quot;,&quot;SYOBJR-98799&quot;,&quot;SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1&quot;)" class="disabledPage"><i class="fa fa-caret-right fnt14"></i><i class="fa fa-caret-right fnt14bold"></i></a></li></ul></div></div><div class="col-md-4 pr_page_pad"><span id="SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1_page_count" class="currentPage page_right_content">1</span><span class="page_right_content pad_rt_2">Page</span></div></div></div><div class="fixed-table-footer" style="display:none"><table onmouseup="relatedmouseup(this)"><tbody><tr></tr></tbody></table></div></div><div class="fixed-table-pagination" style="display:none"></div></div>');
                //$('#SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1').append('<tr data-index="0"><td style="position:relative"><div class="btn-group dropdown"><div class="dropdown column-with-actions" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item" href="#">VIEW</a></li></ul></div></div></td><td class="bs-checkbox wth45"><input data-index="2" name="btSelectItem" type="checkbox" class="custom"><span class="lbl"></span><span class="lbl"></span><span class="lbl"></span></td><td><abbr title="<img title=Acquiring src=/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Cloud_Icon.svg>"><img title="Acquiring" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Cloud_Icon.svg"></abbr></td><td><abbr id="Pending" title="Pending">Pending</abbr></td><td><abbr></abbr></td><td><abbr id="F7423685-5271-4DF6-92CB-A1CF9567E41D"></abbr></td><td><abbr id="F7423685-5271-4DF6-92CB-A1CF9567E41D" title="'+lang+'">'+lang+'</abbr></td><td><abbr id="F7423685-5271-4DF6-92CB-A1CF9567E41D"></abbr></td></tr>');
                //localStorage.setItem("gendoc","no");
            }
            else if ($('#SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1').length) {
                $('#SYOBJR_98799_931DBB80_1A63_4B0A_96BA_FEF9885A08B1').append('<tr data-index="0"><td style="position:relative"><div class="btn-group dropdown"><div class="dropdown column-with-actions" id="ctr_drop"><i data-toggle="dropdown" id="dropdownMenuButton" class="fa fa-sort-desc dropdown-toggle" aria-expanded="false"></i><ul class="dropdown-menu left" aria-labelledby="dropdownMenuButton"><li><a class="dropdown-item" href="#">VIEW</a></li></ul></div></div></td><td class="bs-checkbox wth45"><input data-index="2" name="btSelectItem" type="checkbox" class="custom"><span class="lbl"></span><span class="lbl"></span><span class="lbl"></span></td><td><abbr title="<img title=Acquiring src=/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Cloud_Icon.svg>"><img title="Acquiring" src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Cloud_Icon.svg"></abbr></td><td><abbr id="Pending" title="Pending">Pending</abbr></td><td><abbr></abbr></td><td><abbr id="F7423685-5271-4DF6-92CB-A1CF9567E41D"></abbr></td><td><abbr id="F7423685-5271-4DF6-92CB-A1CF9567E41D" title="' + l + '">' + l + '</abbr></td><td><abbr id="F7423685-5271-4DF6-92CB-A1CF9567E41D title = "' + lang + '">' + lang + '</abbr></td></tr>');
                //localStorage.setItem("gendoc","no");
            }
        }, 3200);
    } else if (data == 0) {
        loadRelatedList('SYOBJR-98799', 'div_CTR_Quote_documents');
    }
}


function fab_details() {
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'RECORD_ID': '',
            'TABNAME': '',
            'ACTION': 'SERVICE FAB DETAILS',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': ''
        }, function (data) {

            CurrentRecordId = data;
            localStorage.setItem('CurrentRecordId', CurrentRecordId);

        });
    } catch (e) {
        console.log(e);
    }
}



function CommonParentTable() {
    AllTreeParam = maintreeparamfunction(CurrentNodeId, 0);
    TreeParam = localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    TreeParentParam = localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    TreeSuperParentParam = localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    nestedcommonparent = 'Common Parent';
    if ($("ul#carttabs_head li.active a span").text() == "Contracts") {
        nestedcommonparent = 'Common Parent Contracts';
    }
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': nestedcommonparent,
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': '',
            'TreeParam': TreeParam,
            'TreeParentParam': TreeParentParam,
            'TreeSuperParentParam': TreeSuperParentParam
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            data11 = dataset[11];
            if (document.getElementById("div_CTR_related_list")) {
                document.getElementById('div_CTR_related_list').innerHTML = datas;
                //$("#div_CTR_related_list").closest('.Related').css('display', 'block');
                $("#div_CTR_related_list").css("display", "block");
            }
            if (data4 == "NORECORDS") {
                document.getElementById('div_CTR_related_list').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                //$("#div_CTR_related_list").closest('.Related').css('display', 'block');
                $("#div_CTR_related_list").css("display", "block");
            }

            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.QUOTE_ITEM_RECORD_ID || row.CONTRACT_ITEM_RECORD_ID;
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }
                        try {
                            cpq.server.executeScript("CQNESTGRID", {
                                'TABNAME': 'Calc',
                                'ACTION': 'BUNDLE CALC',
                                'ATTRIBUTE_NAME': '',
                                'ATTRIBUTE_VALUE': '',
                                'REC_ID': filteredData,
                            }, function (datachild) {
                                if (datachild == 'YES') {
                                    WithBundleParentTable(filteredData, $detail);
                                } else {
                                    CommonChildTable(filteredData, $detail);
                                }

                            });
                        } catch (e) {
                            console.log(e);
                        }




                    }
                });
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.QUOTE_ITEM_RECORD_ID || row.CONTRACT_ITEM_RECORD_ID;
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            try {
                                cpq.server.executeScript("CQNESTGRID", {
                                    'TABNAME': 'Calc',
                                    'ACTION': 'BUNDLE CALC',
                                    'ATTRIBUTE_NAME': '',
                                    'ATTRIBUTE_VALUE': '',
                                    'REC_ID': filteredData,
                                }, function (datachild) {
                                    if (datachild == 'YES') {
                                        WithBundleParentTable(filteredData, $detail);
                                    } else {
                                        CommonChildTable(filteredData, $detail);
                                    }

                                });
                            } catch (e) {
                                console.log(e);
                            }
                        }
                    });
                }, 5000);
            }
            finally {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.QUOTE_ITEM_RECORD_ID || row.CONTRACT_ITEM_RECORD_ID;
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            try {
                                cpq.server.executeScript("CQNESTGRID", {
                                    'TABNAME': 'Calc',
                                    'ACTION': 'BUNDLE CALC',
                                    'ATTRIBUTE_NAME': '',
                                    'ATTRIBUTE_VALUE': '',
                                    'REC_ID': filteredData,
                                }, function (datachild) {
                                    if (datachild == 'YES') {
                                        WithBundleParentTable(filteredData, $detail);
                                    } else {
                                        CommonChildTable(filteredData, $detail);
                                    }

                                });
                            } catch (e) {
                                console.log(e);
                            }
                        }
                    });
                }, 5000);
            }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);

        });
        $(".JCLRgrip").mousedown(function () {

            $("thead.fullHeadFirst").css("cssText", "z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "none");

        });
        var arr_value = [];
        $(".JCLRgrip").mouseup(function () {

            var th_width_resize = [];
            $("#table_common_parent thead.fullHeadFirst tr th").each(function (index) {
                var wid = $(this).css("width");

                if (index == 0 || index == 1) {
                    th_width_resize.push("60px");
                } else {
                    th_width_resize.push(wid);
                }
            });


            $("thead.fullHeadFirst").css("cssText", "position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "table-header-group");

            var txt_alg = []
            $('table#table_common_parent thead.fullHeadSecond tr th').each(function (index) {
                var a = $(this).css('text-align');
                txt_alg.push(a);
            });

            $("#table_common_parent thead.fullHeadFirst tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });
            $("#table_common_parent thead.fullHeadSecond tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });



            $('div[id^=listBoxRelatedMutipleCheckBoxDrop_]').each(function (index) {

                var avoid_set = 0;
                var listdrop_disp = $(this).css('display');

                if (listdrop_disp == 'block') {
                    var cur_grid = $(this).attr('id');

                    var get_id = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').attr('id');

                    var insert_data = cur_grid + '|' + get_id;

                    if (arr_value.indexOf(insert_data) !== -1) {
                        delete arr_value[insert_data];
                        const index = arr_value.indexOf(insert_data);
                        if (index > -1) {
                            arr_value.splice(index, 1);
                        }

                        avoid_set = 1;
                    }
                    else {
                        arr_value.push(insert_data);
                    }

                    if (avoid_set == 0) {
                        var left_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left');

                        if (left_drop) {
                            left_drop = left_drop.split('px');
                            left_drop = parseInt(left_drop[0]) - 1;

                        }

                        left_drop = left_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left', left_drop);


                        var width_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').width();

                        width_drop = width_drop + 1;

                        width_drop = width_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').css('width', width_drop);
                    }

                }
            });


        });
    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_common_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}

function CommonChildTable(filteredData, $detail) {
    ChildEquipmentId = localStorage.setItem("ChildEquipmentId", filteredData)
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Common Child',
            'ACTION': 'CHILDLOAD',
            'ATTRIBUTE_NAME': filteredData,
            'ATTRIBUTE_VALUE': ''
        }, function (datachild) {

            datachld_table = datachild[0];
            datachld = datachild[1];
            datachld2 = datachild[2];
            datachld3 = datachild[3];
            datachld4 = datachild[4];
            datachld5 = datachild[5];
            datachld6 = datachild[6];
            datachld7 = datachild[7];
            datachld8 = datachild[8];
            datachld9 = datachild[9];
            datachld10 = datachild[10];
            datachld11 = datachild[11];
            if (datachld4 == "NORECORDS") {
                $detail.html('<div class="noRecDisp noRecDisp1">No Records to Display</div>')
            }
            else {
                $detail.html(datachld_table).find('table#' + datachld2).bootstrapTable({
                    data: datachld,
                });
            }
            $('#' + datachld2).after(datachld10);
            eval(datachld9);
            eval(datachld3);
            eval(datachld5);
        });
    } catch (e) {
        console.log(e);
    }
}


function SparePartsList() {
    breadCrumb_Reset();
    try {
        cpq.server.executeScript("CQNESTCPSG", {
            'TABNAME': 'Spare Parts Parent',
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': ''
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            if (document.getElementById("div_CTR_related_list")) {
                document.getElementById('div_CTR_related_list').innerHTML = datas;
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
            }
            if (data4 == "NORECORDS") {
                document.getElementById('div_CTR_related_list').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
            }

            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.PART_NUMBER || '';
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }
                        SparePartsSubList(filteredData, $detail);
                    }
                });
            } catch (err) { }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);

        });

    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_spareparts_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}


function SparePartsSubList(filteredData, $detail) {
    //filteredData_1=filteredData.split(">");
    //filteredData_2=filteredData_1[1].split("<");
    //filteredData=filteredData_2[0];
    try {
        cpq.server.executeScript("CQNESTCPSG", {
            'TABNAME': 'Spare Parts Child',
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': filteredData,
            'ATTRIBUTE_VALUE': ''
        }, function (datachild) {

            datachld_table = datachild[0];
            datachld = datachild[1];
            datachld2 = datachild[2];
            datachld3 = datachild[3];
            datachld4 = datachild[4];
            datachld5 = datachild[5];
            datachld6 = datachild[6];
            datachld7 = datachild[7];
            datachld8 = datachild[8];
            datachld9 = datachild[9];
            datachld10 = datachild[10];
            datachld11 = datachild[11];
            if (datachld4 == "NORECORDS") {
                $detail.html('<div class="noRecDisp noRecDisp1">No Records to Display</div>')
            }
            else {
                $detail.html(datachld_table).find('table#' + datachld2).bootstrapTable({
                    data: datachld,
                });
            }
            $('#' + datachld2).after(datachld10);
            eval(datachld9);
            eval(datachld3);
            eval(datachld5);
        });
    } catch (e) {
        console.log(e);
    }
}

//Quote Items With bundle Nested grid functions.....
function WithBundleParentTable(filteredData, $detail) {
    ChildEquipmentId = localStorage.setItem("ChildEquipmentId", filteredData)
    AllTreeParam = maintreeparamfunction(CurrentNodeId, 0);
    TreeParam = localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    TreeParentParam = localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    TreeSuperParentParam = localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'WITH BUNLDLE PARENT TABLE',
            'ACTION': 'CHILDLOAD',
            'ATTRIBUTE_NAME': filteredData,
            'ATTRIBUTE_VALUE': '',
            'TreeParam': TreeParam,
            'TreeParentParam': TreeParentParam,
            'TreeSuperParentParam': TreeSuperParentParam
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            //A055S000P01-3263 issue 1 start
            // localStorage.setItem('openedWithBundleParentTableId',data2);
            // setTimeout(()=>{
            // var a=localStorage.getItem('openedWithBundleParentTableId');
            // openedParentId=$('#'+a).parents('tr').prev().children('td:nth-child(4)').children('a:nth-child(2)').attr('id');
            // console.log(openedParentId);
            // localStorage.setItem('openedWithBundleParentTableId',openedParentId);
            // },500);
            //A055S000P01-3263 issue 1 end
            // if (document.getElementById("div_CTR_With_Bunble_Parent_Table")) {
            // 	document.getElementById('div_CTR_With_Bunble_Parent_Table').innerHTML = datas;
            // 	$("#div_CTR_With_Bunble_Parent_Table").closest('.Related').css('display', 'block');
            // }
            // if (data4 == "NORECORDS"){
            // 	document.getElementById('div_CTR_With_Bunble_Parent_Table').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
            // 	$("#div_CTR_With_Bunble_Parent_Table").closest('.Related').css('display', 'block');
            // }
            if (data4 == "NORECORDS") {
                $detail.html('<div class="noRecDisp noRecDisp1">No Records to Display</div>')
            }
            else {
                $detail.html(datas).find('table#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.QUOTE_ITEM_RECORD_ID || '';
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }
                        CommonChildTable(filteredData, $detail);
                    }
                });
            }
            // $('#' + data2).after(data10);
            // eval(data9);
            // eval(data3);
            // eval(data5);
            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.QUOTE_ITEM_RECORD_ID || '';
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }
                        CommonChildTable(filteredData, $detail);
                    }
                });
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.QUOTE_ITEM_RECORD_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }
                            CommonChildTable(filteredData, $detail);
                        }
                    });
                }, 5000);
            }
            finally {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.QUOTE_ITEM_RECORD_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }
                            CommonChildTable(filteredData, $detail);
                        }
                    });
                }, 5000);
            }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);

        });
        $(".JCLRgrip").mousedown(function () {

            $("thead.fullHeadFirst").css("cssText", "z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "none");

        });
        var arr_value = [];
        $(".JCLRgrip").mouseup(function () {

            var th_width_resize = [];
            $("#table_common_parent thead.fullHeadFirst tr th").each(function (index) {
                var wid = $(this).css("width");

                if (index == 0 || index == 1) {
                    th_width_resize.push("60px");
                } else {
                    th_width_resize.push(wid);
                }
            });


            $("thead.fullHeadFirst").css("cssText", "position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "table-header-group");

            var txt_alg = []
            $('table#table_common_parent thead.fullHeadSecond tr th').each(function (index) {
                var a = $(this).css('text-align');
                txt_alg.push(a);
            });

            $("#table_common_parent thead.fullHeadFirst tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });
            $("#table_common_parent thead.fullHeadSecond tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });



            $('div[id^=listBoxRelatedMutipleCheckBoxDrop_]').each(function (index) {

                var avoid_set = 0;
                var listdrop_disp = $(this).css('display');

                if (listdrop_disp == 'block') {
                    var cur_grid = $(this).attr('id');

                    var get_id = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').attr('id');

                    var insert_data = cur_grid + '|' + get_id;

                    if (arr_value.indexOf(insert_data) !== -1) {
                        delete arr_value[insert_data];
                        const index = arr_value.indexOf(insert_data);
                        if (index > -1) {
                            arr_value.splice(index, 1);
                        }

                        avoid_set = 1;
                    }
                    else {
                        arr_value.push(insert_data);
                    }

                    if (avoid_set == 0) {
                        var left_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left');

                        if (left_drop) {
                            left_drop = left_drop.split('px');
                            left_drop = parseInt(left_drop[0]) - 1;

                        }

                        left_drop = left_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left', left_drop);


                        var width_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').width();

                        width_drop = width_drop + 1;

                        width_drop = width_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').css('width', width_drop);
                    }

                }
            });


        });
    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_common_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}


function salespriceeditablity(ele) {
    service_id = $("#part_shortdesc a:nth-child(1) span").text();
    cpq.server.executeScript("CQCUSTFLDS", {
        'service_id': service_id
    }, function (dataset) {
        editablity = dataset[1];
        if (editablity == "true") {
            $(ele).removeAttr('readonly')
            $('div#seginnerbnr').children('button').css('display', 'none');
            $('#NET_PRICE input').addClass('light_yellow');
            $("#seginnerbnr").append('<button id="hidesalepricesave" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="salepricesave(this)">SAVE</button><button id="hidesalepricecancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="salepricecancel(this)">CANCEL</button>')
        }
        else {
            $('#NET_PRICE input').addClass('cursor_notallow');
        }

    });

}

function salepricesave() {
    lineitemid = $("#RolledUpCartItem  span").text();
    saleprice = $("#NET_PRICE input").val();
    service_id = $("#part_shortdesc a:nth-child(1) span").text();
    cpq.server.executeScript("CQCUSTFLDS", {
        'customfield': "Yes",
        'saleprice': saleprice,
        'service_id': service_id,
        'lineitemid': lineitemid
    }, function (dataset) {
        $('div#seginnerbnr').children('button').css('display', 'none');
        $('#generate-line-items').css('display', 'block');
        $('#CALCULATE_QItems').css('display', 'block');
        localStorage.setItem("add_new_functionality", "TRUE");
        $("[id='qtn_save'] span").click();
    });

}

function salepricecancel() {
    $('div#seginnerbnr').children('button').css('display', 'none');
    $('#generate-line-items').css('display', 'block');
    $('#CALCULATE_QItems').css('display', 'block');
    localStorage.setItem("add_new_functionality", "TRUE");
    $("[id='qtn_save'] span").click();
}


function discounteditablity(ele) {
    service_id = $("#part_shortdesc a:nth-child(1) span").text();
    cpq.server.executeScript("CQCUSTFLDS", {
        'service_id': service_id
    }, function (dataset) {
        editablity = dataset[1];
        if (editablity == "true") {
            $(ele).removeAttr('readonly')
            $('div#seginnerbnr').children('button').css('display', 'none');
            $('#DISCOUNT input').addClass('light_yellow');
            $("#seginnerbnr").append('<button id="hidediscountsave" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="discountsave(this)">SAVE</button><button id="hidediscountcancel" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="discountcancel(this)">CANCEL</button>')
        }
        else {
            $('#DISCOUNT input').addClass('cursor_notallow');
        }

    });

}

function discountsave() {
    lineitemid = $("#RolledUpCartItem  span").text();
    discount = $("#DISCOUNT input").val();
    service_id = $("#part_shortdesc a:nth-child(1) span").text();
    cpq.server.executeScript("CQCUSTFLDS", {
        'customfield': "Yes",
        'discount': discount,
        'service_id': service_id,
        'lineitemid': lineitemid
    }, function (dataset) {
        $('div#seginnerbnr').children('button').css('display', 'none');
        $('#generate-line-items').css('display', 'block');
        $('#CALCULATE_QItems').css('display', 'block');
        localStorage.setItem("add_new_functionality", "TRUE");
        $("[id='qtn_save'] span").click();
    });

}

function discountcancel() {
    $('div#seginnerbnr').children('button').css('display', 'none');
    $('#generate-line-items').css('display', 'block');
    $('#CALCULATE_QItems').css('display', 'block');
    localStorage.setItem("add_new_functionality", "TRUE");
    $("[id='qtn_save'] span").click();
}


function ToolIdleEdit(ele) {
    $("#contract_cust_fields_div").css("display", "block");
    cpq.server.executeScript("CQCONTTLID", { 'ACTION': 'CONT_TOOL_IDLE', 'MODE': 'EDIT' }, function (dataset) {
        var [datas] = [dataset[0]];

        if (document.getElementById("contract_sec_tool")) {
            document.getElementById("contract_sec_tool").innerHTML = datas;

            $('#contract_sec_tool').bootstrapTable({ data: datas });
        }
        $('.contract_tab #ctr_drop').css('cssText', 'display:none !important;');
        $('#contract_sec_tool #container').after('<div id="quotesummarysavecancel" class="col-md-12 text-center"><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn flt_none" onclick="ToolIdleCancel()">CANCEL</button><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn flt_none" onclick="ToolIdleSave()">SAVE</button></div>');

    });
}

function ToolIdleCancel(ele) {
    $("#contract_cust_fields_div").css("display", "block");
    cpq.server.executeScript("CQCONTTLID", { 'ACTION': 'CONT_TOOL_IDLE', 'MODE': 'CANCEL' }, function (dataset) {
        var [datas] = [dataset[0]];

        if (document.getElementById("contract_sec_tool")) {
            document.getElementById("contract_sec_tool").innerHTML = datas;

            $('#contract_sec_tool').bootstrapTable({ data: datas });
        }
        $('.contract_tab #ctr_drop').css('cssText', 'display:block !important;');
        $('#hidesavecancel').css('cssText', 'display:none !important;');


    });
}
function ToolIdleSave(ele) {
    $("#contract_cust_fields_div").css("display", "block");
    var dict = {};
    $('#contract_sec_tool tbody tr').each(function (index) {
        //var nodeText = $(this).find('td:nth-child(1)').text();
        var value = $(this).find('td:nth-child(4) input').length;
        if (value > 0) {
            var nodeText = $(this).find('td:nth-child(4) input').attr('id');
            var nodevalue = $(this).find('td:nth-child(4) input').val();
        }
        var value = $(this).find('td:nth-child(4) select').length;
        if (value > 0) {
            var nodeText = $(this).find('td:nth-child(4) select').attr('id');
            var nodevalue = $(this).find('td:nth-child(4) select').val();
        }
        var value = $(this).find('td:nth-child(4) textarea').length;
        if (value > 0) {
            var nodeText = $(this).find('td:nth-child(4) textarea').attr('id');
            var nodevalue = $(this).find('td:nth-child(4) textarea').val();
        }

        dict[nodeText] = nodevalue;


    });
    cpq.server.executeScript("CQCONTTLID", { 'ACTION': 'CONT_TOOL_IDLE_SAVE', 'MODE': 'SAVE', 'DICT': JSON.stringify(dict) }, function (dataset) {
        var [datas] = [dataset[0]];

        //if (document.getElementById("contract_sec_tool")) {
        //document.getElementById("contract_sec_tool").innerHTML = datas;

        $('#contract_sec_tool').bootstrapTable({ data: datas });
        //}
        $('.contract_tab #ctr_drop').css('cssText', 'display:block !important;');
        $('#hidesavecancel').css('cssText', 'display:none !important;');

        cpq.server.executeScript("CQCONTTLID", { 'ACTION': 'CONT_TOOL_IDLE', 'MODE': 'VIEW' }, function (dataset) {
            var [datas] = [dataset[0]];

            if (document.getElementById("contract_sec_tool")) {
                document.getElementById("contract_sec_tool").innerHTML = datas;

                $('#contract_sec_tool').bootstrapTable({ data: datas });
            }
            $('.contract_tab #ctr_drop').css('cssText', 'display:block !important;');
            $('#hidesavecancel').css('cssText', 'display:none !important;');


        });


    });
}
function QuoteSummaryEdit(ele) {
    //$('#quotesummarysavecancel').show()
    $('.quote_summary_tab  #ctr_drop').css('cssText', 'display:none !important;');
    $('.section_cust_fld_val i.fa.fa-pencil').css('cssText', 'pointer-events: none;');
    $('.quote_summary_sec').wrapAll('<div class="header_section_div header_section_div_pad_bt10 row"></div>');
    $('.section_cust_fld_val i.fa.fa-pencil').addClass('edit_pencil');
    $('.quote_summary_sec:last-child').after('<div id="quotesummarysavecancel" class="col-md-12 text-center"><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn flt_none" onclick="quotesummaryCancel()">CANCEL</button><button id="hidesavecancel" class="btnconfig btnMainBanner sec_edit_sty_btn flt_none" onclick="quotesummarysave()">SAVE</button></div>');
    $('input#discount').removeAttr("disabled");
    $('input#discount').addClass('light_yellow');
    $('.quote_summary_tab').removeAttr('data-toggle');

}

function quotesummarysave() {
    Discount = $('input#discount').val();
    cpq.server.executeScript("CQUDQTSMRY", {
        'Discount': Discount
    }, function (dataset) {
        //$("[id='qtn_save'] span").click();
        localStorage.setItem("add_new_functionality", "TRUE");
        $(".header_section_div.header_section_div_pad_bt10").removeClass();
        $('input#discount').attr("disabled", true);
        $('input#discount').removeClass('light_yellow');
        $('#quotesummarysavecancel').css("display", "none");
        CommonLeftView();
        CurrentNodeId = localStorage.getItem("CurrentNodeId");
        CommonRightView(CurrentNodeId);
        cpq.models.cart.updateCartItems();
    });

}

function quotesummaryCancel() {

    localStorage.setItem("add_new_functionality", "TRUE");
    $(".header_section_div.header_section_div_pad_bt10").removeClass();
    $('input#discount').attr("disabled", true);
    $('input#discount').removeClass('light_yellow');
    $('#quotesummarysavecancel').css("display", "none");
    CommonLeftView();
    CurrentNodeId = localStorage.getItem("CurrentNodeId");
    CommonRightView(CurrentNodeId);
    //$("[id='qtn_save'] span").click();

}
function PricingPickListOnclick() {
    var picklist_value = $("#pricing_picklist_select :selected").attr('value');
    cpq.server.executeScript("SYULODTREE", {
        'ACTION': "ONCHANGE",
        'LOAD': 'PRICING PICKLIST',
        'picklist_value': picklist_value

    }, function (dataset) {
        rec_id = localStorage.getItem("picklist_rec_id")
        subTabDetails('Annualized Items', 'Related', 'SAQICO', rec_id);
    })
}




function hide_year_columns() {
    contract_valid_from = $('.segment_revision_status_text').text();
    contract_valid_to = $('.segment_revision_text').text();
    contract_valid_from_year = contract_valid_from.split('/')[2]
    contract_valid_to_year = contract_valid_to.split('/')[2]
    var date1 = contract_valid_from_year
    var date2 = contract_valid_to_year
    var years = date2 - date1
    if (years == '1') {
        $('th[id="YEAR_2"]').hide();
        $('td[id="YEAR_2"]').hide();
        $('th[id="YEAR_3"]').hide();
        $('td[id="YEAR_3"]').hide();
        $('th[id="YEAR_4"]').hide();
        $('td[id="YEAR_4"]').hide();
        $('th[id="YEAR_5"]').hide();
        $('td[id="YEAR_5"]').hide();
        // $('#YEAR_2').hide();
        // $('#YEAR_3').hide();
        // $('#YEAR_4').hide();
        // $('#YEAR_5').hide();
    }
    else if (years == '2') {
        $('th[id="YEAR_3"]').hide();
        $('td[id="YEAR_3"]').hide();
        $('th[id="YEAR_4"]').hide();
        $('td[id="YEAR_4"]').hide();
        $('th[id="YEAR_5"]').hide();
        $('td[id="YEAR_5"]').hide();
        // $('#YEAR_3').hide();
        // $('#YEAR_4').hide();
        // $('#YEAR_5').hide();
    }
    else if (years == '3') {
        $('th[id="YEAR_4"]').hide();
        $('td[id="YEAR_4"]').hide();
        $('th[id="YEAR_5"]').hide();
        $('td[id="YEAR_5"]').hide();
        // $('#YEAR_4').hide();
        // $('#YEAR_5').hide();
    }
    else if (years == '4') {
        //$('#YEAR_5').hide();
        $('th[id="YEAR_5"]').hide();
        $('td[id="YEAR_5"]').hide();
    }
}


function parts_list() {
    if ($('#AGS_Z0091_TSC_NONCNS').attr('title') == 'Some Exclusions' || $('#AGS_Z0004_TSC_NONCNS').attr('title') == 'Some Exclusions' ||
        $('#AGS_Z0007_TSC_NONCNS').attr('title') == 'Some Exclusions' ||
        $('#AGS_Z0007_TSC_NONCNS').attr('title') == 'Some Inclusions' ||
        $('#AGS_Z0006_TSC_NONCNS').attr('title') == 'Some Exclusions' ||
        $('#AGS_Z0092_TSC_NONCNS').attr('title') == 'Some Exclusions' ||
        $('#AGS_Z0092_TSC_CONADD').attr('title') == 'Some Exclusions' ||
        $('#AGS_Z0091_TSC_CONSUM').attr('title') == 'Some Exclusions' ||
        $('#AGS_Z0004_TSC_CONSUM').attr('title') == 'Some Exclusions' ||
        $('#AGS_Z0007_TSC_CONSUM').attr('title') == 'Some Exclusions' ||
        $('#AGS_Z0007_TSC_CONSUM').attr('title') == 'Some Inclusions' ||
        $('#AGS_Z0006_TSC_CONSUM').attr('title') == 'Some Exclusions') {
        $('div#COMMON_TABS').find("li a:contains('Parts List')").parent().css("display", "block");
    }
    else {
        $('div#COMMON_TABS').find("li a:contains('Parts List')").parent().css("display", "none");
    }
}



/*function showdeliverymodegrid(){
    //breadCrumb_Reset();
    //subTabText = "EDIT DELIVERY SCHEDULE"
	
    $('div#COMMON_TABS').find("li a:contains('Spare Parts')").parent().css("display", "none");
    $('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
    $('div#COMMON_TABS').find("li a:contains('Details')").parent().css("display", "none");
    //$('div#COMMON_TABS').find("li a:contains('Delivery Schedule')").parent().css("display", "block");
    //$('div#COMMON_TABS').find("li a:contains('Entitlements')").parent().css("display", "none");
    $("#div_CTR_related_list").css("display", "none");
    $('div#COMMON_TABS').find("li a:contains('Delivery Schedule')").parent().click();
    $('div#COMMON_TABS').find("li a:contains('Delivery Schedule')").parent().css("display", "none");
    //Action_Str = '<li><a <abbr title="'+subTabText+'">'+subTabText+'</abbr></a><span class="angle_symbol"><img src="/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>'
    //$('ul.breadcrumb').append(Action_Str);
}*/


function showdeliverymodegrid() {
    $('#bulkedit_delivery_mode').css('display', 'none');
    $('#delivery_save').css('display', 'block');
    $('#delivery_cancel').css('display', 'block');
    $('.deliveryclassedit').parent().css('background-color', 'lightyellow');
    $('.deliveryclassedit').removeAttr('disabled');
}


function openDeliveryMatrixDateChangeModal(ele) {
    var billingDate = ele;
    $('div#delivery_viewModal input#DELIVERY_SCHED_DATE').val(billingDate);

    $('div#delivery_viewModal input#DELIVERY_DATE_ORIGINAL').val(billingDate);
    $('#delivery_viewModal').modal('show');
    $('#billingmatrix_save').css('display', 'none');
    $('#billingmatrix_cancel').css('display', 'none');

}
$('.cpq_cust_notify').css('display', 'none');

function showSdeliverysave() {



    var GEtdeliverydictdata = JSON.parse(localStorage.getItem('getdeliverydictdata'));
    var getedited_amt = localStorage.getItem('getdeliveryamt');
    //var totalyear = document.getElementById("getbillyear").innerHTML
    var totalyear = $('#COMMON_TABS li.active').text().trim();

    cpq.server.executeScript("CQBILLEDIT", {
        'deliverydict': GEtdeliverydictdata,
        'totalyear': totalyear,
        'getedited_amt': getedited_amt,
        'deliveryEdit': 'DELIVERYEDIT'


    }, function (data) {
        //console.log('inside---data----',data);
        data2 = data[1];
        //console.log('inside--data2--',data2);
        $('.cpq_cust_notify').css('display', 'block');
        if (data2 == 'NOTSAVE') { $('#delivery_save').css('display', 'none'); } else {
            $('#delivery_save').css('display', 'none');
            $('#delivery_cancel').css('display', 'none');
            $('#bulkedit_delivery_mode').css('display', 'block');
            RecId = "SYOBJR-34575"
            RecName = "div_CTR_related-list"
            loadRelatedList(RecId, RecName);

        }

    });
}
function showSdeliverycancel() {

    RecId = "SYOBJR-34575"
    RecName = "div_CTR_related-list"
    loadRelatedList(RecId, RecName);
    $('#delivery_save').css('display', 'none');
    $('#delivery_cancel').css('display', 'none');
    $('#bulkedit_delivery_mode').css('display', 'block');
}




//Breadcrumb operation regarding fts scenarios.....

function fts_breadcrumb(account_id) {

    Action_Str = '<li><a onclick="fts_redirection_to_account_details()" <abbr title="' + account_id + '">' + account_id + '</abbr></a><span class="angle_symbol"><img src="/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"></span></li>'
    $('ul.breadcrumb').append(Action_Str);

}

function fts_redirection_to_account_details() {
    CurrentNodeId = localStorage.getItem('CurrentNodeId')
    account_details = localStorage.getItem("account_details_hyperlink")
    CommonRightView(CurrentNodeId)
    setTimeout(function () {
        $('#' + account_details).click();
    }, 3500);
}

function EventsTreeTable() {
    breadCrumb_Reset();
    $('#div_CTR_related_list').css('display', 'block');
    AllTreeParam = maintreeparamfunction(CurrentNodeId, 0);
    TreeParam = localStorage.setItem('CommonTreeParam', AllTreeParam['TreeParam']);
    TreeParentParam = localStorage.setItem('CommonTreeParentParam', AllTreeParam['TreeParentLevel0']);
    TreeSuperParentParam = localStorage.setItem('CommonNodeTreeSuperParentParam', AllTreeParam['TreeParentLevel1']);
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Events Parent',
            'ACTION': 'LOAD',
            'ATTRIBUTE_NAME': '',
            'ATTRIBUTE_VALUE': '',
            'TreeParam': TreeParam,
            'TreeParentParam': TreeParentParam,
            'TreeSuperParentParam': TreeSuperParentParam
        }, function (dataset) {
            datas = dataset[0];
            data1 = dataset[1];
            data2 = dataset[2];
            data3 = dataset[3];
            data4 = dataset[4];
            data4 = dataset[4];
            data5 = dataset[5];
            data6 = dataset[6];
            data7 = dataset[7];
            data8 = dataset[8];
            data9 = dataset[9];
            data10 = dataset[10];
            nso_included = dataset[14]; //A055S000P01-20390
            if (document.getElementById("div_CTR_related_list")) {
                document.getElementById('div_CTR_related_list').innerHTML = datas;
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
            }
            if (data4 == "NORECORDS") {
                document.getElementById('div_CTR_related_list').innerHTML = '<div class="noRecDisp">No Records to Display</div>';
                $("#div_CTR_related_list").closest('.Related').css('display', 'block');
            }

            try {
                $('#' + data2).bootstrapTable({
                    data: data1,
                    onExpandRow: function (index, row, $detail) {
                        filteredData = row.QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID || row.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID || row.APPROVAL_CHAIN_STEP_RECORD_ID || '';
                        if (filteredData == '') {
                            filteredData = row.REC_ID
                        }



                        Events_child(filteredData, $detail);
                    }
                });
            } catch (err) {
                setTimeout(function () {
                    $('#' + data2).bootstrapTable({
                        data: data1,
                        onExpandRow: function (index, row, $detail) {
                            filteredData = row.QUOTE_REV_PO_GRNBK_PM_EVEN_ASSEMBLIES_RECORD_ID || row.QUOTE_REV_PO_GBK_GOT_CODE_PM_EVENTS_RECORD_ID || row.APPROVAL_CHAIN_STEP_RECORD_ID || '';
                            if (filteredData == '') {
                                filteredData = row.REC_ID
                            }

                            Events_child(filteredData, $detail);
                        }
                    });
                }, 5000);
            }
            try {
                eval(data9);
                eval(data3);
                eval(data5);
            }
            catch (err) {
                console.log(err);
            }
            $('#' + data2).after(data10);
            //A055S000P01-16760
            if ((AllTreeParam['TreeParentLevel1'] == 'Product Offerings' && (AllTreeParam['TreeParam'] == 'Z0010' || AllTreeParam['TreeParam'] == 'Z0009')) || (AllTreeParam['TreeParentLevel2'] == 'Product Offerings' && (AllTreeParam['TreeParentLevel0'] == 'Z0010' || AllTreeParam['TreeParentLevel0'] == 'Z0009')) || (AllTreeParam['TreeParentLevel4'] == 'Product Offerings' && (AllTreeParam['TreeParentLevel2'] == 'Z0010' || AllTreeParam['TreeParentLevel2'] == 'Z0009'))) {
                $('#' + data2 + ' #INCLUDED').closest('tr').find('td:nth-child(3) input').removeAttr('disabled')
                $('#' + data2 + ' #INCLUDED').closest('tr').find('td:nth-child(3) input').attr("onclick", "OnclickAssemblyEdit(this,'TKM')");
                $('#table_event_parent thead th:nth-child(3)').find('.fht-cell').html('<input name="btSelectAll" type="checkbox" class="custom" onclick ="OnclickAssemblyallEdit(this)"><span class="lbl"></span>');
                var get_include_select = localStorage.getItem("included_value_events_master")
                if (get_include_select=="false" ){
					$('.custom').prop('checked', false);
				}
				//A055S000P01-20811 Start
				else if(get_include_select=="true" ){
					$('.custom').prop('checked', true);
				}
               //A055S000P01-20811 end
                if ($('.segment_revision_sale_id_text').text() != 'CFG-CONFIGURING'){$(".custom").attr("disabled","disabled");}else{$(".custom").removeAttr("disabled");}
            }
            //A055S000P01-20390 //INC08700581 M
        });
        $(".JCLRgrip").mousedown(function () {

            $("thead.fullHeadFirst").css("cssText", "z-index: 2;border-top: 1px solid rgb(220, 220, 220);top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "none");

        });
        var arr_value = [];
        $(".JCLRgrip").mouseup(function () {

            var th_width_resize = [];
            $("#table_event_parent thead.fullHeadFirst tr th").each(function (index) {
                var wid = $(this).css("width");

                if (index == 0 || index == 1) {
                    th_width_resize.push("60px");
                } else {
                    th_width_resize.push(wid);
                }
            });


            $("thead.fullHeadFirst").css("cssText", "position: fixed;z-index: 2;border-top: 1px solid rgb(220, 220, 220); top: 144px;border-right: 0px !important;");
            $("thead.fullHeadSecond").css("display", "table-header-group");

            var txt_alg = []
            $('table#table_event_parent thead.fullHeadSecond tr th').each(function (index) {
                var a = $(this).css('text-align');
                txt_alg.push(a);
            });

            $("#table_event_parent thead.fullHeadFirst tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis", "text-align": txt_alg[index] });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });
            $("#table_event_parent thead.fullHeadSecond tr th").each(function (index) {
                var num = th_width_resize[index].split("px");
                var numsp = parseInt(num[0]);
                numsp = numsp - 1;
                var make_str = numsp + "px";

                var c = "width:" + make_str + ";white-space: nowrap;overflow: hidden;text-overflow: ellipsis;";
                var d = "width:" + make_str + ";";
                $(this).css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div:first-child").css({ "width": make_str, "white-space": "nowrap", "overflow": "hidden", "text-overflow": "ellipsis" });
                $(this).children("div.fht-cell").css({ "width": make_str });
            });



            $('div[id^=listBoxRelatedMutipleCheckBoxDrop_]').each(function (index) {

                var avoid_set = 0;
                var listdrop_disp = $(this).css('display');

                if (listdrop_disp == 'block') {
                    var cur_grid = $(this).attr('id');

                    var get_id = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').attr('id');

                    var insert_data = cur_grid + '|' + get_id;

                    if (arr_value.indexOf(insert_data) !== -1) {
                        delete arr_value[insert_data];
                        const index = arr_value.indexOf(insert_data);
                        if (index > -1) {
                            arr_value.splice(index, 1);
                        }

                        avoid_set = 1;
                    }
                    else {
                        arr_value.push(insert_data);
                    }

                    if (avoid_set == 0) {
                        var left_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left');

                        if (left_drop) {
                            left_drop = left_drop.split('px');
                            left_drop = parseInt(left_drop[0]) - 1;

                        }

                        left_drop = left_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').parent().css('left', left_drop);


                        var width_drop = $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').width();

                        width_drop = width_drop + 1;

                        width_drop = width_drop + 'px';

                        $(this).find('div[id^=innerListBoxRelatedMutipleCheckBoxDrop_]').css('width', width_drop);
                    }

                }
            });


        });
    } catch (e) {
        console.log(e);
    }
    try {
        setTimeout(function () {
            $("#table_event_parent").colResizable({
                resizeMode: 'fit',
            });

        }, 5000);

    } catch (err) { }

}

function Events_child(filteredData, $detail) {
    ChildEquipmentId = localStorage.setItem("ChildEquipmentId", filteredData)
    try {
        cpq.server.executeScript("CQNESTGRID", {
            'TABNAME': 'Events child',
            'ACTION': 'CHILDLOAD',
            'ATTRIBUTE_NAME': filteredData,
            'ATTRIBUTE_VALUE': ''
        }, function (datachild) {

            datachld_table = datachild[0];
            datachld = datachild[1];
            datachld2 = datachild[2];
            datachld3 = datachild[3];
            datachld4 = datachild[4];
            datachld5 = datachild[5];
            datachld6 = datachild[6];
            datachld7 = datachild[7];
            datachld8 = datachild[8];
            datachld9 = datachild[9];
            datachld10 = datachild[10];
            datachld11 = datachild[11];
            if (datachld4 == "NORECORDS") {
                $detail.html('<div class="noRecDisp noRecDisp1">No Records to Display</div>')
            }
            else {
                $detail.html(datachld_table).find('table#' + datachld2).bootstrapTable({
                    data: datachld,
                });
            }
            $('#' + datachld2).after(datachld10);
            eval(datachld9);
            eval(datachld3);
            eval(datachld5);
        });
    } catch (e) {
        console.log(e);
    }
}
//INC08700581
function OnclickAssemblyallEdit(ele){

	included_selecte_vals = $(ele).val();
	included_value = $(ele).prop("checked");
	
	console.log('included_value--->',included_value)
	console.log('included_selecte_vals--->',included_selecte_vals)
	included_value_select = localStorage.setItem("included_value_events_master", included_value)
	//INC08700581 starts here
	included_value_select_two = $("#table_event_parent .bs-checkbox.wid45 .custom").prop("checked");
	console.log('included_value_select_two--->',included_value_select_two)
	included_value_select_two_value = localStorage.setItem("included_value_select_master", included_value_select_two)
	//INC08700581 ends here
	where_condition_events = localStorage.getItem("where_events");
	prod_type = 'TKMALL'
	if (prod_type == 'TKMALL'){
		try {
        cpq.server.executeScript("CQASSMEDIT", {
            'ACTION': 'SAVE_ASSEMBLY_ALL',
            'included_value': included_value,
            'subtab': localStorage.getItem("currentSubTab"),
            'prod_type': prod_type,
			'WHERE_CONDITION':where_condition_events,// INC08700581	A
        }, function (data) {
			subTabDetails('Events', 'Related','SAQTSV', 'A10AAB18-2FD5-4721-AA0F-5902BDA923C2')
        });

    } catch (e) {
        console.log(e);
    }
		
	}
	
	if (included_value== 'true'){
		$(ele).prop("checked");console.log('18164----');
		$('#table_event_parent .custom_events').prop('checked', true);
		$("#table_event_parent #INCLUDED").prop('checked', true);
		}
	else{
					//$('.incevents').prop('checked', true);}
					$('#table_event_parent .custom_events').prop('checked', false);
					$("#table_event_parent #INCLUDED").prop('checked', false);
					}
	
	//if (included_value=='false')
					//{$('.custom').prop('checked', false);$("#table_event_parent #INCLUDED").prop('checked', false);}
				//else{
					//$('.incevents').prop('checked', true);}
					//$('.custom').prop('checked', true);$("#table_event_parent #INCLUDED").prop('checked', true);}
}
//INC08700581
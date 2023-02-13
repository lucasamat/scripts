/* CONFIGURATOR UPDATE 'BEGIN' */
console.log("CONFIGURATOR start"+window.location.href);

cpq.events.sub("API:configurator:updated", function (data) {
	console.log("INSIDE CONFIGURATOR"+window.location.href);
    debugger;
    console.log("CPQ configurator");
	 
	var CurrentTab = $('ul#carttabs_head .active a span').text();
    if (CurrentTab == "Quotes"){
        $('.progress_bar_header').show();
        $('#Generate_Documents').show();
    }
    else{
        $('.progress_bar_header').hide();
        $('#Generate_Documents').hide();
    }
    contract_tab = localStorage.getItem("contract_tab");
    var myVar = setInterval(myTimer, 5000);
        function myTimer() {
            contract_tab_id = document.getElementById("tab_Contracts");
            if (contract_tab == "true"){
                if (contract_tab_id){
                    $("#tab_Contracts").click();
                    localStorage.setItem("contract_tab","false");
                }
            }
        }
    if (localStorage.getItem('SECTION_EDIT') == 'SYSECT-PB-00067' && $('input:checkbox:first').prop('checked') == true) {
        $("#header_section_divapp #SYSECT-PB-00067").attr('data-target', '');
    }
    else if (localStorage.getItem('SECTION_EDIT') == 'SYSECT-PB-00067' && $('input:checkbox:first').prop('checked') == false) {
        $("#header_section_divapp #SYSECT-PB-00067").attr('data-target', '#processing_modal');
    }
    $('.iconhvr label').each(function (index) {
        var label_txt = $(this).text();
        if (label_txt == 'Last Modified By' || label_txt == 'Added By') {
            var added_by = $(this).closest('.iconhvr').children('td:nth-child(2)').children('input').val();
            var lastModified_by = $(this).closest('.iconhvr').children('td:nth-child(3)').children('input').val();
            $(this).closest('.iconhvr').children('td:nth-child(2)').children('input').attr('title', added_by);
            $(this).closest('.iconhvr').children('td:nth-child(3)').children('input').attr('title', lastModified_by);
        }
    });
	try{
		if (window.innerWidth < 1300) {
			$('.cust_primary_btn').closest('div#ctr_drop_prime_panel').css('display', 'block');
			$('.cust_def_btn').css('display', 'none');
		}		
		$(window).resize(function(){
		if (window.innerWidth < 1300) {
			$('.cust_primary_btn').closest('div#ctr_drop_prime_panel').css('display', 'block');
			$('.cust_def_btn').css('display', 'none');
		}
		else{
		    $('.cust_primary_btn').closest('div#ctr_drop_prime_panel').css('display', 'none');
			$('.cust_def_btn').css('display', 'block');
			$('#BTN_MA_ALL_REFRESH').css('display', 'none');
		}
	   })
	}catch (e) {
			console.log(e);
		}
    var page_load = localStorage.getItem("page_reload");
    var btn_txt_val = localStorage.getItem('btn_txt_val');
    if (btn_txt_val == 'SAVE') {
        var keydata = $('#attributesContainer .Detail input').first().val();
        if (keydata != '') {
            localStorage.setItem('keyData', keydata);
        }
    }
    if (page_load == '1') {
        var val = localStorage.getItem("related_page_redirect");
        cont_RL_openaddnew_product(val)
    }
    ButtonName = '';
    if (document.getElementById('BTN_SYACTI_MA_00008_SAVE')) {
        ButtonName = document.getElementById('BTN_SYACTI_MA_00008_SAVE').innerHTML;
    }
    if (ButtonName == 'EDIT') {
        $('#SYSEFL-MA-00434').attr('disabled', 'disabled');
        $('button.pivot_material_action').attr('disabled', 'disabled');
    }
    if (document.getElementById('BTN_SYACTI_MA_00024_EDIT')) {
        ButtonName = document.getElementById('BTN_SYACTI_MA_00024_EDIT').innerHTML;
    }
    if (document.getElementById('BTN_SYACTI_MA_00023_SAVE')) {
        ButtonName = document.getElementById('BTN_SYACTI_MA_00023_SAVE').innerHTML;
    }
	
	$('input').each(function () {
        var inp = $(this).val();
        if (/^[-+]?[0-9]+\.[0-9]+$/.test(inp)) {
            $(this).attr('type', 'number');
        }
    });
 
    var current_tab_name = $('div#attributesContainer div.row div.tabbable.show-large ul.nav.nav-responsive.nav-tabs li.active').text().trim();
    if (current_tab_name != 'Apps' && current_tab_name != 'Tabs' && current_tab_name != 'Actions' && current_tab_name != 'Sections' && current_tab_name != 'Questions' && current_tab_name != 'Messages' && current_tab_name != 'Objects' && current_tab_name != 'Variables' && current_tab_name != 'Scripts') {
        var a = $('div#attributesContainer div.row div.tabbable.show-large ul.nav.nav-responsive.nav-tabs li.active ul').text();
        if (a) { }
        else {
            $('div#attributesContainer ul.nav.nav-responsive.nav-tabs li.active').css('pointer-events', 'none');
        }
    }
    var header_banner_txt = '';
    var header_banner_txt_li_Text = '';
    setTimeout(function () {
        header_banner_txt = $('ul#carttabs_head li.active a span').text();
        header_banner_txt_li_Text = $('div#attributesContainer .row .tabbable.show-large ul.nav.nav-responsive.nav-tabs li ul.dropdown-menu li.active a span').text();
        if (header_banner_txt_li_Text) {
            $('.material_header_banner').text(header_banner_txt_li_Text);
            var Action_btn_Text = localStorage.getItem("Action_Text");
            if (Action_btn_Text == "EDIT") {
                $('.row.tabsmenu2.tabdyn').css('display', 'block');
                var Edit_header = header_banner_txt_li_Text + ' : ' + Action_btn_Text;
                $('.material_header_banner').text(Edit_header);
            } else if (Action_btn_Text == "VIEW") {
                $('.row.tabsmenu2.tabdyn').css('display', 'block');
                var view_header = header_banner_txt_li_Text + ' : ' + Action_btn_Text;
                $('.material_header_banner').text(view_header);
            } else if (Action_btn_Text == "ADD NEW") {
                $('.row.tabsmenu2.tabdyn').css('display', 'block');
                var view_header = header_banner_txt_li_Text + ' : ' + Action_btn_Text;
                $('.material_header_banner').text(view_header);
            } else if (Action_btn_Text == "CLONE") {
                $('.row.tabsmenu2.tabdyn').css('display', 'block');
                var view_header = header_banner_txt_li_Text + ' : ' + Action_btn_Text;
                $('.material_header_banner').text(view_header);
            } else {
                $('.row.tabsmenu2.tabdyn').css('display', 'none');
                $('.material_header_banner').text(header_banner_txt_li_Text);
            }
        } else {
            $('.material_header_banner').text(header_banner_txt);
            var Action_btn_Text = localStorage.getItem("Action_Text");
            if (Action_btn_Text == "EDIT") {
                $('.row.tabsmenu2.tabdyn').css('display', 'block');
                var Edit_header = header_banner_txt + ' : ' + Action_btn_Text;
                $('.material_header_banner').text(Edit_header);
            } else if (Action_btn_Text == "VIEW") {
                $('.row.tabsmenu2.tabdyn').css('display', 'block');
                var view_header = header_banner_txt + ' : ' + Action_btn_Text;
                $('.material_header_banner').text(view_header);
                //$(".req-field").hide();
            } else if (Action_btn_Text == "ADD NEW") {                
                $('.row.tabsmenu2.tabdyn').css('display', 'block');
                var view_header = header_banner_txt + ' : ' + Action_btn_Text;
                $('.material_header_banner').text(view_header);
                $('.product_txt').text(getCurrentTabName);                                    
            } else if (Action_btn_Text == "ATTR_TRIGGER") {                
                $('.row.tabsmenu2.tabdyn').css('display', 'block');
                var view_header = header_banner_txt + ' : ' + Action_btn_Text;
                $('.material_header_banner').text(view_header); 
                $('.product_txt').text(getCurrentTabName);
            }else if (Action_btn_Text == "CLONE") {
                $('.row.tabsmenu2.tabdyn').css('display', 'block');
                var view_header = header_banner_txt + ' : ' + Action_btn_Text;
                $('.material_header_banner').text(view_header);
            } else {
                $('.row.tabsmenu2.tabdyn').css('display', 'none');
                $('.material_header_banner').text(header_banner_txt);
            }
        }
    }, 1000);
    var removeHorLine_edit_get = localStorage.getItem("removeHorLine_edit");
    if (removeHorLine_edit_get == "1") {
        $('.removeHorLine').removeClass('ListEmptySec');
        localStorage.setItem("removeHorLine_edit", "0");
    }
    var table_id;
    var current_tab_name = $('div#attributesContainer div.row div.tabbable.show-large ul.nav.nav-responsive.nav-tabs li.active').text().trim();
    var current_tab_name_ends = current_tab_name.endsWith('s') || current_tab_name.endsWith('S');
    setTimeout(function () {
        $('.qstn_r_contaier p.onlytext div.container table tbody tr td').each(function () {
            table_id = $(this).closest('table').attr('id');
        });
        var clicked_table = '#' + table_id + ' tbody tr';
        var last_row_data_index;
        $(clicked_table).each(function () {
            last_row_data_index = $(this).attr('data-index');
        });
        localStorage.setItem("localstg_table_id", table_id);
        localStorage.setItem("localstg_last_row_data_index", last_row_data_index);
        if (current_tab_name_ends) {
            var dis_block = $('.set_float_List').css('display');
            var dis_block_mat = $('.materialMainBan').css('display');
            if (dis_block == 'block' && dis_block_mat == 'block') {
                $('.set_float_List').addClass('set_float_List_style');
                var a = $('.set_float_List').css('width');
                var b = $('.materialMainBan').css('width');
                if (a != '' && b != '') {
                    var x = a.slice(0, -2);
                    var y = b.slice(0, -2);
                    var c = parseInt(x);
                    var d = parseInt(y);
                    if (c >= d) {
                        $('.set_float_List').addClass('set_float_List_style');
                    } else {
                        $('.set_float_List').removeClass('set_float_List_style');
                    }
                }
                $(".materialMainBan.material_head").removeAttr("style");
            }
        } else {
            $('.set_float_List').removeClass('set_float_List_style');
        }
    }, 1000);
    if (header_banner_txt == 'Categories') {
        setTimeout(function () {
            resize_fun();
        }, 300);
    }
    var module_conf_current_tab = $('div#attributesContainer ul.nav.nav-responsive.nav-tabs li.active').text().trim();
    if (module_conf_current_tab == 'Apps') {
        var btn_cancel = $('#MM_TAB_BTN_CANCEL').css('display');
        var btn_save = $('#MM_TAB_BTN_SAVE').css('display');
        if (btn_cancel == 'block' && btn_save == 'block') { }
    } else if (module_conf_current_tab == 'Tabs') {
        var btn_cancel = $('#MM_TAB_BTN_CANCEL').css('display');
        var btn_save = $('#MM_TAB_BTN_SAVE').css('display');
        if (btn_cancel == 'block' && btn_save == 'block') {
            $('#MM_TAB_MOD_REC_NO').css('background-color', '#fff');
            $('#MM_TAB_OBJ_REC_ID').css('background-color', '#fff');
            $('#MM_TAB_VIS_VAR_REC_NO').css('background-color', '#fff');
        }
    } else if (module_conf_current_tab == 'Actions') {
        var btn_cancel = $('#MM_ACT_BTN_CANCEL').css('display');
        var btn_save = $('#MM_ACT_BTN_SAVE').css('display');
        if (btn_cancel == 'block' && btn_save == 'block') {
            $('#MM_ACT_TAB_REC_ID').css('background-color', '#fff');
            $('#MM_ACT_SCR_REC_ID').css('background-color', '#fff');
            $('#MM_ACT_VIS_VARIABLE_REC_ID').css('background-color', '#fff');
        }
    } else if (module_conf_current_tab == 'Sections') {
        var btn_cancel = $('button.btnstyle.backmod.mrg-rt-8').css('display');
        var btn_save = $('#MM_SEC_BTN_SAVE').css('display');
        if (btn_cancel == 'block' && btn_save == 'block') {
            $('#MM_SEC_TAB_REC_NO').css('background-color', '#fff');
            $('#MM_SEC_PARENT_SEC_RECD_ID').css('background-color', '#fff');
            $('#MM_SEC_PRIMARY_OBJ_REC_ID').css('background-color', '#fff');
        }
    } else if (module_conf_current_tab == 'Questions') {
        var btn_cancel = $('#MM_QST_BTN_CANCEL').css('display');
        var btn_save = $('#MM_QST_BTN_SAVE').css('display');
        if (btn_cancel == 'block' && btn_save == 'block') {
            $('#MM_QST_SEC_RECD_NO').css('background-color', '#fff');
            $('#MM_QST_RES_VIS_VAR_RECD_NO').css('background-color', '#fff');
            $('#MM_QST_RES_EDIT_VAR_RECD_NO').css('background-color', '#fff');
            $('#MM_QST_DEF_RES_VAR_RECD_NO').css('background-color', '#fff');
            $('#MM_QST_REC_VAR_RECD_NO').css('background-color', '#fff');
            $('#MM_QST_VER_RES_VAR_RECD_NO').css('background-color', '#fff');
        }
    } else if (module_conf_current_tab == 'Messages') {
        var btn_cancel = $('#MM_MSG_BTN_CANCEL').css('display');
        var btn_save = $('#MM_MSG_BTN_SAVE').css('display');
        if (btn_cancel == 'block' && btn_save == 'block') {
            $('#MM_MSG_TAB_REC_NO').css('background-color', '#fff');
            $('#MM_MSG_MSG_VAR_REC_NO').css('background-color', '#fff');
        }
    } else if (module_conf_current_tab == 'Objects') {
        var btn_cancel = $('#MM_OBJ_BTN_CANCEL').css('display');
        var btn_ = $('#MM_OBJ_BTN_SAVE').css('display');
    } else if (module_conf_current_tab == 'Variables') {
        var btn_cancel = $('#MM_VAR_BTN_CANCEL').css('display');
        var btn_save = $('#MM_VAR_BTN_SAVE').css('display');
    } else if (module_conf_current_tab == 'Scripts') {
        var btn_cancel = $('#MM_SCR_BTN_CANCEL').css('display');
        var btn_save = $('#MM_SCR_BTN_SAVE').css('display');
        if (btn_cancel == 'block' && btn_save == 'block') {
            $('#MM_SCR_TAB_NAME').css('background-color', '#fff');
            $('#MM_SCR_SCR_MODULES').css('background-color', '#fff');
        }
    }
    var dir_edit_btn = localStorage.getItem("directEdit");
    if (dir_edit_btn == 'Edit') {
        setTimeout(function () {
            $('.Look_up_search').each(function (index) {
                var look_up_id = $(this).attr('id');
                var look_id_split = look_up_id.split('QSTN_LKP');
                var txt_box_id = 'QSTN' + look_id_split[1];
                $('#' + txt_box_id).css('background-color', '#fff');
            });
        }, 500);
    }
    $('ul.chckqty li p.clearfix span.c1 label.middle span.lbl').each(function () {
        var check = $(this).text();
        if (check == 1 && check.length == 1) {
            $(this).css('color', '#fff');
        }
    });
    var rel_tab_count = $('.qstn_r_contaier').length;
    $('.qstn_r_contaier').each(function (index) {
        if (rel_tab_count - 1 == index) {
            $(this).css('padding-bottom', '10px');
        }
    });
    var tab_change_val = localStorage.getItem("tab_change");
    if (tab_change_val == "1") {
        $('.row.tabsmenu2.tabdyn ul.inlinelist li').removeAttr('class');
        $('.row.tabsmenu2.tabdyn ul.inlinelist li:first-child').attr('class', 'active');
        localStorage.setItem("tab_change", "0");
    }
    var mod_conf_txt = localStorage.getItem("mod_cof_id");
    $('.modConf_txt_to_top').text(mod_conf_txt);
    var loc_mod_txt = localStorage.getItem("module_main_txt");
    $('.notification_txt').each(function () {
        var a = $(this).text();
        if (a == "") {
            $(this).parent().css('display', 'none');
        } else { }
    });
    var get_module_txt_to_bind = localStorage.getItem("module_main_txt");
	if (get_module_txt_to_bind != null) {
		if (get_module_txt_to_bind.includes("_") == false) {
			$('.mopduleheader span.main_ban_mod').text(get_module_txt_to_bind);
		}
	}
    var first_list_tab_text = $('ul#carttabs_head > li:first-child a span').text().trim();
    var secondNew_list_tab_text = $('ul#carttabs_head > li:nth-child(2) a span').text().trim();
    var third_list_tab_text = $('ul#carttabs_head > li:nth-child(3) a span').text().trim();
	var app_name = $('#ModuleName').text();
    if (app_name == "Price Models"){
        $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Currency.svg');
    }
    if (first_list_tab_text == 'Materials') {
        $('.mopduleheader i').attr('class', 'fa fa-cubes');
        $('.mopduleheader').css('color', '#81a738');
        $('.mopduleheader img').removeAttr('src');
        $('.mopduleheader i').attr('class', 'fa fa-cubes');
        var active_tab = $('ul#carttabs_head li.active a span').text().trim();
        var hidden_active_tab = $('div#attributesContainer .tabbable.show-large.tabsmenu ul#carttabs_head li.dropdown.pull-right.tabdrop.active ul.dropdown-menu li.active').text().trim();
        if (hidden_active_tab) {
            active_tab = hidden_active_tab;
        }
        if (active_tab == 'Materials' || active_tab == 'Material') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/materials.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Sales Orgs' || active_tab == 'Sales Org') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/salesorg.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Countries' || active_tab == 'Country') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/country.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Plants' || active_tab == 'Plant') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/plants.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Personalizations' || active_tab == 'Personalization') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/personalization.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Attributes' || active_tab == 'Attribute') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/attributes.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
            var btn_count = $('.btnconfig').length;
            if (btn_count == 2) {
                localStorage.setItem('attribute_tab_button', '1');
            } else {
                localStorage.setItem('attribute_tab_button', '0');
            }
        } else if (active_tab == 'Sets' || active_tab == 'Set') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sets.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
            $('#Attributesets_tab').css('display', 'block');
        } else if (active_tab == 'Categories' || active_tab == 'Category') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catagories.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Price Classes' || active_tab == 'Price Class') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/price_class.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Emblem Findings' || active_tab == 'Emblem Finding') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/emblem_finding.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Languages' || active_tab == 'Language') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/language.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Inc Country Templates' || active_tab == 'Inc Country Template') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/inc_country_template.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Config Classes' || active_tab == 'Config Class') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/config_classes.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Award Codes' || active_tab == 'Award Code') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/award_code.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Material Types' || active_tab == 'Material Type') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/material_types.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        } else if (active_tab == 'Box Families' || active_tab == 'Box Family') {
            $('.product_tab_icon img').attr('display', 'block');
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/box_family.svg');
            $('.product_tab_icon i').attr('class', '');
            $('.product_tab_icon i').removeAttr('style');
        }
    } else if (first_list_tab_text == 'Sales Orders' || first_list_tab_text == 'Sales Order') {
        $('.product_tab_icon i').removeAttr('class');
        $('li.mopduleheader').css('color', '#2f8a79');
        $('.mopduleheader img#ModuleIcons').css('display', 'inline-block');
        $('.mopduleheader img#ModuleIcons').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_mng_img_green.svg');
        $('.mopduleheader img#commission_black').css('display', 'none');
        $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
        $('.mopduleheader .main_ban_mod1').css('display', 'none');
        $('.mopduleheader .main_ban_mod').text('Order Management');
        $('.mopduleheader i').removeAttr('class');
        $('.product_tab_icon img').css('float', 'left');
        $('.product_tab_icon img').removeAttr('class');
        $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_mng_img_green.svg');
    } else if (first_list_tab_text == 'Configurable Materials' || first_list_tab_text == 'Configurable Material') {
        $('.product_tab_icon i').removeAttr('class');
        $('li.mopduleheader').css('color', 'rgb(79, 152, 205)');
        $('.mopduleheader img').css('display', 'none');
        $('.mopduleheader .main_ban_mod1').css('display', 'none');
        $('.mopduleheader .main_ban_mod').css('display', 'inline-block');
        $('.mopduleheader .main_ban_mod').text('Configurable Materials');
        $('li.mopduleheader i').attr('class', 'fa fa-pie-chart');
        $('.product_tab_icon img').css('float', 'left');
        $('.product_tab_icon img').removeAttr('class');
        $('li#ModName img#ModuleIcons').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/configuaration.svg');
        $('li#ModName img#ModuleIcons').css('display', 'block');
        $('li.mopduleheader i').css('display', 'none');
        if (active_tab == 'Configurable Materials' || active_tab == 'Configurable Material') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/configuaration.svg');
        } else if (active_tab == 'Sets' || active_tab == 'Set') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sets_config.svg');
        } else if (active_tab == 'Attributes' || active_tab == 'Attribute') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/attributes_config.svg');
        } else if (active_tab == 'Personalizations' || active_tab == 'Personalization') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/personalization_config.svg');
        } else if (active_tab == 'Categories' || active_tab == 'Category') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catagories_config.svg');
        } else if (active_tab == 'Materials' || active_tab == 'Material') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/materials_config.svg');
        } else { }
    } else if (first_list_tab_text == 'Price Models' || first_list_tab_text == 'Price Model') {
        $('.product_tab_icon i').removeAttr('class');
        $('li.mopduleheader').css('color', 'rgb(79, 152, 205)');
        $('.mopduleheader img#ModuleIcons').css('display', 'inline-block');
        $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
        $('.mopduleheader .main_ban_mod').css('display', 'none');
        $('.mopduleheader .main_ban_mod').text('Price Models');
        $('.mopduleheader i').removeAttr('class');
        $('.product_tab_icon img').css('float', 'left');
        $('.product_tab_icon img').removeAttr('class');
        if (active_tab == 'Price Models' || active_tab == 'Price Model') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/price_models.svg');
        } else if (active_tab == 'List Pricebook Sets' || active_tab == 'List Pricebook Set') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/List_price_set.svg');
        } else if (active_tab == 'List Pricebook Entries' || active_tab == 'List Pricebook Entry') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/List_price_entry.svg');
            locked = $("div#check_cont8033  input[type='checkbox']").prop("checked");
            if (locked != true) {
                $('.sec_attr_get #dyn8045 #ctr_drop').show();
                $('.sec_attr_get #dyn8072 #ctr_drop').show();
            } else {
                $('.sec_attr_get #dyn8045 #ctr_drop').hide();
                $('.sec_attr_get #dyn8072 #ctr_drop').hide();
            }
        } else if (active_tab == 'Price Classes' || active_tab == 'Price Class') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_class_blue.svg');
            $('div#pricl_treeGrid').closest('.Detail').css('display', 'block');
        } else if (active_tab == 'Price Methods' || active_tab == 'Price Method') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_method.svg');
        } else if (active_tab == 'Price Factors' || active_tab == 'Price Factor') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_factor.svg');
        } else if (active_tab == 'Price Model Classes' || active_tab == 'Price Model Class') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_model_classes.svg');
        } else if (active_tab == 'Currencies' || active_tab == 'Currency') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/currency.svg');
            $('.main_ban_mod').text('Price Models');
        } else if (active_tab == 'Metals' || active_tab == 'Metal') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/metals.svg');
        } else if (active_tab == 'Sales Orgs' || active_tab == 'Sales Org') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sales_org.svg');
        } else { }
        /*NUMERIC DATA RIGHT ALIGN 'BEGIN'*/
        $('td').filter(function () {
            return /^[-+]?[0-9]+\.[0-9]+$/.test($.text(this));
        }).css('text-align', 'right');
        $('td span').filter(function () {
            return /^[-+]?[0-9]+\.[0-9]+$/.test($.text(this));
        }).closest('td').css('text-align', 'right');
        $('td input:checkbox').closest('td').css('text-align', 'center');
        /*NUMERIC DATA RIGHT ALIGN 'END'*/
        $('input').each(function () {
            var inp = $(this).val();
            if (/^[-+]?[0-9]+\.[0-9]+$/.test(inp)) {
                $(this).attr('type', 'number');
            }
        });
    } else if (first_list_tab_text == 'Price Agreements' || secondNew_list_tab_text == 'Price Agreements' || third_list_tab_text == 'Price Agreements' || first_list_tab_text == 'Price Agreement' || secondNew_list_tab_text == 'Price Agreement' || third_list_tab_text == 'Price Agreement') {
        $('.product_tab_icon i').removeAttr('class');
        $('li.mopduleheader').css('color', 'rgb(194, 77, 126)');
        $('.mopduleheader img').css('display', 'none');
        $('.mopduleheader .main_ban_mod1').css('display', 'none');
        $('li#ModName #ModuleIcons1').css('display', 'none');
        $('.mopduleheader .main_ban_mod').css('display', 'inline-block');
        $('li#ModName img#ModuleIcons').css('display', 'inline-block');
        $('.mopduleheader .main_ban_mod').text('Price Agreements');
        $('li#ModName img#ModuleIcons').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments_main.svg');
        $('.product_tab_icon img').css('float', 'left');
        $('.product_tab_icon img').removeAttr('class');
        if (active_tab == 'Price Agreements' || active_tab == 'Price Agreement') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments.svg');
        } else if (active_tab == 'Programs' || active_tab == 'Program') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/programs.svg');
        } else if (active_tab == 'Program Types' || active_tab == 'Program Type') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/programs_types.svg');
        } else if (active_tab == 'Sales Orgs' || active_tab == 'Sales Org') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sales_org_red.svg');
        } else if (active_tab == 'Countries' || active_tab == 'Country') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/country_red.svg');
        } else if (active_tab == 'Promotions' || active_tab == 'Promotion') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/promotions.svg');
        } else if (active_tab == 'Accounts' || active_tab == 'Account') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Accounts.svg');
        } else if (active_tab == 'Contacts' || active_tab == 'Contact') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/contacts.svg');
        } else if (active_tab == 'Document Types' || active_tab == 'Document Type') {
            $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/seg_doctype.svg');
        } else { }
    } else if (first_list_tab_text == 'Configurations') {
        $('.mopduleheader i').attr('class', 'fa fa-cogs');
        $('.mopduleheader').css('color', '#050708');
        $('.product_tab_icon i').attr('display', 'block');
        $('.product_tab_icon i').attr('class', 'fa fa-cogs');
        $('.product_tab_icon').css('color', '#050708');
        $('.product_tab_icon img').attr('display', 'none');
        $('.product_tab_icon img').removeAttr('src');
    } else { }
    var current_tab_name = $('ul#carttabs_head li.active a span').text().trim();
    var current_tab_name_overflow = $('ul#carttabs_head li.dropdown.pull-right.tabdrop.active ul.dropdown-menu li.active').text().trim();
    if (current_tab_name_overflow == '') {
        localStorage.setItem("record_number", current_tab_name);
    } else {
        localStorage.setItem("record_number", current_tab_name_overflow);
    }
    if (current_tab_name == 'Material') {
        $('#PriceSummary_tab').css('display', 'block');
        $('#Personalization_tab').css('display', 'block');
        $('#Attributes_tab').css('display', 'block');
    } else {
        $('#PriceSummary_tab').css('display', 'none');
        $('#Personalization_tab').css('display', 'none');
        $('#Attributes_tab').css('display', 'none');
    }
    if (current_tab_name == 'Plant' || current_tab_name == 'Personalization') {
        $('#Attributeperpln_tab').css('display', 'block');
    } else {
        $('#Attributeperpln_tab').css('display', 'none');
    }
    var current_record_id = localStorage.getItem("record_number");
    var act_tab_name_txt = localStorage.getItem('active_tab_name_text');
    if (act_tab_name_txt) {
        current_record_id = act_tab_name_txt;
    }
    /* JIRA - ID : A043S001P01-6455 'Begin'*/
    // setTimeout(function () {
        var getCurrentTabName = $('ul#carttabs_head .active a span').text();
        var a = $('ul#carttabs_head .active ul .active a span').text();
        if (a) {
            getCurrentTabName = a;
        }
        //8389 strat
        if (getCurrentTabName == 'Profile') {
            $('#BTN_PROFILE_ADD_NEW').css("display", "none");
        }
        //8389 End
        $('.product_txt_main_tab').text(getCurrentTabName);
        $('.product_txt_main_tab').css('display', 'block');
		$('.product_txt').text(getCurrentTabName);
        // $('.product_txt_main_tab').text(getCurrentTabName);
    // }, 1500);
    /* JIRA - ID : A043S001P01-6455 'Begin'*/
    setTimeout(function () {
        $('ul#carttabs_head li.dropdown.pull-right.tabdrop ul.dropdown-menu li').each(function (index) {
            var c = $(this).css('display');
            if (c == 'none') {
                $(this).remove();
            }
            if (document.getElementById('processing_modal')) {
                $('#processing_modal').modal('hide');
            }
        });
        if ($('table#FULLTABLELOAD')) {
            var table_ful = $('table#FULLTABLELOAD').length;
            if (table_ful == 1) {
                var a = $('ul#carttabs_head .active a span').text();
                var active_dropdown_tab = $('.dropdown ul .active a span').text().trim();
				 if (a == 'Approval Chains' || a == 'Email Templates'){
					//$("thead.fullHeadFirst").css("top", "100px !important");
					$('.fullHeadFirst').addClass('approval-top100');
				//	document.getElementByClass("fullHeadFirst").style = "top:100px";
				}
                $('.product_txt_main_tab').css('display', 'block');
                if (active_dropdown_tab) {
                    $('.product_txt_div span').text(active_dropdown_tab);
                } else {
                    $('.product_txt_div span').text(a);
                }
            }
        }
    }, 5000);
    /* A043S001P01-7172 'End' */
    var record_number_add = localStorage.getItem("record_number_add_new");
    var current_record_id_new;
    if (record_number_add == '1') {
        current_record_id_new = "";
    } else {
        current_record_id_new = localStorage.getItem("record_id_number");
    }
    $('.product_txt_to_top abbr').text(current_record_id_new);
    $('.product_txt_to_top abbr').attr('title', current_record_id_new);
    var local_check_this_list_arr = localStorage.getItem("local_check_this_list");
    if (local_check_this_list_arr) {
        var local_check_split = local_check_this_list_arr.split(',');
        $(local_check_split).each(function (index) {
            var row_id = local_check_split[index];
            $('#' + row_id).addClass("selected_row_highlight");
        });
    }
    var relatedOkLocal_val = localStorage.getItem("relatedOkLocal");
    if (relatedOkLocal_val == "1") {
        $('.row.tabsmenu2.tabdyn ul.inlinelist li:nth-child(2) a').trigger('click');
        $('.row.tabsmenu2.tabdyn ul.inlinelist li').removeAttr('class');
        $('.row.tabsmenu2.tabdyn ul.inlinelist li:nth-child(2)').attr('class', 'active');
        localStorage.setItem('relatedOkLocal', "0");
    }
    setTimeout(function () {
        $('.Look_up_search').each(function (index) {
            var a = $(this).css('display');
            if (a == 'inline-block') {
                var b = $(this).attr('id');
                if (b) {
                    var c = b.split('QSTN_LKP');
                    var d = 'QSTN' + c[1];
                    $('#' + d).addClass('lookupBg');
                }
            }
        });
        $('table#QSTN_SYSEFL_MA_00427_TABLE tbody tr td > input[type="Checkbox"]').each(function (index) {
            $(this).attr('disabled', 'disabled');
        });
        var Related_popup_Edit_1 = localStorage.getItem('Related_popup_Edit');
        var current_active_sub_tab_1 = localStorage.getItem('current_active_sub_tab');
        if (Related_popup_Edit_1 == '1' && current_active_sub_tab_1 == 'Related') {
            localStorage.setItem('Related_popup_Edit', '0');
            var before_click_on_edit = $('.row.tabsmenu2.tabdyn ul.inlinelist li.active a').text().trim();
            var active_before_click_on_edit = $('.row.tabsmenu2.tabdyn ul.inlinelist li.active a').attr('class');
            localStorage.setItem('before_click_on_edit_lstg', before_click_on_edit);
            var fff_test = localStorage.getItem('before_click_on_edit_lstg');
            localStorage.setItem('active_before_click_on_edit_lstg', active_before_click_on_edit);
            var ddd_test = localStorage.getItem('active_before_click_on_edit_lstg');
            $('.' + active_before_click_on_edit).trigger('click');
        }
    }, 1500);
    var current_module = localStorage.getItem("module_main_txt");
    //A043S001P01-6657,A043S001P01-6388 start
    if ($('ul#carttabs_head li.active a span').text() == 'Price Class') {
        var currentModuleTab = 'Price Classes'
    } else {
        var currentModuleTab = localStorage.getItem("icon_edit_lock");
    }
    //A043S001P01-6657,A043S001P01-6388 end
    var curTab;
    if (localStorage.getItem("CHECKBOXVAL")) {
        if (localStorage.getItem("CHECKBOXVAL") == 'true') {
            $(localStorage.getItem("chkid")).prop('checked', true);
        } else {
            $(localStorage.getItem("chkid")).prop('checked', false);
        }
    }
    var current_obj_name = localStorage.getItem("record_id_number");
    var currentObjNamesplit;
    if (current_obj_name) {
        currentObjNamesplit = current_obj_name.split('-');
        curTab = currentObjNamesplit[0];
    }
    if (localStorage.getItem('datepickerErr') != null && localStorage.getItem('CheckboxErr') != null) {
        a = localStorage.getItem('datepickerErr');
        b = localStorage.getItem('CheckboxErr');
        if (a != "" || b != "") {
            $('#seglistID').attr('disabled', 'disabled');
            $('#seglistID').css({
                'background-color': 'lightgray',
                'color': 'gray'
            });
        } else {
            $('#seglistID').removeAttr('disabled');
            $('#seglistID').css({
                'background-color': '',
                'color': ''
            });
        }
    }
    $('abbr').each(function (index) {
        var a = $(this).text().trim();
        $(this).attr('title', a);
    });
    var delete_cont_val = localStorage.getItem('delete_cont_values');
    if (delete_cont_val == "1") {
        var before_click_on_edit = $('.row.tabsmenu2.tabdyn ul.inlinelist li.active a').text().trim();
        var active_before_click_on_edit = $('.row.tabsmenu2.tabdyn ul.inlinelist li.active a').attr('class');
        localStorage.setItem('before_click_on_edit_lstg', before_click_on_edit);
        var fff_test = localStorage.getItem('before_click_on_edit_lstg');
        localStorage.setItem('active_before_click_on_edit_lstg', active_before_click_on_edit);
        var ddd_test = localStorage.getItem('active_before_click_on_edit_lstg');
        $('.' + active_before_click_on_edit).trigger('click');
    }
    var mar_pad_local = localStorage.getItem("cur_id_pad_mar");
    if (mar_pad_local == "1") {
        setTimeout(function () {
            cur_pad_mar()
        }, 1500);
        localStorage.setItem("cur_id_pad_mar", "0");
    }
    /* NEW CODE FOR PAGE REFRESH START*/
    setTimeout(function () {
        var listContainer_len = $('.List_Container_header_txt').length;
        var masterManufac_len = $('.master_manufac').length;
        if (listContainer_len == 0 && masterManufac_len > 0) {
            $('.row.tabsmenu2.tabdyn').css('display', 'block');
        } else {
            $('.row.tabsmenu2.tabdyn').css('display', 'none');
        }
        var prlpbs = $('#prlpbs_treeGrid').length;
        if (prlpbs == 1) {
            $('.row.tabsmenu2.tabdyn').css('display', 'none');
        }
        var tst_2 = localStorage.getItem("pivot_local_save");
        if (tst_2 == "1") {
            localStorage.setItem("pivot_local_save", "0");
            var tst_3 = localStorage.getItem("pivot_local_save");
        }
    }, 500);
    setTimeout(function () {
        var get_first_li_text = "";
        var get_tab_value = $('#carttabs_head > li[id^=tab_]:first-child a span').text().trim();
        if (get_tab_value == "") {
            get_tab_value = $('#carttabs_head > li[id^=tab_]:nth-child(2) a span').text().trim();
        }
        get_first_li_text = get_tab_value;
        var loc_strg_get_first_li_text = localStorage.getItem('first_li_txt');
        var get_key_value = $('.iconhvr .col-md-3.pad-0 input').val();
        var concat_last_letter = loc_strg_get_first_li_text + 's';
        var active_tab = $('ul#carttabs_head li.active a span').text().trim();
        var hidden_active_tab = $('div#attributesContainer .tabbable.show-large.tabsmenu ul#carttabs_head li.dropdown.pull-right.tabdrop.active ul.dropdown-menu li.active').text().trim();
        if (hidden_active_tab) {
            active_tab = hidden_active_tab;
        }
        var before_click_on_edit_lstg_get = localStorage.getItem('before_click_on_edit_lstg');
        var active_before_click_on_edit_lstg_get = localStorage.getItem('active_before_click_on_edit_lstg');
        if ((loc_strg_get_first_li_text == get_first_li_text) || (concat_last_letter == get_first_li_text)) {
            var attr_sunTab = localStorage.getItem('Attribute_sub_tab');
            if (attr_sunTab == '1' && (active_tab == 'Plant' || active_tab == 'Personalization')) {
                $('.createtab45').trigger('click');
            } else {
                //$('.createclose').trigger('click');
            }
            if (get_first_li_text == 'Material' || get_first_li_text == 'Materials') {
                var currentTabName = $('div#attributesContainer .row.tabsfiled .tabsmenu ul#carttabs_head li.active').text().trim();
                $('.main_ban_mod').text(currentTabName);
                $('.product_tab_icon i').removeAttr('class');
                $('.product_tab_icon i').removeAttr('style');
                $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/materials.svg');
                $('.mopduleheader span.main_ban_mod').text('Materials');
                $('.mopduleheader i').attr('class', 'fa fa-cubes');
                $('.mopduleheader').css('color', '#81a738');
                $('.mopduleheader img').removeAttr('src');
                $('.mopduleheader i').attr('class', 'fa fa-cubes');
                if (before_click_on_edit_lstg_get && active_before_click_on_edit_lstg_get) {
                    $('.' + active_before_click_on_edit_lstg_get).trigger('click');
                }
                /* NEW CODE FOR BANNER IMAGE 'BEGIN'*/
                if (active_tab == 'Materials' || active_tab == 'Material') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/materials.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Sales Orgs' || active_tab == 'Sales Org') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/salesorg.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Countries' || active_tab == 'Country') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/country.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Plants' || active_tab == 'Plant') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/plants.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Personalizations' || active_tab == 'Personalization') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/personalization.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Attributes' || active_tab == 'Attribute') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/attributes.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                    var btn_count = $('.btnconfig').length;
                    if (btn_count == 2) {
                        localStorage.setItem('attribute_tab_button', '1');
                    } else {
                        localStorage.setItem('attribute_tab_button', '0');
                    }
                } else if (active_tab == 'Sets' || active_tab == 'Set') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sets.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                    $('#Attributesets_tab').css('display', 'block');
                    var c = $('.row.tabsmenu2.tabdyn ul.inlinelist li.active').text().trim();
                    if (c == 'Details') {
                        $('.pagination_seg_other').css('cssText', 'display:none !important;height: 29px;font-size: 13px;border-width: 0px 0px 1px !important;');
                        $('.pagination_seg').css('cssText', 'display:none !important;height: 29px;font-size: 13px;border-width: 0px 0px 1px !important;');
                    } else {
                        $('.pagination_seg_other').css('cssText', 'display:block !important;height: 29px;font-size: 13px;border-width: 0px 0px 1px !important;');
                        $('.pagination_seg').css('cssText', 'display:block !important;height: 29px;font-size: 13px;border-width: 0px 0px 1px !important;');
                    }
                } else if (active_tab == 'Categories' || active_tab == 'Category') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catagories.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Price Classes' || active_tab == 'Price Class') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/price_class.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Emblem Findings' || active_tab == 'Emblem Finding') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/emblem_finding.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Languages' || active_tab == 'Language') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/language.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Inc Country Templates' || active_tab == 'Inc Country Template') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/inc_country_template.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Config Classes' || active_tab == 'Config Class') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/config_classes.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Award Codes' || active_tab == 'Award Code') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/award_code.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Material Types' || active_tab == 'Material Type') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/material_types.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Box Families' || active_tab == 'Box Family') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/box_family.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else { }
                /*NEW CODE FOR BANNER IMAGE 'END'*/
            } else if (get_first_li_text == 'Price Models' || get_first_li_text == 'Price Model') {
                $('.product_tab_icon i').removeAttr('class');
                $('li.mopduleheader').css('color', 'rgb(79, 152, 205)');
                $('.mopduleheader img#ModuleIcons').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod').text('Price Models');
                $('.mopduleheader i').removeAttr('class');
                $('.product_tab_icon img').css('float', 'left');
                $('.product_tab_icon img').removeAttr('class');
                if (active_tab == 'Price Models' || active_tab == 'Price Model') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/price_models.svg');
                } else if (active_tab == 'List Pricebook Sets' || active_tab == 'List Pricebook Set') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/List_price_set.svg');
                } else if (active_tab == 'List Pricebook Entries' || active_tab == 'List Pricebook Entry') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/List_price_entry.svg');
                } else if (active_tab == 'Price Classes' || active_tab == 'Price Class') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_class_blue.svg');
                    $('div#pricl_treeGrid').closest('.Detail').css('display', 'block');
                } else if (active_tab == 'Price Methods' || active_tab == 'Price Method') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_method.svg');
                } else if (active_tab == 'Price Factors' || active_tab == 'Price Factor') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_factor.svg');
                } else if (active_tab == 'Price Model Classes' || active_tab == 'Price Model Class') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_model_classes.svg');
                } else if (active_tab == 'Currencies' || active_tab == 'Currency') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/currency.svg');
                } else if (active_tab == 'Metals' || active_tab == 'Metal') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/metals.svg');
                } else if (active_tab == 'Sales Orgs' || active_tab == 'Sales Org') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sales_org.svg');
                } else { }
                if (before_click_on_edit_lstg_get && active_before_click_on_edit_lstg_get) {
                    $('.' + active_before_click_on_edit_lstg_get).trigger('click');
                }
            } else if (get_first_li_text == 'Quota Categories' || get_first_li_text == 'Quota Category') {
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('.main_ban_mod1').css('color', 'gray');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Quotas');
                if (active_tab == 'Accounts' || active_tab == 'Accounts') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_account.svg');
                } else if (active_tab == 'Business Units' || active_tab == 'Business Unit') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_bussiness.svg');
                } else if (active_tab == 'Participants' || active_tab == 'Participant') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_participants.svg');
                } else if (active_tab == 'Quota Categories' || active_tab == 'Quota Category') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_quotacatogory.svg');
                } else if (active_tab == 'Quota Subcategories' || active_tab == 'Quota Subcategory') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_quotasubcatogory.svg');
                } else if (active_tab == 'Program Types' || active_tab == 'Program Type') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_programtype.svg');
                } else if (active_tab == 'Programs' || active_tab == 'Program') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_program.svg');
                } else if (active_tab == 'Sales Areas' || active_tab == 'Sales Area') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_salesarea.svg');
                } else if (active_tab == 'Sales Territories' || active_tab == 'Sales Territory') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_saleterritories.svg');
                } else { }
            } else if (get_first_li_text == 'Quotes' || get_first_li_text == 'Quote') {
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('.main_ban_mod1').css('color', 'gray');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Contract Quotes');
				$('#commission_black').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/contract_quotes.svg');
                if (active_tab == 'Quotes' || active_tab == 'Quote') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/contract_quotesfull.svg');
                }
                if (active_tab == 'Contracts' || active_tab == 'Contract') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Contract_top-img.svg');
                }else { }
            }else if (get_first_li_text == 'Catalogs' || get_first_li_text == 'Catalog' || secondNew_list_tab_text == 'Catalogs' || secondNew_list_tab_text == 'Catalog' || third_list_tab_text == 'Catalogs' || third_list_tab_text == 'Catalog') {
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('#commission_black').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catalog_pub.svg');
                $('.main_ban_mod1').css('color', '#f38b42');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Catalogs');
                if (active_tab == 'Catalogs' || active_tab == 'Catalog') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catalog_pub_full.svg');
                } else if (active_tab == 'Categories' || active_tab == 'Category') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments_catalog.svg');
                } else if (active_tab == 'Catalog Users' || active_tab == 'Catalog User') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Accounts_catalog.svg');
                }
                else if (active_tab == 'Languages' || active_tab == 'Language') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/language.svg');
                }
                else { }
            } else if (get_first_li_text == 'Segment Catalog Revisions' || get_first_li_text == 'Segment Catalog Revision') {
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('#commission_black').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catalog_pub.svg');
                $('.main_ban_mod1').css('color', 'gray');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Catalog Publishing');
                if (active_tab == 'Segment Catalog Revisions' || active_tab == 'Segment Catalog Revision') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments_catrev.svg');
                } else if (active_tab == 'Price Agreements' || active_tab == 'Price Agreement') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments_catalog.svg');
                } else if (active_tab == 'Accounts' || active_tab == 'Account') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Accounts_catalog.svg');
                } else { }
            } else if (get_first_li_text == 'Services' || get_first_li_text == 'Service' || secondNew_list_tab_text == 'Services' || secondNew_list_tab_text == 'Service' || third_list_tab_text == 'Services' || third_list_tab_text == 'Service') {
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('#commission_black').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/serviceicon.svg');
                $('.main_ban_mod1').css('color', '#77220D');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Services');
                if (active_tab == 'Service' || active_tab == 'Services') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/serviceapp.svg');
                } else if (active_tab == 'Program Types' || active_tab == 'Program Type') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/service_programs_types.svg');
                } else if (active_tab == 'Award Levels' || active_tab == 'Award Level') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Service_award_level.svg');
                } else if (active_tab == 'Programs' || active_tab == 'Program') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Service_programs.svg');
                } else if (active_tab == 'Award Groups' || active_tab == 'Award Group') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Service_award_group.svg');
                } else { }
            } else if (get_first_li_text == 'Sales Orders' || get_first_li_text == 'Sales Order') {
                $('.product_tab_icon i').removeAttr('class');
                $('li.mopduleheader').css('color', '#2f8a79');
                $('.mopduleheader img#ModuleIcons').css('display', 'inline-block');
                $('.mopduleheader img#ModuleIcons').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_mng_img_green.svg');
                $('.mopduleheader img#commission_black').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').css('display', 'none');
                $('.mopduleheader .main_ban_mod').text('Order Management');
                $('.mopduleheader i').removeAttr('class');
                $('.product_tab_icon img').css('float', 'left');
                $('.product_tab_icon img').removeAttr('class');
                $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_mng_img_green.svg');
                if (active_tab == 'Sales Orders' || active_tab == 'Sales Order') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_salesorder.svg');
                } else if (active_tab == 'Invoices' || active_tab == 'Invoice') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_invoice.svg');
                } else if (active_tab == 'Document Types' || active_tab == 'Document Type') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_doctype.svg');
                } else if (active_tab == 'Pricing Conditions' || active_tab == 'Pricing Condition') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_pricingcondition.svg');
                } else if (active_tab == 'Accounts' || active_tab == 'Account') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_account.svg');
                } else if (active_tab == 'Account Users' || active_tab == 'Account User') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_accountuser.svg');
                } else { }
            } else if (get_first_li_text == 'Configurable Materials' || get_first_li_text == 'Configurable Material') {
                $('.product_tab_icon i').removeAttr('class');
                $('li.mopduleheader').css('color', 'rgb(79, 152, 205)');
                $('.mopduleheader img').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'none');
                $('.mopduleheader .main_ban_mod').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod').text('Configurable Materials');
                $('li.mopduleheader i').attr('class', 'fa fa-pie-chart');
                $('.product_tab_icon img').css('float', 'left');
                $('.product_tab_icon img').removeAttr('class');
                $('li#ModName img#ModuleIcons').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/configuaration.svg');
                $('li#ModName img#ModuleIcons').css('display', 'block');
                $('li.mopduleheader i').css('display', 'none');
                if (active_tab == 'Configurable Materials' || active_tab == 'Configurable Material') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/configuaration.svg');
                } else if (active_tab == 'Sets' || active_tab == 'Set') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sets_config.svg');
                } else if (active_tab == 'Attributes' || active_tab == 'Attribute') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/attributes_config.svg');
                } else if (active_tab == 'Personalizations' || active_tab == 'Personalization') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/personalization_config.svg');
                } else if (active_tab == 'Categories' || active_tab == 'Category') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catagories_config.svg');
                } else if (active_tab == 'Materials' || active_tab == 'Material') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/materials_config.svg');
                    $('.product_tab_icon img').attr('display', 'block');
                } else { }
            }
            else if (get_first_li_text == 'Price Agreements' || get_first_li_text == 'Price Agreement' || secondNew_list_tab_text == 'Price Agreements' || secondNew_list_tab_text == 'Price Agreement' || third_list_tab_text == 'Price Agreements' || third_list_tab_text == 'Price Agreement') {
                $('.product_tab_icon i').removeAttr('class');
                $('li.mopduleheader').css('color', 'rgb(194, 77, 126)');
                $('.mopduleheader img').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'none');
                $('li#ModName #ModuleIcons1').css('display', 'none');
                $('.mopduleheader .main_ban_mod').css('display', 'inline-block');
                $('li#ModName img#ModuleIcons').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod').text('Price Agreements');
                $('li#ModName img#ModuleIcons').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments_main.svg');
                $('.product_tab_icon img').css('float', 'left');
                $('.product_tab_icon img').removeAttr('class');
                if (active_tab == 'Price Agreements' || active_tab == 'Price Agreement') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments.svg');
                } else if (active_tab == 'Programs' || active_tab == 'Program') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/programs.svg');
                } else if (active_tab == 'Program Types' || active_tab == 'Program Type') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/programs_types.svg');
                } else if (active_tab == 'Sales Orgs' || active_tab == 'Sales Org') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sales_org_red.svg');
                } else if (active_tab == 'Countries' || active_tab == 'Country') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/country_red.svg');
                } else if (active_tab == 'Promotions' || active_tab == 'Promotion') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/promotions.svg');
                } else if (active_tab == 'Accounts' || active_tab == 'Account') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Accounts.svg');
                } else if (active_tab == 'Contacts' || active_tab == 'Contact') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/contacts.svg');
                } else if (active_tab == 'Document Type' || active_tab == 'Document Types') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/seg_doctype.svg');
                } else { }
                if (before_click_on_edit_lstg_get && active_before_click_on_edit_lstg_get) {
                    $('.' + active_before_click_on_edit_lstg_get).trigger('click');
                }
            } else if (get_first_li_text == 'Apps' || get_first_li_text == 'App') {
                $('.product_tab_icon i').removeAttr('class');
                $('li.mopduleheader').css('color', '#17438e');
                $('.mopduleheader img').css('display', 'block');
                $('.mopduleheader .main_ban_mod1').css('display', 'none');
                $('.mopduleheader #ModuleIcons').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod').text('System Admin');
                $('li.mopduleheader i').removeAttr('class');
                $('.product_tab_icon img').css('float', 'left');
                $('.product_tab_icon img').removeAttr('class');
                $('.mopduleheader #ModuleIcons').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sys_admin.svg');
                if (active_tab == 'Apps' || active_tab == 'App') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/apps.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Tabs' || active_tab == 'Tab') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/tabs.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                }else if (active_tab == 'Pages' || active_tab == 'Page') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/PAGES.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Actions' || active_tab == 'Action') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/actions.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Sections' || active_tab == 'Section') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sections.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Questions' || active_tab == 'Question') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/questions.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Messages' || active_tab == 'Message') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/messages.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Objects' || active_tab == 'Object') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/objects.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Variables' || active_tab == 'Variable') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/variables.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Scripts' || active_tab == 'Script') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/scripts.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Profiles' || active_tab == 'Profile') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/profiles.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Error Logs' || active_tab == 'Error Log') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/errorlog.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Roles' || active_tab == 'Role') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/roles.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                }else if (active_tab == 'Section Fields' || active_tab == 'Section Field') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sections_fields.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                }
                else {
                    $('.mopduleheader #commission_black').css('display', 'none');
                }
            }else if (get_first_li_text == 'My Approval Queue' || get_first_li_text == 'My Approvals Queue'){
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('.main_ban_mod1').css('color', 'gray');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Approval Center');
                $('#commission_black').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Approval_Center.svg');
                if (active_tab == 'My Approval Queue' || active_tab == 'My Approvals Queue') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/ApproveCenter.svg');
                }else if (active_tab == 'Team Approval Queue' || active_tab == 'Team Approvals Queue') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/ApproveCenter.svg');
                }else if (active_tab == 'Approval Chains' || active_tab == 'Approval Chain') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/approvalchain.svg');
                }else if (active_tab == 'Email Templates' || active_tab == 'Email Template') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/emailtemplate.svg');
                }else { }
                
            } else { }
        } else {
            var attr_sunTab = localStorage.getItem('Attribute_sub_tab');
            if (attr_sunTab == '1' && (active_tab == 'Plant' || active_tab == 'Personalization')) {
                $('.createtab45').trigger('click');
            }
            if (get_first_li_text == 'Material' || get_first_li_text == 'Materials') {
                var currentTabName = $('div#attributesContainer .row.tabsfiled .tabsmenu ul#carttabs_head li.active').text().trim();
                $('.main_ban_mod').text(currentTabName);
                $('.product_tab_icon i').removeAttr('class');
                $('.product_tab_icon i').removeAttr('style');
                $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/materials.svg');
                $('.mopduleheader span.main_ban_mod').text('Materials');
                $('.mopduleheader i').attr('class', 'fa fa-cubes');
                $('.mopduleheader').css('color', '#81a738');
                $('.mopduleheader img').removeAttr('src');
                $('.mopduleheader i').attr('class', 'fa fa-cubes');
                if (before_click_on_edit_lstg_get && active_before_click_on_edit_lstg_get) {
                    $('.' + active_before_click_on_edit_lstg_get).trigger('click');
                }
                /* NEW CODE FOR BANNER IMAGE 'BEGIN'*/
                if (active_tab == 'Materials' || active_tab == 'Material') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/materials.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Sales Orgs' || active_tab == 'Sales Org') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/salesorg.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Countries' || active_tab == 'Country') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/country.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Plants' || active_tab == 'Plant') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/plants.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Personalizations' || active_tab == 'Personalization') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/personalization.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else if (active_tab == 'Attributes' || active_tab == 'Attribute') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/attributes.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                    var btn_count = $('.btnconfig').length;
                    if (btn_count == 2) {
                        localStorage.setItem('attribute_tab_button', '1');
                    } else {
                        localStorage.setItem('attribute_tab_button', '0');
                    }
                }  else if (active_tab == 'Box Families' || active_tab == 'Box Family') {
                    $('.product_tab_icon img').attr('display', 'block');
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/box_family.svg');
                    $('.product_tab_icon i').attr('class', '');
                    $('.product_tab_icon i').removeAttr('style');
                } else { }
                /*NEW CODE FOR BANNER IMAGE 'END'*/
            } else if (get_first_li_text == 'Price Models' || get_first_li_text == 'Price Model') {
                $('.product_tab_icon i').removeAttr('class');
                $('li.mopduleheader').css('color', 'rgb(79, 152, 205)');
                $('.mopduleheader img#ModuleIcons').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.main_ban_mod').text('Price Models');                
                $('.mopduleheader i').removeAttr('class');
                $('.product_tab_icon img').css('float', 'left');
                $('.product_tab_icon img').removeAttr('class');
                if (active_tab == 'Price Models' || active_tab == 'Price Model') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/price_models.svg');
                } else if (active_tab == 'List Pricebook Sets' || active_tab == 'List Pricebook Set') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/List_price_set.svg');
                } else if (active_tab == 'List Pricebook Entries' || active_tab == 'List Pricebook Entry') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/List_price_entry.svg');
                } else if (active_tab == 'Price Classes' || active_tab == 'Price Class') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_class_blue.svg');
                    $('div#pricl_treeGrid').closest('.Detail').css('display', 'block');
                } else if (active_tab == 'Price Methods' || active_tab == 'Price Method') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_method.svg');
                } else if (active_tab == 'Price Factors' || active_tab == 'Price Factor') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_factor.svg');
                } else if (active_tab == 'Price Model Classes' || active_tab == 'Price Model Class') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Price_model_classes.svg');
                } else if (active_tab == 'Currencies' || active_tab == 'Currency') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/currency.svg');
                } else if (active_tab == 'Metals' || active_tab == 'Metal') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/metals.svg');
                } else if (active_tab == 'Sales Orgs' || active_tab == 'Sales Org') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sales_org.svg');
                } else { }
                if (before_click_on_edit_lstg_get && active_before_click_on_edit_lstg_get) {
                    $('.' + active_before_click_on_edit_lstg_get).trigger('click');
                }
            }
            else if (get_first_li_text == 'Services' || get_first_li_text == 'Service' || secondNew_list_tab_text == 'Services' || secondNew_list_tab_text == 'Service' || third_list_tab_text == 'Services' || third_list_tab_text == 'Service') {
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('#commission_black').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/serviceicon.svg');
                $('.main_ban_mod1').css('color', '#77220D');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Services');
                if (active_tab == 'Service' || active_tab == 'Services') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/serviceapp.svg');
                } else if (active_tab == 'Program Types' || active_tab == 'Program Type') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/service_programs_types.svg');
                } else if (active_tab == 'Award Levels' || active_tab == 'Award Level') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Service_award_level.svg');
                } else if (active_tab == 'Programs' || active_tab == 'Program') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Service_programs.svg');
                } else if (active_tab == 'Award Groups' || active_tab == 'Award Group') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Service_award_group.svg');
                } else { }
            } else if (get_first_li_text == 'Sales Orders' || get_first_li_text == 'Sales Order') {
                $('.product_tab_icon i').removeAttr('class');
                $('li.mopduleheader').css('color', '#2f8a79');
                $('.mopduleheader img#ModuleIcons').css('display', 'inline-block');
                $('.mopduleheader img#ModuleIcons').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_mng_img_green.svg');
                $('.mopduleheader img#commission_black').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').css('display', 'none');
                $('.mopduleheader .main_ban_mod').text('Order Management');
                $('.mopduleheader i').removeAttr('class');
                $('.product_tab_icon img').css('float', 'left');
                $('.product_tab_icon img').removeAttr('class');
                $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_mng_img_green.svg');
                if (active_tab == 'Sales Orders' || active_tab == 'Sales Order') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_salesorder.svg');
                } else if (active_tab == 'Invoices' || active_tab == 'Invoice') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_invoice.svg');
                } else if (active_tab == 'Document Types' || active_tab == 'Document Type') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_doctype.svg');
                } else if (active_tab == 'Pricing Conditions' || active_tab == 'Pricing Condition') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_pricingcondition.svg');
                } else if (active_tab == 'Accounts' || active_tab == 'Account') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_account.svg');
                } else if (active_tab == 'Account Users' || active_tab == 'Account User') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_accountuser.svg');
                } else { }
            } else if (get_first_li_text == 'Configurable Materials' || get_first_li_text == 'Configurable Material') {
                $('.product_tab_icon i').removeAttr('class');
                $('li.mopduleheader').css('color', 'rgb(79, 152, 205)');
                $('.mopduleheader img').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'none');
                $('.mopduleheader .main_ban_mod').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod').text('Configurable Materials');
                $('li.mopduleheader i').attr('class', 'fa fa-pie-chart');
                $('.product_tab_icon img').css('float', 'left');
                $('.product_tab_icon img').removeAttr('class');
                $('li#ModName img#ModuleIcons').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/configuaration.svg');
                $('li#ModName img#ModuleIcons').css('display', 'block');
                $('li.mopduleheader i').css('display', 'none');
                if (active_tab == 'Configurable Materials' || active_tab == 'Configurable Material') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/configuaration.svg');
                } else if (active_tab == 'Sets' || active_tab == 'Set') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sets_config.svg');
                } else if (active_tab == 'Attributes' || active_tab == 'Attribute') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/attributes_config.svg');
                } else if (active_tab == 'Personalizations' || active_tab == 'Personalization') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/personalization_config.svg');
                } else if (active_tab == 'Categories' || active_tab == 'Category') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catagories_config.svg');
                } else if (active_tab == 'Materials' || active_tab == 'Material') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/materials_config.svg');
                } else { }
            } else if (get_first_li_text == 'Price Agreements' || get_first_li_text == 'Price Agreement') {
                $('.product_tab_icon i').removeAttr('class');
                $('li.mopduleheader').css('color', 'rgb(194, 77, 126)');
                $('.mopduleheader img').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'none');
                $('li#ModName #ModuleIcons1').css('display', 'none');
                $('.mopduleheader .main_ban_mod').css('display', 'inline-block');
                $('li#ModName img#ModuleIcons').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod').text('Price Agreements');
                $('li#ModName img#ModuleIcons').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments_main.svg');
                $('.product_tab_icon img').css('float', 'left');
                $('.product_tab_icon img').removeAttr('class');
                if (active_tab == 'Price Agreements' || active_tab == 'Price Agreement') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments.svg');
                } else if (active_tab == 'Programs' || active_tab == 'Program') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/programs.svg');
                } else if (active_tab == 'Program Types' || active_tab == 'Program Type') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/programs_types.svg');
                } else if (active_tab == 'Sales Orgs' || active_tab == 'Sales Org') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sales_org_red.svg');
                } else if (active_tab == 'Countries' || active_tab == 'Country') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/country_red.svg');
                } else if (active_tab == 'Promotions' || active_tab == 'Promotion') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/promotions.svg');
                } else if (active_tab == 'Accounts' || active_tab == 'Account') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Accounts.svg');
                } else if (active_tab == 'Contacts' || active_tab == 'Contact') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/contacts.svg');
                } else if (active_tab == 'Document Types' || active_tab == 'Document Types') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/seg_doctype.svg');
                } else { }
                if (before_click_on_edit_lstg_get && active_before_click_on_edit_lstg_get) {
                    $('.' + active_before_click_on_edit_lstg_get).trigger('click');
                }
            } else if (get_first_li_text == 'Quota Categories' || get_first_li_text == 'Quota Category') {
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('.main_ban_mod1').css('color', 'gray');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Quotas');
                if (active_tab == 'Accounts' || active_tab == 'Account') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_account.svg');
                } else if (active_tab == 'Business Units' || active_tab == 'Business Unit') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_bussiness.svg');
                } else if (active_tab == 'Participants' || active_tab == 'Participant') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_participants.svg');
                } else if (active_tab == 'Quota Categories' || active_tab == 'Quota Category') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_quotacatogory.svg');
                } else if (active_tab == 'Quota Subcategories' || active_tab == 'Quota Subcategory') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_quotasubcatogory.svg');
                } else if (active_tab == 'Program Types' || active_tab == 'Program Type') {
                    //console.log("active_tab_prg",active_tab);
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_programtype.svg');
                } else if (active_tab == 'Programs' || active_tab == 'Program') {
                    //console.log("active_tab_prg",active_tab);
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_program.svg');
                } else if (active_tab == 'Sales Areas' || active_tab == 'Sales Area') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_salesarea.svg');
                } else if (active_tab == 'Sales Territories' || active_tab == 'Sales Territory') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/comm_saleterritories.svg');
                } else { }
            }else if (get_first_li_text == 'Quotes' || get_first_li_text == 'Quote') {
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('.main_ban_mod1').css('color', 'gray');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Contract Quotes');
                $('#commission_black').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/contract_quotes.svg');
                if (active_tab == 'Quotes' || active_tab == 'Quote') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/contract_quotesfull.svg');
                }else if (active_tab == 'Contracts' || active_tab == 'Contract') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Contract_top-img.svg');
                }else { }
            }else if (get_first_li_text == 'My Approval Queue' || get_first_li_text == 'My Approvals Queue'){
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('.main_ban_mod1').css('color', 'gray');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Approval Center');
                $('#commission_black').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Approval_Center.svg');
                if (active_tab == 'My Approval Queue' || active_tab == 'My Approvals Queue') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/ApproveCenter.svg');
                }else if (active_tab == 'Team Approval Queue' || active_tab == 'Team Approvals Queue') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/ApproveCenter.svg');
                }else if (active_tab == 'Approval Chains' || active_tab == 'Approval Chain') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/approvalchain.svg');
                }else if (active_tab == 'Email Templates' || active_tab == 'Email Template') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/emailtemplate.svg');
                }else { }
                
            }
             else if (get_first_li_text == 'Catalogs' || get_first_li_text == 'Catalog' || secondNew_list_tab_text == 'Catalogs' || secondNew_list_tab_text == 'Catalog' || third_list_tab_text == 'Catalogs' || third_list_tab_text == 'Catalog') {
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('#commission_black').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catalog_pub.svg');
                $('.main_ban_mod1').css('color', '#f38b42');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Catalogs');
                if (active_tab == 'Catalogs' || active_tab == 'Catalog') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catalog_pub_full.svg');
                } else if (active_tab == 'Categories' || active_tab == 'Category') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments_catalog.svg');
                } else if (active_tab == 'Catalog Users' || active_tab == 'Catalog User') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Accounts_catalog.svg');
                }
                else if (active_tab == 'Languages' || active_tab == 'Language') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/language.svg');
                }
                else { }
            } else if (get_first_li_text == 'Segment Catalog Revisions' || get_first_li_text == 'Segment Catalog Revision') {
                $('#ModuleIcons').css('display', 'none');
                $('.mopduleheader i').removeAttr('class');
                $('#commission_black').css('display', 'inline-block');
                $('#commission_black').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catalog_pub.svg');
                $('.main_ban_mod1').css('color', 'gray');
                $('.mopduleheader .main_ban_mod').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod1').text('Catalog Publishing');
                if (active_tab == 'Segment Catalog Revision' || active_tab == 'Segment Catalog Revisions') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments_catrev.svg');
                } else if (active_tab == 'Price Agreements' || active_tab == 'Price Agreement') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments_catalog.svg');
                } else if (active_tab == 'Accounts' || active_tab == 'Account') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Accounts_catalog.svg');
                } else { }
            } else if (get_first_li_text == 'Apps' || get_first_li_text == 'App') {
                $('.product_tab_icon i').removeAttr('class');
                $('li.mopduleheader').css('color', '#17438e');
                $('.mopduleheader #ModuleIcons').css('display', 'block');
                $('.mopduleheader #commission_black').css('display', 'none');
                $('.mopduleheader .main_ban_mod1').css('display', 'none');
                $('.mopduleheader #ModuleIcons').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod').css('display', 'inline-block');
                $('.mopduleheader .main_ban_mod').text('System Admin');
                $('li.mopduleheader i').removeAttr('class');
                $('.product_tab_icon img').css('float', 'left');
                $('.product_tab_icon img').removeAttr('class');
                $('.mopduleheader #ModuleIcons').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sys_admin.svg');
                if (active_tab == 'Apps' || active_tab == 'App') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/apps.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Tabs' || active_tab == 'Tab') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/tabs.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                }else if (active_tab == 'Pages' || active_tab == 'Page') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/PAGES.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Actions' || active_tab == 'Action') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/actions.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Sections' || active_tab == 'Section') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sections.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Questions' || active_tab == 'Question') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/questions.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Messages' || active_tab == 'Message') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/messages.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Objects' || active_tab == 'Object') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/objects.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Variables' || active_tab == 'Variable') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/variables.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Scripts' || active_tab == 'Script') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/scripts.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Profiles' || active_tab == 'Profile') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/profiles.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Error Logs' || active_tab == 'Error Log') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/errorlog.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                } else if (active_tab == 'Roles' || active_tab == 'Role') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/roles.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                }else if (active_tab == 'Section Fields' || active_tab == 'Section Field') {
                    $('.product_tab_icon img').attr('src', '/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sections_fields.svg');
                    $('.mopduleheader #commission_black').css('display', 'none');
                }
                else {
                    $('.mopduleheader #commission_black').css('display', 'none');
                }
            } else {
                localStorage.setItem('first_li_txt', '');
            }
        }
        if (get_key_value) {
            var bannerContent_dont_update_get = localStorage.getItem('bannerContent_dont_update');
            if (bannerContent_dont_update_get == '0') {
                $('.product_txt_to_top abbr').text(get_key_value);
                $('.product_txt_to_top abbr').attr('title', get_key_value);
            } else { }
        }
    }, 500);
    $('ul#carttabs_head li').each(function (index) {
        var cart_li_id = $(this).attr('id');
        if (cart_li_id) {
            var cart_li_id_replace = cart_li_id.replace(' ', '_');
            $(this).attr('id', cart_li_id_replace);
        }
    });
    var Edit_in_material_value = localStorage.getItem("Edit_in_material");
    if (Edit_in_material_value == 1) {
        $('#QSTN_SYSEFL_MA_00427_TABLE tr:nth-child(1) td button span input').css('cssText', 'background-color: #FFF');
        $('#QSTN_SYSEFL_MA_00427_TABLE tr:nth-child(1) td button').css('cssText', 'pointer-events: all;background-color: #FFF');
    } else {
        $('#QSTN_SYSEFL_MA_00427_TABLE tr:nth-child(1) td button span input').css('cssText', 'background-color: #F1F1F1 !important;');
        $('#QSTN_SYSEFL_MA_00427_TABLE tr:nth-child(1) td button').css('cssText', 'pointer-events: none;background-color: #F1F1F1 !important;');
    }
    /* NEW CODE FOR PAGE REFRESH END*/
    var list_cont_length = $('.List_Container').length;
    if (list_cont_length == 1) {
        $('.Detail').css('display', 'block');
    }
    var acc_part = localStorage.getItem('account_parent');
    if (acc_part == '1') {
        localStorage.setItem('account_parent', '0');
    }
    var loading_related = localStorage.getItem('Related_Loading');
    if (loading_related == 1) {
        $('.Related').each(function (index) {
            $(this).css('display', 'block');
        });
    } else {
        $('.Related').each(function (index) {
            $(this).css('display', 'none');
        });
    }
    var hide_details_related_tab_value = localStorage.getItem('hide_details_related_tab');
    var hide_related_details_tab_closecreate = localStorage.getItem("hide_related_details_tab_closecreate");
    if (hide_details_related_tab_value == '1' || hide_related_details_tab_closecreate == '1') {
        $('.row.tabsmenu2.tabdyn').css('display', 'none');
        localStorage.setItem('hide_details_related_tab', '0');
        localStorage.setItem("hide_related_details_tab_closecreate", "0");
    }
    setTimeout(function () {
        var triggerRelated_value = localStorage.getItem('triggerRelated');
        if (triggerRelated_value == '1') {
            var before_click_on_edit = $('.row.tabsmenu2.tabdyn ul.inlinelist li.active a').text().trim();
            var active_before_click_on_edit = $('.row.tabsmenu2.tabdyn ul.inlinelist li.active a').attr('class');
            localStorage.setItem('before_click_on_edit_lstg', before_click_on_edit);
            var fff_test = localStorage.getItem('before_click_on_edit_lstg');
            localStorage.setItem('active_before_click_on_edit_lstg', active_before_click_on_edit);
            var ddd_test = localStorage.getItem('active_before_click_on_edit_lstg');
            $('.' + active_before_click_on_edit).trigger('click');
            localStorage.setItem('triggerRelated', '0');
        }
    }, 1000);
    module_name = $('span#ModuleName.main_ban_mod1').text()
    if ((module_name) && (module_name == "Quotas")) {
        localStorage.setItem('avoid_loading', '1');
    }
    var KeyValueToTable_txt = localStorage.getItem('KeyValueToTable');
    // //To show the subbanner
    // active_tab = $('ul#carttabs_head li.active a span').text().trim();
    // if (active_tab == 'Quote' || active_tab == 'Quotes'){
	//     //CommonRightView(0);
	//     Subbaner('Details',0, '', 'SAQTMT')
	// }
    //To show the subbanner
    var keyData_val = localStorage.getItem('keyData');
    if (keyData_val) { }
    else {
        keyData_val = $('.iconhvr .col-md-3.pad-0 input[id^=QSTN_]').val();
    }
	if (KeyValueToTable_txt == 'Quotes' && keyData_val =='undefined'){
        keyData_val = localStorage.getItem("masterquoteRecId")
    }
    if (KeyValueToTable_txt) {
        var bannerContentValueReset_txt = localStorage.getItem("bannerContentValueReset");
        var avoid_loading_val = localStorage.getItem('avoid_loading');
        if (avoid_loading_val == '1') {
            try {
                cpq.server.executeScript("SYCONUPDAL", {
                    'keyData_val': keyData_val,
                    'CurrentTab': $("ul#carttabs_head li.active a span").text()
                }, function (dataset) {
                    banner_data = dataset[0];
                    editicon_data = dataset[1];
                    cpqid_data = dataset[2];
                    required_data = dataset[3];
                    currency_data = dataset[4];
                    // RAMESH A043S001P01-8018 START 
                    sectionedit_data = dataset[5];
                    // RAMESH A043S001P01-8018 END 
                    if (banner_data) {
                        if (banner_data[0] && banner_data[1]) {
                            if (banner_data[0] && banner_data[1][0] && banner_data[1][1] && banner_data[1][2]) {
                                if (bannerContentValueReset_txt == '2') {
                                    localStorage.getItem("bannerContentValueReset", '0');
                                    $('.product_txt').text('');
                                    $('.part_number_header').text('');
                                    $('.sap_desc_header').text('');
                                    $('.product_txt_to_top abbr').text('');
                                    $('.product_txt_to_top abbr').attr('title', '');
                                    $('.part_number_content abbr').text('');
                                    $('.part_number_content abbr').attr('title', '');
                                    $('.sap_desc_content abbr').text('');
                                    $('.sap_desc_content abbr').attr('title', '');
                                    $('.segment_part_number_heading').text('');
                                    $('.segment_part_heading').text('');
                                    $('.segment_part_number_text abbr').text('');
                                    $('.segment_part_number_text abbr').attr('title', '');
                                    $('.segment_part_text abbr').text('');
                                    $('.segment_part_text abbr').attr('title', '');
                                    $('.order_mgmt_date_heading').text('');
                                    $('.order_mgmt_date_text abbr').attr('title', '');
                                    $('.order_mgmt_date_text').text('');
                                    $('.segment_revision_heading').text('');
                                    $('.segment_revision_text abbr').attr('title', '');
                                    $('.segment_revision_text').text('');
                                } 	                                  
								else{
									$('.order_mgmt_date').css('display', 'none');
									localStorage.setItem('KeyToCurrency', banner_data[1][0].Value);
									localStorage.setItem('keyData', banner_data[1][0].Value);
									//A043S001P01-8665 Start
									var headerValue_split = banner_data[0].split(',');
									// A043S001P01-8665 End
									$('.product_txt').text(headerValue_split[0]);
									$('.part_number_header').text(headerValue_split[1]);
									$('.sap_desc_header').text(headerValue_split[2]);
									$('.product_txt_to_top abbr').text(banner_data[1][0].Value);
									$('.product_txt_to_top abbr').attr('title', banner_data[1][0].Value);
									$('.product_txt_to_top').text(banner_data[1][0].Value);
									$('.part_number_content abbr').text(banner_data[1][1].Value);
									$('.part_number_content abbr').attr('title', banner_data[1][1].Value);
									$('.sap_desc_content abbr').text(banner_data[1][2].Value);
									$('.sap_desc_content abbr').attr('title', banner_data[1][2].Value);
									$('.segment_part_number_heading').text(headerValue_split[1]);
									$('.segment_part_heading').text(headerValue_split[2]);
									$('.segment_quote_heading').text(headerValue_split[3]);
									$('.segment_part_number_text abbr').text(banner_data[1][1].Value);
									$('.segment_part_number_text abbr').attr('title', banner_data[1][1].Value);
									$('.segment_part_text abbr').text(banner_data[1][2].Value);
                                    $('.segment_part_text abbr').attr('title', banner_data[1][2].Value);
                                    // if (getCurrentTabName == "Approval Chain"){
                                    // 	$('.product_txt').text(headerValue_split[0]);
									// 	$('.part_number_header').text(headerValue_split[1]);
									// 	$('.sap_desc_header').text(headerValue_split[2]);
									// 	$('.product_txt_to_top abbr').text(banner_data[1][0]);
									// 	$('.product_txt_to_top abbr').attr('title', banner_data[1][0]);
									// 	$('.product_txt_to_top').text(banner_data[1][0]);
									// 	$('.part_number_content abbr').text(banner_data[1][1]);
									// 	$('.part_number_content abbr').attr('title', banner_data[1][1]);
									// 	$('.sap_desc_content abbr').text(banner_data[1][2]);
									// 	$('.sap_desc_content abbr').attr('title', banner_data[1][2]);
									// 	$('.segment_part_number_heading').text(headerValue_split[1]);
									// 	$('.segment_part_heading').text(headerValue_split[2]);
									// 	$('.segment_quote_heading').text(headerValue_split[3]);
									// 	$('.segment_part_number_text abbr').text(banner_data[1][1]);
									// 	$('.segment_part_number_text abbr').attr('title', banner_data[1][1]);
									// 	$('.segment_part_text abbr').text(banner_data[1][2]);
									// 	$('.segment_part_text abbr').attr('title', banner_data[1][2]);                                    	
                                    // }
                                    //console.log(banner_data[1][2])
									if ((headerValue_split.length > 3) && (getCurrentTabName != "Contracts")) {
										$('.segment_quote_text abbr').text(banner_data[1][3].Value);
										$('.segment_quote_text abbr').attr('title', banner_data[1][3].Value);
                                    }
                                    // if ((headerValue_split.length > 3) && (getCurrentTabName == "Approval Chain")) {
									// 	$('.segment_quote_text abbr').text(banner_data[1][3]);
									// 	$('.segment_quote_text abbr').attr('title', banner_data[1][3]);
                                    // }
                                    if ((headerValue_split[4]) && (getCurrentTabName != "Contracts")){
                                    	$('.segment_revision_Acc').css('display', 'block');
                                    	$('.segment_revision_Acc_heading').text(headerValue_split[4]);
                                    	$('.segment_revision_Acc_text abbr').text(banner_data[1][4].Value);
                                        $('.segment_revision_Acc_text abbr').attr('title',banner_data[1][4].Value);                                                                             	
                                    }
                                    if ((headerValue_split[5]) && (getCurrentTabName != "Contracts")){
                                    	$('.segment_revision_Sale').css('display', 'block');
                                    	$('.segment_revision_Sale_heading').text(headerValue_split[5]);
                                    	$('.segment_revision_Sale_text abbr').text(banner_data[1][5].Value);
                                        $('.segment_revision_Sale_text abbr').attr('title',banner_data[1][5].Value);                                                                             	
                                    }
                                    // to show check box in PHP for Active column in approval chains tab -start
                                    if ((headerValue_split.length > 5) && (getCurrentTabName == "Approval Chain")){
                                    	var checkvalue = $('#check_cont3176 ul li label input'). prop("checked");
										if (checkvalue == true){
											var td = '<input type="CHECKBOX" value = "True" class="custom" checked disabled><span class="lbl"></span>'
										}
										else{
											var td = '<input type="CHECKBOX" value = "False" class="custom" disabled><span class="lbl"></span>'
										}
										//$('.segment_revision_id').removeClass("disp_none").addClass("disp_blk");
										$('.segment_revision_Sale_heading').text(headerValue_split[5]);
										$('.segment_revision_Sale_text').html(td);
                                    }
                                    // to show check box in PHP for Active column in approval chains tab -end
                                    if ((headerValue_split[3]) && (getCurrentTabName == "Contracts")){
										$('.segment_quote_heading').text(headerValue_split[3]);
										/* OM's Code Start Here */
										// $('.order_mgmt_date_text abbr').text(invoice_date);
										// $('.order_mgmt_date_text abbr').attr('title', invoice_date);
										timestmp = parseInt(banner_data[1][3].Value.match(/\d+/g)[0])
										var dateval = new Date(timestmp)
                                      	var dd = dateval.getDate();
										var mm = dateval.getMonth()+1; 
										var yyyy = dateval.getFullYear();
										formated_date_to_show = mm + "/" + dd + "/" + yyyy;
										$('.segment_quote_text abbr').attr('title', formated_date_to_show);
										$('.segment_quote_text abbr').text(formated_date_to_show);
									}
									if (headerValue_split[7]) {
										$('.segment_revision_heading').text(headerValue_split[7]);
										/* OM's Code Start Here */
										// $('.order_mgmt_date_text abbr').text(invoice_date);
										// $('.order_mgmt_date_text abbr').attr('title', invoice_date);
										timestmp = parseInt(banner_data[1][7].Value.match(/\d+/g)[0])
										var dateval = new Date(timestmp)
                                        if (CurrentTab=="Quote" ){
                                            var dd = dateval.getDate().toString().padStart(2, "0");
                                            var month = dateval.getMonth()+1;
                                            var mm = month.toString().padStart(2, "0");
                                        }
                                        else {
                                      	var dd = dateval.getDate();
										var mm = dateval.getMonth()+1; 
                                        }
                                        var yyyy = dateval.getFullYear();
										formated_date_to_show = mm + "/" + dd + "/" + yyyy;
										$('.segment_revision_text abbr').attr('title', formated_date_to_show);
										$('.segment_revision_text abbr').text(formated_date_to_show);
                                    }
                                    if (currenttab == "Quote")
                                    {
                                        $('.product_txt_div').css('display','none');
                                    }
                                    //A055S000P01-3259 to restrict quote type & sale type labels in PHP while navigating from Source contract id hyperlink from quote information node -start 
                                    if (getCurrentTabName == "Contracts"){
										$(".segment_revision_Acc").css("display","none");
										$(".segment_revision_Sale").css("display","none");
									}
                                    //A055S000P01-3259 to restrict quote type & sale type labels in PHP while navigating from Source contract id hyperlink from quote information node -end
                                    if (currenttab == "Contracts"){
                                        if (headerValue_split[4]) {
                                            $('.segment_revision_heading').text(headerValue_split[4]);
                                            /* OM's Code Start Here */
                                            // $('.order_mgmt_date_text abbr').text(invoice_date);
                                            // $('.order_mgmt_date_text abbr').attr('title', invoice_date);
                                            timestmp = parseInt(banner_data[1][4].Value.match(/\d+/g)[0])
                                            var dateval = new Date(timestmp)
                                            var dd = dateval.getDate();
                                            var mm = dateval.getMonth()+1; 
                                            var yyyy = dateval.getFullYear();
                                            formated_date_to_show = mm + "/" + dd + "/" + yyyy;
                                            $('.segment_revision_text abbr').attr('title', formated_date_to_show);
                                            $('.segment_revision_text abbr').text(formated_date_to_show);
                                        }
                                    }
                                    if ((headerValue_split.length > 4) && (getCurrentTabName == "Quote")) {
                                        var cur = $('ul#carttabs_head .active').text().trim();
                                        var invoice_date = '';
                                        if (cur == 'Invoice') {
                                            var date_time = $('div#mat9864 input.form-control').val();
                                            var date_remove_time = '';
                                            if (date_time) {
                                                date_remove_time = date_time.split(' ');
                                                date_remove_time = date_remove_time[0];
                                            }
                                            invoice_date = date_remove_time;
                                            //invoice_date = $('div#datePick6547 .col-md-3.pad-0 .input-group.date-field input.form-control').val();
                                        } else if (cur == 'Sales Order') {
                                            var date_time = $('div#mat9841 input.form-control').val();
                                            var date_remove_time = '';
                                            if (date_time) {
                                                date_remove_time = date_time.split(' ');
                                                date_remove_time = date_remove_time[0];
                                            }
                                            invoice_date = date_remove_time;
                                            //invoice_date = $('div#datePick6516 .col-md-3.pad-0 .input-group.date-field input.form-control').val();
                                        } else {
                                            try{
                                                invoice_date = banner_data[1][6].Value
                                            }catch(e){
                                                invoice_date = '';
                                            }
                                        }
                                        getCurrentTabName = $('ul#carttabs_head .active a span').text();
                                        if ((invoice_date == null || invoice_date == '') && (getCurrentTabName == 'Account')) {
                                            invoice_date = 'NONE'
                                        }
                                        $('.order_mgmt_date').css('display', 'block');
                                        $('.order_mgmt_date_heading').text(headerValue_split[6]);
                                        /* OM's Code Start Here */
                                        // $('.order_mgmt_date_text abbr').text(invoice_date);
                                        // $('.order_mgmt_date_text abbr').attr('title', invoice_date);
                                        if (invoice_date != "" && invoice_date != 'NONE')
                                        {
                                            timestmp = parseInt(invoice_date.match(/\d+/g)[0])
                                        }
                                        
                                        var dateval = new Date(timestmp)
                                        if (CurrentTab=="Quote" ){
                                            var dd = dateval.getDate().toString().padStart(2, "0");
                                            var month = dateval.getMonth()+1;
                                            var mm = month.toString().padStart(2, "0");
                                        }
                                        else {
                                      	var dd = dateval.getDate();
										var mm = dateval.getMonth()+1; 
                                        }
                                        var yyyy = dateval.getFullYear();
                                        formated_date_to_show = mm + "/" + dd + "/" + yyyy;
                                        $('.order_mgmt_date_text abbr').text(formated_date_to_show);
                                        $('.order_mgmt_date_text abbr').attr('title',formated_date_to_show);
                                        /* Om's Code Ends Here */
                                    }
								}
                                
                            }
                        }// A043S001P01-13633 Start
                        else {
                            localStorage.setItem("Banner_Hiding_Var", '0');
                            $('.product_txt').text(currenttab);
                            $('.part_number_header').text('');
                            $('.sap_desc_header').text('');
                            $('.product_txt_to_top abbr').text('');
                            $('.product_txt_to_top abbr').attr('title', '');
                            $('.part_number_content abbr').text('');
                            $('.part_number_content abbr').attr('title', '');
                            $('.sap_desc_content abbr').text('');
                            $('.sap_desc_content abbr').attr('title', '');
                            $('.segment_part_number_heading').text('');
                            $('.segment_part_heading').text('');
                            $('.segment_part_number_text abbr').text('');
                            $('.segment_part_number_text abbr').attr('title', '');
                            $('.segment_part_text abbr').text('');
                            $('.segment_part_text abbr').attr('title', '');
                            $('.order_mgmt_date_heading').text('');
                            $('.order_mgmt_date_text abbr').attr('title', '');
                            $('.order_mgmt_date_text').text('');
                            $('.segment_revision_heading').text('');
                            $('.segment_revision_text abbr').attr('title', '');
                            $('.segment_revision_text').text('');
                        }// A043S001P01-13633 End
                    }
                    if (currency_data) {
                        data = currency_data[0]
                        data1 = currency_data[1]
                        data2 = currency_data[2];
                        if (data) {
                            locked = $("div#check_cont8033  input[type='checkbox']").prop("checked");
                            if (locked != true) {
                                $('.sec_attr_get #dyn8045 #ctr_drop').show();
                                $('.sec_attr_get #dyn8072 #ctr_drop').show();
                            } else {
                                $('.sec_attr_get #dyn8045 #ctr_drop').hide();
                                $('.sec_attr_get #dyn8072 #ctr_drop').hide();
                            }
                            $(data).each(function (index) {
                                var count = 0;
                                var currency_list_value = data[index];
                                if (data1 != undefined){
                                var decimal_val = data1[index];
                                }
                                if (currency_list_value) {
                                    var currency_field_label_symbol = currency_list_value.split('|');
                                    $('.iconhvr label.col-md-2').each(function (indexval) {
                                        var lbl_txt = $(this).text().trim();
                                        if (lbl_txt == currency_field_label_symbol[0]) {
                                            var inp_val_to_concat = $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val();

                                            if (inp_val_to_concat == "") {
                                                inp_val_to_concat = 0
                                                var concat_val = parseFloat(inp_val_to_concat).toFixed(decimal_val)
                                                var concat_symbol_value = currency_field_label_symbol[1] + '' + concat_val;
                                                $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val(concat_symbol_value);
                                            }

                                            else if ((/^[a-zA-Z0-9-. ]*$/).test(inp_val_to_concat) == false) {
                                                // if (lbl_txt == 'Merchandise / Other Material Cost in Sales Org Currency' || lbl_txt == 'Merchandise / Other Material Cost in Material Currency') {
                                                //     count = count + 1;
                                                //     if (count > 1) {
                                                //         $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').attr('type', 'text');
                                                //         inp_val_to_concat_spilt = inp_val_to_concat.split('');
                                                //         inp_val_to_concat_spilt_len = inp_val_to_concat_spilt.length
                                                //         if (inp_val_to_concat_spilt[inp_val_to_concat_spilt_len - 1] != '') {
                                                //             var concat_val = Number(inp_val_to_concat_spilt[inp_val_to_concat_spilt_len - 1]).toFixed(decimal_val)
                                                //             var concat_symbol_value = currency_field_label_symbol[1] + '' + concat_val;
                                                //             $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val(concat_symbol_value);
                                                //         }
                                                //     }

                                                // }

                                                // else {
                                                // inp_val_to_concat = inp_val_to_concat.substring(1);
                                                $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').attr('type', 'text');
                                                if (inp_val_to_concat != '') {
                                                    if ($.isNumeric(parseInt(inp_val_to_concat)) == false) {
                                                        inp_val_to_concat = inp_val_to_concat.replace(/[^0-9\.]/ig, "");
                                                    }
                                                    var concat_val = parseFloat(inp_val_to_concat).toFixed(decimal_val)
                                                    var concat_symbol_value = currency_field_label_symbol[1] + '' + concat_val;
                                                    $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val(concat_symbol_value);
                                                }
                                                //}

                                            }
                                            else {
                                                var cu_val = $('#QSTN_SYSEFL_PB_01496').val();
                                                var inr_curr;
                                                if (cu_val) {
                                                    inr_curr = cu_val.trim();
                                                }
                                                if (lbl_txt == 'Merch/Oth Mtrl Cost in SO Curr' || lbl_txt == 'Merchandise / Other Material Cost in Sales Org Currency') {
                                                    count = count + 1;
                                                    if (count > 1 && inr_curr != '') {
                                                        $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').attr('type', 'text');
                                                        inp_val_to_concat_spilt = inp_val_to_concat.split('');
                                                        if (inp_val_to_concat != '') {
                                                            if ($.isNumeric(parseInt(inp_val_to_concat)) == false) {
                                                                inp_val_to_concat = inp_val_to_concat.replace(/[^0-9\.]/ig, "");
                                                            }
                                                            var concat_val = parseFloat(inp_val_to_concat).toFixed(decimal_val)
                                                            var concat_symbol_value = currency_field_label_symbol[1] + '' + concat_val;
                                                            $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val(concat_symbol_value);
                                                        }
                                                    } else if (count == 1) {
                                                        $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').attr('type', 'text');
                                                        if (inp_val_to_concat != '') {
                                                            if ($.isNumeric(parseInt(inp_val_to_concat)) == false) {
                                                                inp_val_to_concat = inp_val_to_concat.replace(/[^0-9\.]/ig, "");
                                                            }
                                                            var concat_val = parseFloat(inp_val_to_concat).toFixed(decimal_val)
                                                            var concat_symbol_value = currency_field_label_symbol[1] + '' + concat_val;
                                                            $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val(concat_symbol_value);
                                                        }
                                                    } else { }
                                                } else {
                                                    $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').attr('type', 'text');
                                                    if (inp_val_to_concat != '') {
                                                        if ($.isNumeric(parseInt(inp_val_to_concat)) == false) {
                                                            inp_val_to_concat = inp_val_to_concat.replace(/[^0-9\.]/ig, "");
                                                        }
                                                        var concat_val = parseFloat(inp_val_to_concat).toFixed(decimal_val)
                                                        var concat_symbol_value = currency_field_label_symbol[1] + '' + concat_val;
                                                        $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val(concat_symbol_value);
                                                    }
                                                }
                                            }
                                        }
                                    });
                                }
                            });
                        }
                        if (data2) {
                            $(data2).each(function (index) {
                                var factor_str_with_symbol = data2[index];
                                if (factor_str_with_symbol) {
                                    var factor_values = factor_str_with_symbol.split('|');
                                    var fields = $('.iconhvr label.col-md-2');
                                    if (fields.length == 0) {
                                        fields = $('.iconhvr label.col-md-11');
                                    }
                                    fields.each(function (index_val) {
                                        var label_txt = $(this).text().trim();
                                        if (label_txt == factor_values[0]) {
                                            var factor_input_val = $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val();
                                            var isDisabled = $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').prop('disabled');
                                            var input_val = $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val();
                                            if (factor_input_val != '' && isDisabled == true && input_val[input_val.length - 1] != factor_values[1]) {
                                                $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').attr('type', 'text');
                                                var concat_factor_symbol_value = factor_input_val + '' + factor_values[1];
                                                $(this).closest('.iconhvr').children('.col-md-3.pad-0').children('input').val(concat_factor_symbol_value);
                                            }
                                        }
                                    });
                                }
                            })
                        }
                    }
					if (cpqid_data){
						if (cpqid_data[0] != "" && cpqid_data[1] != "" ) {
							key = cpqid_data[0];
							try {
								$('#' + key).val("");
								value = cpqid_data[1];
								if (key != '' && value != '') {
									$('input#' + key).val(value);
								}
								$('.product_txt_to_top_banner').text(value);                            
							} catch (err) {
								console.log(err);
							}
						}
					}
                    /*if (required_data) {
                        $(required_data).each(function (indexes) {
                            var list_value = required_data[indexes];
                            $('.iconhvr div label').each(function (index) {
                                var field_txt = $(this).text();
                                if (field_txt == list_value) {
                                    $(this).closest('.iconhvr').children('div').children('a').children('i').siblings('.req-field').remove();
                                    $(this).closest('.iconhvr').children('div').children('a').children('i').after('<span class="req-field" style="margin-left: 3px;float: left;">*</span>');
                                }
                            });
                        });
                    }*/
                    if (required_data) {
                        $(required_data).each(function (indexes) {
                            var list_value = required_data[indexes];
                            $('.iconhvr div label').each(function (index) {
                                var field_txt = $(this).text();
                                if (field_txt == list_value) {
                                    $(this).closest('.iconhvr').children('div').children('a').children('i').siblings('.req-field').remove();
                                    $(this).closest('.iconhvr').children('div').children('a').children('i').after('<span class="req-field mrg_lft_ft_lft" >*</span>');
                                }
                                getCurrentTabName = $('ul#carttabs_head .active a span').text();
                                btn_txt_val = localStorage.getItem('btn_txt_val')
                                // TO HIDE THE SECTION EDIT BUTTONS GLOBALLY WHEN THE SAVE AND CANCEL BUTTON PRESENTS
                                // A043S001P01-12219 STARTS
                                CANCEL_DISPLAY = $('button[name="CANCEL"]').css('display')
                                SAVE_DISPLAY = $('button[name="SAVE"]').css('display')
                                if ((CANCEL_DISPLAY == 'block') && (SAVE_DISPLAY == 'block')) {
                                	if (btn_txt_val == "SAVE"){
                                	    $(".emp_notifiy").css('display','block');
                                        document.querySelectorAll('div#ctr_drop').forEach(el => el.style.display = 'none');
                                	}
                                    if (btn_txt_val == 'ADD NEW' || btn_txt_val == 'REFRESH') {
                                        document.querySelectorAll('div#ctr_drop').forEach(el => el.style.display = 'none');
                                        //Added to show information message for Approval Chain Id field in Approval chains tab add new mode - start
                                        if (CurrentTab == "Approval Chain"){
                                            req = $('input#QSTN_SYSEFL_AC_00002').val();
                                            if(req.length>=0){
                                                //console.log('wwwwwwwwwwww')
                                                $('span#QSTN_SYSEFL_AC_00002').text('* This field should be 8 Characters - alphanumeric only');
                                                $('span#QSTN_SYSEFL_AC_00002').closest('div').show();
                                                $("span#QSTN_SYSEFL_AC_00002").attr({'title' : '* This field should be 8 Characters - alphanumeric only'});
                                                $('span#QSTN_SYSEFL_AC_00002').parent().next().addClass('cust_QSTN_SYSEFL_AC_00002_next');
                                                $('span#QSTN_SYSEFL_AC_00002').parent().addClass('cust_QSTN_SYSEFL_AC_00002');                                                
                                            }
                                        }
                                        //Added to show information message for Approval Chain Id field in Approval chains tab add new mode - end
                                    }
                                }
                                else{
                                	$(".emp_notifiy").css('display','none');
                                }
                                if (getCurrentTabName == 'Participant') {
                                    if (required_data.indexOf('Company Code') == -1 || required_data.indexOf('Payroll File Number') == -1) {
                                        $('#QSTN_SYSEFL_CM_00119').parent().prev().children().next().children().next().remove();
                                        $('#QSTN_SYSEFL_CM_02831').parent().prev().children().next().children().next().remove();
                                    }
                                    btn_txt_val = localStorage.getItem('btn_txt_val')
                                    if (btn_txt_val == 'ADD NEW') {
                                        document.querySelectorAll('div#ctr_drop').forEach(el => el.style.display = 'none');
                                        setTimeout(function () {
                                            document.querySelectorAll('div#ctr_drop').forEach(el => el.style.display = 'none');
                                        }, 3500);
                                    }
                                    PARTICIPANT_SAVE_BTN = $('#BTN_SYACTI_CM_00050_SAVE').css('display')
                                    PARTICIPANT_CANCEL_BTN = $('#BTN_SYACTI_CM_00049_BACKTOLIST').css('display')
                                    if (PARTICIPANT_SAVE_BTN == 'block' && PARTICIPANT_CANCEL_BTN == 'block') {
                                        document.querySelectorAll('div#ctr_drop').forEach(el => el.style.display = 'none');
                                        setTimeout(function () {
                                            document.querySelectorAll('div#ctr_drop').forEach(el => el.style.display = 'none');
                                        }, 4500);
                                    }
                                    var today = new Date();
                                    var dd = String(today.getDate()).padStart(2, '0');
                                    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
                                    var yyyy = today.getFullYear();
                                    today = mm + '/' + dd + '/' + yyyy;
                                    var date1 = new Date(today);
                                    get_comm_date = localStorage.getItem('commdate');
                                    dt_com = $('#Comm_End_Date_value').val()
                                    var date2 = new Date(dt_com);
                                    var diffTime = date2 - date1;
                                    var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                                    if ((get_comm_date) && (dt_com) && (diffDays >= 0)) {
                                        chckbx_clck()
                                        localStorage.setItem('commdate', '');
                                    }
                                }
                            });
                        });
                        getCurrentTabName = $('ul#carttabs_head .active a span').text();
                        if (getCurrentTabName == 'Participant') {
                            END_DATE_REQUIRED = localStorage.getItem('END_DATE_REQ')
                            if (END_DATE_REQUIRED != '') {
                                setTimeout(function () {
                                    END_DATE_REQUIRED = localStorage.getItem('END_DATE_REQ')
                                    if (END_DATE_REQUIRED == 'FALSE' && END_DATE_REQUIRED != null && END_DATE_REQUIRED != undefined) {
                                        $('#datePick9670').find('.req-field').css('display', 'none');
                                        localStorage.setItem('END_DATE_REQ', '')
                                    }
                                    if (END_DATE_REQUIRED == 'TRUE' && END_DATE_REQUIRED != null && END_DATE_REQUIRED != undefined) {
                                        $('#datePick9670 div:nth-child(1) a.col-md-1').children('span').remove()
                                        $('#datePick9670 div:nth-child(1) a.col-md-1').append('<span class="req-field mrg_lft_ft_lft">*</span>')
                                        localStorage.setItem('END_DATE_REQ', '')
                                    }
                                }, 3000);
                            } else {
                                setTimeout(function () {
                                    END_DATE_REQUIRED = localStorage.getItem('END_DATE_REQ')
                                    if (END_DATE_REQUIRED == 'FALSE' && END_DATE_REQUIRED != null && END_DATE_REQUIRED != undefined) {
                                        $('#datePick9670').find('.req-field').css('display', 'none');
                                        localStorage.setItem('END_DATE_REQ', '')
                                    }
                                    if (END_DATE_REQUIRED == 'TRUE' && END_DATE_REQUIRED != null && END_DATE_REQUIRED != undefined) {
                                        $('#datePick9670 div:nth-child(1) a.col-md-1').children('span').remove()
                                        $('#datePick9670 div:nth-child(1) a.col-md-1').append('<span class="req-field mrg_lft_ft_lft">*</span>')
                                        localStorage.setItem('END_DATE_REQ', '')
                                    }
                                }, 6000);
                            }
                        }
                    }
                    $('.g4.except_sec.removeHorLine.iconhvr > .col-md-3.pad-0 > input').each(function (index) {
                        if (index == 0) {
                            var lbl_txt = $(this).parent().siblings().children('abbr').children('label').text().trim();
                            if (lbl_txt == 'Key' || lbl_txt == 'Fulfillment Fee Record ID') {
                                var key_value = $(this).val();
                                CurrentTab = $('#attributesContainer div.tabsmenu ul#carttabs_head li.active a span').text();
                                //A043S001P01-10742 start
                                $(this).val($('.product_txt_to_top_banner').text())
                                //A043S001P01-10742 end

                                // else {
                                //     $('.product_txt_to_top_banner').text(key_value);
                                // }
                            }
                        }
                    });
                    if (editicon_data) {
                        var field_txt_list = [];
                        $(editicon_data).each(function (index) {
                            var data_txt = editicon_data[index];
                            var data_txt_splited;
                            if (data_txt) {
                                data_txt_splited = data_txt.split('|');
                                var concat_data = data_txt_splited[1] + '|' + data_txt_splited[2];
                                field_txt_list.push(concat_data);
                                $('.iconhvr label').each(function (index) {
                                    var iconhvr_lbl_txt = $(this).text().trim();
                                    if (data_txt_splited[1]) {
                                        var data_txt_splited_1 = data_txt_splited[1].trim().toLowerCase();
                                        iconhvr_lbl_txt = iconhvr_lbl_txt.toLowerCase();
                                        if (data_txt_splited_1 == iconhvr_lbl_txt) {
                                            if (data_txt_splited[2]) {
                                                if (data_txt_splited[2].trim() == "READ ONLY") {

                                                    //A043S001P01-12214 start
                                                    if (data_txt_splited_1 = 'currency' && localStorage.getItem('BTNADDNEW') != '') {
                                                    }
                                                    else {
                                                        $(this).parent().siblings().children('.editiconright').children('a').children('i').attr('class', 'fa fa-lock');
                                                        $(this).closest('abbr').parent().siblings().children('.editiconright').children('a').children('i').attr('class', 'fa fa-lock');
                                                    }
                                                    //A043S001P01-12214 end
                                                } else {
                                                    locked = $("div#check_cont8033  input[type='checkbox']").prop("checked");
                                                    if (locked != true || data_txt_splited_1 == 'locked') {
                                                        $('.sec_attr_get #dyn8045 #ctr_drop').show();
                                                        $('.sec_attr_get #dyn8072 #ctr_drop').show();
                                                        $(this).parent().siblings().children('.editiconright').children('a').children('i').attr('class', 'fa fa-pencil');
                                                        $(this).closest('abbr').parent().siblings().children('.editiconright').children('a').children('i').attr('class', 'fa fa-pencil');
                                                    } else {
                                                        $('.sec_attr_get #dyn8045 #ctr_drop').hide();
                                                        $('.sec_attr_get #dyn8072 #ctr_drop').hide();
                                                        $(this).parent().siblings().children('.editiconright').children('a').children('i').attr('class', 'fa fa-lock');
                                                        $(this).closest('abbr').parent().siblings().children('.editiconright').children('a').children('i').attr('class', 'fa fa-lock');
                                                    }
                                                }
                                            }
                                        }
                                        //A043S001P01-8665 start
                                        else if (getCurrentTabName == "Pages" || getCurrentTabName == "Page") {
                                            if (iconhvr_lbl_txt == "tab label" || iconhvr_lbl_txt == "tab type" || iconhvr_lbl_txt == "tab app" ) {
                                                $(this).parent().siblings().children('.editiconright').children('a').children('i').attr('class', 'fa fa-lock');
                                                $(this).closest('abbr').parent().siblings().children('.editiconright').children('a').children('i').attr('class', 'fa fa-lock');
                                            }
                                        }
                                        //A043S001P01-8665 end
                                    }
                                });
                            }
                        });
                        var attribute_tab_button_val = localStorage.getItem('attribute_tab_button');
                        if (attribute_tab_button_val == '1') {
                            if (getCurrentTabName != 'Attributes' && getCurrentTabName != 'Attribute') {
                                setTimeout(function () {
                                    $('.editiconright a.editclick i').each(function (index) {
                                        $(this).attr('class', 'fa fa-lock');
                                    });
                                    localStorage.setItem('attribute_tab_button', '0');
                                }, 1000);
                            }

                        }
                        var active_tab_set = $('ul#carttabs_head li.active a span').text().trim();
                        if (active_tab_set == "Price Model") {
                            if (localStorage.getItem("Action_Text") == "VIEW") {
                                $('input:checkbox').prop('disabled', true);
                            }
                            //A043S001P01-8500 start
                            // if (localStorage.getItem("Action_Text") == "EDIT") {
                            // var selectedMarketType = $('#QSTN_SYSEFL_PB_01449 :selected').text();
                            // var selectedModelType = $('#QSTN_SYSEFL_PB_01444 :selected').text()
                            // // RAMESH A043S001P01-7497-START
                            // if (selectedMarketType != "NON MARKET BASED") {
                            // // $('input:checkbox').prop('disabled', false);
                            // // $('input:checkbox:first').prop('disabled', true);
                            // // $('input:checkbox:first').prop('checked', false);
                            // } else {
                            // if (selectedModelType != "DISCOUNT DOWN") {
                            // // $('input:checkbox:first').prop('checked', false);
                            // // $('input:checkbox:first').prop('disabled', true);
                            // } else {
                            // // $('input:checkbox').prop('disabled', false);
                            // }
                            // }
                            // // RAMESH A043S001P01-7497-END
                            // }
                            //A043S001P01-8500 end
                        }
                        if (active_tab_set == 'Price Agreement') {
                            $('#mat4713 .editclick i').attr('class', 'fa fa-lock');
                            $("#mat4713").attr("disabled", false);
                            $("#lk4714").attr("disabled", false);
                            $('#lk4714 .editclick i').attr('class', 'fa fa-lock');
                        }
                    }
                    //RAMESH A043S001P01-8018 START 
                    if (sectionedit_data) {
                        $(sectionedit_data).each(function (index) {
                            var section_edit_id = sectionedit_data[index];
                            $("#" + section_edit_id).closest('#ctr_drop').css("display", "none")
                        });
                    }// RAMESH A043S001P01-8018 END 
                });
            } catch (e) {
                console.log(e);
            }
        }
    }
    current_url=window.location.href;
    if(current_url.includes('https://sandbox.webcomcpq.com/Configurator.aspx')){
        $('div.material_btn > div.material_btn_bg > div.segmentButtons .primary_grid_button').hide();
	}
    var currentTabName = $('ul#carttabs_head li.active').text().trim();
    if (currentTabName == 'List Pricebook Entry') {
        if (localStorage.getItem('lbe_lock') == 'checked') {
            if (document.getElementById("ctr_drop")) {
                // document.getElementById("ctr_drop").style.display = "none";
            }
        }
    }
    var Material_fiew_edit = localStorage.getItem('Material_view_obj_details');
    if (Material_fiew_edit == '1') {
        $('.Related').css('display', 'none');
        localStorage.setItem('Material_view_obj_details', '0');
    }
    var button_text_lstg = localStorage.getItem('button_text_clone');
    if (button_text_lstg == 'clone') {
        $('.btnMainBanner').each(function (index) {
            var btnMainBanner_txt = $(this).text().trim();
            if (btnMainBanner_txt == 'CLONE') {
                $(this).css('display', 'block');
            }
        });
    } else {
        $('.btnMainBanner').each(function (index) {
            var btnMainBanner_txt = $(this).text().trim();
            if (btnMainBanner_txt == 'CLONE') {
                $(this).css('display', 'none');
            }
        });
    }
    var active_tab_set = $('ul#carttabs_head li.active a span').text().trim();
    if (active_tab_set == 'Set') {
        $('#Attributesets_tab').css('display', 'block');
    } else {
        $('#Attributesets_tab').css('display', 'none');
    }
    $('input').each(function () {
        var inp = $(this).val();
        if (/^[-+]?[0-9]+\.[0-9]+$/.test(inp)) {
            $(this).attr('type', 'number');
        }
    });
    if ($('#jqxSplitter')) {
        var jqxSplitter_length = $('#jqxSplitter').length;
        if (jqxSplitter_length > 0) {
            $('html').css('overflow-y', 'hidden');
        } else {
            $('html').css('overflow-y', 'auto');
        }
    } else {
        $('html').css('overflow-y', 'auto');
    }
    setTimeout(function () {
        /* update banner-content value 'begin'*/
        var attrTypeCont = localStorage.getItem('attr_type_cont');
        var save_length = 0;
        if ($('#BTN_SYACTI_MA_00023_SAVE')) {
            save_length = $('#BTN_SYACTI_MA_00023_SAVE').length;
        }
        if (attrTypeCont == '1') {
            $('div#Attr_Jqxdropdown').css('cssText', 'background-color:lightyellow;pointer-events:all;border-left: 1px solid #dcdcdc;border-right: 1px solid #dcdcdc;border-radius: 0;');
            $('div[id^=listitem]').css('background-color', 'lightyellow');
        } else {
            if (save_length == 1) {
                $('div#Attr_Jqxdropdown').css('cssText', 'background-color:lightyellow;pointer-events:all;border-left: 1px solid #dcdcdc;border-right: 1px solid #dcdcdc;border-radius: 0;');
                $('div[id^=listitem]').css('background-color', 'lightyellow');
                localStorage.setItem('attr_type_cont', '1');
            } else {
                $('div#Attr_Jqxdropdown').css('cssText', 'background-color:#fff;pointer-events:none;border:0;');
                $('div[id^=listitem]').css('background-color', '#fff');
            }
        }
        $('div#check_cont5250 > .col-md-1 > .editiconright > a.editclick > i').attr('class', 'fa fa-lock');
    }, 2000);
    setTimeout(function () {
        var b = $('#QSTN_SYSEFL_MA_05164').val();
        var a = $('#HELP_TEXT').val();
        if (a != b) {
            $('#HELP_TEXT').parent().siblings('td').children('a').children('.fa-warning').remove();
            $('#HELP_TEXT').parent().siblings('td').children('a').children('.fa-info-circle').after('<i class="fa fa-warning" style="color:darkred;"></i>');
        } else {
            $('#HELP_TEXT').parent().siblings('td').children('a').children('.fa-warning').remove();
        }
        var page_load2 = localStorage.getItem("page_reload_2");
        if (page_load2 == '2') {
            $('a.createclose').trigger('click');
        }
        var Banner_Hiding_Var_local = localStorage.getItem("Banner_Hiding_Var");
        if (Banner_Hiding_Var_local == '1') {
            $('.product_txt_div').css('display', 'none');
            $('.part_number_txt').css('display', 'none');
            $('.sap_desc_txt').css('display', 'none');
        } 

        else if(CurrentTab == 'Quote'  || CurrentTab == 'Email Template' || CurrentTab == "App" || CurrentTab == "Tab" || CurrentTab == "Page" || CurrentTab == "Object" || CurrentTab == "Script" || CurrentTab == "Profile" || CurrentTab == "Variable")
        {
            $('.product_txt_div').css('display', 'none');
        }
        else {            
            $('.product_txt_div').css('display', 'block');
            $('.part_number_txt').css('display', 'block');
            $('.sap_desc_txt').css('display', 'block');
                        
        }

        var pr_cls_cld = localStorage.getItem('PriceClassesChild');
        if (pr_cls_cld == '1') {
            $("#QSTN_SYSEFL_MA_00464 option:nth-child(1)").attr('selected', 'selected');
            $('select#QSTN_SYSEFL_MA_00464 option:nth-child(2)').css('display', 'none');
            $("#QSTN_SYSEFL_PB_01569 option:nth-child(1)").attr('selected', 'selected');
            $('select#QSTN_SYSEFL_PB_01569 option:nth-child(2)').css('display', 'none');
            localStorage.setItem('PriceClassesChild', '0');
        }
        var tab_classname_in_list = ['li[class^=tab_Item_Category]', 'li[class^=tab_Fulfillment]', 'li[class^=tab_Material_Type]', 'li[class^=tab_Award_Code]'];
        $(tab_classname_in_list).each(function (index) {
            $(tab_classname_in_list[index]).each(function (indexes) {
                if (indexes > 0) {
                    $(this).css('cssText', 'display:none !important');
                } else {
                    $(this).css('cssText', 'display:block !important');
                }
            });
        });
    }, 1500);
    setTimeout(function () {
        /* New Freeze code for tree view 'begin' */
        var th_width_tree_tree = [];
        $('#table_price_class thead tr th').each(function (index) {
            var wid = $(this).css('width');
            if (index == 0 || index == 1) {
                th_width_tree_tree.push('60px');
            } else {
                th_width_tree_tree.push(wid);
            }
        });
        var get_thead_code = $('#table_price_class thead').html();
        var get_thead_join_code = "<thead class='fullHeadSecond'>" + get_thead_code + "</thead>";
        $('#table_price_class tbody').before(get_thead_join_code);
        $('#table_price_class thead:first-child').css('cssText', 'position: fixed;z-index: 2;border-top: 1px solid #dcdcdc;top: 152px;border-right: 0 !important;');
        $('#table_price_class thead:first-child').attr('class', 'fullHeadFirst');
        $('#table_price_class').css('cssText', 'margin-top: 5px !important;');
        $('#table_price_class').before('<div style="height: 9px;position: fixed;width: 100%;top: 146px;background-color: #fff !important;z-index: 2;"></div>');
        $('#table_price_class thead:first-child tr th').each(function (index) {
            var num = th_width_tree_tree[index].split('px');
            var numsp = parseInt(num[0]);
            numsp = numsp - 1;
            var make_str = numsp + 'px';
            var style_min_max = 'width:' + make_str + ';white-space: nowrap;overflow: hidden;text-overflow: ellipsis;';
            $(this).css('cssText', style_min_max);
            if (index != 0 && index != 1) {
                $(this).children('.th-inner').css('cssText', style_min_max);
            }
        });
        /* New Freeze code for tree view 'end' */
    }, 1000);
    var local_stg_sec_rel = localStorage.getItem('sec_edit_to_rel_tab');
    if (local_stg_sec_rel == '1') {
        localStorage.setItem('sec_edit_to_rel_tab', '0');
    }
    // 5053 starts....
    currenttab = $('ul#carttabs_head li.active a span').text();
    //Added the button in My Approvals Queue tab only..
    // if(CurrentTab == 'My Approvals Queue'){
    //     $('#submit_for_approval_btn_primary').show()
    //     $('#recall_for_edit_approval').show();
    // }
    if (CurrentTab == 'Quote'){
        //Added to hide & show edit button in PHP based on the quote status - start
        que = $('#QSTN_SYSEFL_QT_00009 option:selected').text();
        var editbtn_disp = localStorage.getItem("dispRecall");
    	if (que == 'REJECTED' && editbtn_disp == 'True'){
    		$('#recall_for_edit').show();    		
    	}
    	else{
    		$('#recall_for_edit').hide();
        }
        //QuoteStatus();
		dynamic_status();
        // ADDED code for dynamic changes for Workflow status bar depends on Quote status
        QTID = $('#QSTN_SYSEFL_QT_00001').attr('title');
        cpq.server.executeScript("ACSECTACTN", {
        'ACTION': "STATUS",
        'QuoteNumber': QTID
        }, function (data) {
        if(data == 'APPROVED'){
            $("#approve_status").text(data);
            //$("#approve_status").parent().css('background','#4CCA82');
            $("#approve_status_outer").removeClass('active');
            $("#approve_status_outer").addClass('complete');
            $("#approve_status_outer").removeClass('reject');
            $("#approve_status").attr("title",data);
            $("#approve_status_reject").css('display','none');
            $("#approve_status_numb").css('display','none');
            $("#approve_status_compl").css('display','block');

        }
        else if(data == 'REJECTED'){
            $("#approve_status").text(data);
            //$("#approve_status").parent().css('background','#ea4335');
            $("#approve_status_outer").removeClass('complete');
            $("#approve_status_outer").addClass('reject');
            $("#approve_status_outer").removeClass('active');
            $("#approve_status").attr("title",data);
            $("#approve_status_numb").css('display','none');
            $("#approve_status_compl").css('display','none');
            $("#approve_status_reject").css('display','block');
        }
        else if(data != 'REJECTED' && data != 'APPROVED')
        {
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
        //Added to hide & show edit button in PHP based on the quote status - end
    }
    // Added for hiding and showing attribute based on picklist value selection in Approval Chains tab Add NEW- start
    if (currenttab == 'Approval Chain'){
    	val = $('#QSTN_SYSEFL_AC_00006 option:selected').text();
    		if (val == 'SERIES STEP APPROVAL' || val == 'PARALLEL STEP APPROVAL' || val == '..Select'){    			
    			$('#mat3037 ').hide();
    			}
    		else{
    			$('#mat3037 ').show();
    		}	
    			
        }
    // Added for hiding and showing attribute based on picklist value selection in Approval Chains tab Add NEW- end   
    if (currenttab == 'List Pricebook Entry') {
        $('#check_cont8033').on('change', function () {
            try {
                cpq.server.executeScript("SYRLEXEEND", {}, function () {
                    $('.BTN_MA_ALL_REFRESH').click();
                });
            } catch (e) {
                //console.log('ruleenderror',e);
            }
            locked = $("div#check_cont8033  input[type='checkbox']").prop("checked");
            if (locked != true) {
                $('.sec_attr_get #dyn8045 #ctr_drop').show();
                $('.sec_attr_get #dyn8072 #ctr_drop').show();
            } else {
                $('.sec_attr_get #dyn8045 #ctr_drop').hide();
                $('.sec_attr_get #dyn8072 #ctr_drop').hide();
            }
        });
    } // 5053 ends....
    var ActiveTab = $('ul#carttabs_head li.active a span').text();
    var get_Banner_Hiding_Var = localStorage.getItem("Banner_Hiding_Var");
    if (ActiveTab == 'Price Class' && get_Banner_Hiding_Var == '1') {
        localStorage.setItem("page_reload", "1");
    }
    setTimeout(function () {
        var sectionFieldsEditable = localStorage.getItem('section_fields_editable');
        if (sectionFieldsEditable == '2') {
            if ($('input#QSTN_SYSEFL_SE_00303')) {
                $('input#QSTN_SYSEFL_SE_00303').css('background-color', 'lightyellow');
                //$('div[id^=dyn] div#ctr_drop').css('display', 'none');
            } else {
                $('input#QSTN_SYSEFL_SE_00303').css('background-color', '#fff');
            }
        }
    }, 1000);
    var act_tab_name_txt = $('ul#carttabs_head li.active a span').text()
    if (act_tab_name_txt != '' && act_tab_name_txt == 'Price Factor') {
        if ($('#QSTN_SYSEFL_PB_01607 option:selected').text() == 'PERCENT') {
            var isDisabled = $("input#QSTN_SYSEFL_PB_00091").prop('disabled');
            if (isDisabled == true) {
                $("input#QSTN_SYSEFL_PB_00091").attr('type', 'text');
                var input_val = $("input#QSTN_SYSEFL_PB_00091").val();
                if (input_val[input_val.length - 1] != '%') {
                    $("input#QSTN_SYSEFL_PB_00091").val(input_val + '' + '%');
                }
            }//A043S001P01-7418 - Start
            else if (isDisabled == false) {
                //console.log("per")
                $("input#QSTN_SYSEFL_PB_00091").attr('type', 'number');
            }
        }
        else if ($('#QSTN_SYSEFL_PB_01607 option:selected').text() == 'NUMBER') {
            var isDisabled = $("input#QSTN_SYSEFL_PB_00091").prop('disabled');
            //console.log("ïsdisabled", isDisabled)
            if (isDisabled == false) {
                //console.log("hello")
                $("input#QSTN_SYSEFL_PB_00091").attr('type', 'number');
            }
        } //A043S001P01-7418 - End
    }
    var pric_name = $('div#attributesContainer .row.tabsfiled .tabbable.show-large.btnmodule li#ModName span.main_ban_mod').text()
    if (pric_name == 'Pricebooks' || pric_name == 'Price Models') {
        document.getElementById("ModuleName").style.display = "inline-block";
        document.getElementById("ModuleName1").style.display = "none";
        document.getElementById("ModuleIcons").style.display = "inline-block";
        document.getElementById("ModuleIcons1").style.display = "none";
    } /* else {
        document.getElementById("ModuleName").style.display = "none";
        document.getElementById("ModuleName1").style.display = "inline-block";
        document.getElementById("ModuleIcons").style.display = "none";
        document.getElementById("ModuleIcons1").style.display = "inline-block";
    } */
    SECTION_EDIT = localStorage.getItem("SECTION_EDIT");
    div_id = localStorage.getItem('div_id');
    a = ''
    var testloop_get = localStorage.getItem('testloop');
    if (testloop_get == '1') {
        a = 'test';
        localStorage.setItem("Action_Text", 'ATTR_TRIGGER')
    } else if (testloop_get == '0') {
        a = 'test';
    }
    btn_Val = localStorage.getItem("Action_Text");
    var locked = 'FALSE'; //5053 starts.. 5053 ends...
    if (String(btn_Val) == 'VIEW') {
        //5053 starts....
        $('.sec_attr_get #dyn4850 #ctr_drop').hide();
        $('.sec_attr_get #dyn6973 #ctr_drop').hide();
        $('.sec_attr_get #dyn5057 #ctr_drop').show();
        //$('#textinformation').css('display', 'none');
        //5053 ends...
        if (document.getElementById("QSTN_SYSEFL_MA_00077")) {
            sel_val = $('#QSTN_SYSEFL_MA_00077 option:selected').text();
            if (String(sel_val) != 'ZMAT SET' && String(sel_val) != 'VARIANT SET' && String(sel_val) != 'COMPONENT SET') {
                $('.sec_attr_get #ctr_drop').hide();
                //A043S001P01-6661 Start
                $('.sec_attr_get #EMBLEM_EDIT').hide();
                // A043S001P01-6661 End
            } else {
                $('.sec_attr_get #ctr_drop').show();
                //A043S001P01-6661 Start
                $('.sec_attr_get #EMBLEM_EDIT').show();
                // A043S001P01-6661 End
            }
        } else if (document.getElementById("QSTN_SYSEFL_PB_01459")) {
            price_method = $('#QSTN_SYSEFL_PB_01459').val();
            //5053 starts...
            locked = $("div#check_cont8033  input[type='checkbox']").prop("checked");
            if ((String(price_method) == 'RPWORD' || String(price_method) == 'MANUAL') && locked != true) {
                $('.sec_attr_get #dyn8072 #ctr_drop').show();
            } else if (locked != true) {
                $('.sec_attr_get #dyn8072 #ctr_drop').show();
            }
            if (locked != true) {
                $('.sec_attr_get #dyn8045 #ctr_drop').show();
                $('.sec_attr_get #dyn8072 #ctr_drop').show();
            } else {
                $('.sec_attr_get #dyn8045 #ctr_drop').hide();
                $('.sec_attr_get #dyn8072 #ctr_drop').hide();
            } //5053 ends...
        }
    } else if (String(btn_Val) == 'ATTR_TRIGGER') {
        // A043S001P01-6661 Start
        $('.header_section_div #ctr_drop').hide();
        if (act_tab_name_txt != 'Price Agreement') {
            $('.sec_attr_get #ctr_drop').hide();
        }

        $('.sec_attr_get #EMBLEM_EDIT').hide();
        //Added to restrict more than 8 characters for APPROVAL CHAIN ID field - start
        if (act_tab_name_txt == 'Approval Chain'){
        	$("input#QSTN_SYSEFL_AC_00002").prop('maxLength', 8);
        }
        //Added to restrict more than 8 characters for APPROVAL CHAIN ID field - end
        //$('#textinformation').css('display', 'none');
        //A043S001P01-6661 End
    } else {
        //A043S001P01-6661 Start
        $('.sec_attr_get #EMBLEM_EDIT').hide();
        //A043S001P01-6661 End
        $('.sec_attr_get #ctr_drop').hide();
    }
    if (document.getElementsByClassName("header_section_div").length == 0) {
        if (SECTION_EDIT != '' && a == 'test' && (String(btn_Val) == 'SEC_EDIT' || String(btn_Val) == 'VIEW' || String(btn_Val) == 'ATTR_TRIGGER')) {
            var sec_count = 0
            var str = ""
            $('.sec_attr_get div').each(function () {
                id = String($(this).attr('id'))
                if (id.includes("dyn")) {
                    if (String(id) == String(div_id)) {
                        sec_count += 1;
                        // $('#' + id).attr('style', 'margin-top: -1px !important');

                        $('.SEC_ACT').attr('style', 'display:none !important');
                        str = ""
                    } else {
                        sec_count = 0;
                    }
                }
                if (id != 'material_emblem_style' && id != 'EMBLEM_EDIT' && id != 'undefined' && id != 'ctr_drop' && String(id.includes("ban")) != 'true' && (String(id.includes("conta")) != 'true' || String(id) == 'conta6102') && String(id.includes("div")) != 'true' && String(id.includes("ctr")) != 'true' && id != 'Attr_Jqxdropdown') {
                    if (sec_count == 1) {
                        //A043S001P01-12230 Ramesh
                        if (str == '' && id.includes("SegAlert") != 1) {
                            str += '#' + id
                        } else {
                            if (id.includes("SegAlert") != 1) {
                                str += ',#' + id
                            }
                        }
                        //A043S001P01-12230 Ramesh
                    }
                }
            });
            //5053 starts...
            if (String(SECTION_EDIT) == 'SYSECT-PB-00068' || (String(SECTION_EDIT) == 'SYSECT-PB-00067' && locked != true) || String(SECTION_EDIT) == 'SYSECT-PB-00070' || String(SECTION_EDIT) == 'SYSECT-PB-00071' || String(SECTION_EDIT) == 'SYSECT-PB-00405' || String(SECTION_EDIT) == 'SYSECT-PB-00058') { //5053 ends....
                setTimeout(function () {
                    $(str).wrapAll('<div class="header_section_div header_section_div_pad_bt10 col-md-12"/>'); //padding: 10px;
                    //JIRA ID 6722 changed the save and cancel button order
                    $(".header_section_div").append('<div class="g4  except_sec removeHorLine iconhvr sec_edit_sty"><button id="SEC_DIS_CLOSE" style="display: none;" data-target="#processing_modal" data-toggle="modal" ></button><button data-target="#processing_modal" data-toggle="modal" id="' + SECTION_EDIT + '" class="btnconfig btnMainBanner sec_edit_sty_btn_inh" onclick="sec_save_tab(this)">SAVE</button><button id="' + SECTION_EDIT + '"class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="sec_cancel_tab(this)">CANCEL</button></div>');
                }, 1000);
                $('#' + div_id + ' #ctr_drop').hide()
                // A043S001P01-6661 Start
                $('.sec_attr_get #EMBLEM_EDIT').hide();
                //A043S001P01-6661 End
            }
            //JIRA ID 6722 changed the save and cancel button order
            else {
                // COMMENTING THE CODE TO RESTRICT MULTIPLE CANCEL & SAVE BUTTONS WHILE CLICKING SECTION EDIT BUTTON - START
                // setTimeout(function () {
                //     if (String(SECTION_EDIT) == 'SYSECT-PB-00434') {
                //         $("#dyn10274,#drop10273,#drop_cont10273,#drop9247,#drop_cont9247,#drop10266,#drop_cont10266").wrapAll('<div class="header_section_div header_section_div_pad_bt10" />');
                //     }
                //     else {
                //         if (String(localStorage.getItem("SECTION_EDIT"))) {
                //             $(str).wrapAll('<div class="header_section_div header_section_div_pad_bt10 col-md-12" />'); //padding: 10px;
                //         }
                //     }
                //     //JIRA ID 6722 changed the save and cancel button order
                //     if (String(localStorage.getItem("SECTION_EDIT"))) {
                //         $(".header_section_div").append('<div class="g4  except_sec removeHorLine iconhvr sec_edit_sty"><button id="SEC_DIS_CLOSE" style="display: none;"  ></button><button   id="' + SECTION_EDIT + '" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="sec_cancel_tab(this)">CANCEL</button><button id="' + SECTION_EDIT + '" class="btnconfig btnMainBanner sec_edit_sty_btn_inh" onclick="sec_save_tab(this)">SAVE</button></div>');
                //     }
                //     textAreaAccess();
                // }, 1000);
                // COMMENTING THE CODE TO RESTRICT MULTIPLE CANCEL & SAVE BUTTONS WHILE CLICKING SECTION EDIT BUTTON - END
                $(str).wrapAll('<div class="header_section_div header_section_div_pad_bt10 col-md-12" />');
                $(".header_section_div").append('<div class="g4  except_sec removeHorLine iconhvr sec_edit_sty"><button id="SEC_DIS_CLOSE" style="display: none;"  ></button><button   id="' + SECTION_EDIT + '" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="sec_cancel_tab(this)">CANCEL</button><button id="' + SECTION_EDIT + '" class="btnconfig btnMainBanner sec_edit_sty_btn_inh" onclick="sec_save_tab(this)">SAVE</button></div>');
                //JIRA ID 6722 changed the save and cancel button order
                $('#' + div_id + ' #ctr_drop').hide()
                // A043S001P01-6661 Start
                $('.sec_attr_get #EMBLEM_EDIT').hide();
                // A043S001P01-6661 End

            }
            if (document.getElementById("QSTN_SYSEFL_MA_00077")) {
                sel_val = $('#QSTN_SYSEFL_MA_00077 option:selected').text();
                setTimeout(function () {
                    if (String(sel_val) != 'ZMAT SET' && String(sel_val) != 'VARIANT SET' && String(sel_val) != 'COMPONENT SET') {
                        $('#QSTN_SYSEFL_MA_00387').attr('disabled', 'disabled');
                        $('#QSTN_SYSEFL_MA_04895').attr('disabled', 'disabled');
                    }
                }, 1000);
            }
        }else{
            textAreaAccess();
        }
        // A043S001P01-6657 Start
        if (String(btn_Val) == 'EDIT') {
            setTimeout(function () {
                $('div[id^=dyn] div#ctr_drop').css('display', 'none');
                //$('#textinformation').css('display', 'none');
            }, 1000);
        }
        // A043S001P01-6657 End
    }
    var savedrf = localStorage.getItem('save_drf');
    if (savedrf == '1') {
        $('div#ctr_drop').css('display', 'inline-block');
    }
    //hide edit dropdown when in edit mode start in system admin starts A055S000P01-3351
    var sect_edit_flag = localStorage.getItem("sect_edit_flag")
    if(sect_edit_flag == '1'){
		$('div[id^=dyn] div#ctr_drop').css('display', 'none');	
		localStorage.setItem("sect_edit_flag", '0')
    }
    //hide edit dropdown when in edit mode start in system admin ends A055S000P01-3351
    //A055S000P01-2811 to hide edit dropdown when in edit mode start
    if ($('#BTN_SYACTI_AC_00006_SAVE')) {
		save_length = $('#BTN_SYACTI_AC_00006_SAVE').length;
		if ((btn_txt_val == 'SAVE'|| btn_txt_val == 'CANCEL') && save_length == 1){
			$('div[id^=dyn] div#ctr_drop').css('display', 'none');
            if(req.length>=0){				
				$('span#QSTN_SYSEFL_AC_00002').text('* This field should be 8 Characters - alphanumeric only');
				$('span#QSTN_SYSEFL_AC_00002').closest('div').show();
				$("span#QSTN_SYSEFL_AC_00002").attr({'title' : '* This field should be 8 Characters - alphanumeric only'});
			}
			$("input#QSTN_SYSEFL_AC_00002").prop('maxLength', 8);
	}}
    //A055S000P01-2811 end
    var th_width_tree_tree = [];
    $('#table_price_class thead tr th').each(function (index) {
        var wid = $(this).css('width');
        if (index == 0 || index == 1) {
            th_width_tree_tree.push('60px');
        } else {
            th_width_tree_tree.push(wid);
        }
    });
    var get_thead_code = $('#table_price_class thead').html();
    var get_thead_join_code = "<thead class='fullHeadSecond'>" + get_thead_code + "</thead>";
    $('#table_price_class tbody').before(get_thead_join_code);
    $('#table_price_class thead:first-child').css('cssText', 'position: fixed;z-index: 2;border-top: 1px solid #dcdcdc;top: 152px;border-right: 0 !important;');
    $('#table_price_class thead:first-child').attr('class', 'fullHeadFirst');
    $('#table_price_class').css('cssText', 'margin-top: 5px !important;');
    $('#table_price_class').before('<div style="height: 9px;position: fixed;width: 100%;top: 146px;background-color: #fff !important;z-index: 2;"></div>');
    $('#table_price_class thead:first-child tr th').each(function (index) {
        var num = th_width_tree_tree[index].split('px');
        var numsp = parseInt(num[0]);
        numsp = numsp - 1;
        var make_str = numsp + 'px';
        var style_min_max = 'width:' + make_str + ';white-space: nowrap;overflow: hidden;text-overflow: ellipsis;';
        $(this).css('cssText', style_min_max);
        if (index != 0 && index != 1) {
            $(this).children('.th-inner').css('cssText', style_min_max);
        }
    });
    /* JIRA:6011 , Avoid Duplicate tab 'Begin' */
    $('ul#carttabs_head li').each(function (index) {
        var count = 0;
        var Current_tab_id_value = $(this).attr('id');
        var Current_tab_txt = $(this).text().trim();
        $('ul#carttabs_head li').each(function (indexes) {
            var tab_id_value = $(this).attr('id');
            if (Current_tab_txt == 'Account') {
                $('li.tab_Accounts.active').css('display', 'none');
            } else if (Current_tab_txt == 'Price Class') {
                $('li.tab_Price_Classes.active').css('display', 'none');
            } else if (Current_tab_txt == 'Currency') {
                $('li.tab_Currencies.active').css('display', 'none');
            } else if (Current_tab_txt == 'Country') {
                $('li.tab_Countries.active').css('display', 'none');
            }
            if (Current_tab_id_value == tab_id_value) {
                count += 1;
                if (count > 1) {
                    $(this).remove();
                }
            }
        });
    });
    /* JIRA:6011 , Avoid Duplicate tab 'End' */
    var key1 = $('#QSTN_SYSEFL_PB_01452').val();
    if (key1) {
        try {
            cpq.server.executeScript("PRLDORICON", {
                'KEY': key1
            }, function (data) {
                for (i = 0; i < data.length; i++) {
                    var id = data[i].split('-').join('_') + 'warning'
                    if (document.getElementById(id)) { } else {
                        if (data) {
                            $('#QSTN_' + data[i].split('-').join('_')).parent().siblings('div:first-child').children('a').children('i').after('<i id="' + id + '" class="fa fa-warning" style="color: #931010;float: left;padding-top: 0px;margin-left: 5px;"></i>');
                            $('#QSTN_' + data[i].split('-').join('_')).parent().siblings('div:first-child').children('a').css('cssText', 'text-align: left;padding: 7px 0px;color: green;width: 1.8%;');
                        }
                    }
                }
            });
        } catch (e) {
            console.log(e);
        }
    }
    setTimeout(function () {
        $('.sec_attr_get .g4.except_sec.container_grid.contain_mater > p > div').each(function (index) {
            var sty_val = $(this).css('display');
            if (sty_val == 'none') {
                $(this).parent().parent().css('display', 'none');
                $('#container5913').css('display', 'block');
                $('#container5913').css('display', 'block');
                $('#container4374').css('display', 'block');
                $('#container4375').css('display', 'block');
                $('#container4867').css('display', 'block');
            }
        });
    }, 2000);
    // var action = localStorage.getItem("Action_Text");
    // var Primary = localStorage.getItem('keyData');
    // var active = localStorage.getItem('KeyValueToTable');
    // var test_local = localStorage.getItem('test');
    // if (active == "Currencies" && Primary != "" && test_local != '1') {
    // if (action == "VIEW") {
    // try {
    // cpq.server.executeScript("SYALLTABOP", {
    // 'Primary_Data': Primary,
    // 'TabNAME': active,
    // 'ACTION': 'VIEW',
    // 'RELATED': 'TRUE'
    // }, function () {
    // localStorage.setItem("Action_Text", "VIEW");
    // $(".BTN_MA_ALL_REFRESH").click();
    // });
    // } catch (e) {
    // console.log(e);
    // }
    // localStorage.setItem('test', '1');
    // }
    // } else {
    // localStorage.setItem('test', '0');
    // }
    var Profile_ACTION = localStorage.getItem('Profile_ACTION');
    var Profile_edit = localStorage.getItem("Profile_EDITACTION");
    if (Profile_edit == 'EDIT') {
        var profile_grid_edit = localStorage.getItem('profileGridEdit');
        if (profile_grid_edit == '1') {
            setTimeout(function () {
                Profile_EDIT('SYSECT-SY-00001');
            }, 2000);
        }
    }

    //A043S001P01-12214 start
    if (btn_txt_val == 'ADD NEW') {
        document.querySelectorAll('div#ctr_drop').forEach(el => el.style.display = 'none');
        //To show information text in PHP in Approval Chain tab add new mode - start
        if (CurrentTab == "Approval Chain" && btn_Val != 'VIEW'){            
            //$('.product_txt_div').text(getCurrentTabName);
            if ($('#textinformation').length == 0){
                $('div.product_txt_div').append('<div class="text_header" id = "textinformation"><i class = "fa fa-info-circle"></i>Please name the Approval Chain and enter the Approval Chain Step criteria to configure Approvals for a Target Object.</div>')
                $('div.product_txt_div').css('max-width', '100%');
            }
            //Added to restrict more than 8 characters for APPROVAL CHAIN ID field - start
            $("input#QSTN_SYSEFL_AC_00002").prop('maxLength', 8);
            //Added to restrict more than 8 characters for APPROVAL CHAIN ID field - end                                        	
        }
        //To show information text in PHP in Approval Chain tab add new mode - end
    }
    //A043S001P01-12214 end
    // To Hide section edit in save mode
    else if (btn_txt_val == 'SAVE'){
        if($('#QSTN_SYSEFL_SY_03318').val() == ""){
    		$('.dropdown').hide()
    	}
        var sav_btn = $(".material_btn_bg").find('button#BTN_SYPSAC_SY_00023_SAVE')
        if (sav_btn.length == 1){
                document.querySelectorAll('div#ctr_drop').forEach(el => el.style.display = 'none');
        }
        if ($('#BTN_SYPGAC_SY_00014_SAVE').length == 1){
        	document.querySelectorAll('div#ctr_drop').forEach(el => el.style.display = 'none');        	
        }
        
     }
    // To Hide section edit in save mode
    var viewobjset = localStorage.getItem("Profile_OBJ_SET_VIEW")
    if (viewobjset == "OBJ_SET_VIEW") {
        $('#BTN_PROFILE_OBJSET_SAVE').css('display', 'none');
        $('#BTN_PROFILE_OBJSET_CAN').css('display', 'none');
    }
    var viewobjset = localStorage.getItem("Profile_OBJ_SET_EDIT")
    if (viewobjset == "OBJ_SET_EDIT") {
        $('#BTN_PROFILE_OBJSET_EDIT').css('display', 'none');
        $('#BTN_PROFILE_OBJSET_BTL').css('display', 'none');
    }
    mode = localStorage.getItem("Profile_ACTION")
    if (mode != '' && mode != null && mode != 'ADD NEW' && mode != 'ADD_NEW_VIEW' && mode != 'GRID_EDIT') {
        banner_contents = localStorage.getItem("PROFILE_BANNER")
        if (banner_contents != '' && banner_contents != null) {
            var banner_contents_final = banner_contents.split(",");
            var Profile_record_id = banner_contents_final[0];
            var Profile_id = banner_contents_final[1];
            var Profile_name = banner_contents_final[2];
            $("#PROFILE_BANNER_RECORD_ID abbr").text(Profile_record_id);
            $("#PROFILE_BANNER_RECORD_ID abbr").attr('title', Profile_record_id);
            $("#PROFILE_BANNER_ID abbr").text(Profile_id);
            $("#PROFILE_BANNER_ID abbr").attr('title', Profile_id);
            $("#PROFILE_BANNER_NAME abbr").text(Profile_name)
            $("#PROFILE_BANNER_NAME abbr").attr('title', Profile_name)
        }
    }
    mode = localStorage.getItem("ErrLog_ACTION")
    var tabname = localStorage.getItem('active_tab_name_text');
    if (tabname == 'Error Logs') {
        banner_contents = localStorage.getItem("ERRORLOG_banner")
        if (banner_contents != '' && banner_contents != null) {
            var banner_contents_final = banner_contents.split(",");
            var EL_ID = banner_contents_final[0];
            var EL_MSG_ID = banner_contents_final[1];
            var EL_NAME = banner_contents_final[2];
            $("#ERRLOG_BANNER_RECORD_ID abbr").text(EL_ID);
            $("#ERRLOG_BANNER_RECORD_ID abbr").attr('title', EL_ID);
            $("#ERRLOG_BANNER_ID abbr").text(EL_MSG_ID);
            $("#ERRLOG_BANNER_ID abbr").attr('title', EL_MSG_ID);
            $("#ERRLOG_BANNER_NAME abbr").text(EL_NAME);
            $("#ERRLOG_BANNER_NAME abbr").attr('title', EL_NAME);
            EL_ID1 = $("input#ERROR_LOGS_RECORD_ID").val()
            $("#ERRLOG_BANNER_RECORD_ID abbr").text(EL_ID1);
            $("#ERRLOG_BANNER_RECORD_ID abbr").attr('title', EL_ID1);
            var EL_MSG_ID = $("input#ERRORMESSAGE_RECORD_ID").val()
            $("#ERRLOG_BANNER_ID abbr").text(EL_MSG_ID);
            $("#ERRLOG_BANNER_ID abbr").attr('title', EL_MSG_ID);
            var EL_NAME = $("input#OBJECT_TYPE").val()
            $("#ERRLOG_BANNER_NAME abbr").text(EL_NAME);
            $("#ERRLOG_BANNER_NAME abbr").attr('title', EL_NAME);
            setTimeout(function () {
                var guidval = $("input#ERROR_LOGS_RECORD_ID").val();
                $("#ERRLOG_BANNER_RECORD_ID abbr").text(guidval);
                $("#ERRLOG_BANNER_RECORD_ID abbr").attr('title', guidval);
                var EL_MSG_ID = $("input#ERRORMESSAGE_RECORD_ID").val()
                $("#ERRLOG_BANNER_ID abbr").text(EL_MSG_ID);
                $("#ERRLOG_BANNER_ID abbr").attr('title', EL_MSG_ID);
                var EL_NAME = $("input#OBJECT_TYPE").val()
                $("#ERRLOG_BANNER_NAME abbr").text(EL_NAME);
                $("#ERRLOG_BANNER_NAME abbr").attr('title', EL_NAME);
            }, 2000);
        }
    }
    //5060, 8127 STARTS...
    //material_active_tab = $('ul#carttabs_head .active a span').text();
    material_active_tab = localStorage.getItem('KeyValueToTable');
    Primary_Data = localStorage.getItem('keyDataVal');
    if ($('ul#carttabs_head .active a span').text() == 'List Pricebook Entry' || $('ul#carttabs_head .active a span').text() == 'Pricebook Entry') {
        try {
            cpq.server.executeScript("SYERRMSGVL", {
                'RecordId': Primary_Data,
                'Level': 'TAB',
                'TabName': material_active_tab,
                'Action': 'VIEW'
            }, function (data) {
                if (data != '') {
                    // A043S001P01-5060 START
                    localStorage.setItem('err_msg_avail', '1');
                    // A043S001P01-5060 END
                    //6597 starts...
                    if (material_active_tab == 'Pricebook Entries' || material_active_tab == 'List Pricebook Entries') {
                        var container = document.getElementById("SegAlert_notifcation");
                        if (container) {
                            container.innerHTML = ''
                        }
                        for (var i = 0; i < data.length; i++) {
                            if (container) {
                                if (i == 0) {
                                    /*if (data[i].includes("INFORMATION")) {
                                        container.innerHTML += '<div class="col-md-12 alert-info" id="lblSegAlert_' + i + '">' + data[i] + '</div>';
                                    } else {*/
                                    container.innerHTML += '<div class="col-md-12 alert-warning" id="lblSegAlert_' + i + '">' + data[i] + '</div>';
                                    //}
                                } else {
                                    //if (data[i].includes("INFORMATION")) {
                                    //container.innerHTML += '<div class="col-md-12 alert-info mrg_tp10"  id="lblSegAlert_' + i + '">' + data[i] + '</div>';
                                    //} else {
                                    container.innerHTML += '<div class="col-md-12 alert-warning mrg_tp10" id="lblSegAlert_' + i + '">' + data[i] + '</div>';
                                    //}
                                }
                            }
                            //$('#lblSegAlert_'+i+'').html('');
                            //$('#SegAlert_notifcation').css('display', 'none');
                            //$('#lblSegAlert_'+i+'').append(data[i]);
                            // $('#SegAlert_notifcation').css('display', 'block');
                        }
                        if (data.length > 0) {
                            $('#SegAlert').css('display', 'block');
                        }
                    } else { //6597 ends...
                        $('div#SegAlert #lblSegAlert').html('');
                        $('div#SegAlert').css('display', 'none');
                        $('div#SegAlert #lblSegAlert').append(data);
                        $('div#SegAlert').css('display', 'block');
                        $('div#lblSegAlert').css('display', 'block');
                    }
                } else {
                    //A043S001P01-5060 START
                    localStorage.setItem('err_msg_avail', '0');
                    //A043S001P01-5060 END
                    $('div#SegAlert').css('display', 'none');
                }
            });
        } catch (e) {
            console.log(e)
        }
    }//5060, 8127 ENDS....
    setTimeout(function () {
        if (document.getElementById('QSTN_SYSEFL_MA_00464')) {
            Priceclass = $('#QSTN_SYSEFL_MA_00464 :selected').text();
            if (Priceclass == 'SUPER CLASS') {
                $('#QSTN_SYSEFL_MA_00464').parent().siblings(".col-md-1").children('div').children('a').html('<i class="fa fa-lock" aria-hidden="true"></i>');
            }
        }
    }, 3000);
    try {
        if (document.getElementById("jqxSplitter")) {
            $('#jqxSplitter').jqxSplitter({
                theme: 'summer',
                width: '100%',
                panels: [{ size: '20%', min:'0' }, { size: '70%', min:'0' }]
            });
        }
    } catch (err) { }
 

  //   $('.jqx-splitter-collapse-button-vertical').click(function() {
   //     if ($('.jqx-splitter-collapse-button-vertical').hasClass('jqx-splitter-collapse-button-hover')){
    //        $("#content1234").show();
    //        $(".jqx-splitter-splitbar-vertical").css('left','20%');
  //  $("#content12345").css('width','79%');
   //     } else {
    //        $("#content1234").hide();
    //        $(".jqx-splitter-splitbar-vertical").css('left','0');
  //  $("#content12345").css('width','100%');
   //       }
  //  });

 

    if ($('.active').attr('id') == 'tab_Price_Model') {
        $('.sap_desc_txt').css({
            'max-width': '40%',
            'overflow': 'hidden',
            'text-overflow': 'ellipsis'
        });
    }    
    //Added to restrict Special characters for APPROVAL CHAIN ID field label - start
    $('input#QSTN_SYSEFL_AC_00002').on('keypress', function (event) {
        $('input#QSTN_SYSEFL_AC_00002').prop('maxLength',8);
        var regex = new RegExp("^[a-zA-Z0-9]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : 		event.charCode);
        if (!regex.test(key)) {
           event.preventDefault();
           return false;
        }
    });
    $('input#REQUIRE_EXPLICIT_APPROVAL').on('change', function() {
        $('input#ENABLE_SMARTAPPROVAL').not(this).prop('checked', false);  
    });
    //Added to restrict Special characters for APPROVAL CHAIN ID field label - end
    $('div[id^=sear]').each(function (index) {
        $(this).siblings('div[id^=rownum]').children('.search_txt_file').children('.col-md-10.pad-0').children('input').css('cssText', 'border-left: 1px solid rgb(220, 220, 220);border-right: 1px solid rgb(220, 220, 220);background-color: lightyellow !important;');        
    });
$('#RichTextArea').click()    
});
setTimeout(function () {
    var grid_add = localStorage.getItem("Pricebtn_hide");
    if (grid_add == "1") {
        $('.dropdown').css('display', 'none');
        localStorage.setItem("Pricebtn_hide", "0");
    }
}, 5000);
setTimeout(function () {
    auto_elem = $('input[id^="QSTN"]').first();
    auto_num_value = auto_elem.val();
    id_value = auto_elem.attr('id');
    $('#' + id_value).attr('title', auto_num_value);
}, 2000);

if ((localStorage.getItem("KeyValueToTable") == 'Sales Orders') && (localStorage.getItem('moveNextTab') == 'TRUE')) {
    localStorage.setItem("moveNextTab", "");
    $(".BTN_MA_ALL_REFRESH").click();
}

function  offerinf_edit(ele) {
    var values = [];
    var table = $("#SYOBJR_98788_87896663_6F9D_4D6E_B1C1_6DA146B56815");
    localStorage.setItem("EDIT_COMPR_action", "Compre_Line_Edit");
    if (table.find('[type="checkbox"]:checked').length) {
        table.find('[type="checkbox"]:checked').map(function () {
            sap = $(this).closest('tr').find('td:nth-child(1)').text();
            if (sap != undefined) {
                values.push(sap)
            }
        });
    }
    else {
        table.find('[type="checkbox"]').map(function () {
            sap = $(this).closest('tr').find('td:nth-child(1)').text();
            if (sap != undefined && sap != "") {
                values.push(sap)
            }
        });
    }

   
}

console.log("CONFIGURATOR END"+window.location.href);

/* CONFIGURATOR UPDATE 'END' */
$( window ).on( "load", function() {
       $("#div_CTR_Quote_Preview").prev().css("display", "none");
    });

console.log("API-CART-URL"+window.location.href);
var current_url = window.location.href;
var regex = new RegExp('sapcrm\/saplogin\.aspx');  // Check Regex pattern Only for Quotes.
if (regex.test(current_url)){
    localStorage.setItem("CurrentTAB",'')
    localStorage.setItem("sales_current_tab",'')    
}

// FROM CRM TO CPQ Landing 
var regex = new RegExp('contractid\=');
var newRevisionQuoteRegex = new RegExp('newRevision\=');
if (regex.test(current_url)){
    let count = 0;
    var cid= (current_url.match(/(\d+)$/))[0]
    var ele= '<abbr id=\"'+cid+'\" title=\"'+cid+'\">'+cid+'</abbr>'
    localStorage.setItem("CurrentTAB", 'Contracts' );
    localStorage.setItem("sales_current_tab", 'Contracts' );
    localStorage.setItem("CRMCONTRACTPAGE", 1);
    cpq.ready(function(){
        TabContainerFullList();
    });
    let interval=setInterval(function(){
        cpq.server.executeScript("CQQUOTEEDT",{'Quoteid':ele,'CurrentTab':'Contracts'}, function(data) {
        if(data){
                cpq.server.executeScript("CQCNTCTEDT",{}, function(result) {
                    count += 1;
                    if(result == 'Quote Loaded'){
                        clearInterval(interval);
                        location.href='\Cart.aspx?TabId=5'
                    }
                    else if(count === 10){ // Contract not present in CPQ, It will load "No Quote Loaded!"
                        clearInterval(interval);
                        location.href='\Cart.aspx?TabId=5'
                    }
                });
            }
        });
    }, 1000);
}
else if (newRevisionQuoteRegex.test(current_url)){
    let count = 0;
    var cid= (current_url.match(/(\d+)/))[0]
    var ele= '<abbr id=\"'+cid+'\" title=\"'+cid+'\">'+cid+'</abbr>'
    localStorage.setItem("CurrentTAB", 'Quotes' );
    localStorage.setItem("sales_current_tab", 'Quotes' );
	
	cpq.server.executeScript("CQQUOTEEDT",{'Quoteid':ele,'CurrentTab':'Quotes'}, function(data) {		
		if(data){
			cpq.server.executeScript("CQREVISION", { 'Opertion': 'NEW_REV','cartrev':'','QuoteId':data}, function (dataset) {				
				let interval=setInterval(function(){
					cpq.server.executeScript("CQCNTCTEDT",{}, function(result) {						
						count += 1;
						if(result == 'Quote Loaded'){
							clearInterval(interval);
							location.href='\Cart.aspx?TabId=5'
						}
						else if(count === 10){ // Sale not present in CPQ, It will load "No Quote Loaded!"
							clearInterval(interval);
							location.href='\Cart.aspx?TabId=5'
						}
					});
				}, 1000);
			});
		}
	});
    
}
else { 
	var regex = new RegExp('QUOTATION\/LOADQUOTE');  // Check Regex pattern Only for Quotes.
	if (regex.test(current_url))
	{
		//const CCP = localStorage.getItem('CRMCONTRACTPAGE'); //CRM to CPQ Landing SET Variable.
		var CurrentTab = $('ul#carttabs_head .active a span').text();
		console.log("API-CART-Updated"+CurrentTab);
		//if(!CCP){  //Direct PAGE
			cpq.ready(function(){
				TabContainerFullList();
			});
		//}else if(CCP == 1){ //BACK TO LIST NAVIGATION
		//	cpq.ready(function(){
		//		TabContainerFullList();
		//	});
		//}
	}
}

/*
var regex = new RegExp('contractid\=');
// FROM CRM TO ACCESS CONTRACT DIRECTLY 
if (regex.test(current_url)){
    let count = 0;
    var cid= (current_url.match(/(\d+)$/))[0]
	var ele= '<abbr id=\"'+cid+'\" title=\"'+cid+'\">'+cid+'</abbr>'
	localStorage.setItem("CurrentTAB", 'Contracts' );
	localStorage.setItem("sales_current_tab", 'Contracts' );
    localStorage.setItem("CRMCONTRACTPAGE", 1);
    let interval=setInterval(function(){
    cpq.server.executeScript("CQQUOTEEDT",{'Quoteid':ele,'CurrentTab':'Contracts'}, function(data) {
        if(data){
		        cpq.server.executeScript("CQCNTCTEDT",{}, function(result) {
                    count += 1;
                    if(result == 'Quote Loaded'){
                        clearInterval(interval);
                        location.href='\Cart.aspx?TabId=5'
                    }
                    else if(count === 10){ // Contract not present in CPQ, It will load "No Quote Loaded!"
                        clearInterval(interval);
                        location.href='\Cart.aspx?TabId=5'
                    }
                });
		    }
        });
    }, 1000);
            
}

var regex = new RegExp('QUOTATION\/LOADQUOTE');  // Check Regex pattern Only for Quotes.
if (regex.test(current_url))
{
	//const CCP = localStorage.getItem('CRMCONTRACTPAGE'); //CRM to CPQ Landing SET Variable.
	var CurrentTab = $('ul#carttabs_head .active a span').text();
	console.log("API-CART-Updated"+CurrentTab);
	//if(!CCP){  //Direct PAGE
		cpq.ready(function(){
			TabContainerFullList();
		});
	//}else if(CCP == 1){ //BACK TO LIST NAVIGATION
	//	cpq.ready(function(){
	//		TabContainerFullList();
	//	});
	//}
}

//$( window ).on( "load", function()  {
    //localStorage.setItem("CurrentTAB","Quotes")
    //localStorage.setItem("sales_current_tab","Quotes")
//});
/*$( window ).on( "load", function()  {
$('#multiple-checkboxes').multiselect({
    includeSelectAllOption: true,
  });
});*/ //It Throws an error.
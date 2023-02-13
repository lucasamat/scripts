function redirect_new123(ele) {
    Record_Id = ele.innerText.trim();
    localStorage.setItem("message_tab", "1");
    localStorage.setItem("msg_record_id", Record_Id);
    Primary_Data = Record_Id.split('-');
        if (Primary_Data[0] == 'SYMSGS') 
        {
            localStorage.setItem("message_tab", "1");
            localStorage.setItem("msg_record_id", Record_Id);
            ids = $(ele).closest('tr').attr('id');
            $('#tab_Messages').trigger('click');
        } 
        else if (Primary_Data[0] == 'SYSEFL') 
        {
            localStorage.setItem("message_tab", "1");
            localStorage.setItem("msg_record_id", Record_Id);
            ids = $(ele).closest('tr').attr('id');
            $('#tab_Questions').trigger('click');
        } 
        else if (Primary_Data[0] == 'SYTABS') 
        {
            localStorage.setItem("message_tab", "1");
            localStorage.setItem("msg_record_id", Record_Id);
            ids = $(ele).closest('tr').attr('id');
            $('#tab_Tabs').trigger('click');
        } 
        else if (Primary_Data[0] == 'SYSECT') 
        {
            localStorage.setItem("message_tab", "1");
            localStorage.setItem("msg_record_id", Record_Id);
            ids = $(ele).closest('tr').attr('id');
            $('#tab_Sections').trigger('click');
        } 
        else if (Primary_Data[0] == 'SYPSAC') 
        {
            localStorage.setItem("message_tab", "1");
            localStorage.setItem("msg_record_id", Record_Id);
            ids = $(ele).closest('tr').attr('id');
            $('#tab_Actions').trigger('click');
        }  
        else if (Primary_Data[0] == 'SYMODL') 
        {
            localStorage.setItem("message_tab", "1");
            localStorage.setItem("msg_record_id", Record_Id);
            ids = $(ele).closest('tr').attr('id');
            $('#tab_Modules').trigger('click');
        } 
        else if (Primary_Data[0] == 'MMVAR') 
        {
            localStorage.setItem("message_tab", "1");
            localStorage.setItem("msg_record_id", Record_Id);
            ids = $(ele).closest('tr').attr('id');
            $('#tab_Variables').trigger('click');
        } 
        else if (Primary_Data[0] == 'SYSCRP') 
        {
            localStorage.setItem("message_tab", "1");
            localStorage.setItem("msg_record_id", Record_Id);
            ids = $(ele).closest('tr').attr('id');
            $('#tab_Scripts').trigger('click');
        } 
        else if (Primary_Data[0] == 'MMOBJ') 
        {
            localStorage.setItem("message_tab", "1");
            localStorage.setItem("msg_record_id", Record_Id);
            ids = $(ele).closest('tr').attr('id');
            $('#tab_Objects').trigger('click');
        }
}
function modules_local(mod_txt) 
{
    localStorage.setItem('avoid_loading', '0');
    localStorage.setItem("modules_local", "1");
    var txt_val = $(mod_txt).attr('name');
    var id_txt_val = $(mod_txt).attr('id');
    var home_appname = $(mod_txt).attr("name");
	localStorage.setItem('appnameee', home_appname);
    var txt_val_val = '';
    if (txt_val.indexOf(' ') > 0) 
    {
        var a = txt_val.split(' ');
        var b = a[0].slice(0, 1);
        var txt_val_remain_01 = a[0].slice(1).toLowerCase();
        var txt_val_remain_0 = b.toUpperCase();
        var c = a[1].slice(0, 1);
        var txt_val_remain_sec_1 = a[1].slice(1).toLowerCase();
        var txt_val_remain_sec_0 = c.toUpperCase();
        txt_val_val = txt_val_remain_0 + txt_val_remain_01 + ' ' + txt_val_remain_sec_0 + txt_val_remain_sec_1;
    } 
    else 
    {
        var txt_val_first = txt_val.slice(0, 1);
        var txt_val_remain = txt_val.slice(1).toLowerCase();
        txt_val_val = txt_val_first + txt_val_remain;
    }
    localStorage.setItem("module_main_txt", txt_val_val);
    localStorage.setItem("module_main_txt_id", id_txt_val);
    var record_txt_id_value = txt_val_val.toUpperCase();
    localStorage.setItem("record_number", record_txt_id_value);
    var loc_mod_txt_123 = localStorage.getItem("module_main_txt");
    var record_number_123 = localStorage.getItem("record_number");
    localStorage.setItem("record_id_number", "");
    localStorage.setItem('hide_details_related_tab', '1');
}

function returnhome() 
{
    location.href = "/Catalogue/CategoryTree.aspx";
    localStorage.setItem('stopRedirect', '1');
};
function sysadminhome() 
{
    location.href = "/Configurator.aspx?pid=271";
};
function CatalogPublishing() 
{
    //location.href = "/QuoteList?tab=3";
  //  location.href = "/Configurator.aspx?pid=775";
    location.href = "/Configurator.aspx?pid=710";
};
function CatalogRedirect() 
{
    location.href = "/Configurator.aspx?pid=772";
}
function wholeModules(mod) {
    setTimeout(function () {
        text1 = ''
        $(document).ready(function () {
            localStorage.setItem("Action_Text", "");
            localStorage.setItem("Action_Text_new", "");
            try
            {
                localStorage.setItem('CURRENTTABFROMCARTPAGE','');
                cpq.server.executeScript("SYLDMDMENU", {'test': 'test'}, function (data) {
                    if (data.toString().startsWith("<html>"))
                    {
                        //$( ".catalog-products" ).append(data.toString());
                        //console.log("html data for GI");
                        text1 = data.toString();
                    }
                    else
                    {
                        if (data == 'Invalid login') 
                        {
                            location.reload();
                        } 
                        else 
                        {
                            text1 = '<div class="col-md-4 mainicon"   onclick="returnhome()" title="HOME"><a class="row mainiconinner"  ><div class="row homeicon"><i class="fa fa-home pad-5" aria-hidden="true"></i> </div> <div class="row hometext" >HOME</div></a></div>'
                            for (i = 0; i < data.length; i++) {
                                product = data[i].split('|')[0]
                                    product_url = data[i].split('|')[1]

                                    if (product == 'MATERIALS') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="MATERIALS" data-target="#pageloader" onclick="location.href=\'' + product_url + '\';" ><div class="row maticon"><a class="row mainiconinner" id="fa fa-cubes" name="' + product + '" onclick="modules_local(this)" ><i class="fa fa-cubes pad-5" aria-hidden="true"></i></a></div> <div class="row icontext mattext"> ' + product + '</div></div>'
                                    } else if (product == 'PRICE MODELS') {

                                        text1 += '<div class="col-md-4 mainicon"  title="PRICE MODELS" data-toggle="modal" data-target="#pageloader" onclick="location.href=\'' + product_url + '\';" ><div class="row priceicon"><a class="row mainiconinner" id="fa fa-money" name="' + product + '" onclick="modules_local(this)" href="' + product_url + '"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/pricebook.svg" class="pricebk confviewicon"/><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/pricebook-hover.svg" class="pricebk_hvr confviewicon" /></a></div> <div class="row icontext pricetext"> PRICE MODELS</div></div>'
                                    } else if (product == 'ORDER MANAGEMENT') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="ORDER MANAGEMENT"  data-target="#pageloader" onclick="location.href=\'' + product_url + '\';" ><div class="row ordericon"><a class="row mainiconinner" id="fa fa-money" name="' + product + '" onclick="modules_local(this)" href="' + product_url + '"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_mng_img_green.svg" class="ord_mng confviewicon" /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/order_mng_img_green_hvr.svg" class="ord_mng_hover confviewicon"/></a></div> <div class="row icontext ordertext">ORDER MANAGEMENT</div></div>'
                                    } else if (product == 'SERVICES') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="SERVICES" data-target="#pageloader" onclick="location.href=\'' + product_url + '\';" ><a class="row mainiconinner"   name="' + product + '" onclick="modules_local(this)" href="' + product_url + '"><div class="row ordericon"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/serviceicon.svg" class="service_mng servivemainwicon confviewicon" /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/serviceicon_hvr.svg" class="service_hover confviewicon"/></div> <div class="row icontext ">SERVICES</div></a></div>'
                                    } else if (product == 'SUBSCRIPTIONS') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="SUBSCRIPTIONS" data-target="#pageloader" onclick="location.href=\'' + product_url + '\';" ><a class="row mainiconinner"   name="' + product + '" onclick="modules_local(this)" href="' + product_url + '"><div class="row ordericon"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/subscription.svg" class="subscrip_mng subscripicon confviewicon" /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/subscription_hvr.svg" class="subscrip_hover confviewicon"/></div> <div class="row icontext ">SUBSCRIPTIONS</div></a></div>'
                                    } else if (product == 'CONTRACT QUOTES') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="CONTRACTS" data-target="#pageloader" onclick="location.href=\'' + product_url + '\';" ><a class="row mainiconinner"   name="' + product + '" onclick="modules_local(this)" href="' + product_url + '"><div class="row ordericon"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/contract_quotes.svg" class="contract_mng contracticon confviewicon" /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/contract_quotes_hvr.svg" class="contract_hover confviewicon"/></div> <div class="row icontext contrqts ">CONTRACT QUOTES</div></a></div>'
                                    } else if (product == 'CATALOGS') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="CATALOGS" data-target="#pageloader"  onclick="CatalogRedirect()" ><a class="row mainiconinner" name="' + product + '" onclick="modules_local(this)"><div class="row catalogicon"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catalog_pub.svg" class="catalogmain confviewicon"  /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/catalog_pub_hvr.svg" class="catalog_hvr confviewicon"  /></div> <div class="row catalogtext" >CATALOGS</div></a></div>'
                                    } else if (product == 'PRICE AGREEMENTS') {

                                        if (product_url.endsWith("id=398")) {
                                            text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="PRICE AGREEMENTS" data-target="#pageloader" onclick="location.href=\'' + product_url + '\';" ><div class="row segicon"><a class="row mainiconinner" id="PRICE_AGREEMENTS" name="' + product + '" onclick="modules_local(this)" href="' + product_url + '"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments_main.svg" class="priceagree_img contracticon confviewicon" /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/segments_main_hvr.svg" class="priceagree_imghvr confviewicon"/></a></div> <div class="row icontext segtext"> ' + product + '</div></div>'
                                        }
                                    } else if (product == 'CONFIGURABLE MATERIALS') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="CONFIGURABLE MATERIALS" data-target="#pageloader" onclick="location.href=\'' + product_url + '\';" ><div class="row conficon"><a class="row mainiconinner" id="fa fa-cogs" name="' + product + '" onclick="modules_local(this)" href="' + product_url + '"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/configuaration.svg" class="configgprd confviewicon"  /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/configuaration-hover.svg" class="configgprd_hvr confviewicon" /></a></div>  <div class="row icontext conftext">' + product + '</div></div>'
                                    } else if (product == 'QUOTAS') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="QUOTAS" data-target="#pageloader" onclick="location.href=\'' + product_url + '\';" ><div class="row commisicon"><a class="row mainiconinner" id="fa fa-cogs" name="' + product + '" onclick="modules_local(this)" href="' + product_url + '"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/TerritoriesAndQuotes.png" class="commismain confviewicon"  /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/territories_quotas_hvr.svg" class="commismain_hvr confviewicon" /></a></div>  <div class="row icontext commisiontext">QUOTAS</div></div>'
                                    } else if (product == 'QUOTAS') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="QUOTAS" data-target="#pageloader" onclick="location.href=\'' + product_url + '\';" ><div class="row commisicon"><a class="row mainiconinner" id="fa fa-cogs" name="' + product + '" onclick="modules_local(this)" href="' + product_url + '"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/TerritoriesAndQuotes.png" class="commismain confviewicon"  /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/territories_quotas_hvr.svg" class="commismain_hvr confviewicon" /></a></div>  <div class="row icontext commisiontext">QUOTAS</div></div>'
                                    }else if (product == 'SYSTEM ADMIN') {

                                        text1 += '<div class="col-md-4 mainicon" onclick="sysadminhome()" title="SYSTEM ADMIN" ><a class="row mainiconinner" onclick="modules_local(this)" name="' + product + '"><div class="row sysadminicon"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sys_admin.svg" class="sysadminmain confviewicon"  /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sys_admin_hover.svg" class="sysadminmain_hvr confviewicon"  /></div> <div class="row icontext" >SYSTEM ADMIN</div></a></div>'
                                    }else if (product == 'APPROVAL CENTER') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="APPROVAL CENTER" data-target="#pageloader"  onclick="CatalogPublishing()" ><a class="row mainiconinner"  name="' + product + ' " onclick="modules_local(this)" href="' + product_url + '"><div class="row approveicon"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Approval_Center.svg" class="approvemain confviewicon"  /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/Approval_Center_hvr.svg" class="approve_hvr confviewicon"  /></div> <div class="row icontext" >APPROVAL CENTER</div></a></div>'
                                    }
                                    else if (product == 'SYSTEM ADMIN ADV') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="SYSTEM ADMIN ADV" data-target="#pageloader" ><a class="row mainiconinner" href="' + product_url + '"  name="' + product + '" onclick="modules_local(this)" ><div class="row approveicon"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sys_admin_adv.svg" class="sysadminadvmain confviewicon"  /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/sys_admin_advhvr.svg" class="sysadminadv_hvr confviewicon"  /></div> <div class="row icontext" >SYSTEM ADMIN ADV</div></a></div>'
                                    }
                                    else if (product == 'SALES') {

                                        text1 += '<div class="col-md-4 mainicon" data-toggle="modal" title="SALES" data-target="#pageloader"   ><a class="row mainiconinner"  name="' + product + '" href="' + product_url + '" onclick="modules_local(this)" ><div class="row approveicon"><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/salesorg.svg" class="salesmain confviewicon"  /><img src="/mt/APPLIEDMATERIALS_PRD/Additionalfiles/salesorg_hvr.svg" class="sales_hvr confviewicon"  /></div> <div class="row icontext" >SALES</div></a></div>'
                                    } else {
                                        
                                        text1 += '<div class="col-md-4 mainicon" title="' + product + '" data-toggle="modal" data-target="#pageloader" onclick="location.href=\'' + product_url + '\';" ><div class="row"><a class="row mainiconinner exticon" id="fa fa-tasks" name="' + product + '" onclick="modules_local(this)" href="' + product_url + '"><i class="fa fa-star pad-5"></i></a></div> <div class="row icontext exttext">' + product + '</div></div>'
                                    }
                            }
                        }  
                    }
                    document.getElementById('ul_bind').innerHTML = text1;
            });
            }
            catch (e)
            {
                console.log(e);
            }
        });

        var a = $(mod).parent().attr('class');
        if (a == 'open') {
            $('.tabsfiled').css('z-index', '2');
            $('.material_btn_bg').css('z-index', '2');
        } else {
            $('.tabsfiled').css('z-index', '2');
            $('.material_btn_bg').css('z-index', '2');
        }
    }, 50);
}

function cartTabsClick(currentTab) {

    var a = $(currentTab).attr('id');
    var b = '#' + a + ' li';
    setTimeout(function () {
        $(b).each(function (index) {
            var z = $(this).attr('class');
            if (z == 'dropdown pull-right tabdrop open' || z == 'dropdown pull-right tabdrop active open') {
                $('.material_btn_bg').css('z-index', '2');
            } else if (z == 'dropdown pull-right tabdrop') {
                $('.material_btn_bg').css('z-index', '9');
            } else {}

        });
    }, 20);

}

$(document).ready(function () {
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });
    var activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
        $('#myTab a[href="' + activeTab + '"]').tab('show');
    }
});

var path = $(location).attr('href');
var quote = path.split("?")[1];

if (quote == "tab=2") {


    setTimeout(function () {

        $("#SYTABS-CA-00001").removeClass("active");
        $("#SYTABS-CA-00005").addClass("active");
    }, 2000);
}

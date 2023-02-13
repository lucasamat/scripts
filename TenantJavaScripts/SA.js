var CurrentNodeId = TreeParam = TreeParentParam = TreeParentNodeId = TreeParentNodeRecId = TreeSuperParentParam = TreeSuperParentId = TreeSuperParentRecId = TreeTopSuperParentParam = TreeTopSuperParentId = TreeTopSuperParentRecId = add_new_load = ActiveTab = CurrentId = node = RecName = data = button_name = data1 = ParentTreeTopSuperParentParam = ParentTreeTopSuperParentId = ParentTreeTopSuperParentRecId = '';

function Profile_Tabs(profileTabs)
	{
		
		
		$('.Detail, .Related').removeClass('disp_blk');
		$('.Detail, .Related').addClass('disp_none');

		[CurrentRecordId,RecName] = ['SYOBJR-93159','div_CTR_Tab_Field_Settings'];
		loadRelatedList(CurrentRecordId,RecName);
		
		$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
		$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
		$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
		
		$('#content_banner').removeClass('disp_blk');
		$('#content_banner').addClass('disp_none');
		var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
		
		$('.SYSECT-SY-00001, .SYSECT-SY-00009').removeClass('disp_blk');
		$('.SYSECT-SY-00001, .SYSECT-SY-00009').addClass('disp_none');
	} 
	
function Profile_Sections(profileSections){
	
		$('.Detail, .Related').removeClass('disp_blk');
		$('.Detail, .Related').addClass('disp_none');
		
		var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
		[CurrentRecordId,RecName] = ['SYOBJR-93160','div_CTR_Sec_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
						
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
						
						$('#content_banner').removeClass('disp_blk');
						$('#content_banner').addClass('disp_none');
	
}
	
	
function Profile_Qst(profileQuestions){
	
	
		$('.Detail, .Related').removeClass('disp_blk');
		$('.Detail, .Related').addClass('disp_none');
		var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
		[CurrentRecordId,RecName] = ['SYOBJR-93162','div_CTR_Qst_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
						
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
						
						$('#content_banner').removeClass('disp_blk');
						$('#content_banner').addClass('disp_none');
}
	
function Profile_Details(progdetail)
	{
		
		
		$('.Related').removeClass('disp_blk');
		$('.Related').addClass('disp_none');

		$('.Detail, #sysprofiledetail').removeClass('disp_none');
		$('.Detail, #sysprofiledetail').addClass('disp_blk');
		
		$('div#sysprofiledetail').find("li").removeClass('disp_blk');
		$('div#sysprofiledetail').find("li").addClass('disp_none');

		$('div#sysprofiledetail').find("li").removeClass('active');
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");
		
		$('div#sysprofiledetail').find("li:nth-child(1)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(1)").addClass('disp_blk');
		
		$('div#sysprofiledetail').find("li:nth-child(2)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(2)").addClass('disp_blk');
	
		
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");
		ProfileTreeParentParam  = localStorage.getItem('ProfileTreeParentParam')
		
		if (ProfileTreeParentParam== 'Tabs')
		{
			Pro_ID = $("input#PROFILE_TAB_RECORD_ID").val();
			
			$('div#sysprofiledetail').find("li:nth-child(4)").removeClass('disp_none');
			$('div#sysprofiledetail').find("li:nth-child(4)").addClass('disp_blk');
		}
		else if (ProfileTreeParentParam== 'Sections')
	{
			$("input#PROFILE_SECTION_RECORD_ID").val();
			
			$('div#sysprofiledetail').find("li:nth-child(6)").removeClass('disp_none');
			$('div#sysprofiledetail').find("li:nth-child(6)").addClass('disp_blk');
		}
		else
		{
			Pro_ID = $("input#PROFILE_APP_RECORD_ID").val();
				
				$('div#sysprofiledetail').find("li:nth-child(3)").removeClass('disp_none');
				$('div#sysprofiledetail').find("li:nth-child(3)").addClass('disp_blk');
		}
		
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':Pro_ID, 'TableId':TreeParentNodeRecId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) 
			{
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			
			$('.SYSECT-SY-00015, #sub_child_content_banner, #sub_content_banner','#content_banner').removeClass('disp_blk');
			$('.SYSECT-SY-00015, #sub_child_content_banner, #sub_content_banner','#content_banner').addClass('disp_none');
			$(".Profile_Related_Detail").addClass("tree_second_child");
			
				
				$('.SYSECT-SY-00015').removeClass('disp_blk');
				$('.SYSECT-SY-00015').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
	}

function ProfilesLeftTreeView(ele) 
{
	
	try
	{	
		button_name = $("input#PROFILE_RECORD_ID").val();
		if(button_name === "")
		{	
			$(this).treeview('unselectNode', [node.nodeId, { silent: false }]);
			$('#profile_SavePopup').modal('show');
			$('#Profilestreeview').treeview('selectNode', [0, { silent: true }]);
		}
		var table_id = $(ele).closest('table').attr('id');
		currentRecordId = $(ele).closest('tr').children('td:nth-child(3)').text().trim();
		var ids = $(ele).closest('tr').attr('id');	
		var stsrecid = $("#" + ids + " td:nth-child(3)").text().trim();
		var Primary_Data = localStorage.getItem('id_primarydata') || $("#" + ids + " td:nth-child(3)").text().trim();
		//A043S001P01-9518 Start
		var Profile_Name = localStorage.getItem('Profile_Name')
		cpq.server.executeScript("SYPRFLOPTN", {'LOAD':'Treeload','Primary_Data':Primary_Data,'Profile_Name':Profile_Name}, function (dataset) {
			//A043S001P01-9518 End
			var [data,data1] = [dataset[0],dataset[1]];
			localStorage.setItem('profileTreedatasetnew',data1);
			$('#Profilestreeview').treeview({
				data: data,
				levels: 1,
				onNodeSelected: function (event, node) {
					CurrentNodeId = node.nodeId;
					localStorage.setItem("CurrentNodeId", CurrentNodeId);
					$(this).treeview('unselectNode', [node.nodeId, { silent: false }]);
					TreeParam = node.text;
					$('#Profilestreeview').treeview('selectNode', [ parseInt(CurrentNodeId), { silent: true }]);
					if (CurrentNodeId != '' && CurrentNodeId != null ) {
						TreeParentParam = $('#Profilestreeview').treeview('getParent', CurrentNodeId).text;
						TreeParentNodeId = $('#Profilestreeview').treeview('getParent', CurrentNodeId).nodeId;
						TreeParentNodeRecId = $('#Profilestreeview').treeview('getParent', CurrentNodeId).id;
					}
					if (TreeParentNodeId != '' && TreeParentNodeId != null ) {
						TreeSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).text;
						TreeSuperParentId = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).nodeId;
						TreeSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).id;
					}
					if (TreeSuperParentId != '' && TreeSuperParentId != null ) {
						TreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).text;
						TreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).nodeId;
						TreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).id;
					}
					
					var GrandTreeTopSuperParentParam = GrandTreeTopSuperParentId = GrandTreeTopSuperParentRecId = Grand_GrandTreeTopSuperParentParam = Grand_GrandTreeTopSuperParentId = Grand_GrandTreeTopSuperParentRecId = Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_GrandTreeTopSuperParentId = Grand_Grand_GrandTreeTopSuperParentRecId = Grand_Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_GrandTreeTopSuperParentId = Grand_Grand_Grand_GrandTreeTopSuperParentRecId = Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_Grand_GrandTreeTopSuperParentId = Grand_Grand_Grand_Grand_GrandTreeTopSuperParentRecId ='';

					if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null ) {
						GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).text;
						GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
						GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).id;
					}
					if (GrandTreeTopSuperParentId != '' && GrandTreeTopSuperParentId != null ) {
						Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).text;
						Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).nodeId;
						Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).id;
					}
					if (Grand_GrandTreeTopSuperParentId != '' && Grand_GrandTreeTopSuperParentId != null ) {
						Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).id;
					}
					if (Grand_Grand_GrandTreeTopSuperParentId != '' && Grand_Grand_GrandTreeTopSuperParentId != null ) 
					{
						Grand_Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).id;
					}
					if (Grand_Grand_Grand_GrandTreeTopSuperParentId != '' && Grand_Grand_Grand_GrandTreeTopSuperParentId != null ) 
					{
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).id;
					}
					
					
					if (TreeSuperParentId === undefined){
						TreeSuperParentParam = ''
					}
					if (TreeTopSuperParentId === undefined){
						TreeTopSuperParentParam = ''
					}
					if(TreeParam == "Profile Information")
                    {
                    	
                    	TreeParentParam = TreeSuperParentParam = TreeTopSuperParentParam = GrandTreeTopSuperParentParam = Grand_GrandTreeTopSuperParentParam = Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_GrandTreeTopSuperParentParam = "";
                    }

					localStorage.setItem('ProfileTreeParam', TreeParam);
					localStorage.setItem('ProfileTreeParentParam', TreeParentParam);
					localStorage.setItem('ProfileNodeTreeSuperParentParam', TreeSuperParentParam);
					localStorage.setItem('ProfileTopSuperParentParam', TreeTopSuperParentParam);
					localStorage.setItem('ProfileParentNodeRecId','');
					localStorage.setItem('ProfileParentNodeRecId', TreeParentNodeRecId);
					localStorage.setItem('ProfileTreeSuperParentRecId', TreeSuperParentRecId);
					localStorage.setItem('ProfileTopSuperParentRecId', TreeTopSuperParentRecId);
					
					localStorage.setItem('ProfileGrandTreeTopSuperParentParam', GrandTreeTopSuperParentParam);
					localStorage.setItem('ProfileGrand_GrandTreeTopSuperParentParam', Grand_GrandTreeTopSuperParentParam);
					localStorage.setItem('ProfileGrand_Grand_GrandTreeTopSuperParentParam', Grand_Grand_GrandTreeTopSuperParentParam);
					localStorage.setItem('ProfileGrand_Grand_Grand_GrandTreeTopSuperParentParam', Grand_Grand_Grand_GrandTreeTopSuperParentParam);

					setTimeout(function () {
 
						var unique_breadcrumb_list = [Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam,Grand_Grand_Grand_GrandTreeTopSuperParentParam,Grand_Grand_GrandTreeTopSuperParentParam,Grand_GrandTreeTopSuperParentParam,GrandTreeTopSuperParentParam,TreeTopSuperParentParam,TreeSuperParentParam,TreeParentParam,TreeParam];
						
						unique_breadcrumb_list = unique_breadcrumb_list.reverse();
                        
						var z = 0;
						var y;
						$(unique_breadcrumb_list).each(function(index){
							var a = unique_breadcrumb_list[index];
							if(a == '' || a.toString().indexOf('function(e)') != -1)
							{
								if(z == 0)
								{
									y = index;
									z +=1;
								}
							}
						});
                        unique_breadcrumb_list = unique_breadcrumb_list.splice(0,y);
                        unique_breadcrumb_list = unique_breadcrumb_list.reverse();
						var unique_breadcrumb_list_filtered = unique_breadcrumb_list.filter(function (el) {
							return el != '' || el.indexOf('function(e)') != -1 || el.indexOf('ƒ (e)') != -1 || el.indexOf('ƒ') != -1;
						});

						var build_breadcrumb = '<ul class="breadcrumb">'
							$(unique_breadcrumb_list_filtered).each(function (index) {
								
								build_breadcrumb += '<li><a onclick="profile_breadCrumb_redirection(this)"><abbr title="'+unique_breadcrumb_list_filtered[index]+'">'+unique_breadcrumb_list_filtered[index]+'</abbr></a><span class="angle_symbol"><img src = "/mt/APPLIEDMATERIALS_PRD/images/productimages/BREADCRUMB_ICON_TRANS.PNG"/></span></li>';
							});
						build_breadcrumb += '</ul>';
						
						if(TreeParam)
						{
							$('div#header_label').html(build_breadcrumb);
						}

						$('ul.breadcrumb > li > a').each(function (index) {

							var a = $(this).text();

							if (a.indexOf('function(e)') != -1) { 
								$(this).parent('li').remove();
							}
						});
						
						
						var header_label_parent_height = breadcrumb_height = header_label_parent_height_split = header_label_convert_to_int = breadcrumb_height_split = breadcrumb_height_convert_to_int = header_label_parent_width = header_label_parent_width_split = header_label_width_convert_to_int = breadcrumb_content_length = set_width_for_breadcrumb = set_width_for_breadcrumb_px = set_width_for_breadcrumb_level2 = set_width_for_breadcrumb_level2_last = breadcrumb_width_split = breadcrumb_width_convert_to_int = '';
						
						header_label_parent_height = $('div#header_label').parent().css('height');
						breadcrumb_height = $('div#header_label ul.breadcrumb').css('height');
						if(header_label_parent_height)
						{
							header_label_parent_height_split = header_label_parent_height.split('px');
							header_label_convert_to_int = parseInt(header_label_parent_height_split[0]);
						}
						if(breadcrumb_height)
						{
							breadcrumb_height_split = breadcrumb_height.split('px');
							breadcrumb_height_convert_to_int = parseInt(breadcrumb_height_split[0]);
						}
						
						header_label_parent_width = $('div#header_label').parent().css('width');
						if(header_label_parent_width)
						{
							header_label_parent_width_split = header_label_parent_width.split('px');
							header_label_width_convert_to_int = parseInt(header_label_parent_width_split[0]) - 70;
						}
						var breadcrumb_width = $('div#header_label ul.breadcrumb').css('width');
						if(breadcrumb_width)
						{
                            breadcrumb_width_split = breadcrumb_width.split('px'); 
                            breadcrumb_width_convert_to_int = parseInt(breadcrumb_width_split[0]);
						}
						breadcrumb_content_length = unique_breadcrumb_list_filtered.length;
						set_width_for_breadcrumb = parseInt(header_label_parent_width_split[0] / breadcrumb_content_length);
						set_width_for_breadcrumb_px = set_width_for_breadcrumb + 'px';							
						set_width_for_breadcrumb_level2 = set_width_for_breadcrumb - 20;
						set_width_for_breadcrumb_level2 = set_width_for_breadcrumb_level2 + 'px';
						//set_width_for_breadcrumb_level2_last = set_width_for_breadcrumb - 70;
						//set_width_for_breadcrumb_level2_last = set_width_for_breadcrumb_level2_last + 'px';
						
						if((header_label_convert_to_int < breadcrumb_height_convert_to_int) || (breadcrumb_width_convert_to_int > header_label_width_convert_to_int))
						{
							$('div#header_label ul.breadcrumb li').css('width', set_width_for_breadcrumb_px);
							
							$('div#header_label').children('ul.breadcrumb').find('a').css('width',set_width_for_breadcrumb_level2);
							
						}

					}, 1300);
	
					try
					{
						
						cpq.server.executeScript("SYPRFLOPTN", { 'LOAD':'GlobalSet', 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam ,'GrandTreeTopSuperParentParam':GrandTreeTopSuperParentParam,'Grand_GrandTreeTopSuperParentParam':Grand_GrandTreeTopSuperParentParam,'Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_GrandTreeTopSuperParentParam}, function (dataset) {
							Profiles_enable_disable('Profilestreeview');
						});
					}
					catch(e){
						console.log(e);
					}
				},
				onNodeUnselected: function (event, node) {
					$(this).treeview('selectNode', [node.nodeId, { silent: true }]);
				}
			});
			try
			{
				[add_new_load,CurrentNodeId] = [localStorage.getItem("add_new_load"),localStorage.getItem("CurrentNodeId")];
				if (CurrentNodeId != '' && CurrentNodeId != null && CurrentNodeId != "undefined") {
					CurrentId = CurrentNodeId;
				}
				else {
					CurrentId = 0;
					localStorage.setItem('CurrentNodeId', 0);
				}
				if(add_new_load != 'true')
				{
					$('#Profilestreeview').treeview('selectNode', [parseInt(CurrentId), { silent: true }]);
				}
				Profiles_enable_disable('Profilestreeview');
				ActiveTab = $('ul#carttabs_head li.active a span').text();
				document.getElementById("header_label_left").innerHTML= ActiveTab.toUpperCase() +' EXPLORER';
				//document.getElementById("header_label").innerHTML= ActiveTab.toUpperCase() +' INFORMATION';
				
			}
			catch(e){
				console.log(e)
			}
		});
	}
	catch(e){
		console.log(e);
	}
}

function ErrLogLeftTreeView(ele) {
	try
	{
		var ids = $(ele).closest('tr').attr('id');	
		var Primary_Data = localStorage.getItem('Error_log_id_primarydata') || $("#" + ids + " td:nth-child(3)").text().trim();	
		cpq.server.executeScript("SYERLOOPTN", {'LOAD':'Treeload','Primary_Data':Primary_Data}, function (dataset) {
			var [data,data1] = [dataset[0],dataset[1]];
			localStorage.setItem('errorLogTreedatasetnew',data1);
			$('#ErrorLogstreeview').treeview({
				data: data,
				levels: 1,
				onNodeSelected: function (event, node) {
					CurrentNodeId = node.nodeId;
					localStorage.setItem("CurrentNodeId", CurrentNodeId);
					$(this).treeview('unselectNode', [node.nodeId, { silent: false }]);
					TreeParam = node.text;
					$('#ErrorLogstreeview').treeview('selectNode', [ parseInt(CurrentNodeId), { silent: true }]);
					if (CurrentNodeId != '' && CurrentNodeId != null ) {
						TreeParentParam = $('#ErrorLogstreeview').treeview('getParent', CurrentNodeId).text;
						TreeParentNodeId = $('#ErrorLogstreeview').treeview('getParent', CurrentNodeId).nodeId;
						TreeParentNodeRecId = $('#ErrorLogstreeview').treeview('getParent', CurrentNodeId).id;
					}
					if (TreeParentNodeId != '' && TreeParentNodeId != null ) {
						TreeSuperParentParam = $('#ErrorLogstreeview').treeview('getParent', TreeParentNodeId).text;
						TreeSuperParentId = $('#ErrorLogstreeview').treeview('getParent', TreeParentNodeId).nodeId;
						TreeSuperParentRecId = $('#ErrorLogstreeview').treeview('getParent', TreeParentNodeId).id;
					}
					if (TreeSuperParentId != '' && TreeSuperParentId != null ) {
						TreeTopSuperParentParam = $('#ErrorLogstreeview').treeview('getParent', TreeSuperParentId).text;
						TreeTopSuperParentId = $('#ErrorLogstreeview').treeview('getParent', TreeSuperParentId).nodeId;
						TreeTopSuperParentRecId = $('#ErrorLogstreeview').treeview('getParent', TreeSuperParentId).id;
					}
					if (TreeSuperParentId === undefined){
						TreeSuperParentParam = ''
					}
					if (TreeTopSuperParentId === undefined){
						TreeTopSuperParentParam = ''
					}
					var button_name = $("input#PROFILE_RECORD_ID").val();
					if(button_name === "")
					{
						$(this).treeview('unselectNode', [node.nodeId, { silent: false }]);
						$('#profile_SavePopup').modal('show');
						$('#ErrorLogstreeview').treeview('selectNode', [0, { silent: true }]);
					}
					localStorage.setItem('ErrorLogTreeParam', TreeParam);
					localStorage.setItem('ErrorLogTreeParentParam', TreeParentParam);
					localStorage.setItem('ErrorLogNodeTreeSuperParentParam', TreeSuperParentParam);
					localStorage.setItem('ErrorLogTopSuperParentParam', TreeTopSuperParentParam);
					localStorage.setItem('ErrorLogParentNodeRecId','');
					localStorage.setItem('ErrorLogParentNodeRecId', TreeParentNodeRecId);
					localStorage.setItem('ErrorLogTreeSuperParentRecId', TreeSuperParentRecId);
					localStorage.setItem('ErrorLogTopSuperParentRecId', TreeTopSuperParentRecId);
					try
					{
						cpq.server.executeScript("SYERLOOPTN", { 'LOAD':'GlobalSet', 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam }, function (dataset) {
							ErrorLogs_enable_disable('ErrorLogstreeview');
						});
					}
					catch(e){
						console.log(e);
					}
				},
				onNodeUnselected: function (event, node) {
					$(this).treeview('selectNode', [node.nodeId, { silent: true }]);
				}
			});
			try{
				[add_new_load,CurrentNodeId] = [localStorage.getItem("add_new_load"),localStorage.getItem("CurrentNodeId")];
				if (CurrentNodeId != '' && CurrentNodeId != null && CurrentNodeId != "undefined") {
					CurrentId = CurrentNodeId;
				} else {
					CurrentId = 0;
					localStorage.setItem('CurrentNodeId', 0);
				}
				if(add_new_load != 'true')
				{
					$('#ErrorLogstreeview').treeview('selectNode', [parseInt(CurrentId), { silent: true }]);
				}
				ErrorLogs_enable_disable('ErrorLogstreeview');
				ActiveTab = $('ul#carttabs_head li.active a span').text();
				document.getElementById("header_label_left").innerHTML= ActiveTab.toUpperCase() +' EXPLORER';
				//document.getElementById("header_label").innerHTML= ActiveTab.toUpperCase() +' INFORMATION';
			}
			catch(e)
			{
				console.log(e);
			}
		});
	}
	catch(e)
	{
		console.log(e);
	}
}

function RolesLeftTreeView(ele) {
	try
	{	
		var Role_ID = localStorage.getItem("RoleId");	
		localStorage.setItem('Role_ACTION','VIEW')
		cpq.server.executeScript("SYUROLESTN", {'LOAD':'RoleTreeload','Role_id':Role_ID}, function (dataset) {
			var [data,data1] = [dataset[0],dataset[1]];
			localStorage.setItem('syrolesnew',data1);
			$('#Rolestreeview').treeview({
				data: data,
				levels: 1,
				onNodeSelected: function (event, node) {
					CurrentNodeId = node.nodeId;
					localStorage.setItem("CurrentNodeId", CurrentNodeId);
					$(this).treeview('unselectNode', [node.nodeId, { silent: false }]);
					TreeParam = node.text;
					$('#Rolestreeview').treeview('selectNode', [ parseInt(CurrentNodeId), { silent: true }]);
					if (CurrentNodeId != '' && CurrentNodeId != null ) {
						TreeParentParam = $('#Rolestreeview').treeview('getParent', CurrentNodeId).text;
						TreeParentNodeId = $('#Rolestreeview').treeview('getParent', CurrentNodeId).nodeId;
						TreeParentNodeRecId = $('#Rolestreeview').treeview('getParent', CurrentNodeId).id;
					}
					if (TreeParentNodeId != '' && TreeParentNodeId != null ) {
						TreeSuperParentParam = $('#Rolestreeview').treeview('getParent', TreeParentNodeId).text;
						TreeSuperParentId = $('#Rolestreeview').treeview('getParent', TreeParentNodeId).nodeId;
						TreeSuperParentRecId = $('#Rolestreeview').treeview('getParent', TreeParentNodeId).id;
					}
					if (TreeSuperParentId != '' && TreeSuperParentId != null ) {
						TreeTopSuperParentParam = $('#Rolestreeview').treeview('getParent', TreeSuperParentId).text;
						TreeTopSuperParentId = $('#Rolestreeview').treeview('getParent', TreeSuperParentId).nodeId;
						TreeTopSuperParentRecId = $('#Rolestreeview').treeview('getParent', TreeSuperParentId).id;
					}
					if (TreeSuperParentId === undefined){
						TreeSuperParentParam = ''
					}
					if (TreeTopSuperParentId === undefined){
						TreeTopSuperParentParam = ''
					}
					var button_name = $("input#PROFILE_RECORD_ID").val();
					if(button_name === "")
					{
						$(this).treeview('unselectNode', [node.nodeId, { silent: false }]);
						$('#profile_SavePopup').modal('show');
						$('#Rolestreeview').treeview('selectNode', [0, { silent: true }]);
					}
					localStorage.setItem('RolesTreeParam', TreeParam);
					localStorage.setItem('RolesParentParam', TreeParentParam);
					localStorage.setItem('RolesTreeSuperParentParam', TreeSuperParentParam);
					localStorage.setItem('RolesTopSuperParentParam', TreeTopSuperParentParam);
					localStorage.setItem('RolesParentNodeRecId','');
					localStorage.setItem('RolesParentNodeRecId', TreeParentNodeRecId);
					localStorage.setItem('RolesTreeSuperParentRecId', TreeSuperParentRecId);
					localStorage.setItem('RolesTopSuperParentRecId', TreeTopSuperParentRecId);
					try
					{
						cpq.server.executeScript("SYROLEACTN", { 'LOAD':'GlobalSet', 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TreeTopSuperParentParam': TreeTopSuperParentParam }, function (dataset) {
							Roles_enable_disable('Rolestreeview');
						});
					}
					catch(e){
						console.log(e);
					}
				},
				onNodeUnselected: function (event, node) {
					$(this).treeview('selectNode', [node.nodeId, { silent: true }]);
				}
			});
			try{
				[add_new_load,CurrentNodeId] = [localStorage.getItem("add_new_load"),localStorage.getItem("CurrentNodeId")];
				if (CurrentNodeId != '' && CurrentNodeId != null && CurrentNodeId != "undefined") {
					CurrentId = CurrentNodeId;
				} else {
					CurrentId = 0;
					localStorage.setItem('CurrentNodeId', 0);
				}
				if(add_new_load != 'true')
				{
					$('#Rolestreeview').treeview('selectNode', [parseInt(CurrentId), { silent: true }]);
				}
				Roles_enable_disable('Rolestreeview');
				//ActiveTab = $('ul#carttabs_head li.active a span').text();
				//document.getElementById("header_label_left").innerHTML= ActiveTab.toUpperCase() +' EXPLORER';
				//document.getElementById("header_label").innerHTML= ActiveTab.toUpperCase() +' INFORMATION';
			}
			catch(e)
			{
				console.log(e);
			}
		});
	}
	catch(e)
	{
		console.log(e);
	}
}
function Roles_opencreate(ele)
{	
	var table_id = $(ele).closest('table').attr('id');
	localStorage.setItem("Role_EDITACTION", "GRID_EDIT");
	localStorage.setItem('Role_ACTION',"EDIT");
	localStorage.setItem("REFRESH","TRUE");
	var ids = $(ele).closest('tr').attr('id');
	var Role_Record_ID = $(ele).closest('tr').children('td:nth-child(3)').text().trim();
	
	var Role_ID = $(ele).closest('tr').children('td:nth-child(4)').text().trim();
	
	var Role_Name = $(ele).closest('tr').children('td:nth-child(5)').text().trim();
	try 
	{		  
		cpq.server.executeScript("SYPRCTEDIT", {
			'RECORD_ID': Role_Record_ID,
			'TabNAME': 'Role',
			'MODE': 'EDIT',
			'LOAD':'TreeLoad'
		}, function(dataset) {
					
			$('#BTN_MA_ALL_REFRESH').click();
			var datas = dataset;
			$('div#Rolestreeview ul.list-group li.list-group-item').trigger('click');
			setTimeout(function(){
					if (document.getElementById("righttreeview"))
					{
						document.getElementById("righttreeview").innerHTML = datas;
					}		
			}, 8000);
		  });
	} 
	catch(e){
		console.log(e);
	}
}
function Profileopencreate(ele)
{
	
	var table_id = $(ele).closest('table').attr('id');
	localStorage.setItem("Profile_EDITACTION", "GRID_EDIT");
	localStorage.setItem('Profile_ACTION',"EDIT");
	localStorage.setItem("REFRESH","TRUE");
	var ids = $(ele).closest('tr').attr('id');
	var Profile_Record_ID = $(ele).closest('tr').children('td:nth-child(3)').text().trim();
	
	var Profile_ID = $(ele).closest('tr').children('td:nth-child(4)').text().trim();
	
	var Profile_Name = $(ele).closest('tr').children('td:nth-child(5)').text().trim();
	
	var Primary_Data = $("#" + ids + " td:nth-child(3)").text().trim();
	localStorage.setItem("id_primarydata", Primary_Data);
	// BANNER_CONTENT VALUES STARTS
	localStorage.setItem("PROFILE_BANNER",Profile_Record_ID +','+ Profile_ID +','+ Profile_Name);
	// BANNER_CONTENT VALUES ENDS
	var [Primary_Data_list,Primary_Data_list_val,Profile_ID,Profile_Name] = [Primary_Data.replace(/\s+/, " ").split(' '),'',$("#" + ids + " td:nth-child(4)").text().trim(),$("#" + ids + " td:nth-child(5)").text().trim()];
	if (Primary_Data_list.length > 1) 
	{
		Primary_Data_list_val = Primary_Data_list[0];
	}
		
	
	try 
	{		  
		cpq.server.executeScript("SYPRCTEDIT", {
			'RECORD_ID': Profile_Record_ID,
			'TabNAME': 'Profile',
			'MODE': 'EDIT',
			'LOAD':'Treeload'
		}, function(dataset) {
					
			$('#BTN_MA_ALL_REFRESH').click();
			$("#PROFILE_BANNER_RECORD_ID abbr").text(Profile_ID);
					$("#PROFILE_BANNER_RECORD_ID abbr").attr('title',Profile_ID);
					
					
					$("#PROFILE_BANNER_ID abbr").text(Profile_Record_ID);
					$("#PROFILE_BANNER_ID abbr").attr('title',Profile_Record_ID);

				
					$("#PROFILE_BANNER_NAME abbr").text(Profile_Name);
					$("#PROFILE_BANNER_NAME abbr").attr('title',Profile_Name);
			var datas = dataset;
			$('div#Profilestreeview ul.list-group li.list-group-item').trigger('click');
			setTimeout(function(){
					if (document.getElementById("Profile_Detail"))
					{
						document.getElementById("Profile_Detail").innerHTML = datas;
					}
			//A043S001P01-9205 start		
			}, 8000);
			//A043S001P01-9205 end
		  });
	} 
	catch(e){
		console.log(e);
	}
}
cpq.events.sub("API:configurator:updated", function(data){		
	var [Profile_ACTION,Profile_edit,profile_grid_edit] = [localStorage.getItem('Profile_ACTION'),localStorage.getItem("Profile_EDITACTION"),localStorage.getItem('profileGridEdit')];
	if (Profile_edit == 'EDIT')
	{
		if(profile_grid_edit == '1')
		{
			setTimeout(function() {			
				Profile_EDIT('SYSECT-SY-00001');
			}, 2000);
		}
	}
});
//A043S001P01-9114 start
function proflietabValidate(ele){
	
	var visvalue = $('input#VISIBLE').prop("checked");
	
	if (!visvalue)
	{
		
		$('#alert_msg div label').text('ERROR:In order to grant access to this app, the user is required to have access to at least one tab. Please assign permissions to one tab within this app before saving');
		
		$('#alert_msg').removeClass('disp_none');
		$('#alert_msg').addClass('disp_blk');
		$('#prf_save_sec').attr('disabled', 'disabled');
	}
	else{
		
		$('#prf_save_sec').removeAttr('disabled');
		
		$('#alert_msg').removeClass('disp_blk');
		$('#alert_msg').addClass('disp_none');
	}

}
//A043S001P01-9114 End


//A043S001P01-9162 start
function proflieSecValidate(ele)
{
	
	var visvalue = $('input#VISIBLE').prop("checked");
	
	if (!visvalue)
	{
		
		$('#alert_msg div label').text('ERROR:In order to grant access to this Tab, the user is required to have access to at least one Section. Please assign permissions to one tab within this section before saving');
		
		$('#alert_msg').removeClass('disp_none');
		$('#alert_msg').addClass('disp_blk');
		$('#prf_save_sec').attr('disabled', 'disabled');
	}
	else{
		
		$('#prf_save_sec').removeAttr('disabled');
		
		$('#alert_msg').removeClass('disp_blk');
		$('#alert_msg').addClass('disp_none');
	}

}
//A043S001P01-9162 end

//A043S001P01-9163 Start
function proflieQstValidate(ele)
{
	
	var visvalue = $('input#VISIBLE').prop("checked");
	
	if (!visvalue)
	{
		
		$('#alert_msg div label').text('ERROR:In order to grant access to this Section, the user is required to have access to at least one question. Please assign permissions to one question within this section before saving');
		
		$('#alert_msg').removeClass('disp_none');
		$('#alert_msg').addClass('disp_blk');
		$('#prf_save_sec').attr('disabled', 'disabled');
	}
	else{
		
		$('#prf_save_sec').removeAttr('disabled');
		
		$('#alert_msg').removeClass('disp_blk');
		$('#alert_msg').addClass('disp_none');
	}

}
//A043S001P01-9163 end


//A043S001P01-9092,9114 start	
function ProfiletreeSAVE(){
	var [RecordId,dict_new,id_val] = [$("table tbody tr td input").val(),{},''];
		//A043S001P01-9077 start
				
				$('.SYSECT-SY-00024').removeClass('disp_blk');
				$('.SYSECT-SY-00024').addClass('disp_none');
				//A043S001P01-9077 end
	$("#Profile_Detail #container table tbody tr td select").each(function () {
		dict_new[$(this).attr('id')] = $(this).children(":selected").val();
	});
	$("#Profile_Detail #container table tbody tr td input").each(function () {
		if ($(this).attr('type') == 'CHECKBOX') {
			dict_new[$(this).attr('id')] = String($(this).prop("checked"));
		} else {
			id_val = $(this).attr('id');
			dict_new[$(this).attr('id')] = $('#Profile_Detail #container table tbody tr td input#'+id_val).val();
		} 
	});
	dict_new['RECORDID'] =  RecordId ;
	var appid = dict_new['APP_ID'];
	
	var VISIBLESA = dict_new['VISIBLE'];
	
	var [visval,visdef] = [dict_new['VISIBLE'],dict_new['DEFAULT']];
	var visvalue = $('input#VISIBLE').prop("checked");
	var appid = $('input#APP_ID').val();
	var [TableId,TreeParam,TreeParentParam,TreeSuperParentParam,TopSuperParentParam,TreeTopSuperParentParam] = [localStorage.getItem('TableId_cancel_fun'),localStorage.getItem('ProfileTreeParam'),localStorage.getItem('ProfileTreeParentParam'),localStorage.getItem('ProfileNodeTreeSuperParentParam'),localStorage.getItem('ProfileTopSuperParentParam'),localStorage.getItem('ProfileTopSuperParentParam')];
	
		
		$('#alert_msg').removeClass('disp_blk');
		$('#alert_msg').addClass('disp_none');
	
		try
		{
			
			cpq.server.executeScript("SYSECTSAVE", { 'RECORD': JSON.stringify(dict_new), 'TableId':TableId, 'TreeParam': TreeParam, 'TreeParentParam': TreeParentParam, 'TreeSuperParentParam': TreeSuperParentParam, 'TopSuperParentParam': TopSuperParentParam, }, function (data) {
				
				if (data[1] == "" && data[2] == "") 
				{	
					try
					{				
						cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':RecordId, 'TableId':TableId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'NEWVAL': '', 'MODE':'VIEW', 'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1 }, function (dataset) {
							var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
							localStorage.setItem('Lookupobjd',data5)
							if(document.getElementById("Profile_Detail"))
							{
								document.getElementById("Profile_Detail").innerHTML = datas;	
								//A043S001P01-9077 start
					
					$('.SYSECT-SY-00024').removeClass('disp_blk');
					$('.SYSECT-SY-00024').addClass('disp_none');

					//A043S001P01-9077 end						
							}								
						});
						
					}
					catch(err)
					{
						console.log(err);
					}			
				}
				else{
					
					data1 = data[3]
					
					$('#alert_msg div label').text("ERROR:CPQ Administrator must set visible permission to system admin app");
					
					$('#alert_msg').removeClass('disp_none');
					$('#alert_msg').addClass('disp_blk');
				}
			});
		}
		catch(e)
		{
			console.log(e);
		}	


	//}
	
	
}
//A043S001P01-9092 sEnd
cpq.events.sub("API:configurator:updated", function (data) {
	
	var viewobjset = localStorage.getItem("Profile_OBJ_SET_VIEW");
	if (viewobjset == "OBJ_SET_VIEW")
	{		
		
		$('#BTN_PROFILE_OBJSET_SAVE, #BTN_PROFILE_OBJSET_CAN').removeClass('disp_blk');
		$('#BTN_PROFILE_OBJSET_SAVE, #BTN_PROFILE_OBJSET_CAN').addClass('disp_none');
	}
	var viewobjset = localStorage.getItem("Profile_OBJ_SET_EDIT")
	if (viewobjset == "OBJ_SET_EDIT")
	{
		
		$('#BTN_PROFILE_OBJSET_EDIT, #BTN_PROFILE_OBJSET_BTL').removeClass('disp_blk');
		$('#BTN_PROFILE_OBJSET_EDIT, #BTN_PROFILE_OBJSET_BTL').addClass('disp_none');
	}
});

function profileObjSet(ele)
{
	localStorage.setItem("Profile_OBJ_SET_VIEW", "OBJ_SET_VIEW");
	var [table_id,keys,key_value] = ['SYOBJR_93130_MMOBJ_00266','KEY',$(ele).closest('td').siblings('td:nth-child(3)').text()];
	try
	{
	cpq.server.executeScript("SYPRFLOBST", {'KEYS':'KEY', 'tableId':table_id,'key_value':key_value,'mode':'VIEW'}, function(datas) {
			var data = datas;
			if(document.getElementById("viewPrefileRelatedListDiv")) 
			{
				clearDivContent('viewPrefileRelatedListDiv');
				document.getElementById("viewPrefileRelatedListDiv").innerHTML = data;	


					$('button#BTN_PROFILE_OBJSET_SAVE, button#BTN_PROFILE_OBJSET_CAN').addClass('disp_none');
			}					
	});
	}
	catch(e){
		console.log(e);
	}
	
	$('#BTN_PROFILE_OBJSET_SAVE, #BTN_PROFILE_OBJSET_CAN').removeClass('disp_blk');
	$('#BTN_PROFILE_OBJSET_SAVE, #BTN_PROFILE_OBJSET_CAN').addClass('disp_none');
}
function profileObjSetEdit(ele)
{		
	localStorage.setItem("Profile_OBJ_SET_EDIT", "OBJ_SET_EDIT");
	var [table_id,keys,key_value] = ['SYOBJR_93130_MMOBJ_00266','KEY',$(ele).closest('td').siblings('td:nth-child(3)').text()];
	try
	{
	cpq.server.executeScript("SYPRFLOBST", {'KEYS':'KEY', 'tableId':table_id,'key_value':key_value,'mode':'edit'}, function(datas) {
			var data = datas;
			if(document.getElementById("viewPrefileRelatedListDiv")) {
				clearDivContent('viewPrefileRelatedListDiv');
				document.getElementById("viewPrefileRelatedListDiv").innerHTML = data;	
				
				$('button#BTN_PROFILE_OBJSET_EDIT').addClass('disp_none');
			}					
	});
	}
	catch(e){
		console.log(e);
	}
	
	$('button#BTN_PROFILE_OBJSET_EDIT, button#BTN_PROFILE_OBJSET_BTL').removeClass('disp_blk');
	$('button#BTN_PROFILE_OBJSET_EDIT, button#BTN_PROFILE_OBJSET_BTL').addClass('disp_none');
}
function clearDivContent(elementID)
{
    document.getElementById(elementID).innerHTML = "";
}
function profileObjSetModalEdit(ele)
{
	localStorage.setItem("Profile_OBJ_SET_EDIT", "OBJ_SET_EDIT");
	var [table_id,keys,key_value] = ['SYOBJR_93130_MMOBJ_00266','KEY',$('#Profile_ObjSettings tr:nth-child(1) input').val()];
	try
	{
	cpq.server.executeScript("SYPRFLOBST", {'KEYS':'KEY', 'tableId':table_id,'key_value':key_value,'mode':'edit'}, function(datas) {
			var data = datas;
			if(document.getElementById("viewPrefileRelatedListDiv")) {
				clearDivContent('viewPrefileRelatedListDiv');
				document.getElementById("viewPrefileRelatedListDiv").innerHTML = data;
				

				$('button#BTN_PROFILE_OBJSET_EDIT').addClass('disp_none');
							
			}					
	});
	}
	catch(e){
				console.log(e);
			}
	
	$('#BTN_PROFILE_OBJSET_EDIT, #BTN_PROFILE_OBJSET_BTL').removeClass('disp_blk');
	$('#BTN_PROFILE_OBJSET_EDIT, #BTN_PROFILE_OBJSET_BTL').addClass('disp_none');
}

function Profiletree_RelatedList_View(ele){
	var [table_id,keys,values] = [$(ele).closest('table').attr('id'),[],[]];
	$("table#"+table_id+" thead tr th .th-inner").each(function(){
			keys.push($(this).text().trim());
	});
	$(ele).closest('tr').find('td').each(function(){
		if ($(this).text().trim() != '' && $(this).text().trim() != '!')
		{
			values.push($(this).text().trim())
		}
		else
		{			
			values.push($(this).val());			
		}
	});	
	try
	{
	cpq.server.executeScript("SYPFRLPPVW", {'KEYS':keys, 'VALUES':values}, function(datas) {
		var data = datas;
		if(document.getElementById("viewPrefileRelatedListDiv")) {
			clearDivContent('viewPrefileRelatedListDiv');
			document.getElementById("viewPrefileRelatedListDiv").innerHTML = data;						 
		}					
	});
	}
	catch(e){
				console.log(e);
			}
	
	setTimeout(function(){
		$('.in div#container .row.pad-10.bg-lt-wt.brdr').before('<div class="cont_sty_ad_bf"></div>');
		var [popUp_height,table_heigth] = [$('div#VIEW_DIV_ID div#container').height(),$('div#VIEW_DIV_ID div#container table').height()];
		if(table_heigth > popUp_height)
		{
			
			$('.modal-content div#container > div.row.pad-10.bg-lt-wt.brdr').addClass('wid96');
		}
	},3000);
	

	$('.modal-dialog').addClass('width80');
}

function Profiletree_edit_RL(ele)
{ 	
	var [table_id,MODE] = [$(ele).closest('table').attr('id'),$(ele).innerText];	
	var record_id = table_id.split('_');	
	var TableId = record_id[0]+'-'+record_id[1];	
	localStorage.setItem('TableId_cancel_fun',TableId);
	var RecordId = $(ele).closest('tr').find('td:nth-child(3)').text();	
	
	$('.Detail, .Profile_Related_Detail').removeClass('disp_none');
	$('.Detail, .Profile_Related_Detail').addClass('disp_blk');
	
	$('.Related, .SYSECT-SY-00024').removeClass('disp_blk');
	$('.Related, .SYSECT-SY-00024').addClass('disp_none');
	
	//A043S001P01-9077 start
	
				//A043S001P01-9077 end
	localStorage.setItem('TreeParamRecordId', RecordId);
	var GrandTreeTopSuperParentParam = localStorage.getItem('ProfileGrandTreeTopSuperParentParam');
	//localStorage.getItem('ProfileTopSuperParentParam', TreeTopSuperParentParam);
	var Grand_GrandTreeTopSuperParentParam = localStorage.getItem('ProfileGrand_GrandTreeTopSuperParentParam');
	var Grand_Grand_GrandTreeTopSuperParentParam  = localStorage.getItem('ProfileGrand_Grand_GrandTreeTopSuperParentParam');
	var Grand_Grand_Grand_GrandTreeTopSuperParentParam = localStorage.getItem('ProfileGrand_Grand_Grand_GrandTreeTopSuperParentParam');
	
	var ParentTreeTopSuperParentParam = localStorage.getItem('ProfileParentTreeTopSuperParentParam');
	var [TreeParam,TreeParentParam,TreeSuperParentParam,TreeTopSuperParentParam] = [localStorage.getItem('ProfileTreeParam'),localStorage.getItem('ProfileTreeParentParam'),localStorage.getItem('ProfileNodeTreeSuperParentParam'),localStorage.getItem('ProfileTopSuperParentParam')];	
	try
	{
		cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':RecordId, 'TableId':TableId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam,'GrandTreeTopSuperParentParam':GrandTreeTopSuperParentParam,'Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_GrandTreeTopSuperParentParam,'Grand_Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_Grand_GrandTreeTopSuperParentParam,'ParentTreeTopSuperParentParam':ParentTreeTopSuperParentParam,'NEWVAL': '', 'MODE': MODE, 'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1 }, function (dataset) {
				
			var [datas,data1,data2,data3,data4,data5] =[dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
			localStorage.setItem('Lookupobjd',data5)
			if(document.getElementById("Profile_Detail"))
			{
				document.getElementById("Profile_Detail").innerHTML = datas;
				$(".Profile_Related_Detail").addClass("tree_second_child");
				//A043S001P01-9077 start
				
				$('.SYSECT-SY-00024').removeClass('disp_blk');
				$('.SYSECT-SY-00024').addClass('disp_none');
				//A043S001P01-9077 end
				
				$('#sub_child_content_banner, #sub_content_banner,#content_banner').removeClass('disp_blk');
				$('#sub_child_content_banner, #sub_content_banner,#content_banner').addClass('disp_none');
				var SECTION_EDIT = data3;					
				if (String(SECTION_EDIT)!='' )
				{						
				
					("." + SECTION_EDIT).addClass('header_section_div');
					$("."+SECTION_EDIT).append('<div class="g4  except_sec removeHorLine iconhvr sec_edit_sty"><button id="prf_save_sec" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="ProfiletreeSAVE(this)">SAVE</button><button  class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="ProfiletreeCancel(this)">CANCEL</button></div>');
				}	
				
				node = $('#Profilestreeview').treeview('getNode', data4);
				CurrentNodeId = node.nodeId
				TreeParam = node.text;
				var childrenNodes = _getChildren(node);
				if (childrenNodes.length > 0){
					child = 'true';
				}
				else {
					child = 'false';
				}
				localStorage.setItem('Mtrlchildavailable', child);
				//A043S001P01-9077 start
				
				$('.SYSECT-SY-00024').removeClass('disp_blk');
				$('.SYSECT-SY-00024').addClass('disp_none');
				//A043S001P01-9077 end
				localStorage.setItem("CurrentNodeId", CurrentNodeId);
				try {
				
					$('#Profilestreeview').treeview('selectNode', [ parseInt(CurrentNodeId), { silent: true }]);
					if (CurrentNodeId != '' && CurrentNodeId != null ) {
						TreeParentParam = $('#Profilestreeview').treeview('getParent', CurrentNodeId).text;
						TreeParentNodeId = $('#Profilestreeview').treeview('getParent', CurrentNodeId).nodeId;
						TreeParentNodeRecId = $('#Profilestreeview').treeview('getParent', CurrentNodeId).id;
					}
					if (TreeParentNodeId != '' && TreeParentNodeId != null ) {
						TreeSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).text;
						TreeSuperParentId = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).nodeId;
						TreeSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).id;
					}
					if (TreeSuperParentId != '' && TreeSuperParentId != null ) {
						TreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).text;
						TreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).nodeId;
						TreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).id;
					}
					if (TreeSuperParentId != '' && TreeSuperParentId != null ) {
						TreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).text;
						TreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).nodeId;
						TreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).id;
					}
					
					var GrandTreeTopSuperParentParam = GrandTreeTopSuperParentId = GrandTreeTopSuperParentRecId = Grand_GrandTreeTopSuperParentParam = Grand_GrandTreeTopSuperParentId = Grand_GrandTreeTopSuperParentRecId = Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_GrandTreeTopSuperParentId = Grand_Grand_GrandTreeTopSuperParentRecId = Grand_Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_GrandTreeTopSuperParentId = Grand_Grand_Grand_GrandTreeTopSuperParentRecId = '';

					if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null ) {
						GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).text;
						GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
						GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).id;
					}
					if (GrandTreeTopSuperParentId != '' && GrandTreeTopSuperParentId != null ) {
						Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).text;
						Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).nodeId;
						Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).id;
					}
					if (Grand_GrandTreeTopSuperParentId != '' && Grand_GrandTreeTopSuperParentId != null ) {
						Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).id;
					}
					if (Grand_Grand_GrandTreeTopSuperParentId != '' && Grand_Grand_GrandTreeTopSuperParentId != null ) 
					{
						Grand_Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).id;
					}
					if (Grand_Grand_Grand_GrandTreeTopSuperParentId != '' && Grand_Grand_Grand_GrandTreeTopSuperParentId != null ) 
					{
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).id;
					}
					
					
					if (TreeSuperParentId === undefined){
						TreeSuperParentParam = ''
					}
					if (TreeTopSuperParentId === undefined){
						TreeTopSuperParentParam = ''
					}
					if (TreeSuperParentId === undefined){
						TreeSuperParentParam = ''
					}
					if (TreeTopSuperParentId === undefined){
						TreeTopSuperParentParam = ''
					}
					if (document.getElementById("header_label")) {
						//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
						//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
						
					}
					//A043S001P01-9077 start
					
					$('.SYSECT-SY-00024').removeClass('disp_blk');
					$('.SYSECT-SY-00024').addClass('disp_none');
					//A043S001P01-9077 end
					localStorage.setItem('ProfileTreeParam', TreeParam);
					localStorage.setItem('ProfileTreeParentParam', TreeParentParam);
					localStorage.setItem('ProfileNodeTreeSuperParentParam', TreeSuperParentParam);
					localStorage.setItem('ProfileTopSuperParentParam', TreeTopSuperParentParam);	
					localStorage.setItem('ProfileParentNodeRecId', TreeParentNodeRecId);
					localStorage.setItem('ProfileTreeSuperParentRecId', TreeSuperParentRecId);
					localStorage.setItem('ProfileTopSuperParentRecId', TreeTopSuperParentRecId);
					localStorage.setItem('ProfileGrandTreeTopSuperParentParam', GrandTreeTopSuperParentParam);
					localStorage.setItem('ProfileGrand_GrandTreeTopSuperParentParam', Grand_GrandTreeTopSuperParentParam);
					localStorage.setItem('ProfileGrand_Grand_GrandTreeTopSuperParentParam', Grand_Grand_GrandTreeTopSuperParentParam);
					localStorage.setItem('ProfileGrand_Grand_Grand_GrandTreeTopSuperParentParam', Grand_Grand_Grand_GrandTreeTopSuperParentParam);
					if( TreeParam == 'Profile Information')
					{
						TreeParentParam = TreeSuperParentParam = TreeTopSuperParentParam = GrandTreeTopSuperParentParam = Grand_GrandTreeTopSuperParentParam = Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_GrandTreeTopSuperParentParam =  Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam= '';
					}
					
					if(TreeParentParam == '')
					{
                        TreeSuperParentParam = TreeTopSuperParentParam = GrandTreeTopSuperParentParam = Grand_GrandTreeTopSuperParentParam = Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_GrandTreeTopSuperParentParam =  Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam= '';
					}
					if(TreeSuperParentParam == '')
					{
						TreeTopSuperParentParam = GrandTreeTopSuperParentParam = Grand_GrandTreeTopSuperParentParam = Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_GrandTreeTopSuperParentParam =  Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam = '';
					}
					if(TreeTopSuperParentParam == '')
					{
						GrandTreeTopSuperParentParam = Grand_GrandTreeTopSuperParentParam = Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_GrandTreeTopSuperParentParam =  Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam = '';
					}
					if(GrandTreeTopSuperParentParam == '')
					{
						Grand_GrandTreeTopSuperParentParam = Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam = '';
					}
					if(Grand_GrandTreeTopSuperParentParam == '')
					{
						Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam = '';
					}
					if(Grand_Grand_GrandTreeTopSuperParentParam == '')
					{
						Grand_Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam = '';
					}
					if(Grand_Grand_Grand_GrandTreeTopSuperParentParam == '')
					{
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam = '';
					}
					
                   
				}
				catch(err){	
					console.log(err);
				}
			}
		});
	}
	catch(e)
	{
		
	}
}
function ProfileTree_lookup_popup(elem) {

	var value1 = $(elem).attr('id');	
	var value_split=value1.split("|");
	var [value,table,look_up_id,input_val,pop_id,assoc] = [value_split[0],value_split[1],$(elem).closest('td').children('input:first').attr('id'),[],[],{}];
	localStorage.setItem("look_up_id", look_up_id);
	$("#VIEW_DIV_ID #container input:not(.popup)").each(function () {
		if ($(this).attr('type') == 'CHECKBOX' && $(this).closest('div').attr('id') != 'checkboxes') 
		{
			input_val.push($(this).prop('checked'));
			pop_id.push($(this).attr('id'));
		} 
		else if ($(this).attr('type') != 'checkbox') 
		{
			input_val.push($(this).val());
			pop_id.push($(this).attr('id'));
		}
	});
	$("#VIEW_DIV_ID #container select:not(#select_id)").each(function () {
		input_val.push($(this).children("option:selected").text());
		pop_id.push($(this).attr('id'));
	});
	for (var i = 0; i < pop_id.length; i++) 
	{
		assoc[pop_id[i]] = input_val[i];
	}
	localStorage.setItem("assoc_array_value_view", JSON.stringify((assoc)));
	var [ids,table,keyData,price_mod_id] = [$(elem).attr('id'),$(elem).closest('table'),localStorage.getItem('keyData'),''];
	
	if (document.getElementById('PRICEMODEL_ID_VALUE'))
	{
		price_mod_id = document.getElementById('PRICEMODEL_ID_VALUE').value;
	}
	try
	{
		cpq.server.executeScript("SYCTLKPPUP", { 'TABLEID': value, 'OPER': 'ProfileTreeView', 'ATTRIBUTE_NAME': '', 'ATTRIBUTE_VALUE': '', 'GSCONTLOOKUP': '','TABLENAME': value1, 'PRICE_MOD_ID':price_mod_id, 'KEYDATA':keyData, 'ARRAYVAL': '' }, function (dataset) {		
			var [datas,data1,data2,data3] = [dataset[0],dataset[1],dataset[2],dataset[3]];
			if (document.getElementById('VIEW_DIV_ID'))
			{
				document.getElementById('VIEW_DIV_ID').innerHTML = datas;
			}
			try 
			{ 
				$('#' + data2).bootstrapTable({ data: data1 }); 
			} 
			catch(err) 
			{
				setTimeout(function () {
					$('#' + data2).bootstrapTable({ data: data1 });
				}, 5000);
			}
			finally { }
			eval(data3);
		});
	}
	catch(e)
	{
		console.log(e);
	}
}

function ProfiletreeCancel()
{
	var [RecordId,TableId,TreeParam,TreeParentParam,TreeSuperParentParam,TopSuperParentParam,TreeTopSuperParentParam,tabId_cancel_fun] = [$("table tbody tr td input").val(),localStorage.getItem('ProfileParentNodeRecId'),localStorage.getItem('ProfileTreeParam'),localStorage.getItem('ProfileTreeParentParam'),localStorage.getItem('ProfileNodeTreeSuperParentParam'),localStorage.getItem('ProfileTopSuperParentParam'),localStorage.getItem('ProfileTopSuperParentParam'),localStorage.getItem('TableId_cancel_fun')];
	//A043S001P01-9077 start
				
				$('.SYSECT-SY-00024').removeClass('disp_blk');
				$('.SYSECT-SY-00024').addClass('disp_none');
				//A043S001P01-9077 end
	if(tabId_cancel_fun)		
	{		
		TableId = tabId_cancel_fun;
	}
	try
	{
		cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':RecordId, 'TableId':TableId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'NEWVAL': '', 'MODE':'CANCEL', 'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1 }, function (dataset) {				
			var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
			
			localStorage.setItem('Lookupobjd',data5)
			if(document.getElementById("Profile_Detail"))
			{				
				document.getElementById("Profile_Detail").innerHTML = datas;	
				//A043S001P01-9077 start
				
				$('.SYSECT-SY-00024').removeClass('disp_blk');
				$('.SYSECT-SY-00024').addClass('disp_none');
				//A043S001P01-9077 end			
			}								
		});
	}
	catch(e)
	{
		console.log(e);
	}
	
	$('.SYSECT-SY-00024').removeClass('disp_blk');
	$('.SYSECT-SY-00024').addClass('disp_none');
}

function Profiletree_view_RL(ele)
{  
	
	var [table_id,ids] = [$(ele).closest('table').attr('id'),$(ele).closest('tr').attr('id')];
	var [Primary_Data,obj_vsl,RecordId,TreeParam,TreeParentParam,TreeSuperParentParam,TreeTopSuperParentParam,object_val_prob] = [$("#" + ids + " td:nth-child(3)").text().trim(),$(ele).closest('td').siblings('td:nth-child(4)').text(),$(ele).closest('tr').find('td:nth-child(3)').text(),localStorage.getItem('object_val_prob'),localStorage.getItem('ProfileTreeParentParam'),localStorage.getItem('ProfileTreeSuperParentParam'),localStorage.getItem('ProfileTopSuperParentParam'),localStorage.getItem('object_val_prob')];
	localStorage.setItem('object_val_prob', obj_vsl);	

	var GrandTreeTopSuperParentParam = localStorage.getItem('ProfileGrandTreeTopSuperParentParam');
	//localStorage.getItem('ProfileTopSuperParentParam', TreeTopSuperParentParam);
	var Grand_GrandTreeTopSuperParentParam = localStorage.getItem('ProfileGrand_GrandTreeTopSuperParentParam');
	var Grand_Grand_GrandTreeTopSuperParentParam  = localStorage.getItem('ProfileGrand_Grand_GrandTreeTopSuperParentParam');
	var Grand_Grand_Grand_GrandTreeTopSuperParentParam = localStorage.getItem('ProfileGrand_Grand_Grand_GrandTreeTopSuperParentParam');
	var ParentTreeTopSuperParentParam = localStorage.getItem('ProfileParentTreeTopSuperParentParam');
	var record_id = table_id.split('_');
	var TableId = record_id[0]+'-'+record_id[1];
	localStorage.setItem('TableId_cancel_fun',TableId);
	
	$('.Detail, .Profile_Related_Detail, #sysprofiledetail').removeClass('disp_none');
	$('.Detail, .Profile_Related_Detail, #sysprofiledetail').addClass('disp_blk');

	
	$('.Related').removeClass('disp_blk');
	$('.Related').addClass('disp_none');
	
	setTimeout(function(){
			
			$('.SYSECT-SY-00024').removeClass('disp_blk');
			$('.SYSECT-SY-00024').addClass('disp_none');
		},1000);
		
		$('div#sysprofiledetail').removeClass('disp_blk');
		$('div#sysprofiledetail').addClass('disp_none');

		$('div#sysprofiledetail').find("li").removeClass('active');
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");
		
		$('div#sysprofiledetail').find("li:nth-child(1)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(1)").addClass('disp_blk');
		
		$('div#sysprofiledetail').find("li:nth-child(2)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(2)").addClass('disp_blk');
		
		
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");$('#sysprofiledetail').removeClass('disp_none');
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");$('#sysprofiledetail').addClass('disp_blk');
				
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");
		prfparentTreeparam = localStorage.getItem('ProfileTreeParentParam');
		if (prfparentTreeparam == 'App Level Permissions'){
		
			$('div#sysprofiledetail').find("li:nth-child(3)").removeClass('disp_none');
			$('div#sysprofiledetail').find("li:nth-child(3)").addClass('disp_blk');
		}
	setTimeout(function(){
		
			$('.SYSECT-SY-00024').removeClass('disp_blk');
			$('.SYSECT-SY-00024').addClass('disp_none');
		},1000);
	localStorage.setItem('TreeParamRecordId', obj_vsl);
	try
	{
		cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':RecordId, 'TableId':TableId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam,'GrandTreeTopSuperParentParam':GrandTreeTopSuperParentParam,'Grand_GrandTreeTopSuperParentParam':Grand_GrandTreeTopSuperParentParam,'Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_GrandTreeTopSuperParentParam,'Grand_Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_Grand_GrandTreeTopSuperParentParam, 'NEWVAL': '', 'MODE': 'VIEW', 'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1,'object_val_prob':object_val_prob }, function (dataset) {
			var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
			localStorage.setItem('Lookupobjd',data5)
			if(document.getElementById("Profile_Detail"))
			{
				document.getElementById("Profile_Detail").innerHTML = datas;
				$(".Profile_Related_Detail").addClass("tree_second_child");
				
				$('#sub_child_content_banner, #sub_content_banner').removeClass('disp_blk');
				$('#sub_child_content_banner, #sub_content_banner').addClass('disp_none');
				var node = $('#Profilestreeview').treeview('getNode', data4);					
				var nodeidval = node;
				CurrentNodeId = node.nodeId;
				TreeParam = localStorage.getItem('object_val_prob');
				localStorage.setItem("CurrentNodeId", CurrentNodeId);
				try 
				{
					$('#Profilestreeview').treeview('selectNode', [ parseInt(CurrentNodeId), { silent: true }]);
					if (CurrentNodeId != '' && CurrentNodeId != null ) {
						TreeParentParam = $('#Profilestreeview').treeview('getParent', CurrentNodeId).text;
						TreeParentNodeId = $('#Profilestreeview').treeview('getParent', CurrentNodeId).nodeId;
						TreeParentNodeRecId = $('#Profilestreeview').treeview('getParent', CurrentNodeId).id;
					}
					if (TreeParentNodeId != '' && TreeParentNodeId != null ) {
						TreeSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).text;
						TreeSuperParentId = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).nodeId;
						TreeSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).id;
					}
					if (TreeSuperParentId != '' && TreeSuperParentId != null ) {
						TreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).text;
						TreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).nodeId;
						TreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).id;
					}
					var GrandTreeTopSuperParentParam = GrandTreeTopSuperParentId = GrandTreeTopSuperParentRecId = Grand_GrandTreeTopSuperParentParam = Grand_GrandTreeTopSuperParentId = Grand_GrandTreeTopSuperParentRecId = Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_GrandTreeTopSuperParentId = Grand_Grand_GrandTreeTopSuperParentRecId = Grand_Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_GrandTreeTopSuperParentId = Grand_Grand_Grand_GrandTreeTopSuperParentRecId = '';

					if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null ) {
						GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).text;
						GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
						GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).id;
					}
					if (GrandTreeTopSuperParentId != '' && GrandTreeTopSuperParentId != null ) {
						Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).text;
						Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).nodeId;
						Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).id;
					}
					if (Grand_GrandTreeTopSuperParentId != '' && Grand_GrandTreeTopSuperParentId != null ) {
						Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).id;
					}
					if (Grand_Grand_GrandTreeTopSuperParentId != '' && Grand_Grand_GrandTreeTopSuperParentId != null ) 
					{
						Grand_Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).id;
					}
					if (Grand_Grand_Grand_GrandTreeTopSuperParentId != '' && Grand_Grand_Grand_GrandTreeTopSuperParentId != null ) 
					{
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).id;
					}
					
					
					if (TreeSuperParentId === undefined){
						TreeSuperParentParam = ''
					}
					if (TreeTopSuperParentId === undefined){
						TreeTopSuperParentParam = ''
					}
					localStorage.setItem('ProfileTreeParam', TreeParam);
					localStorage.setItem('ProfileTreeParentParam', TreeParentParam);
					localStorage.setItem('ProfileNodeTreeSuperParentParam', TreeSuperParentParam);
					localStorage.setItem('ProfileTopSuperParentParam', TreeTopSuperParentParam);	
					localStorage.setItem('ProfileParentNodeRecId', TreeParentNodeRecId);
					localStorage.setItem('ProfileTreeSuperParentRecId', TreeSuperParentRecId);
					localStorage.setItem('ProfileTopSuperParentRecId', TreeTopSuperParentRecId);
					
					
					localStorage.setItem('ProfileGrandTreeTopSuperParentParam', GrandTreeTopSuperParentParam);
					localStorage.setItem('ProfileGrand_GrandTreeTopSuperParentParam', Grand_GrandTreeTopSuperParentParam);
					localStorage.setItem('ProfileGrand_Grand_GrandTreeTopSuperParentParam', Grand_Grand_GrandTreeTopSuperParentParam);
					localStorage.setItem('ProfileGrand_Grand_Grand_GrandTreeTopSuperParentParam', Grand_Grand_Grand_GrandTreeTopSuperParentParam);

					if (document.getElementById("header_label")) {
						//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
						//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
						
					}
					
					$('#content_banner').removeClass('disp_blk');
					$('#content_banner').addClass('disp_none');
					if (TableId == 'SYOBJR-93122')
					{		
						
					
						$('.Related').removeClass('disp_blk');
						$('.Related').addClass('disp_none');
					
						$('.Detail').removeClass('disp_none');
						$('.Detail').addClass('disp_blk');
						try
						{
							cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':'SYOBJR-93159', 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam,'GrandTreeTopSuperParentParam':GrandTreeTopSuperParentParam,'Grand_GrandTreeTopSuperParentParam':Grand_GrandTreeTopSuperParentParam,'Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_GrandTreeTopSuperParentParam,'Grand_Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_Grand_GrandTreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'EDIT','Flag':1 }, function (dataset) {
								var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
								localStorage.setItem('Lookupobjd',data5)
								if(document.getElementById("Profile_Detail"))
								{					
									document.getElementById("Profile_Detail").innerHTML = datas;
								}
							});
							if (document.getElementById("header_label")) {
								//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
								//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
								
							}
							setTimeout(function(){
							
								$('.SYSECT-SY-00024').removeClass('disp_blk');
								$('.SYSECT-SY-00024').addClass('disp_none');
							},1000);
							
							$('#sub_child_content_banner, #sub_content_banner,#content_banner').removeClass('disp_blk');
							$('#sub_child_content_banner, #sub_content_banner,#content_banner').addClass('disp_none');
						}
						catch(e){
							console.log(e);
						}
						[CurrentRecordId,RecName] = ['SYOBJR-93130','div_CTR_Object_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
						
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
						
						$('.SYSECT-SY-00015').removeClass('disp_blk');
						$('.SYSECT-SY-00015').addClass('disp_none');
					}
					if (TableId == 'SYOBJR-93121')
					{			
				var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
						[CurrentRecordId,RecName] = ['SYOBJR-93159','div_CTR_Tab_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
						
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
						
						$('.SYSECT-SY-00015').removeClass('disp_blk');
						$('.SYSECT-SY-00015').addClass('disp_none');
					}
					
				}
				catch (err) 
				{ 
					console.log(err);
				}
			}
		});
	}
	catch(e)
	{	
	}
}

function Profile_EDIT (ele)
{
	var SECTION_EDIT;
	if(ele == 'SYSECT-SY-00001')
	{	
		SECTION_EDIT = ele;
	}
	else
	{
		SECTION_EDIT = $(ele).attr('id');
	}
	localStorage.setItem('SECTION_LEVEL_EDIT_ID_PROFILE',SECTION_EDIT);
	//A043S001P01-9037 strat
	setTimeout(function(){
					
					$('.SYSECT-SY-00024').removeClass('disp_blk');
					$('.SYSECT-SY-00024').addClass('disp_none');
	},3000);
	//A043S001P01-9037 End
	var [RecordId,TreeParam,TableId] = [$("table tbody tr td input").val(),'',$("#colls"+SECTION_EDIT+" table").attr('id')];
	try
	{
		cpq.server.executeScript("SYPROFVIEW", { 'RECORD_ID':RecordId, 'TableId':TableId, 'MODE': 'EDIT','SECTION_EDIT':SECTION_EDIT }, function (dataset) {
			var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
			if(document.getElementById("Profile_Detail"))
			{
				document.getElementById("Profile_Detail").innerHTML = datas;
				//A043S001P01-9037 strat
				
				$('.SYSECT-SY-00024').removeClass('disp_blk');
				$('.SYSECT-SY-00024').addClass('disp_none');
				//A043S001P01-9037 end
			}
			$("."+SECTION_EDIT).addClass("SEC_EDIT_ARROW")
			
			$("." + SECTION_EDIT).addClass('header_section_div');
			$("."+SECTION_EDIT).append('<div class="g4  except_sec removeHorLine iconhvr sec_edit_sty"><button class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="profile_overview_save(this)" id="SAVE" >SAVE</button><button class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="profile_overview_cancel(this)" id="CANCEL" >CANCEL</button></div>');
			});
				//A043S001P01-9037 strat
			setTimeout(function(){
					
					$('.SYSECT-SY-00024').removeClass('disp_blk');
					$('.SYSECT-SY-00024').addClass('disp_none');
	},3000);
				//A043S001P01-9037 
	}
	catch(e){
	}
	setTimeout(function(){
					
					$('.SYSECT-SY-00024').removeClass('disp_blk');
					$('.SYSECT-SY-00024').addClass('disp_none');
	},3000);
}

function profile_overview_cancel(ele){
	var [TableId,RecordId] = [$(ele).parent().prev().children(':first-child').attr('id'),$("table tbody tr td input").val()];
	try
	{
		cpq.server.executeScript("SYPROFVIEW", { 'RECORD_ID': RecordId, 'TableId':TableId, 'MODE': 'VIEW','SECTION_EDIT':'' }, function (dataset) {
			var [datas,data1,data2] = [dataset[0],dataset[1],dataset[2]];
			if(document.getElementById("Profile_Detail"))
			{
				document.getElementById("Profile_Detail").innerHTML = datas;
			}
		});
	}
	catch(e)
	{
		console.log(e);
	}
}

function GetSAValue(ele)
{
	
	visvalue = $('input#VISIBLE').prop("checked");
	
	if (visvalue === 'False')
	{
		
		$('#alert_msg div label').text('ERROR:CPQ Administrator must set visible permission to system admin app');
		
		$('#alert_msg').removeClass('disp_none');
		$('#alert_msg').addClass('disp_blk');
	}
	else
	{
		
		$('#alert_msg').removeClass('disp_blk');
		$('#alert_msg').addClass('disp_none');
	}
}


function profile_overview_save(ele){
	localStorage.setItem("Profile_ACTION","SEC_EDIT_SAVE");
	var [dict_new,TableId,table_before_div,RecordId_value,id_val,Pro_ID,Pro_Name] = [{},$(ele).parent().prev().children(':first-child').attr('id'),$(ele).parent().prev().attr('id'),$("table tbody tr td input").val(),'','',''];
	$("#Profile_Detail #container #"+table_before_div+" table#"+TableId+" tbody tr td input").each(function () {
		if ($(this).attr('type') == 'CHECKBOX') 
		{
			dict_new[$(this).attr('id')] = String($(this).prop("checked"));
		} 
		else 
		{
			id_val = $(this).attr('id');
			dict_new[$(this).attr('id')] = $("#Profile_Detail #container table#" +TableId+" tbody tr td input#"+id_val).val();			
		} 
	});
	$("#Profile_Detail #container #"+table_before_div+" table#"+TableId+" tbody tr td textarea").each(function () {
		id_val = $(this).attr('id');
		dict_new[$(this).attr('id')] = $("#Profile_Detail #container table#" +TableId+" tbody tr td textarea#"+id_val).val();			
	});
	
	$('.glyphicon-plus').removeClass('disp_none');
	$('.glyphicon-plus').addClass('disp_blk');
	try
	{
		//A043S001P01-9058 A043S001P01-9059 START
		if ($("input#PROFILE_ID").val() == "" || $("input#PROFILE_NAME").val() == "" || $("textarea#PROFILE_DESCRIPTION").val() == "")
		{
			
			$('#alert_msg').addClass('disp_blk_mrg10');
		}
		else
		{
			try
			{
			cpq.server.executeScript("SYPROFSAVE", { 'RECORD': JSON.stringify(dict_new), 'TableId':TableId,'REC_VALUE':RecordId_value,'MODE':'SEC_EDIT_SAVE'}, function (data) {
			
				if(data != null && data != '') 
				{
					RecordId = $("table tbody tr td input").val();
					try
					{
						cpq.server.executeScript("SYPROFVIEW", { 'RECORD_ID': RecordId, 'TableId':TableId,'MODE': 'VIEW'}, function (dataset) {
							var [datas,data1,data2] = [dataset[0],dataset[1],dataset[2]];
							if(document.getElementById("Profile_Detail")){
								document.getElementById("Profile_Detail").innerHTML = datas;
							}
						});
						Pro_ID = $("input#PROFILE_ID").val();
						$("#PROFILE_BANNER_ID abbr").text(Pro_ID);
						$("#PROFILE_BANNER_ID abbr").attr('title',Pro_ID);

						Pro_Name = $("input#PROFILE_NAME").val();
						$("#PROFILE_BANNER_NAME abbr").text(Pro_Name);
						$("#PROFILE_BANNER_NAME abbr").attr('title',Pro_Name);
					}
					catch(err){
						console.log(err);
					}
				}
			});
			}
			catch(e){
				console.log(e);
			}
			
			localStorage.setItem("Profile_ACTION","VIEW");
		}
		//A043S001P01-9058 A043S001P01-9059 END
    }
	catch(e)
	{
		console.log(e);
	}
}
function profileObjectSetSave(ele)
{
	var [TableId,key,objName,value] = ['SYOBJR_93130_MMOBJ_00266',[],localStorage.getItem('object_val_prob'),[]];	
	$('table#Profile_ObjSettings tbody tr.iconhvr').each(function(index){
		var [key_name,textvalue,checkval] = [$(this).children('td').children('label').text(),$(this).children('td').children('input[type=text]').val(),$(this).children('td').children('input[type=checkbox]').prop("checked")];
		key.push(key_name)
		if (textvalue){
			value.push(textvalue)
		}
		else{
		value.push(checkval)
		}
	});
	try
	{
		var [CurrentRecordId,RecName] = ['SYOBJR-93130','div_CTR_Object_Field_Settings'];
		cpq.server.executeScript("SYPOBFSAVE", {'TableId':TableId, 'key':key,'value':value}, function (dataset) {
			var data = dataset;
			loadRelatedList(CurrentRecordId,RecName);
			
			$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
			$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
			$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
			
			$('.SYSECT-SY-00015').removeClass('disp_blk');
			$('.SYSECT-SY-00015').addClass('disp_none');	
		});
		loadRelatedList(CurrentRecordId,RecName);
	
		$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
		$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
		$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
		
		$('.SYSECT-SY-00015').removeClass('disp_blk');
		$('.SYSECT-SY-00015').addClass('disp_none');
	}
	catch(e)
	{
		console.log(e);
	}
}
	
function ProfileEDIT(ele)
{	
	var SECTION_EDIT=$(ele).attr('id');
	
	var prf_record_id = $("input#PROFILE_RECORD_ID").val();
	localStorage.setItem('P_SECTION_LEVEL_EDIT_ID',SECTION_EDIT);
	RecordId = $("table tbody tr td input").val();
	
	TreeParam = "";
	
	$('.SYSECT-SY-00024').removeClass('disp_blk');
	$('.SYSECT-SY-00024').addClass('disp_none');
	TableId = localStorage.getItem('ProfileParentNodeRecId');
	
	MODE=(ele).innerText;
	
	TreeParam = localStorage.getItem('ProfileTreeParam');
	TreeParentParam = localStorage.getItem('ProfileTreeParentParam');
	TreeSuperParentParam = localStorage.getItem('ProfileNodeTreeSuperParentParam');
	TopSuperParentParam = localStorage.getItem('ProfileTopSuperParentParam');
	TreeTopSuperParentParam = localStorage.getItem('ProfileTopSuperParentParam');
	var can_fun_tabId = localStorage.getItem('TableId_cancel_fun');
	GrandTreeTopSuperParentParam = localStorage.getItem('ProfileGrandTreeTopSuperParentParam');
	//localStorage.getItem('ProfileTopSuperParentParam', TreeTopSuperParentParam);
	Grand_GrandTreeTopSuperParentParam = localStorage.getItem('ProfileGrand_GrandTreeTopSuperParentParam');
	Grand_Grand_GrandTreeTopSuperParentParam  = localStorage.getItem('ProfileGrand_Grand_GrandTreeTopSuperParentParam');
	Grand_Grand_Grand_GrandTreeTopSuperParentParam = localStorage.getItem('ProfileGrand_Grand_Grand_GrandTreeTopSuperParentParam');
	ParentTreeTopSuperParentParam = localStorage.getItem('ProfileParentTreeTopSuperParentParam');
	//var can_fun_tabId = localStorage.getItem('TableId_cancel_fun');		
	if(can_fun_tabId)		
	{		
		TableId = can_fun_tabId;		
	}
	try
	{
		cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':RecordId, 'TableId':TableId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TopSuperParentParam':TopSuperParentParam,'TreeTopSuperParentParam':TreeTopSuperParentParam, 'NEWVAL': '', 'MODE': MODE, 'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':SECTION_EDIT,'prf_record_id':prf_record_id,'GrandTreeTopSuperParentParam':GrandTreeTopSuperParentParam, 'Grand_GrandTreeTopSuperParentParam':Grand_GrandTreeTopSuperParentParam,'Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_GrandTreeTopSuperParentParam,'ParentTreeTopSuperParentParam':ParentTreeTopSuperParentParam,'Grand_Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_Grand_GrandTreeTopSuperParentParam}, function (dataset) {
			var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
			localStorage.setItem('Lookupobjd',data5)
			if(document.getElementById("Profile_Detail"))
			{
				document.getElementById("Profile_Detail").innerHTML = datas;
				$(".Profile_Related_Detail").addClass("tree_second_child");
				
				$('#sub_child_content_banner, #sub_content_banner, .SYSECT-SY-00024').removeClass('disp_blk');
				$('#sub_child_content_banner, #sub_content_banner, .SYSECT-SY-00024').addClass('disp_none');
			}	
			$("."+SECTION_EDIT).addClass("SEC_EDIT_ARROW")
			
			$("." + SECTION_EDIT).addClass('header_section_div');
			$("."+SECTION_EDIT).append('<div class="g4  except_sec removeHorLine iconhvr sec_edit_sty"><button id="prf_save_sec" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="ProfiletreeSAVE(this)">SAVE</button><button id="prf_cancel_sec" class="btnconfig btnMainBanner sec_edit_sty_btn" onclick="ProfiletreeCancel(this)">CANCEL</button></div>');
		});
	}
	catch(e)
	{
	}
	
	$('.SYSECT-SY-00024').removeClass('disp_blk');
	$('.SYSECT-SY-00024').addClass('disp_none');
}

function Save_profile()
{
	var modes = localStorage.getItem("Profile_ACTION");
	if ((modes == "ADD NEW" && modes!='') || (modes == 'EDIT' && modes!=null && modes!='') )
	{
		var [dict_new,TableId,table_before_div,RecordId_value,refresh] = [{},$("#Profile_Detail table").attr('id'),$("#Profile_Detail").children().next().children().next().attr('id'),$("table tbody tr td input").val(),localStorage.getItem("REFRESH")];
		localStorage.setItem("Profile_ACTION","");
		$("#Profile_Detail #container #"+table_before_div+" table#"+TableId+" tbody tr td input").each(function () {
			if ($(this).attr('type') == 'CHECKBOX') 
			{
				dict_new[$(this).attr('id')] = String($(this).prop("checked"));
			} 
			else
			{
				id_val = $(this).attr('id');
				dict_new[$(this).attr('id')] = $("#Profile_Detail #container table#" +TableId+" tbody tr td input#"+id_val).val();
			} 
		});
		$("#Profile_Detail #container #"+table_before_div+" table#"+TableId+" tbody tr td textarea").each(function () {
				id_val = $(this).attr('id');
				dict_new[$(this).attr('id')] = $("#Profile_Detail #container table#" +TableId+" tbody tr td textarea#"+id_val).val();				
		});
		try
		{
			//A043S001P01-9058 043S001P01-9059 START
			if ($("input#PROFILE_ID").val() == "" || $("input#PROFILE_NAME").val() == "" || $("textarea#PROFILE_DESCRIPTION").val() == "")
			{
				
				$('#alert_msg').addClass('disp_blk_mrg10');
				localStorage.setItem("Profile_ACTION",modes);
			}
			else
			{
				try
				{
				cpq.server.executeScript("SYPROFSAVE", { 'RECORD': JSON.stringify(dict_new), 'TableId':TableId,'MODE':modes,'REC_VALUE':RecordId_value}, function (data) {			
					RecordId = data['PROFILE_RECORD_ID']
					if(RecordId != undefined) 
					{
					RecordId = data['PROFILE_RECORD_ID']
					$("#PROFILE_BANNER_RECORD_ID abbr").text(RecordId);
					$("#PROFILE_BANNER_RECORD_ID abbr").attr('title',RecordId);
					
					Pro_ID = $("input#PROFILE_ID").val()
					$("#PROFILE_BANNER_ID abbr").text(Pro_ID);
					$("#PROFILE_BANNER_ID abbr").attr('title',Pro_ID);

					Pro_Name = $("input#PROFILE_NAME").val()
					$("#PROFILE_BANNER_NAME abbr").text(Pro_Name);
					$("#PROFILE_BANNER_NAME abbr").attr('title',Pro_Name);
					localStorage.setItem("Profile_ACTION","ADD_NEW_VIEW")
					}
					//localStorage.setItem("Profile_ACTION","ADD_NEW_VIEW")
					
					if(data != null && data != '' && RecordId != undefined) 
					{
						localStorage.setItem("Profile_ACTION","ADD_NEW_VIEW")
						RecordId = data['PROFILE_RECORD_ID']
						localStorage.setItem("PROFILE_RECORD_ID_ADD_NEW",RecordId)
						if((RecordId != null && RecordId!='')|| modes=='EDIT' )
						{	
							try
							{
								cpq.server.executeScript("SYPROFVIEW", { 'RECORD_ID': RecordId, 'TableId':TableId,'MODE': 'VIEW'}, function (dataset) {
									var [datas,data1,data2] = [dataset[0],dataset[1],dataset[2]];
									if (refresh!='' && refresh=='TRUE' && refresh!= null && refresh!='FALSE')
									{
										$("#MM_ALL_REFRESH").click();
										localStorage.setItem("REFRESH","FALSE")
									}
									if(document.getElementById("Profile_Detail"))
									{
										document.getElementById("Profile_Detail").innerHTML = datas;
									}
								});
							}
							catch(err){
								console.log(err);
							}
						}
					}	
					else if  (RecordId == undefined)
					{
						
						localStorage.setItem("Profile_ACTION",modes);
						$('#alert_msg div label').text('ERROR:PROFILE ID AND PROFILE NAME SHOULD BE UNIQUE');
						
						$('#alert_msg').removeClass('disp_none');
						$('#alert_msg').addClass('disp_blk');		
					}
					else
					{
					
						localStorage.setItem("Profile_ACTION",modes);
					$('#alert_msg div label').text('ERROR:PROFILE ID AND PROFILE NAME SHOULD BE UNIQUE');
					
					$('#alert_msg').removeClass('disp_none');
					$('#alert_msg').addClass('disp_blk');	
				}
				});
				}
				catch(e){
					console.log(e);
				}
			}
		}
		//A043S001P01-9058 043S001P01-9059 END
		catch(e){
			console.log(e);
		}
	}
}
function PROFILEProgramRelatedHyperLink(value, row)
{
	return '<a href="#" onclick="Profiletree_view_RL(this)">'+ value +'</a>'
}

function Getvisibleval()
{
	var visibleval  = $('input#VISIBLE').prop("checked");
	if (visibleval === 'True')
	{		
		$('#DEFAULT input').removeAttr('checked');
	}
	else
	{
		$('#DEFAULT input,#VISIBLE input').attr('checked',visibleval);
	}
}
function Profiles_enable_disable(id) 
{	
	CurrentNodeId = localStorage.getItem("CurrentNodeId");
	node = $('#Profilestreeview').treeview('getNode', CurrentNodeId);	
	CurrentNodeId = node.nodeId	
	if (CurrentNodeId == undefined)
	{
		$('div#Profilestreeview ul.list-group li.list-group-item').trigger('click');
	}
	CurrentRecordId = node.id;
	var TreeParam = node.text;	
	
	/* JIRA-ID: A043S001P01-9029 - 'Begin'*/
	var txt_local = localStorage.getItem('profileFirstTime');
	if(txt_local == '1')
	{
		TreeParam = 'Profile Information';
		localStorage.setItem('profileFirstTime','0');
	}
	/* JIRA-ID: A043S001P01-9029 - 'End'*/
	
	localStorage.setItem("CurrentNodeId", CurrentNodeId);
	data1 = localStorage.getItem('profileTreedatasetnew');
	if (data1 !== null)
	{
		data = data1.split(',');
	}
	$('#Profilestreeview').treeview('selectNode', [ parseInt(CurrentNodeId), { silent: true }]);
	if (CurrentNodeId != '' && CurrentNodeId != null ) {
		TreeParentParam = $('#Profilestreeview').treeview('getParent', CurrentNodeId).text;
		TreeParentNodeId = $('#Profilestreeview').treeview('getParent', CurrentNodeId).nodeId;
		TreeParentNodeRecId = $('#Profilestreeview').treeview('getParent', CurrentNodeId).id;
	}
	if (TreeParentNodeId != '' && TreeParentNodeId != null ) {
		TreeSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).text;
		TreeSuperParentId = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).nodeId;
		TreeSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeParentNodeId).id;
	}
	if (TreeSuperParentId != '' && TreeSuperParentId != null ) {
		TreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).text;
		TreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).nodeId;
		TreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeSuperParentId).id;
	}
	
	if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null ) {
		ParentTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).text;
		ParentTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
		ParentTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).id;
	}

	var GrandTreeTopSuperParentParam = GrandTreeTopSuperParentId = GrandTreeTopSuperParentRecId = Grand_GrandTreeTopSuperParentParam = Grand_GrandTreeTopSuperParentId = Grand_GrandTreeTopSuperParentRecId = Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_GrandTreeTopSuperParentId = Grand_Grand_GrandTreeTopSuperParentRecId = Grand_Grand_Grand_GrandTreeTopSuperParentParam = Grand_Grand_Grand_GrandTreeTopSuperParentId = Grand_Grand_Grand_GrandTreeTopSuperParentRecId = '';

					if (TreeTopSuperParentId != '' && TreeTopSuperParentId != null ) {
						GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).text;
						GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).nodeId;
						GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', TreeTopSuperParentId).id;
					}
					if (GrandTreeTopSuperParentId != '' && GrandTreeTopSuperParentId != null ) {
						Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).text;
						Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).nodeId;
						Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', GrandTreeTopSuperParentId).id;
					}
					if (Grand_GrandTreeTopSuperParentId != '' && Grand_GrandTreeTopSuperParentId != null ) {
						Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_GrandTreeTopSuperParentId).id;
					}
					if (Grand_Grand_GrandTreeTopSuperParentId != '' && Grand_Grand_GrandTreeTopSuperParentId != null ) 
					{
						Grand_Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_Grand_GrandTreeTopSuperParentId).id;
					}
					if (Grand_Grand_Grand_GrandTreeTopSuperParentId != '' && Grand_Grand_Grand_GrandTreeTopSuperParentId != null ) 
					{
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentParam = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).text;
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentId = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).nodeId;
						Grand_Grand_Grand_Grand_GrandTreeTopSuperParentRecId = $('#Profilestreeview').treeview('getParent', Grand_Grand_Grand_GrandTreeTopSuperParentId).id;
					}
	if (TreeSuperParentId === undefined){
		TreeSuperParentParam = ''
	}
	if (TreeTopSuperParentId === undefined){
		TreeTopSuperParentParam = ''
	}

	
	localStorage.setItem('ProfileTreeParam', TreeParam);
	localStorage.setItem('ProfileTreeParentParam', TreeParentParam);
	localStorage.setItem('ProfileNodeTreeSuperParentParam', TreeSuperParentParam);
	localStorage.setItem('ProfileTopSuperParentParam', TreeTopSuperParentParam);
	localStorage.setItem('ProfileParentNodeRecId', TreeParentNodeRecId);
	localStorage.setItem('ProfileTreeSuperParentRecId', TreeSuperParentRecId);
	localStorage.setItem('ProfileTopSuperParentRecId', TreeTopSuperParentRecId);
	localStorage.setItem('ProfileParentTreeTopSuperParentParam', ParentTreeTopSuperParentParam);
	
	localStorage.setItem('ProfileGrandTreeTopSuperParentParam', GrandTreeTopSuperParentParam);
	localStorage.setItem('ProfileGrand_GrandTreeTopSuperParentParam', Grand_GrandTreeTopSuperParentParam);
	localStorage.setItem('ProfileGrand_Grand_GrandTreeTopSuperParentParam', Grand_Grand_GrandTreeTopSuperParentParam);
	localStorage.setItem('ProfileGrand_Grand_Grand_GrandTreeTopSuperParentParam', Grand_Grand_Grand_GrandTreeTopSuperParentParam);
	
	if(jQuery.inArray(TreeParam, data) !== -1 && TreeParam != 'Profile Information')
	{		
		
		button_name = $("input#PROFILE_RECORD_ID").val();
		
		$('#sysprofiledetail').removeClass('disp_blk');
		$('#sysprofiledetail').addClass('disp_none');		
		if(button_name === "")
		{						
			
			$('.Detail').removeClass('disp_none');
			$('.Detail').addClass('disp_blk');
			
			$('.Profile_Related_Detail, .Related, #sub_child_content_banner, #sub_content_banner').removeClass('disp_blk');
			$('.Profile_Related_Detail, .Related, #sub_child_content_banner, #sub_content_banner').addClass('disp_none');
		}
		else
		{
			
			$('.Detail, .Profile_Related_Detail, .Related').removeClass('disp_blk');
			$('.Detail, .Profile_Related_Detail, .Related').addClass('disp_none');
			RecName = 'div_CTR_'+TreeParam.replace(/\ /g,'_');
			loadRelatedList(CurrentRecordId,RecName);
			if (document.getElementById("header_label")) 
			{
				//document.getElementById("header_label").innerHTML = TreeParam.toUpperCase();
			}
			$(".Profile_Related_Detail").removeClass("tree_second_child");
			
			$('#sub_child_content_banner, #sub_content_banner, .SYSECT-SY-00015').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner, .SYSECT-SY-00015').addClass('disp_none');
			
			$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
			$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
			$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
			$("div[id='"+RecName+"']").closest('.Related').removeClass("tree_second_child tree_third_child tree_forth_child");
			
			$('.container_banner_inner_sec').removeClass('disp_none');
			$('.container_banner_inner_sec').addClass('disp_blk');
		}
	}
	else if(TreeParam == 'App Level Permissions' || TreeParam == 'Assigned Members' || TreeParam == 'Object Level Permissions')
	{
		
		button_name = $("input#PROFILE_RECORD_ID").val();
		
		setTimeout(function(){
					
					$('.SYSECT-SY-00024').removeClass('disp_blk');
					$('.SYSECT-SY-00024').addClass('disp_none');
		},3000);
		if(button_name === "")
		{
			
			$('.Detail').removeClass('disp_none');
			$('.Detail').addClass('disp_blk');
			
			$('.Profile_Related_Detail, .Related, #sub_child_content_banner, #sub_content_banner').removeClass('disp_blk');
			$('.Profile_Related_Detail, .Related, #sub_child_content_banner, #sub_content_banner').addClass('disp_none');
		}
		else
		{						
		
		$('.Detail, .Profile_Related_Detail, .Related').removeClass('disp_blk');
		$('.Detail, .Profile_Related_Detail, .Related').addClass('disp_none');
		RecName = 'div_CTR_'+TreeParam.replace(/\ /g,'_');
		loadRelatedList(CurrentRecordId,RecName);
		if (document.getElementById("header_label")) 
		{
			//document.getElementById("header_label").innerHTML = TreeParam.toUpperCase();
			setTimeout(function(){
					
					$('.SYSECT-SY-00024').removeClass('disp_blk');
					$('.SYSECT-SY-00024').addClass('disp_none');
			},3000);
		}
		$(".Profile_Related_Detail").removeClass("tree_second_child");
		
		$('#sub_child_content_banner, #sub_content_banner, #content_banner').removeClass('disp_blk');
		$('#sub_child_content_banner, #sub_content_banner, #content_banner').addClass('disp_none');

		
		$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
		$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');

		$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
		$("div[id='"+RecName+"']").closest('.Related').removeClass("tree_second_child tree_third_child tree_forth_child");}
		
		$('.SYSECT-SY-00024').removeClass('disp_blk');
		$('..SYSECT-SY-00024').addClass('disp_none');
	}
	else if(TreeParam == 'Tabs' &&  TreeSuperParentParam == 'App Level Permissions')
	{
	
		
		$('.Related, .Detail, #sysprofiledetail').removeClass('disp_none');
		$('.Related, .Detail, #sysprofiledetail').addClass('disp_blk');
		$('.Related, .Detail, #sysprofiledetail').addClass('disp_none');
		[CurrentRecordId,RecName] = ['SYOBJR-93159','div_CTR_Tab_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
						
		
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
		

						$('#content_banner, .SYSECT-SY-00001, .SYSECT-SY-00009').removeClass('disp_blk');
						$('#content_banner, .SYSECT-SY-00001, .SYSECT-SY-00009').addClass('disp_none');
						var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
	}
	else if(TreeParam == 'Object Level Permissions')
	{
		
		
		$('.Related, .Detail, #content_banner, .SYSECT-SY-00001, .SYSECT-SY-00009').removeClass('disp_blk');
		$('.Related, .Detail, #content_banner, .SYSECT-SY-00001, .SYSECT-SY-00009').addClass('disp_none');

		[CurrentRecordId,RecName] = ['SYOBJR-93122','div_CTR_Object_Level_Permissions'];
						loadRelatedList(CurrentRecordId,RecName);
						
		
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
		
						var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
	}
	
	else if(TreeParam == 'Fields')
	{
		
		$('.Related, .Detail').removeClass('disp_blk');
		$('.Related, .Detail').addClass('disp_none');
		[CurrentRecordId,RecName] = ['SYOBJR-93130','div_CTR_Object_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
						
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
		var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
	}
	else if(TreeParentParam == 'Fields' && TreeParam != '')
	{
	
		
		$('.Related').removeClass('disp_blk');
		$('.Related').addClass('disp_none');

		$('.Detail').removeClass('disp_none');
		$('.Detail').addClass('disp_blk');
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':'SYOBJR-93130', 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'EDIT','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) {
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			
			

			$('#sub_child_content_banner, #sub_content_banner,#content_banner, .SYSECT-SY-000019').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner,#content_banner, .SYSECT-SY-000019').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
		
	}
	else if(TreeParentParam == 'Related List' && TreeParam != '')
	{
		
		

		$('.Related').removeClass('disp_blk');
		$('.Related').addClass('disp_none');

		$('.Detail').removeClass('disp_none');
		$('.Detail').addClass('disp_blk');
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':'SYOBJR-93170', 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'EDIT','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) {
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			
			

			$('#sub_child_content_banner, #sub_content_banner,#content_banner, .SYSECT-SY-000019').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner,#content_banner, .SYSECT-SY-000019').addClass('disp_none');

		}
		catch(e){
			console.log(e);
		}
		
		
	}
	else if(TreeParam == 'Related List' )
	{
		
		
		$('.Related, .Detail, #sysprofiledetail, .SYSECT-SY-00024').removeClass('disp_blk');
		$('.Related, .Detail, #sysprofiledetail, .SYSECT-SY-00024').addClass('disp_none');
		[CurrentRecordId,RecName] = ['SYOBJR-93170','div_CTR_Related_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
						
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
						
						$('#content_banner').removeClass('disp_blk');
						$('#content_banner').addClass('disp_none');
						var treeparam = localStorage.getItem('ProfileTreeParam');
						$('span#container_banner_id').text(treeparam);
						
	}
	
	else if(TreeParam == 'Sections' &&  TreeSuperParentParam == 'Tabs')
	{
		
		

		$('.Related, .Detail, #sysprofiledetail, .SYSECT-SY-00024').removeClass('disp_blk');
		$('.Related, .Detail, #sysprofiledetail, .SYSECT-SY-00024').addClass('disp_none');

		[CurrentRecordId,RecName] = ['SYOBJR-93160','div_CTR_Sec_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
		
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
		
						$('#content_banner').removeClass('disp_blk');
						$('#content_banner').addClass('disp_none');
						var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
		
	}
	else if(TreeParam == 'Questions' &&  TreeSuperParentParam == 'Sections')
	{
		
		
		$('.Related, .Detail, #sysprofiledetail').removeClass('disp_blk');
		$('.Related, .Detail, #sysprofiledetail').addClass('disp_none');
		[CurrentRecordId,RecName] = ['SYOBJR-93162','div_CTR_Qst_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
		
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
		
						$('#content_banner').removeClass('disp_blk');
						$('#content_banner').addClass('disp_none');
						var treeparam = localStorage.getItem('ProfileTreeParam');
						$('span#container_banner_id').text(treeparam);
		
	}
	else if(TreeParam == 'Actions' && TreeSuperParentParam == 'Tabs')
	{
		
		$('.Related, .Detail').removeClass('disp_blk');
		$('.Related, .Detail').addClass('disp_none');

		[CurrentRecordId,RecName] = ['SYOBJR-93169','div_CTR_SEARCH_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
		
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
		
						$('#content_banner').removeClass('disp_blk');
						$('#content_banner').addClass('disp_none');
						var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
						
	}
	
	else if(TreeParam == 'Actions' &&  TreeSuperParentParam == 'Sections')
	{
		
		$('.Related, .Detail').removeClass('disp_blk');
		$('.Related, .Detail').addClass('disp_none');
		[CurrentRecordId,RecName] = ['SYOBJR-93188','div_CTR_Actions_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
		
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
		
						$('#content_banner').removeClass('disp_blk');
						$('#content_banner').addClass('disp_none');
						var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
						
	}
	else if(TreeParam == 'Related List')
	{
	
		$('.Related, .Detail').removeClass('disp_blk');
		$('.Related, .Detail').addClass('disp_none');
		[CurrentRecordId,RecName] = ['SYOBJR-93170','div_CTR_Related_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
						
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
						
						$('#content_banner').removeClass('disp_blk');
						$('#content_banner').addClass('disp_none');
						var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
		
	}
	else if(TreeParentParam == 'Tabs' &&  TreeTopSuperParentParam == 'App Level Permissions' && TreeParam != '')
	{
		
		$('.Related, .Detail').removeClass('disp_blk');
		$('.Related, .Detail').addClass('disp_none');

		$('#sysprofiledetail').removeClass('disp_none');
		$('#sysprofiledetail').addClass('disp_blk');

		$('div#sysprofiledetail').find("li").removeClass('disp_blk');
		$('div#sysprofiledetail').find("li").addClass('disp_none');

		$('div#sysprofiledetail').find("li").removeClass('active');
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");

		$('div#sysprofiledetail').find("li:nth-child(1)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(1)").addClass('disp_blk');

		$('div#sysprofiledetail').find("li:nth-child(2)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(2)").addClass('disp_blk');

		$('div#sysprofiledetail').find("li:nth-child(4)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(4)").addClass('disp_blk');

		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':'SYOBJR-93159', 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'EDIT','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) {
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			
			
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
		
		
		
		
	}
	
	else if(TreeParentParam == 'Tabs' &&  TreeTopSuperParentParam == 'App Level Permissions' && TreeParam != '')
	{
		
		
		$('.Related').removeClass('disp_blk');
		$('.Related').addClass('disp_none');

		$('.Detail, #sysprofiledetail').removeClass('disp_none');
		$('.Detail, #sysprofiledetail').addClass('disp_blk');

		$('div#sysprofiledetail').find("li").removeClass('disp_blk');
		$('div#sysprofiledetail').find("li").addClass('disp_none');

		$('div#sysprofiledetail').find("li").removeClass('active');
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");

		$('div#sysprofiledetail').find("li:nth-child(1)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(1)").addClass('disp_blk');

		$('div#sysprofiledetail').find("li:nth-child(2)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(2)").addClass('disp_blk');

		$('div#sysprofiledetail').find("li:nth-child(4)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(4)").addClass('disp_blk');

		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':'SYOBJR-93159', 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'EDIT','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) {
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();

			}
			
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
		
		
		
		
	}
	else if(TreeParentParam == 'Actions' &&  TreeTopSuperParentParam == 'Sections' && TreeParam != '')
	{
		
		
		$('.Related, #sysprofiledetail').removeClass('disp_blk');
		$('.Related #sysprofiledetail').addClass('disp_none');

		$('.Detail').removeClass('disp_none');
		$('.Detail').addClass('disp_blk');

		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':'SYOBJR-93188', 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'EDIT','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) {
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			
			
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
		
		
		
		
	}
	
	else if(TreeParentParam == 'Actions' &&  TreeTopSuperParentParam == 'Tabs' && TreeParam != '')
	{
		
		
		$('.Related').removeClass('disp_blk');
		$('.Related').addClass('disp_none');
		
		$('.Related').removeClass('disp_none');
		$('.Related').addClass('disp_blk');
		
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':'SYOBJR-93169', 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'EDIT','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) {
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			
			
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
		
		
		
		
	}
	
	else if(jQuery.inArray(TreeParentParam, data) !== -1 && TreeParam != '')
	{	
		if (TreeParentParam != 'App Level Permissions')
		{
			
			if (TreeParam != 'Profile Information'){
				
			
			$('.Related').removeClass('disp_blk');
			$('.Related').addClass('disp_none');
			
			$('.Detail').removeClass('disp_none');
			$('.Detail').addClass('disp_blk');
			try
			{
				cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':TreeParentNodeRecId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1 }, function (dataset) {
					var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
					localStorage.setItem('Lookupobjd',data5)
					if(document.getElementById("Profile_Detail"))
					{					
						document.getElementById("Profile_Detail").innerHTML = datas;
					}
				});
				if (document.getElementById("header_label")) 
				{
					//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
					//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
					
				}
				
				$(".Profile_Related_Detail").addClass("tree_second_child");
				

				$('.SYSECT-SY-00015, #sub_child_content_banner, #sub_content_banner,#content_banner, .Related').removeClass('disp_none');
				$('.SYSECT-SY-00015, #sub_child_content_banner, #sub_content_banner,#content_banner, .Related').addClass('disp_blk');
			
				$('.Detail').removeClass('disp_none');
				$('.Detail').addClass('disp_blk');
		
			//[CurrentRecordId,RecName] = ['SYOBJR-93130','div_CTR_Object_Field_Settings'];
							//loadRelatedList(CurrentRecordId,RecName);
							
							//$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
							
			
					
					$('.SYSECT-SY-00015').removeClass('disp_blk');
					$('.SYSECT-SY-00015').addClass('disp_none');
			}
			catch(e){
				console.log(e);
			}
			}
		}
		else if(TreeParam == 'Profile Information' )
		{		
		
		$('.Detail').removeClass('disp_none');
		$('.Detail').addClass('disp_blk');

		
		$('.Profile_Related_Detail, .Related, #sysprofiledetail').removeClass('disp_blk');
		$('.Profile_Related_Detail, .Related, #sysprofiledetail').addClass('disp_none');
		var Primary_Data = localStorage.getItem('id_primarydata');
		if (document.getElementById("header_label")) 
		{
			//document.getElementById("header_label").innerHTML = TreeParam;
		}
		var mode = localStorage.getItem("Profile_ACTION")		
		if (mode == 'VIEW' && mode !='' )
		{
			try
			{
				cpq.server.executeScript("SYPROFVIEW", { 'RECORD_ID':Primary_Data,'MODE':'VIEW' }, function (dataset){
					var [datas,data1] = [dataset[0],dataset[1]];
					if(document.getElementById("Profile_Detail"))
					{
						document.getElementById("Profile_Detail").innerHTML = datas;
					}
				});			
			}
			catch(e){
				console.log(e);
			}
		}
		}
		else if (TreeParentParam == 'App Level Permissions'){
			
			
		
		$('.Related').removeClass('disp_blk');
		$('.Related').addClass('disp_none');

		
		$('.Detail, #sysprofiledetail').removeClass('disp_none');
		$('.Detail, #sysprofiledetail').addClass('disp_blk');

		
		$('div#sysprofiledetail').find("li").removeClass('disp_blk');
		$('div#sysprofiledetail').find("li").addClass('disp_none');

		$('div#sysprofiledetail').find("li").removeClass('active');
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");
		
		$('div#sysprofiledetail').find("li:nth-child(1)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(1)").addClass('disp_blk');

		
		$('div#sysprofiledetail').find("li:nth-child(2)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(2)").addClass('disp_blk');

		
		$('div#sysprofiledetail').find("li:nth-child(3)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(3)").addClass('disp_blk');
		$('#alert_msg').addClass('disp_none');
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':TreeParentNodeRecId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) 
			{
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			
			$(".Profile_Related_Detail").addClass("tree_second_child");
			
				
				$('.SYSECT-SY-00015, #sub_child_content_banner, #sub_content_banner','#content_banner, .SYSECT-SY-00015').removeClass('disp_blk');
				$('.SYSECT-SY-00015, #sub_child_content_banner, #sub_content_banner','#content_banner, .SYSECT-SY-00015').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
		$('#alert_msg').addClass('disp_none');
		}
		else{
			
			
			$('.Related').removeClass('disp_blk');
			$('.Related').addClass('disp_none');
			$('#alert_msg').addClass('disp_none');
			$('.Detail').removeClass('disp_none');
			$('.Detail').addClass('disp_blk');
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':TreeParentNodeRecId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) 
			{
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			
			$(".Profile_Related_Detail").addClass("tree_second_child");
			
				$('.Detail').removeClass('disp_none');
				$('.Detail').addClass('disp_blk');
				[CurrentRecordId,RecName] = ['SYOBJR-93130','div_CTR_Object_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
			
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');

						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
			

				$('.SYSECT-SY-00015, #sub_child_content_banner, #sub_content_banner, .Related, .SYSECT-SY-00015').removeClass('disp_blk');
				$('.SYSECT-SY-00015, #sub_child_content_banner, #sub_content_banner, .Related, .SYSECT-SY-00015').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}}
		
	}
	//8389 start--
	else if(TreeParam != '' && TreeParentParam == 'App Level Permissions' )
	{		
		

		$('Related').removeClass('disp_blk');
		$('Related').addClass('disp_none');

		$('.Detail').removeClass('disp_none');
		$('.Detail').addClass('disp_blk');
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':TreeParentNodeRecId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) {
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			[CurrentRecordId,RecName] = ['SYOBJR-93159','div_CTR_Tab_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
						
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');

						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
			$(".Profile_Related_Detail").addClass("tree_second_child");
			
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
	}
	else if(TreeParam != '' && ParentTreeTopSuperParentParam == 'App Level Permissions' && TreeParentParam != '')
	{		
		
		
		$('.Related').removeClass('disp_blk');
		$('.Related').addClass('disp_none');
		
		$('.Detail').removeClass('disp_none');
		$('.Detail').addClass('disp_blk');
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':TreeParentNodeRecId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1,'ParentTreeTopSuperParentParam':ParentTreeTopSuperParentParam }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) {
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			
			
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
	}
	
	else if(TreeParam != '' && TreeSuperParentParam == 'Assigned Apps' && TreeParentParam != '' && TreeTopSuperParentParam == 'Profile Information' )
	{		
		
		
		$('.Detail').removeClass('disp_none');
		$('.Detail').addClass('disp_blk');
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':'SYOBJR-93159', 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'EDIT','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) {
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			[CurrentRecordId,RecName] = ['SYOBJR-93160','div_CTR_Sec_Field_Settings'];
						loadRelatedList(CurrentRecordId,RecName);
						
						$("div[id='"+RecName+"']").closest('.Related').removeClass('disp_none');
						$("div[id='"+RecName+"']").closest('.Related').addClass('disp_blk');
						$("div[id='"+RecName+"']").closest('.Related').addClass("tree_first_child");
						var treeparam = localStorage.getItem('ProfileTreeParam');
		$('span#container_banner_id').text(treeparam);
			$(".Profile_Related_Detail").addClass("tree_second_child");
			
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
		
	}
	
	else if(TreeParam != '' && TreeSuperParentParam != '' && TreeParentParam == 'Sections' && TreeTopSuperParentParam == 'Tabs' )
	{		
		
		
		$('.Related').removeClass('disp_blk');
		$('.Related').addClass('disp_none');
		
		$('.Detail, #sysprofiledetail').removeClass('disp_none');
		$('.Detail, #sysprofiledetail').addClass('disp_blk');

		
		$('div#sysprofiledetail').find("li").removeClass('disp_blk');
		$('div#sysprofiledetail').find("li").addClass('disp_none');
		$('div#sysprofiledetail').find("li").removeClass('active');
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");
		
		$('div#sysprofiledetail').find("li:nth-child(1)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(1)").addClass('disp_blk');

		$('div#sysprofiledetail').find("li:nth-child(2)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(2)").addClass('disp_blk');

		$('div#sysprofiledetail').find("li:nth-child(6)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(6)").addClass('disp_blk');

		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':'SYOBJR-93160', 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam,'GrandTreeTopSuperParentParam':GrandTreeTopSuperParentParam,'Grand_GrandTreeTopSuperParentParam':Grand_GrandTreeTopSuperParentParam,'Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_GrandTreeTopSuperParentParam,'Grand_Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_Grand_GrandTreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'EDIT','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
					
					$('.SYSECT-SY-00024').removeClass('disp_blk');
					$('.SYSECT-SY-00024').addClass('disp_none');
				}
			});
			if (document.getElementById("header_label")) {
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
				$('.SYSECT-SY-00024').removeClass('disp_blk');
				$('.SYSECT-SY-00024').addClass('disp_none');
				
			}
			
			
				setTimeout(function(){
			

			$('#sub_child_content_banner, #sub_content_banner,#content_banner, .SYSECT-SY-00024').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner,#content_banner, .SYSECT-SY-00024').addClass('disp_none');
	},3000);
			
		}
		catch(e){
			console.log(e);
		}
	}
	else if(TreeParam != '' && TreeParentParam == 'Questions' && Grand_GrandTreeTopSuperParentParam == 'Tabs' && TreeTopSuperParentParam == 'Sections' )
	{		
		
		
		$('.Related').removeClass('disp_blk');
		$('.Related').addClass('disp_none');

		$('.Detail, #sysprofiledetail').removeClass('disp_none');
		$('.Detail, #sysprofiledetail').addClass('disp_blk');

		$('div#sysprofiledetail').find("li").removeClass('disp_blk');
		$('div#sysprofiledetail').find("li").addClass('disp_none');
		$('div#sysprofiledetail').find("li").removeClass('active');
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");

		$('div#sysprofiledetail').find("li:nth-child(1)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(1)").addClass('disp_blk');

		$('div#sysprofiledetail').find("li:nth-child(2)").removeClass('disp_none');
		$('div#sysprofiledetail').find("li:nth-child(2)").addClass('disp_blk');
		
		$("div#sysprofiledetail").find("li:nth-child(2)").addClass("active");
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':'SYOBJR-93162', 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam,'GrandTreeTopSuperParentParam':GrandTreeTopSuperParentParam,'Grand_GrandTreeTopSuperParentParam':Grand_GrandTreeTopSuperParentParam,'Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_GrandTreeTopSuperParentParam,'Grand_Grand_Grand_GrandTreeTopSuperParentParam':Grand_Grand_Grand_GrandTreeTopSuperParentParam,'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'EDIT','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) {
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			
			
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner,#content_banner').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
	}
	else if(TreeParam != '' && TreeParentParam == 'Assigned Members')
	{	
		
		
		$('.Related').removeClass('disp_blk');
		$('.Related').addClass('disp_none');
		
		$('.Detail').removeClass('disp_none');
		$('.Detail').addClass('disp_blk');
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':TreeParentNodeRecId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{	
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) 
			{
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			$(".Profile_Related_Detail").addClass("tree_second_child");
			

			$('#sub_child_content_banner, #sub_content_banner').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
	}
	else if(TreeParam != '' && TreeParentParam == 'Object Level Permissions' )
	{
		
		$('.Related').removeClass('disp_blk');
		$('.Related').addClass('disp_none');
		
		$('.Detail').removeClass('disp_none');
		$('.Detail').addClass('disp_blk');
		try
		{
			cpq.server.executeScript("SYPRFLVIEW", { 'RECORD_ID':CurrentRecordId, 'TableId':TreeParentNodeRecId, 'TreeParam':TreeParam, 'TreeParentParam':TreeParentParam, 'TreeSuperParentParam' :TreeSuperParentParam, 'TreeTopSuperParentParam':TreeTopSuperParentParam, 'MODE':'VIEW','NEWVAL': '',  'LOOKUPOBJ':'', 'LOOKUPAPI': '','SECTION_EDIT':'','Flag':1 }, function (dataset) {
				var [datas,data1,data2,data3,data4,data5] = [dataset[0],dataset[1],dataset[2],dataset[3],dataset[4],dataset[5]];
				localStorage.setItem('Lookupobjd',data5)
				if(document.getElementById("Profile_Detail"))
				{					
					document.getElementById("Profile_Detail").innerHTML = datas;
				}
			});
			if (document.getElementById("header_label")) 
			{
				//document.getElementById("header_label").innerHTML = TreeParentParam.toUpperCase();
				//document.getElementById("banner_label").innerHTML = TreeParam.toUpperCase();
				
			}
			$(".Profile_Related_Detail").addClass("tree_second_child");
			
			$('#sub_child_content_banner, #sub_content_banner').removeClass('disp_blk');
			$('#sub_child_content_banner, #sub_content_banner').addClass('disp_none');
		}
		catch(e){
			console.log(e);
		}
	}
	else if(CurrentNodeId == 0 && TreeParam == 'Profile Information' )
	{		
		
		$('.Detail').removeClass('disp_none');
		$('.Detail').addClass('disp_blk');
		

		$('.Profile_Related_Detail, .Related, #sysprofiledetail').removeClass('disp_blk');
		$('.Profile_Related_Detail, .Related, #sysprofiledetail').addClass('disp_none');		
		var Primary_Data = localStorage.getItem('id_primarydata');
		if (document.getElementById("header_label")) 
		{
			//document.getElementById("header_label").innerHTML = TreeParam;
		}
		var mode = localStorage.getItem("Profile_ACTION")		
		if (mode == 'VIEW' && mode !='' )
		{
			try
			{
				cpq.server.executeScript("SYPROFVIEW", { 'RECORD_ID':Primary_Data,'MODE':'VIEW' }, function (dataset){
					var [datas,data1] = [dataset[0],dataset[1]];
					if(document.getElementById("Profile_Detail"))
					{
						document.getElementById("Profile_Detail").innerHTML = datas;
					}
				});			
			}
			catch(e){
				console.log(e);
			}
		}
		else if (mode == 'ADD NEW' && mode !='')
		{
			try
			{
				cpq.server.executeScript("SYPRADDNEW", {}, function (dataset) {
					var datas = dataset[0];
					if(document.getElementById("Profile_Detail"))
					{
						document.getElementById("Profile_Detail").innerHTML = datas;
					}
				});			
			}
			catch(e){
				console.log(e);
			}
		}
		else if (mode == 'ADD_NEW_VIEW' && mode !='' )
		{
			var [PRO_REC_ID_ADD_NEW,Profile_ID,Profile_Name]= [localStorage.getItem("PROFILE_RECORD_ID_ADD_NEW"),$("input#PROFILE_ID").val(),$("input#PROFILE_NAME").val()];
			$("#PROFILE_BANNER_RECORD_ID abbr").text(PRO_REC_ID_ADD_NEW);
			$("#PROFILE_BANNER_RECORD_ID abbr").attr('title',PRO_REC_ID_ADD_NEW);
			$("#PROFILE_BANNER_ID abbr").text(Profile_ID);
			$("#PROFILE_BANNER_ID abbr").attr('title',Profile_ID);
			$("#PROFILE_BANNER_NAME abbr").text(Profile_Name);
			$("#PROFILE_BANNER_NAME abbr").attr('title',Profile_Name);
			localStorage.setItem("Profile_ACTION","");
			try
			{
				cpq.server.executeScript("SYPROFVIEW", { 'RECORD_ID':PRO_REC_ID_ADD_NEW,'MODE':'VIEW' }, function (dataset){
					var [datas,data1] = [dataset[0],dataset[1]];
					
					if(document.getElementById("Profile_Detail"))
					{
						document.getElementById("Profile_Detail").innerHTML = datas;
					}
				});			
			}
			catch(e){
				console.log(e);
			}
		}
		else if (mode == 'GRID_EDIT' && mode !='' && mode!=null)
		{
			var [RecordId,Profile_ID,Profile_Name] = [localStorage.getItem("PROFILE_RECORD_ID_BACK_TO_LIST"),$("input#PROFILE_ID").val(),$("input#PROFILE_NAME").val()];
			$("#PROFILE_BANNER_RECORD_ID abbr").text(RecordId);
			$("#PROFILE_BANNER_RECORD_ID abbr").attr('title',RecordId);
			$("#PROFILE_BANNER_ID abbr").text(Profile_ID);
			$("#PROFILE_BANNER_ID abbr").attr('title',Profile_ID);
			$("#PROFILE_BANNER_NAME abbr").text(Profile_Name);
			$("#PROFILE_BANNER_NAME abbr").attr('title',Profile_Name);
			try
			{
				cpq.server.executeScript("SYPROFVIEW", { 'RECORD_ID': RecordId, 'TableId':'SYPRFL', 'MODE': 'VIEW','SECTION_EDIT':'' }, function (dataset) {
					var datas = dataset[0];
					if(document.getElementById("Profile_Detail"))
					{
						document.getElementById("Profile_Detail").innerHTML = datas;
					}
					localStorage.setItem("Profile_ACTION","")
				});			
			}
			catch(e){
				console.log(e);
			}
		}
		
		$('.Profile_Related_Detail').removeClass('disp_none');
		$('.Profile_Related_Detail').addClass('disp_blk');
		
		$('#sub_child_content_banner, #sub_content_banner, #content_banner').removeClass('disp_blk');
		$('#sub_child_content_banner, #sub_content_banner, #content_banner').addClass('disp_none');
		$('#Profile_Detail').addClass("tree_first_child");
		$('#Profile_Detail').removeClass("tree_second_child tree_third_child tree_forth_child tree_fifth_child");
	}
	else
	{
		$('div#Profilestreeview ul.list-group li.list-group-item').trigger('click');
		
		$('.Detail, .Profile_Related_Detail, .Related, #sub_child_content_banner, #sub_content_banner, #content_banner').removeClass('disp_blk');
		$('.Detail, .Profile_Related_Detail, .Related, #sub_child_content_banner, #sub_content_banner, #content_banner').addClass('disp_none');

		if (document.getElementById("header_label")) 
		{
			//document.getElementById("header_label").innerHTML = TreeParam;
		}
	}
	
	
	
}

cpq.events.sub("API:configurator:updated", function(data) {
	var mode = localStorage.getItem("Profile_ACTION");
	var modeview = localStorage.getItem("Profile_MEMEBR");
	 var currentprofileId = localStorage.getItem("Primary_Dataapp");
	if (modeview=='VIEW'){
		$("#PROFILE_BANNER_RECORD_ID abbr").text(currentprofileId);
        $("#PROFILE_BANNER_RECORD_ID abbr").attr('title', currentprofileId);
		}
	if (mode!='' && mode!=null && mode!='ADD NEW' && mode!='ADD_NEW_VIEW' && mode!='GRID_EDIT')
	{
		var [banner_contents,PROFILE_RECORD_ID_ADD_NEW,PROFILE_BANNER_ID,PROFILE_BANNER_NAME] = [localStorage.getItem("PROFILE_BANNER"),localStorage.getItem("PROFILE_RECORD_ID_ADD_NEW"),localStorage.getItem("PROFILE_BANNER_ID"),localStorage.getItem("PROFILE_BANNER_NAME")];
		$("#PROFILE_BANNER_RECORD_ID abbr").text(PROFILE_RECORD_ID_ADD_NEW);
		$("#PROFILE_BANNER_RECORD_ID abbr").attr('title',PROFILE_RECORD_ID_ADD_NEW);
		$("#PROFILE_BANNER_ID abbr").text(PROFILE_BANNER_ID);
		$("#PROFILE_BANNER_ID abbr").attr('title',PROFILE_BANNER_ID);
		$("#PROFILE_BANNER_NAME abbr").text(PROFILE_BANNER_NAME);
		$("#PROFILE_BANNER_NAME abbr").attr('title',PROFILE_BANNER_NAME);
	}
}); 

var get_Idlist = [];
function save_assignedapp()
{
	reload_appUser_val();
	var selected_app_list =[];
	var get_Idlist = [];
	selected_app_list =JSON.parse(localStorage.getItem("selected_app_item"));
	var mode = localStorage.getItem("Profile_ACTION");
	var [currentprofileId,currentprofilename,Primary_Data] = [$("input#QSTN_SYSEFL_SY_00125").val(),$("input#QSTN_SYSEFL_SY_00129").val(),$("input#QSTN_SYSEFL_SY_00125").val()];
	 localStorage.setItem("prfid",currentprofileId)
	 localStorage.setItem("Primary_Dataapp",Primary_Data)
	 localStorage.setItem("prfname",currentprofilename)
	  localStorage.setItem("Profile_MEMEBR","VIEW")
	$('table#assignedUsers_addnew tbody.app_id tr').each(function(index){
		var classname = $(this).attr('class');
		
		if( classname=='selected')
		{
			var get_Id= $(this).children('td:nth-child(2)').text();
			get_Idlist.push($(this).children('td:nth-child(2)').text());
		}
	});
	localStorage.setItem("SELECTED_ASSIGNEDUSERID",JSON.stringify(get_Idlist))
	var currentid = localStorage.getItem("CurrentNodeId");
	
	try
	{
		cpq.server.executeScript("SYUSERSAVE", { 'CURRREC':currentprofileId,'SELECTROW':JSON.parse(localStorage.getItem("SELECTED_ASSIGNEDUSERID")),'Primary_Data':Primary_Data,'currentprofilename':currentprofilename }, function () {
					
			$('.BTN_MA_ALL_REFRESH').click();
			
			
		});
		
		$("#PROFILE_BANNER_RECORD_ID abbr").text(Primary_Data);
        $("#PROFILE_BANNER_RECORD_ID abbr").attr('title', Primary_Data);
		$('#Profilestreeview').treeview('selectNode', [parseInt(currentid), { silent: true }]);
		[CurrentRecordId,RecName] = ['SYOBJR-95800','div_CTR_Assigned_Members'];
		loadRelatedList(CurrentRecordId,RecName);
		
	}
	catch(e) 
	{
		console.log(e);
	}
}
localStorage.setItem("selected_app_item",JSON.stringify([]));

function GS_ADDNEW_USERS(showResultCount,recordEnd)
{
	var [table_id,first_record_id,first_record_feild] = ['ADDNEW__SYOBJR_95800_SYOBJ_00458',localStorage.getItem("keyData"),$('#attributesContainer .Detail input').first().attr('id')];
	localStorage.setItem("first_record_id", first_record_id);
	localStorage.setItem("first_record_feild", first_record_feild);
	var selected_app_list =[]
	selected_app_list =JSON.parse(localStorage.getItem("selected_app_item"));
	localStorage.setItem('cont_table_id', table_id)
	try 
	{
		cpq.server.executeScript("SYUADNWPOP", { 'TABLEID': table_id, 'OPER': 'NO', 'RECORDID': first_record_id, 'RECORDFEILD': first_record_feild, 'NEWVALUE': '', 'LOOKUPOBJ': '', 'LOOKUPAPI': '' ,'Offset_Skip_Count':recordEnd,'Fetch_Count':showResultCount,'selected_app_list':JSON.parse(localStorage.getItem("selected_app_item"))}, function (data) {
			var [date_field,assoc,api_name,data4,data5,data6] = [data[3],data[1],data[2],data[4],data[5],data[6]];
			table_id = localStorage.getItem('cont_table_id')
			
			try 
			{ 
				if (date_field == 'NORECORDS'){
					
				}
				else{
			
					$('#assignedUsers_addnew').bootstrapTable('load', date_field ); 
				}
			}
			catch (err) 
			{
				setTimeout(function () {
					$('#assignedUsers_addnew').bootstrapTable('load', date_field);
				}, 5000);
			}
			finally { }	
			$('#assignedapp_footer').html(data6);
			eval(data5); 
		});
	}
	catch(e) 
	{
		console.log(e);
	}
}
///////////////A055S000P01-3370 start
function GS_ADDNEW_POPUP(showResultCount,recordEnd)
{
	var table_id=localStorage.getItem('lookup_ids').split(',')[0];
	var table_id_name=localStorage.getItem('lookup_ids').split(',')[1];
	var lookup_idname=localStorage.getItem('lookup_ids').split(',')[2];
	localStorage.setItem('cont_table_id', table_id)
	try 
	{
		cpq.server.executeScript("SYCTLKPPUP", { 'TABLEID': table_id_name, 'OPER': 'YES','GSCONTLOOKUP': 'GSCONTLOOKUP',
		'TABLENAME':table_id , 'KEYDATA':'','ARRAYVAL':'{}','ATTRIBUTE_VALUE':'','ATTRIBUTE_NAME':'','LOOKUP_ID': lookup_idname,'Offset_Skip_Count':recordEnd,'Fetch_Count':showResultCount}, function (data) {
			var data=data;
			
			try 
			{ 
				if (data == ''){
					
				}
				else{
			
					$('#'+table_id_name).bootstrapTable('load', data ); 
				}
			}
			catch (err) 
			{
				setTimeout(function () {
					$('#'+table_id_name).bootstrapTable('load', data);
				}, 5000);
			}
			finally { }	
			totalRecordsCount=$('#TotalRecAppCount').text();
			if (recordEnd<=0)
				rec_start=1
			else
			    rec_start=recordEnd+1
			rec_end=(rec_start+showResultCount)-1;
			if(rec_end>totalRecordsCount){
				rec_end=totalRecordsCount;
			}
			pg_no=Number((rec_start-1)/showResultCount)+1;
			$('#Rec_App_Start_End').html(rec_start+' - '+rec_end+' of ');
	        $('#popup_footer #page_count').text(parseInt(pg_no));
		});
	}
	catch(e) 
	{
		console.log(e);
	}
}
///////////////A055S000P01-3370 end
//////////////A055S000P01-3655 start
function GS_LKUP_POPUP(showResultCount,recordEnd)
{
	var rec_id = localStorage.getItem('lookup_ids').split(',')[0];
	var table_id_name = localStorage.getItem('lookup_ids').split(',')[1];
	try{
    cpq.server.executeScript("SYLDLKPPUP", {
        "REC_ID": rec_id,
        "LOOKUP": "LOOKUP_ONCHANGE",
        "ELEMENT": "",
        "ATTRIBUTE_NAME": '',
        "ATTRIBUTE_VALUE": '',
        "Offset_Skip_Count":recordEnd,
        "Fetch_Count":showResultCount
    }, function(data) {
    		var data=data;
			try 
			{ 
				if (data == '' || data.length==0){
					return;
				}
				else{
					$('#'+table_id_name).bootstrapTable('load', data ); 
				}
			}
			catch (err) 
			{
				setTimeout(function () {
					$('#'+table_id_name).bootstrapTable('load', data);
				}, 5000);
			}
			finally { }	
			totalRecordsCount=$('#TotalRecAppCount').text();
			if (recordEnd<=0)
				rec_start=1
			else
			    rec_start=recordEnd+1
			rec_end=(rec_start+showResultCount)-1;
			if(rec_end>totalRecordsCount){
				rec_end=totalRecordsCount;
			}
			pg_no=Number((rec_start-1)/showResultCount)+1;
			$('#Rec_App_Start_End').html(rec_start+' - '+rec_end+' of ');
	        $('#popup_footer #page_count').text(pg_no);
    });
	}
	catch(e) 
	{
		console.log(e);
	}
}
//////////////A055S000P01-3655 end
function reload_appUser_val()
{		
	if (localStorage.getItem("selected_app_item").length == 0)
	{	
		var selected_app_item = [];
	}
	else
	{			
		var selected_app_item = JSON.parse(localStorage.getItem("selected_app_item"))			
	}
	$('table#assignedUsers_addnew tbody.app_id tr').each(function(index){
		var classname = $(this).attr('class');
	   
		if( classname=='selected')
		{
			var get_Id= $(this).children('td:nth-child(2)').text();
			get_Idlist.push($(this).children('td:nth-child(2)').text());
		}
		
		if(jQuery.inArray(get_Idlist, selected_app_item) == -1)
		{			
			selected_app_item.push(get_Idlist);
		}
	});	
	var unchecked_app1 = []
	$('table#assignedUsers_addnew tbody.app_id tr').each(function(index){
		var classname = $(this).attr('class');   
	
		if( classname !='selected')
		{
			var unchecked_app= $(this).children('td:nth-child(2)').text();
			unchecked_app1.push($(this).children('td:nth-child(2)').text());
		}
		});
		let difference = selected_app_item.filter(x => !unchecked_app1.includes(x));
		localStorage.setItem("selected_app_item",JSON.stringify(difference))
}
function ShowResultCountFunction_GS_ADD_APP_USERS(ele)
{
	reload_appUser_val();
	var recordsStartAndEnd = $( "#Rec_App_Start_End" ).text();
	var recordEnd = recordsStartAndEnd.split(' ')[0];
	GS_ADDNEW_USERS(showResultCount=parseInt(ele.value), parseInt(recordEnd));
}
function ShowResultCountFunction_GS_ADD_NEW_APP_USERS(ele)
{
	reload_appUser_val();
	var recordsStartAndEnd = $( "#Rec_App_Start_End" ).text();
	var recordEnd = recordsStartAndEnd.split(' ')[0];
	GS_ADDNEW_USERS(showResultCount=parseInt(ele.value), parseInt(recordEnd));
}
function GetNextResultFunction_GS_ADD_NEW_APP_USERS()
{
	
	reload_appUser_val();
	var [showResultCount,recordsStartAndEnd] = [$( "#ShowResultCountsApp option:selected" ).text(),$( "#Rec_App_Start_End" ).text()];
	var TotalRecAppCount=$("#TotalRecAppCount").text()
	var recordEnd = recordsStartAndEnd.split(' ')[2] ;
	if (TotalRecAppCount == recordEnd) {return}
	var recordEnd = parseInt(recordEnd )+1;
	GS_ADDNEW_USERS(showResultCount=parseInt(showResultCount), recordEnd=parseInt(recordEnd) > 0 ? parseInt(recordEnd) : 0);

}


function GetPreviuosResultFunction_GS_ADD_NEW_APP_USERS()
{
	reload_appUser_val();
	var [showResultCount,recordsStartAndEnd] = [$( "#ShowResultCountsApp option:selected" ).text(),$( "#Rec_App_Start_End" ).text()];
	if(recordsStartAndEnd.split(' ')[0]=="1"){return;}
	var recordEnd = parseInt(recordsStartAndEnd.split(' ')[0]) - parseInt(showResultCount);
	GS_ADDNEW_USERS(showResultCount=parseInt(showResultCount), recordEnd=parseInt(recordEnd) > 0 ? parseInt(recordEnd) : 0);
}

function GetFirstResultFunction_GS_ADD_NEW_APP_USERS()
{
	reload_appUser_val();
	var showResultCount = $( "#ShowResultCountsApp option:selected" ).text();
	GS_ADDNEW_USERS(showResultCount=parseInt(showResultCount), recordEnd=0);
}

function GetLastResultFunction_GS_ADD_NEW_APP_USERS()
{
	reload_appUser_val();
	var [showResultCount,totalRecordsCount] = [$( "#ShowResultCountsApp option:selected" ).text(),$( "#TotalRecAppCount" ).text()];
	var recordEnd = parseInt(totalRecordsCount) - parseInt(showResultCount) + 1;
	GS_ADDNEW_USERS(showResultCount=parseInt(showResultCount), recordEnd=parseInt(recordEnd));
}

//////////////A055S000P01-3370 start
function Pagination_GS_ADD_NEW_POPUP(filter_val,len){
	$("#popup_footer").show();
	if(filter_val==""){
        total_rec=localStorage.getItem('total_lookup_records');
        show=$('#ShowResultCountsApp').val();
		start_end="1 - "+show+" of ";
		$('#TotalRecAppCount').text(total_rec);   
	}
	else{
		var start_end=$('#Rec_App_Start_End').text();
		start_end="1 - "+len+" of ";
		$('#TotalRecAppCount').text(len);
	}
	$('#Rec_App_Start_End').text(start_end);
}
function ShowResultCountFunction_GS_ADD_NEW_POPUP(ele,script)
{
	var recordsStartAndEnd = $( "#Rec_App_Start_End" ).text();
	var recordEnd = recordsStartAndEnd.split(' ')[0];
	var val=parseInt(ele.value);
	$('#ShowResultCountsApp').val(val).attr('selected', true);
	if (val < parseInt($('#TotalRecAppCount').text())){
		if(script=='SYCTLKPPUP'){
			GS_ADDNEW_POPUP(showResultCount=parseInt(ele.value), parseInt(recordEnd-1));
			return;
		}
		if(script=='SYLDLKPPUP'){
			GS_LKUP_POPUP(showResultCount=parseInt(ele.value), parseInt(recordEnd-1));
		}
	}
}
function GetNextResultFunction_GS_ADD_NEW_POPUP(script)
{
	var [showResultCount,recordsStartAndEnd] = [$( "#ShowResultCountsApp option:selected" ).text(),$( "#Rec_App_Start_End" ).text()];
	var TotalRecAppCount=$("#TotalRecAppCount").text()
	var recordEnd = recordsStartAndEnd.split(' ')[2] ;
	if (TotalRecAppCount == recordEnd) {return}
	var recordEnd = parseInt(recordEnd);
	if(script=='SYCTLKPPUP'){
		GS_ADDNEW_POPUP(showResultCount=parseInt(showResultCount), recordEnd=parseInt(recordEnd));
		return;
	}
	if(script=='SYLDLKPPUP'){
		GS_LKUP_POPUP(showResultCount=parseInt(showResultCount), recordEnd=parseInt(recordEnd));
	}
}


function GetPreviuosResultFunction_GS_ADD_NEW_POPUP(script)
{
	var [showResultCount,recordsStartAndEnd] = [$( "#ShowResultCountsApp option:selected" ).text(),$( "#Rec_App_Start_End" ).text()];
	if(recordsStartAndEnd.split(' ')[0]=="1"){return;}
	var recordEnd = parseInt(recordsStartAndEnd.split(' ')[0]) - parseInt(showResultCount) -1;
	if(script=='SYCTLKPPUP'){
		GS_ADDNEW_POPUP(showResultCount=parseInt(showResultCount), recordEnd=parseInt(recordEnd) > 0 ? parseInt(recordEnd) : 0);
		return;
	}
	if(script=='SYLDLKPPUP'){
		GS_LKUP_POPUP(showResultCount=parseInt(showResultCount), recordEnd=parseInt(recordEnd) > 0 ? parseInt(recordEnd) : 0);
	}
}

function GetFirstResultFunction_GS_ADD_NEW_POPUP(script)
{
	var showResultCount = $( "#ShowResultCountsApp option:selected" ).text();
	if($('#Rec_App_Start_End').text().split(' ')[0]=="1"){return;}
	if(script=='SYCTLKPPUP'){
		GS_ADDNEW_POPUP(showResultCount=parseInt(showResultCount), recordEnd=0);
		return;
	}
	if(script=='SYLDLKPPUP'){
		GS_LKUP_POPUP(showResultCount=parseInt(showResultCount), recordEnd=0);
	}
}

function GetLastResultFunction_GS_ADD_NEW_POPUP(script)
{
	
	var [showResultCount,totalRecordsCount] = [$( "#ShowResultCountsApp option:selected" ).text(),$( "#TotalRecAppCount" ).text()];
	var recordsStartAndEnd=$('#Rec_App_Start_End').text();
	if (totalRecordsCount == recordsStartAndEnd.split(' ')[2]) {return}
	var recordEnd = Math.floor((parseInt(totalRecordsCount)/parseInt(showResultCount)))*showResultCount;
	if(recordEnd==totalRecordsCount){recordEnd=recordEnd-showResultCount;}
	if(script=='SYCTLKPPUP'){
		GS_ADDNEW_POPUP(showResultCount=parseInt(showResultCount), recordEnd=parseInt(recordEnd));
		return;
	}
	if(script=='SYLDLKPPUP'){
		GS_LKUP_POPUP(showResultCount=parseInt(showResultCount), recordEnd=parseInt(recordEnd));
	}
}
//////////////A055S000P01-3370 end

cpq.events.sub("API:configurator:updated", function(data) {
	var [mode,tabname] = [localStorage.getItem("ErrLog_ACTION"),localStorage.getItem('active_tab_name_text')];
	if  (tabname == 'Error Log'){
		var banner_contents = localStorage.getItem("ERRORLOG_banner");
		var [banner_contents_final,EL_ID,EL_MSG_ID,EL_NAME] = [banner_contents.split(","),banner_contents_final[0],banner_contents_final[1],banner_contents_final[2]];
		
		EL_ID = $("input#ERROR_LOGS_RECORD_ID").val()
		$("#ERRLOG_BANNER_RECORD_ID abbr").text(EL_MSG_ID);
		$("#ERRLOG_BANNER_RECORD_ID abbr").attr('title',EL_MSG_ID);
		
		$("#ERRLOG_BANNER_NAME abbr").text(EL_NAME);
		$("#ERRLOG_BANNER_NAME abbr").attr('title',EL_NAME);
		
		EL_MSG_ID = $("input#ERRORMESSAGE_RECORD_ID").val()
		$("#ERRLOG_BANNER_ID abbr").text(EL_MSG_ID);
		$("#ERRLOG_BANNER_ID abbr").attr('title',EL_MSG_ID);

		EL_NAME = $("input#OBJECT_TYPE").val()
		$("#ERRLOG_BANNER_NAME abbr").text(EL_NAME);
		$("#ERRLOG_BANNER_NAME abbr").attr('title',EL_NAME);
		setTimeout(function() {
			var EL_MSG_ID = $("input#ERRORMESSAGE_RECORD_ID").val()
			$("#ERRLOG_BANNER_ID abbr").text(EL_MSG_ID);
			$("#ERRLOG_BANNER_ID abbr").attr('title',EL_MSG_ID);

			var EL_NAME = $("input#OBJECT_TYPE").val()
			$("#ERRLOG_BANNER_NAME abbr").text(EL_NAME);
			$("#ERRLOG_BANNER_NAME abbr").attr('title',EL_NAME);
			var guidval = $("input#ERROR_LOGS_RECORD_ID").val();
			
			$("#ERRLOG_BANNER_RECORD_ID abbr").text(guidval);
			$("#ERRLOG_BANNER_RECORD_ID abbr").attr('title',guidval);
		}, 2000);
	}
});

function ErrorLogs_enable_disable(id) 
{
	CurrentNodeId = localStorage.getItem("CurrentNodeId");	
	node = $('#ErrorLogstreeview').treeview('getNode', CurrentNodeId);	
	CurrentNodeId = node.nodeId	
	if (CurrentNodeId == undefined)
	{
		$('div#ErrorLogstreeview ul.list-group li.list-group-item').trigger('click');
	}
	CurrentRecordId = node.id;	
	TreeParam = node.text;	
	localStorage.setItem("CurrentNodeId", CurrentNodeId);
	data1 = localStorage.getItem('errorlogTreedatasetnew');
	if (data1 !== null)
	{
		data = data1.split(',');
	}
	$('#ErrorLogstreeview').treeview('selectNode', [ parseInt(CurrentNodeId), { silent: true }]);
	if (CurrentNodeId != '' && CurrentNodeId != null ) {
		TreeParentParam = $('#ErrorLogstreeview').treeview('getParent', CurrentNodeId).text;
		TreeParentNodeId = $('#ErrorLogstreeview').treeview('getParent', CurrentNodeId).nodeId;
		TreeParentNodeRecId = $('#ErrorLogstreeview').treeview('getParent', CurrentNodeId).id;
	}
	if (TreeParentNodeId != '' && TreeParentNodeId != null ) {
		TreeSuperParentParam = $('#ErrorLogstreeview').treeview('getParent', TreeParentNodeId).text;
		TreeSuperParentId = $('#ErrorLogstreeview').treeview('getParent', TreeParentNodeId).nodeId;
		TreeSuperParentRecId = $('#ErrorLogstreeview').treeview('getParent', TreeParentNodeId).id;
	}
	if (TreeSuperParentId != '' && TreeSuperParentId != null ) {
		TreeTopSuperParentParam = $('#ErrorLogstreeview').treeview('getParent', TreeSuperParentId).text;
		TreeTopSuperParentId = $('#ErrorLogstreeview').treeview('getParent', TreeSuperParentId).nodeId;
		TreeTopSuperParentRecId = $('#ErrorLogstreeview').treeview('getParent', TreeSuperParentId).id;
	}
	if (TreeSuperParentId === undefined){
		TreeSuperParentParam = ''
	}
	if (TreeTopSuperParentId === undefined){
		TreeTopSuperParentParam = ''
	}
	localStorage.setItem('ErrorLogTreeParam', TreeParam);
	localStorage.setItem('ErrorLogTreeParentParam', TreeParentParam);
	localStorage.setItem('ErrorLogNodeTreeSuperParentParam', TreeSuperParentParam);
	localStorage.setItem('ErrorLogTopSuperParentParam', TreeTopSuperParentParam);
	localStorage.setItem('ErrorLogParentNodeRecId', TreeParentNodeRecId);
	localStorage.setItem('ErrorLogTreeSuperParentRecId', TreeSuperParentRecId);
	localStorage.setItem('ErrorLogTopSuperParentRecId', TreeTopSuperParentRecId);
	if(CurrentNodeId == undefined || TreeParam == 'Error Log Information' )
	{		
		
		$('.Detail').removeClass('disp_none');
		$('.Detail').addClass('disp_blk');

		
		$('.ErrorLog_Related_Detail, .Related').removeClass('disp_blk');
		$('.ErrorLog_Related_Detail, .Related').addClass('disp_none');
		var Primary_Data = localStorage.getItem('Error_log_id_primarydata');
		if (document.getElementById("header_label")) 
		{
			//document.getElementById("header_label").innerHTML = TreeParam;
		}
		var [mode, tabname] = [localStorage.getItem("ErrLog_ACTION"),localStorage.getItem('active_tab_name_text')];
		if (mode == 'VIEW' && mode !='' )
		{
			try
			{
				cpq.server.executeScript("SYPROFVIEW", { 'ER_RECORD_ID':Primary_Data,'ER_MODE':'VIEW','TAB_NAME':tabname }, function (dataset) {
					var [datas,data1,EL_guidtokey] = [dataset[0],dataset[1],dataset[2]];
					localStorage.setItem("EL_guidtokey",EL_guidtokey);
					if(document.getElementById("ErrorLog_Detail"))
					{
						document.getElementById("ErrorLog_Detail").innerHTML = datas;
					}
				});		

				EL_ID = $("input#ERROR_LOGS_RECORD_ID").val()
				$("#ERRLOG_BANNER_RECORD_ID abbr").text(EL_ID);
				$("#ERRLOG_BANNER_RECORD_ID abbr").attr('title',EL_ID);
				
				EL_MSG_ID = $("input#ERRORMESSAGE_RECORD_ID").val()
				$("#ERRLOG_BANNER_ID abbr").text(EL_MSG_ID);
				$("#ERRLOG_BANNER_ID abbr").attr('title',EL_MSG_ID);

				EL_NAME = $("input#OBJECT_TYPE").val()
				$("#ERRLOG_BANNER_NAME abbr").text(EL_NAME);
				$("#ERRLOG_BANNER_NAME abbr").attr('title',EL_NAME);
			}
			catch(e){
				console.log(e);
			}
		}
	}
}
function Roles_AddNewSave()
{
	var modes = localStorage.getItem("Role_ACTION");
	if ((modes == "ADD NEW" && modes!='') || (modes == 'EDIT' && modes!=null && modes!='') )
	{
		var [dict_new,TableId,table_before_div,RecordId_value,refresh] = [{},$("#righttreeview table").attr('id'),$("#righttreeview").children().next().children().next().attr('id'),$("table tbody tr td input").val(),localStorage.getItem("REFRESH")];
		localStorage.setItem("Role_ACTION","");
		$("#righttreeview #container #"+table_before_div+" table#"+TableId+" tbody tr td input").each(function () {
			if ($(this).attr('type') == 'CHECKBOX') 
			{
				dict_new[$(this).attr('id')] = String($(this).prop("checked"));
			} 
			else
			{
				id_val = $(this).attr('id');
				dict_new[$(this).attr('id')] = $("#righttreeview #container table#" +TableId+" tbody tr td input#"+id_val).val();
			} 
		});
		$("#righttreeview #container #"+table_before_div+" table#"+TableId+" tbody tr td textarea").each(function () {
				id_val = $(this).attr('id');
				dict_new[$(this).attr('id')] = $("#righttreeview #container table#" +TableId+" tbody tr td textarea#"+id_val).val();				
		});
		try
		{
			//A043S001P01-9058 043S001P01-9059 START
			if ($("input#ROLE_ID").val() == "" || $("input#ROLE_NAME").val() == "" || $("input#ROLE_DESCRPTION").val() == "")
			{
				
				$('#alert_msg').addClass('disp_blk_mrg10');
				localStorage.setItem("Role_ACTION",modes);
			}
			else
			{
				try
				{
				cpq.server.executeScript("SYPROFSAVE", { 'RECORD': JSON.stringify(dict_new), 'TableId':'SYROMA','MODE':modes,'REC_VALUE':RecordId_value}, function (data) {			
					RecordId = data['ROLE_RECORD_ID']
					localStorage.setItem("EditRecID",RecordId)
					if(RecordId != undefined) 
					{
					RecordId = data['PROFILE_RECORD_ID']
					$("#PROFILE_BANNER_RECORD_ID abbr").text(RecordId);
					$("#PROFILE_BANNER_RECORD_ID abbr").attr('title',RecordId);
					
					Pro_ID = $("input#ROLE_ID").val()
					$("#PROFILE_BANNER_ID abbr").text(Pro_ID);
					$("#PROFILE_BANNER_ID abbr").attr('title',Pro_ID);

					Pro_Name = $("input#ROLE_NAME").val()
					$("#PROFILE_BANNER_NAME abbr").text(Pro_Name);
					$("#PROFILE_BANNER_NAME abbr").attr('title',Pro_Name);
					localStorage.setItem("Role_ACTION","ADD_NEW_VIEW")
					}
					//localStorage.setItem("Profile_ACTION","ADD_NEW_VIEW")
					
						localStorage.setItem("Role_ACTION","ADD_NEW_VIEW")
						RecordId = data['ROLE_RECORD_ID']
						localStorage.setItem("ROLE_RECORD_ID_ADD_NEW",RecordId)
						localStorage.setItem("RoleRecId",RecordId)
						if((RecordId != null && RecordId!='')|| modes=='EDIT' )
						{	
							var Role_Rec_ID = localStorage.getItem('EditRecID')
							try
							{
								cpq.server.executeScript("SYPROFVIEW", {'TAB_NAME':'Roles','RL_REC_ID':Role_Rec_ID,'RL_MODE':'VIEW'}, function (dataset) {
									data0 = dataset[0];
									data1 = dataset[1];
									if (refresh!='' && refresh=='TRUE' && refresh!= null && refresh!='FALSE')
									{
										$("#MM_ALL_REFRESH").click();
										localStorage.setItem("REFRESH","FALSE")
									}
									if(document.getElementById("righttreeview"))
									{
										document.getElementById("righttreeview").innerHTML = data0;
									}
								});
							}
							catch(err){
								console.log(err);
							}
						}
				});
				}
				catch(e){
					console.log(e);
				}
			}
		}
		//A043S001P01-9058 043S001P01-9059 END
		catch(e){
			console.log(e);
		}
	}
}
function Roles_view_RL(ele){
	x = localStorage.getItem('CurrentNodeId')
	node = $('#Rolestreeview').treeview('getNode', [parseInt(x), { silent: true } ]);
	$('#Rolestreeview').treeview('expandNode', [ 1, {silent: true } ]);
	var childrenNodes = _getChildren(node);
	var treeparam = node.text
	if (treeparam == "Users"){
		xxxx = $(ele).closest('tr').children('td:nth-child(4)').text().trim();
	}
	$(childrenNodes).each(function(){
    y = $('#Rolestreeview').treeview('getNode', [ this.nodeId, { silent: true } ]);
	if (y.id == xxxx){
	vi = y.nodeId
	$('#Rolestreeview').treeview('selectNode', [parseInt(vi), { silent: true } ]);
	localStorage.setItem('CurrentNodeId',vi)
	Roles_enable_disable('Rolestreeview')
	}
	});
}
function Roles_enable_disable(id)
{
	CurrentNodeId = localStorage.getItem("CurrentNodeId");
	node = $('#Rolestreeview').treeview('getNode',CurrentNodeId)
	CurrentNodeId = node.nodeId	
	if (CurrentNodeId == undefined)
	{
		$('div#Rolestreeview ul.list-group li.list-group-item').trigger('click');
	}
	CurrentRecordId = node.id;
	var TreeParam = node.text;
	localStorage.setItem("CurrentNodeId", CurrentNodeId);
	data1 = localStorage.getItem('syrolesnew');
	if (data1 !== null)
	{
		data = data1.split(',');
	}
	if (CurrentNodeId != '' && CurrentNodeId != null ) {
	TreeParentParam = $('#Rolestreeview').treeview('getParent', CurrentNodeId).text;
	TreeParentNodeId = $('#Rolestreeview').treeview('getParent', CurrentNodeId).nodeId;
	TreeParentNodeRecId = $('#Rolestreeview').treeview('getParent', CurrentNodeId).id;
	}
	localStorage.setItem('RoleTreeParam', TreeParam);
	localStorage.setItem('RoleTreeParentParam', TreeParentParam);
	if(jQuery.inArray(TreeParam, data) !== -1 && TreeParam != 'Role Information')
	{
		if (TreeParam == 'Users'){
			loadRelatedList('SYOBJR-94452','righttreeview')
		}
		
	}
	else if(TreeParentParam == 'Users' && TreeParam != 'Role Information'){
		try{
			cpq.server.executeScript("SYPROFVIEW", { 'TAB_NAME':'Roles','US_REC_ID':CurrentRecordId,'US_MODE':'VIEW' }, function (dataset) {
					data0 = dataset[0];
					data1 = dataset[1];
					$('#righttreeview').html(data0);
			});		
		}
		catch(e){
				console.log(e);
			}
	}
	else if(TreeParam == 'Role Information'){
		var role_id = localStorage.getItem('RoleRecId');
		mode = localStorage.getItem('Role_ACTION')
		if (mode != 'ADD NEW' && mode != ''){
		try
			{
				cpq.server.executeScript("SYPROFVIEW", { 'TAB_NAME':'Roles','RL_REC_ID':role_id,'RL_MODE':'VIEW' }, function (dataset) {
					data0 = dataset[0];
					data1 = dataset[1];
					$('#righttreeview').html(data0);
			});		
			}
			catch(e){
				console.log(e);
			}
		}
		
	}
	
		
}

function ErrorLogopencreate(ele)
{
	localStorage.setItem("ErrorLog_EDITACTION", "GRID_EDIT");
	localStorage.setItem('ErrorLog_ACTION',"EDIT")
	localStorage.setItem("REFRESH","TRUE")
	var ids = $(ele).closest('tr').attr('id');
	var [Primary_Data,id_primarydata,Primary_Data_list,Profile_Record_ID,Profile_ID,Profile_Name] = [$("#" + ids + " td:nth-child(3)").text().trim(),$("#" + ids + " td:nth-child(3)").text().trim(),$("#" + ids + " td:nth-child(3)").text().trim().replace(/\s+/, " ").split(' '),$("#" + ids + " td:nth-child(3)").text().trim(),$("#" + ids + " td:nth-child(4)").text().trim(),$("#" + ids + " td:nth-child(5)").text().trim()];
	localStorage.setItem("id_primarydata", id_primarydata);
	if (Primary_Data_list.length > 1) 
	{
		Primary_Data = Primary_Data_list[0]
	}
	
	// BANNER_CONTENT VALUES STARTS
	localStorage.setItem("PROFILE_BANNER",Profile_Record_ID+','+Profile_ID+','+Profile_Name);
	// BANNER_CONTENT VALUES ENDS
	try 
	{
		cpq.server.executeScript("SYPRCTEDIT", {
		'RECORD_ID': Primary_Data,
		'TabNAME': 'Error Logs',
		'MODE': 'EDIT',
		'LOAD':'Treeload'
		}, function(dataset) {
			var datas = dataset;			
			$("#MM_ALL_REFRESH").click();
			$('div#ErrorLogstreeview ul.list-group li.list-group-item').trigger('click');
			setTimeout(function(){
				if (document.getElementById("ErrorLog_Detail"))
				{
					document.getElementById("ErrorLog_Detail").innerHTML = datas;
				}
			}, 5000);

		});
	} 
	catch (e) {
		console.log(e);
	}
}

setInterval(function(){
		var check_ul = $('div#header_label ul.breadcrumb').text();
		if(!check_ul)
		{
			var txt = $('div#Profilestreeview ul.list-group .node-selected').text();
			$('div#header_label ul.breadcrumb').html('<a onclick="breadCrumb_redirection(this)"><abbr title="'+txt+'">'+txt+'</abbr></a>');
		}
}, 1000);

function profile_breadCrumb_redirection(leftNode) {
    var left_text = $(leftNode).text();
	
    $('ul.list-group li.list-group-item.node-Profilestreeview').each(function (index) {
        var nodeText = $(this).text();
		
        if (nodeText == left_text) {
			
            $(this).trigger('click');
        }
    });
}


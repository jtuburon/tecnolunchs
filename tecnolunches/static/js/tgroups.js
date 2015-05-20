function show_groups(){
	enableTab(2);
	$.get("groups/", function( data ) {
		$("#main_container").html(data);
	});
}

function show_group_details(group_id){
	$.get("group_details/"+ group_id, function( data ) {
		$("#groups_details").html(data);
	});
}

function show_menues(){
	enableTab(5);
	$.get("menues/", function( data ) {		
		$("#main_container").html(data);		
		$(".menu-available-sw").bootstrapSwitch();
		$(".menu-available-sw").on('switchChange.bootstrapSwitch', function(event, state) {
			data= this.name.split("-");
			menu_id= data[data.length-1];
			set_availability(menu_id, state)			
		});		
	});
}

function add_menu_item(){	
	$('#menu_item_modal').modal('show');
	$('#menu_item_modal').on('shown.bs.modal', function (e) {			  
		$.get("menues/new/", function( data ) {
			$("#menu_modal_body").html(data);
		});
	});
}

function edit_menu_item(menu_id){	
	$('#menu_item_modal').modal('show');
	$('#menu_item_modal').on('shown.bs.modal', function (e) {			  
		$.get("menues/find/"+ menu_id+"/", function( data ) {
			$("#menu_modal_body").html(data);
		});
	});
}

function set_availability(menu_id, status){
	$.get("menues/setavailable/"+menu_id+"/"+status+"/", function( data ) {						
		show_menues();
	});
}

function show_queues(){
	enableTab(3);
	$.get("queues/", function( data ) {
		$("#main_container").html(data);
	});
}

function show_settings(){
	enableTab(4);
	$.get("admin/", function( data ) {
		$("#main_container").html(data);
	});
}

function save_general_settings(){	
	$.post("admin/save_gral_settings/", 
		{
			group_size: $("#group_size").val(), 
			final_time: $("#final_time").val(), 
			csrfmiddlewaretoken: '{{ csrf_token }}'
		},
		function(data) {		
			$("#general_settings").html(data);				
		}
	);
}

function save_menu_item(){	
	$.post("menues/save/", 
		{menu_item: $("#menu_id").val(), name: $("#menu_name").val(), csrfmiddlewaretoken: '{{ csrf_token }}'},
		function(data) {		
			$('#menu_item_modal').modal('hide');
			$('#menu_item_modal').on('hidden.bs.modal', function (e) {			  
				show_menues();
			});
						
		}
	);
	
}

function show_today_admin(){
	enableTab(7);
	$.get("admin/today/", function( data ) {		
		$("#main_container").html(data);		
		$(".accomplishment-sw").bootstrapSwitch();
		$(".accomplishment-sw").on('switchChange.bootstrapSwitch', function(event, state) {
			data= this.name.split("-");
			group_member_id= data[data.length-1];			
			set_accomplishment_state(group_member_id, state);
		});
	});
}

function set_accomplishment_state(group_member, state){
	$.get("admin/today/group_member/set_accomplishment/"+group_member+"/"+state, function( data ) {						
		show_today_admin();
	});
}

function show_members(){
	enableTab(6);
	$.get("members/", function( data ) {
		$("#main_container").html(data);
		$(".member-permanent-sw").bootstrapSwitch();
		$(".member-permanent-sw").on('switchChange.bootstrapSwitch', function(event, state) {
			data= this.name.split("-");
			member_id= data[data.length-1];
			set_member_type(member_id, state)			
		});		
	});

}


function set_member_type(member_id, type){
	$.get("members/settype/"+member_id+"/"+type+"/", function( data ) {						
		show_members();
	});
}

function request_my_lunch(){
	enableTab(1);
	$.get("requests/", function( data ) {
		$("#main_container").html(data);	
	});
	
}




function enableTab(tabID){
	for(id=1 ; id<=7; id++){
		if(tabID== id){
			$('#op0'+id).toggleClass("active");
		}else{
			$('#op0'+id).removeClass();
		}
	}
}
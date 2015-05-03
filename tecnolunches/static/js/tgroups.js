function show_groups(){
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
}

function edit_menu_item(menu_id){	
	$('#menu_item_modal').modal('show');
}

function set_availability(menu_id, status){
	$.get("menues/setavailable/"+menu_id+"/"+status+"/", function( data ) {						
		show_menues();
	});
}

function show_queues(){
	$.get("queues/", function( data ) {
		$("#main_container").html(data);
	});
}

function show_settings(){
	$.get("admin/", function( data ) {
		$("#main_container").html(data);
	});
}

function save_general_settings(){	
	$.get("admin/save_gral_settings/"+ $("#group_size").val() + "/", function( data ) {				
		$("#general_settings").html(data);
	});
}

function save_menu_item(){	
	$.post("menues/save/", 
		{ menu_item: -1, name: $("#menu_name").val(), csrfmiddlewaretoken: '{{ csrf_token }}'},
		function(data) {		
			$('#menu_item_modal').modal('hide');
			$('#menu_item_modal').on('hidden.bs.modal', function (e) {			  
				show_menues();
			});
						
		}
	);
	
}

function show_today_admin(){
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
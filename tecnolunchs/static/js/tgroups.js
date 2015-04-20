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

function show_today_admin(){
	$.get("admin/today/", function( data ) {
		$("#main_container").html(data);
		$("#accomplishment-sw").bootstrapSwitch();
	});
}

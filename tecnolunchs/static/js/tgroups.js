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
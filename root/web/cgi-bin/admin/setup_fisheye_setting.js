var meun = "Fisheye Setting";
var settingList = ["mount_type", "source_type" ];

function initUI() {

}
function initValue() {
	var value;
	settingList.forEach(function(id){
		var obj  =  $("#" + id );
			$("[name=" + id + "][value=" + fishInfo[id] + "]").prop("checked", true);
	});
}
function initEvent() {
	$("#btOK").click( function(){
		var data = "msubmenu=fisheye&action=apply";
		var new_value;;
		var changed = false;
		var OK = /OK/;
		settingList.forEach(function(id){
			new_value = $("[name=" + id + "]:checked").val()
			if(  fishInfo[id] != new_value ){
				data += "&" + id + "=" + new_value;
				changed = true;	
			}
		});
		if(changed ){
			$.ajax({
				type:"get",
				url: "/cgi-bin/admin/fisheye.cgi",
				data: data,
				success: function(resp){
					if( OK.test(resp) ){
						settingSuccess(menu);
						refreshMenuContent()
					} else {
						settingFail(menu);
					}
				},
				error: function(resp){
					settingFail(menu, "Connection Error. retry again!" + resp);
				}

			});
		} else {
			settingFail(menu, "Nothing change!");
		}
	});
}

function onLoadPage() {
	initUI();
	initValue();
	initEvent();
}
$(document).ready( function() {
    onLoadPage();
});

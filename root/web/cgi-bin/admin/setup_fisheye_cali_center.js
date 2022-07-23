var meun = "Calibration Center";
var settingList = ["pos_x", "pos_y", "radius", "finded" ];

function initUI() {

}
function initValue() {
	var value;
	settingList.forEach(function(id){
		var obj  =  $("#" + id );
		if(obj.length != 0){
			if( obj.get(0).tagName == "LABEL" ){
				if( id == "finded" ) {
					value = fishInfo['cali_center']['finded'] == 0 ? "Default" : "Calibration";
				} else  {
					value = fishInfo['cali_center'][id];
				}
				$("#" + id ).append( value );
			}
		} else {
			$("[name=" + id + "][value=" + fishInfo[id] + "]").prop("checked", true);
		}
	});
}
function initEvent() {
	$("#btAutoCalibration").click( function(){
		var data = "msubmenu=cali_center&action=run";
		var OK = /OK/;
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
	});
	$("#btDefault").click( function(){

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

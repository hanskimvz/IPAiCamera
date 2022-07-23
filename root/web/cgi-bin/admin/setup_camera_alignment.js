var VLCManager = new VLC("image_box", capInfo, VideoInputInfo, "lstProfile");
if(typeof(VLCManager) == undefined ){
	console.log("VLCManager initialize fail");
	VLCManager = null;
}
function onLoadPage() {
	if(typeof(VLCManager) == undefined ){
		console.log("VLCManager initialize fail");
		VLCManager = null;
	}
	getJson();
	initLanguage();
	VLCManager.setPlayInfo(userInfo, rtspPort);
	var VLC  = VLCManager.init(1);
	if(VLC){
		VLCManager.doGo();
	}
    else {
        VLCManager.setPlayInfo(userInfo, rtspPort);
        VLC = VLCManager.initPreview("image_box", true);

    }
	initUI();
	initEvent();
	initValue();
}
function initUI(){
	var obj = '',
		i = 0;
	for( i=0 ; i < capInfo.video_in ; i++) {
		obj += '<div style="width:25%; display:inline-block;text-align:center;" id="';
		obj += Number(i+1) + '">';
		obj += '<button id="clockwise' + i;
		obj += '"class="button clockwise" name="buttons" value="0">';
//		obj += getLanguage("setup_counter_clock_wise") + '</button>';
		obj += '</button>';
		obj += ' <button id="counterclockwise' + i;
		obj += '"class="button counterclockwise" name="buttons" value="1">';
//		obj += getLanguage("setup_clock_wise") + '</button>';
		obj += '</button>';
		obj += '</div>';
	}
	$("#image_box").after(obj);
}

function initEvent(){
	$("button[name=buttons]").mousedown(function(e){
		var types = $("input[type=radio][name=types]:checked").val();
		var src = $("#" + e.currentTarget.id).parent()[0].id;
		var dir = e.currentTarget.value;
		_ajax(src, types, dir);
	}).mouseup(function(e){
		var types = $("input[type=radio][name=types]:checked").val();
		var src = $("#" + e.currentTarget.id).parent()[0].id;
		var dir = e.currentTarget.value;
		if( types == 'continous'){
			_ajax(src, 'stop', dir);
		}
	});
}

function _ajax(src, types, dir) {
	var params = {
		msubmenu: "alignment",
		source : src,
		direction : dir,
		type : types,
	};
	$.ajax({
		type:"get",
		url: "/cgi-bin/admin/camera.cgi",
		data: params,
		success: function(resp){
			console.log(resp);
		}, 
		error: function(resp){
			console.log(resp);
		}
	});
}

function initValue(){

}

$(document).ready( function(){
	onLoadPage();
});

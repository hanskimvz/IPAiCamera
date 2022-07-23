{
var menu = getLanguage("setup_camera_profile_conf");
var debug_level=0;
var count;
var select_item;

function init() {
	//MJ.id = 0;
	$("#vin_source").attr("disabled", true);
	$("#vin_source option:eq("+MJ.id+")").prop("selected", "selected");
	initUI();
	initValue();
	initEvent();
}
function initUI()
{	
	$("tr[name=list_items]").remove();
	var cmd = '',
		i, 
		count=0;
	for( i=0 ; i < profileInfo.length ; i++ ){
		if( profileInfo[i].id == 0 )
			continue;
		cmd += "<tr name='list_items' class='list_items' id=" + profileInfo[i].id + "><td>";
		cmd += "<label for='profile" + i + "'></label>" + getLanguage("setup_camera_profile") + Number(++count) + "</td>";
		cmd += "<td id='fixed" + i + "'></td>";
		cmd += "<td><label id='name" + i + "'></td></tr>";
	}
	$("#profile").append(cmd);
	initLanguage();
}

function initValue()
{
	profileInfo.forEach(function(obj, index){
		//$("#profile" + index).text(obj.name);
		$("#fixed" + index).text(obj.fixed == 1 ? "O" : "X");
		$("#name" + index).text(obj.name);
	});
}

function initEvent() 
{
	function _ajax(action) {
		var data;
		var param;
		if( action == "add") {
			data = prompt(getLanguage("setup_req_profile_name"));
			if( data == null ) return;
			if(!checkCharacters("camera_profile",data)){
                var pop_msg = "You can not enter spaces in your profile.";
                settingFail(menu,pop_msg);
                refreshMenuContent();
                return 0;
            }
            param = "msubmenu=profiles&action=" + action + "&name=" + encodeURIComponent(data);
            
		}
//		else if( action == "modify") {
//			data = prompt("Please Enter the Profile Name");
//			if( data == null ) return;
//			var id = $(".sel_list_item").attr('id');
//			if( typeof(id) == 'undefined' ) {
//				settingFail(getLanguage("msg_profile_choose_profile"));
//				return;
//			}
//			profileInfo.forEach(function(e){ 
//				if(  id == e.id ){ 
//					param = "msubmenu=profiles&action=" + action + "&id=" + e.id +"&name=" + encodeURIComponent(data);
//				}
//			});
//		}
		else if( action == "delete"  || action == "apply") {
			var id = $(".sel_list_item").attr('id');
			if( typeof(id) == 'undefined' ) {
				settingFail(getLanguage("msg_profile_choose_profile"));
				return;
			}
			profileInfo.forEach(function(e){ if(  id == e.id ) data = e.id; });
			param = "msubmenu=profiles&action=" + action + "&id=" + data;
		} else {
			settingFail(getLanguage("msg_profile_choose_profile"));
			return;
		}
		$.ajax({
			type : 'get',
			url  : '/cgi-bin/admin/camera.cgi',
			data : param,
			async : false,
			cache	: false,
			success : function(args) {
				var pattern = /OK/g;
                console.log("success: "+args);
				if( pattern.test(args) == true){
					settingSuccess(menu);
					refreshMenuContent();
				}else{
					settingFail(menu);
				}
			},
			error 	: function(args) {
				settingFail(menu, null);
			},
		});
	}
	$("tr[name=list_items]").on("click", function(e) {
		$("tr[name=list_items]").removeClass("sel_list_item");
		$("#" + e.delegateTarget.id).addClass("sel_list_item");
		select_item = Number($(".sel_list_item").attr("val"));
	});
	$("button").click(function(e) {
		_ajax(e.currentTarget.value);
	});
}
}

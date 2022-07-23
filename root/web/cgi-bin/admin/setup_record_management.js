try {
var menu = getLanguage("setup_record_config");
var MaxRecordingJob = capInfo.max_record;
var select_item = -1;
var MODE = "list";
var SettingList = ["enabled",  "file_type", "storage_device", "continous", "pre_duration", "post_duration"];
var data;
var translate = { "storage_type" : 
	[ getLanguage("setup_none"), getLanguage("setup_sdcard") ]
};

/* ------------------------------------- INITIALIZING END --------------------------------------- */
function ChangeUI(view){
	if( view == "add" || view == "modify") {
		$("#record_index").css("display", "none");
		$("#record_add_modify").css("display", "block");	
	} else {
		MODE = "LIST";
		$("#record_index").css("display", "block");
		$("#record_add_modify").css("display", "none");	
	}
}
function initSettingsValue(index){
	if( typeof(index) == "undefined" ) {
		$("#enabled_on").trigger("click");
		//$("#stream_id").val(0);
        if( capInfo["board_chipset"]== "amba_s2lm55" || capInfo["board_chipset"]== "amba_s2l66" ){
		    $("#file_type").val(0);

        }
        else{
		    $("#file_type").val(1);
            
        }
		$("#stroage_type").val(1);
		$("#storage_device").val(0);
		$("#continous_off").trigger("click");
        console.log($("#continous_off").trigger("click"));
		$("#pre_duration").val(5);
		$("#post_duration").val(5);
	}else{
		var val = new Value();
		val.setValue(SettingList, data[index], translate);
        if( capInfo["board_chipset"]== "amba_s2lm55" || capInfo["board_chipset"]== "amba_s2l66" ){
		    $("#file_type").val(0);

        }
        else{
		    $("#file_type").val(1);
            
        }
		$("#storage_device").trigger('change');
        $("#storage_device").attr("disabled",true);
		if( $("input[name=continous]:checked").val() == 0 ) {
			$("#pre_duration").attr("disabled", false);
			$("#post_duration").attr("disabled", false);
		} else {
			$("#pre_duration").attr("disabled", true);
			$("#post_duration").attr("disabled", true);
		}
	}
}
function initUI() {
	// init Target Stream	
	var option = "<option value='-1'>" + getStorageTypeName(0) + "</option>";
	//for(var i=0; i < mStorageDeviceConf.length ; i++) {
	for(var i=0; i < capInfo.have_sdcard ; i++) {
		option += "<option value='"+ (i) + "'>";
		option += getStorageTypeName(mStorageDeviceConf[i].Type);
		option += " " + (i+1) +"</option>";
	}
	$("#storage_device").append(option);

    var select_file_type= document.getElementById("file_type");
	if( capInfo["board_chipset"]== "amba_s2lm55" || capInfo["board_chipset"]== "amba_s2l66" ){
		select_file_type.remove(1);
	}else{
		select_file_type.remove(0);
	} 

	var theader = $(".headline").find('th');
	var width =$('.headline').width() / theader.length;
	theader.css("width", width + 'px');
}
function setEventForListItem(){
	$("tr[name=list_items]").on("click", function(e) {
		$("tr[name=list_items]").removeClass("sel_list_item");
		$("#" + e.delegateTarget.id).addClass("sel_list_item");
	});
}
function disabledButton(cmd)
{
	if( cmd !== true && cmd != false ) return -1;
	$("button").attr("disabled", cmd);
}
function initEvent() {
	var  pop_msg ="";
	setEventForListItem();
	var org_stream ;
	org_stream = data[0].target_stream ;

	$("#storage_device").change(function(e){
		var idx = e.currentTarget.value;
		var storage_type = 0;
		if( idx >= 0 ) {
			storage_type = mStorageDeviceConf[idx].Type;
		}
		$("#storage_type").val(getStorageTypeName(storage_type));
	});
	$("#save_global_setting").click(function(){
		if ( org_stream == $("#target_stream").val() ){
			settingFail(menu, getLanguage("msg_nothing_changed"));
			disabledButton(false);
			return ;
		}
		var data = "msubmenu=manage&target_stream=" + $("#target_stream").val();		

		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/record.cgi",
			data: data,
			success: function(msg){
				var test = /OK/;
				if(test.test(msg)){
					settingSuccess(menu, null);
				} else {
					settingFail(menu, null);
				}
				refreshMenuContent();
			},
			error: function(e){
				console.log(e);
			}
		});
	});
	$("[name=continous]").click(function(e){
		if( e.delegateTarget.value == 0 ) {
			$("#pre_duration").attr("disabled", false);
			$("#post_duration").attr("disabled", false);
		} else {
			$("#pre_duration").attr("disabled", true);
			$("#post_duration").attr("disabled", true);
		}
	});
	$("#modify").click(function(e){
		select_item = getSelectListItem();
		if( select_item < 0 )
		{
			pop_msg = getLanguage("msg_select_item");
			settingFail(menu, pop_msg);
			return ;
		}
		MODE = "apply";
		ChangeUI("modify")
		initSettingsValue(select_item);
	});
	$("#save").click(function(e){
		var x = $('#pre_duration').val();
		var y = $('#post_duration').val();
		if (!x.match(/^[0-9]+$/))
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			$('#pre_duration').focus();
			return 0;
		}
		if (!y.match(/^[0-9]+$/))
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			$('#post_duration').focus();
			return 0;
		}
		disabledButton(true);
		var datas = "";
		var val = new Value();
		for( var i = 0 ; i < SettingList.length ; i++) {
			datas += SettingList[i] + "=" + val.getValue(SettingList[i]) + "&";
		}
		if(datas.length != 0) {
			datas = "msubmenu=manage&action=" + MODE + "&"+ datas;
		} else {
			settingFail(menu, getLanguage("msg_nothing_changed"));
			disabledButton(false);
			return ;
		}
		if( MODE === "apply") {
			datas += "&index=" + data[select_item].index;
		}
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/record.cgi",
			data: datas,
			success: function(msg){
				var tmp= msg.trim().split('\n');
				var response = tmp[0];
				var error_code = tmp[1];
				if(response == "OK") {
					settingSuccess(menu, null);
					refreshMenuContent();
				} else {
					settingFail(menu, tmp[1]);
				}
			},
			error: function() {
				settingFail(menu, getLanguage("msg_fail_retry"));
				refreshMenuContent();
			}
		});
		disabledButton(false);
	});
	$("#cancel").click(function(e){
		ChangeUI(e.target.id);
	});
	$("[name=always]").click(function(e){ 
		$("[name=schedule]").attr('disabled', e.target.value == 0 ? false : true);
	});
	$("#action_type").change(function(e){
		EventTypeManager[e.target.value].onLoadPage();
	});
	$("#shour").change(function(e){
		$("#ehour").find("option").remove();
		for(var i= e.target.value; i < 24 ; i++ ){
			$("#ehour").append("<option val=" + i + ">"+i +"</option>")
		}
	});
}

function initValue() {
	var content;
	var file_type, stroage, continous, enabled, storage_device;
	var i;

	$("tr[name=list_items]").remove();
	$("#target_stream").val(data[0].target_stream);
	var length = data.length -1;
	var max = length > capInfo.max_record ? capInfo.max_record : length;
	// var theader = $(".headline").find('th');
	// var width = Math.floor($('.headline').width() / theader.length);
	// theader.css("width", width + 'px');

	for(i=1 ; i <= max ; i++) {
		enabled = data[i]['enabled'] == 1 ? "O" : "X";
		continous = data[i]['continous'] == 0 ? getLanguage("EVENT_OFF") : getLanguage("EVENT_ON") ;

		if( data[i]['file_type'] == 0 ){
			file_type = "TS";
		} else if( data[i]['file_type'] == 1 ) {
            file_type = "MP4";
        } else {
			file_type = "Unknown";
		}

		storage = translate.storage_type[ data[i]['storage_type'] ];

		if( data[i]['storage_device'] == -1 ){
			storage_device = getLanguage("setup_none");
		}
		else {
			storage_device = getLanguage("storage") + Number(data[i].storage_device+1);
		}

		content = 	"<td headers='th1' class='th1'>" + data[i]['name'] + "</td>";
		content +=  "<td headers='th2' class='th2'>" + enabled + "</td>";
		content += 	"<td headers='th3' class='th3'>" + file_type + "</td>";
		content += 	"<td headers='th4' class='th4'>" + storage_device + "</td>";
		content +=  "<td headers='th5' class='th5'>" + continous + "</td>";
		$("#result_table").append("<tr class='list_items' name='list_items' id='list_item"+ i + "' val='" + i + "'>" + content +"</tr>");
	}
}
function initDependency() {
	if( capInfo.is_proxy_camera ) {
		$("#storage_device").attr("disabled", true);
	}
}

function onLoadPage() {
	initUI();
	initDependency();
	initValue();
	initEvent();
}
$(document).ready( function() {
	$.ajaxSetup({async: false});
	data = getInformation($(".select_minor").attr("id"));
	$.ajaxSetup({async: true});
	onLoadPage();
});
}
catch(e) {
	console.trace(e);
}

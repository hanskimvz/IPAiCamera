try {
var STORAGE_TYPE_NFS = 2;
var format_state = false;
var menu;
var last_menu = $(".select_minor").attr("id");
var timeOutId = 0;
var moStorageStatus;
var CVal = new Value();

var mStorageDevice = {
	selItem : 0 ,
	"toggleUI" : function(){
		$object = $("#storage_infomation");
		if( $object ) {
			var display = $object.css("display");
			$object.css("display",  display == "block" ? "none" : "block");
			$("#storage_list").css("display", display == "block" ? "block" : "none");
			mStorageDevice.setValue(mStorageDeviceConf[mStorageDevice.selItem]);

			var type =  mStorageDeviceConf[mStorageDevice.selItem].Type == 2 ? true : false;
			$("#format").attr("disabled", type);			
		}
	},
	"init" : function() {
		var idx = 0;
		mStorageDeviceConf.forEach(function(Device) {
			var content ='';
			if( Device.hasOwnProperty("Type")){
				if( Device.Type != 0 ){
					content += "<tr class='list_items' name='list_items' id=storage" + idx + ">";
					content += "<td>" + getStorageTypeName(Device.Type) + Number(idx+1)  +"</td>"
					content += "<td id='mount" + idx + "'>-</td>";
					content += "<td id='size" + idx + "'>-</td>";
					content += "<td id='used" + idx + "'>-</td>";
					content += "<td id='avail" + idx + "'>-</td>";
					content +=  "</tr>";
				}
			}
			idx++;	
			$("#result_table").append(content);
		});
	}
	, "setValue" : function(data){
		console.log(data);
		var used = convertStorageUnit(moStorageStatus[mStorageDevice.selItem].used);
		var total = convertStorageUnit(moStorageStatus[mStorageDevice.selItem].total);

		$("#sd_size").text( used + " / " + total);
		$("[name=over_write]").removeProp("checked");
		$("[name=over_write][value=" + data.OverWrite + "]").prop("checked", true);
		$("#auto_delete").val(data.AutoDelete);
	}
	, "getChanged" : function(){
		var cmd=""
		var settings = [ "over_write", "auto_delete" ];
		var value;
		settings.forEach(function(e) {
			value = CVal.getValue(e);
			if( value != mStorageDevice.selItem[e] ) {
				cmd += e + "=" + value + "&";
			}
		});
		return cmd;
	}
};

function convertStorageUnit(number){
	var text="0";
	if( number ){
		if( number > 1024 ) 
			text = (number/1024).toFixed(1) + "GB";
		else {
			text = number + "MB";
		}
	}
	return text;
}

function getStorageDeviceStatus()
{
	if( timeOutId != 0  ) clearTimeout(timeOutId);
    if(format_state)    // format 중일땐 query하지 않는다.
    {                   
    	return;
    }
    $.ajax({
    	type : "get",
    	url  : "/cgi-bin/admin/transfer.cgi",
    	data : "msubmenu=sdcard&action=get",
    	success : function(req) {
			moStorageStatus = eval(req);
			$list = $("tr[name=list_items]");
			for(var i=0; i < moStorageStatus.length && $list[i]; i++) {
				$("#mount" +i).text( moStorageStatus[i].mount == 0 ? 'X' : 'O');
				$("#size" + i).text(convertStorageUnit(moStorageStatus[i].total));
				$("#avail" + i).text(convertStorageUnit(moStorageStatus[i].free));
				$("#used" + i).text(moStorageStatus[i].used_percent + '%');
			}
			var used = convertStorageUnit(moStorageStatus[mStorageDevice.selItem].used);
			var total = convertStorageUnit(moStorageStatus[mStorageDevice.selItem].total);
			$("#sd_size").text( used + " / " + total);
			timeOutId = setTimeout(getStorageDeviceStatus, 2000);
		},
		error	: function(){
			setTimeout(getStorageDeviceStatus, 5000);
		}
	});
}

function onFail(req) {
	settingFail(menu, "ajax fail.");
	refreshMenuContent();
}
function getStorageDeviceIndex(){
	return Number(mStorageDevice.selItem);
}

function initEvent() {
	menu = getLanguage("setup_storage_config");
	$("[name=list_items]").click(function(e){
		mStorageDevice.selItem = Number(e.currentTarget.id.replace("storage", ""));
		mStorageDevice.toggleUI();
	});
	$("#format").click(function(){
		var param = "msubmenu=sdcard&action=format";
		param += "&storage_no=" + getStorageDeviceIndex();
		//if( confirm("Do you want to start formatting the SD card?") ) {
		if( confirm(getLanguage("msg_format_start_msg")) ) {
			$.ajax({
				type : 'get',
				url  : '/cgi-bin/admin/transfer.cgi',
				data : param,
				success : function(req) {
					var pattern = /OK/;
					if( pattern.test(req) ){
						$('#sd_status').html('DONE');
						settingSuccess(menu, getLanguage("setup_format"));
						refreshMenuContent();
					} else {
						$('#sd_status').html('FAIL');
						settingFail(menu, parserErroncode(req.split('\n')[1]));
						refreshMenuContent();
					}
					format_state = false;
				},
				error	: onFail
			});
			format_state = true;
			$('#sd_status').html('Formatting...');
			$('#format').attr("disabled", true);
			$('#sd_save').attr("disabled", true);
		}
	});
	$("#unmount").click( function(){
		var param = "msubmenu=sdcard&action=unmount";
		param += "&storage_no=" + getStorageDeviceIndex();
		$.ajax({
			type : 'get',
			url  : '/cgi-bin/admin/transfer.cgi',
			data : param,
			success : function(req) {
				var response = req.replace(/\r\n/g, '');
				if( response == "OK"){
					settingSuccess(menu, getLanguage("setup_unmount"));
					refreshMenuContent();
				} else {
					settingFail(menu, parserErroncode(req.split('\n')[1]));
					refreshMenuContent();
				}
			},
			error	: onFail
		});
		format_state = true;
	});
	$("#cancel").click( function(e){
		$("#storage_infomation").css("display", "none");
		$("#storage_list").css("display", "block");
	});
	$("#save").click( function(){

		var cmd = mStorageDevice.getChanged();

		if(cmd =="") return; 

		cmd += "storage_no=" + getStorageDeviceIndex();

		$.ajax({
			type:'get',
			url:'/cgi-bin/admin/transfer.cgi?msubmenu=sdcard&action=apply',
			data:cmd,
			success:function(req){
				var response = req.replace(/\r\n/g, '');
				if( response == "OK") {
					pop_msg = getLanguage("setup_save");
					settingSuccess(menu, pop_msg);
					refreshMenuContent();
				} else {
					pop_msg = getLanguage("setup_save");
					settingFail(menu, pop_msg);
				}
			},
			error:function(req){
				console.log(req);
			}
		});
	});
}
function initUI()
{
	mStorageDevice.init();

	$("[class=headline").find("th").addClass("fifth");
	$("[name=list_items").find("td").addClass("fifth");

	if(gLanguage == 2)  {
		$("#unmount").css("font-size", "9px");
		$("#format").css("font-size", "9px");	
	}
	else{
		$("#unmount").css("font-size", "12px");
		$("#format").css("font-size", "12px");
	}
}
function onLoadPage()
{
	initUI();
	initEvent();
    getStorageDeviceStatus();
}
$(document).error(function(msg){
	console.log(msg);
});
$(document).ready( function() {
	onLoadPage();
});
} catch(e ) {
	console.trace(e);
}

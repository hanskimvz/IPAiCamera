var menu = "Action Rules Setting";
var MaxNumRecord = capInfo.max_record;
var data;
var select_item = -1;
var MODE = "list";
var ActionSettingList = Array();
var SettingList = [ 'name', 'duration'];
var NONE = getLanguage("setup_none");
var Reccording = getLanguage("setup_reccording");
var FTP_RECIPIENT = getLanguage("setup_ftp_rev"); 
var SMTP_RECIPIENT = getLanguage("setup_smtp_rev");
var RELAY_OUT = getLanguage('setup_relay_out');
var FTP_CLIP_RECIPIENT = getLanguage("setup_ftp_clip_rev"); // clip
var PRESET = getLanguage('preset1');
var PRESET_TOUR = getLanguage('preset_tour1');
var WHITE_LED = getLanguage('white_led');
var HTTP_ACTION_RECIPIENT = getLanguage('setup_http_config');
var ActionTypeList = [ NONE, Reccording, FTP_RECIPIENT ,SMTP_RECIPIENT, RELAY_OUT, HTTP_ACTION_RECIPIENT, PRESET, PRESET_TOUR, WHITE_LED, FTP_CLIP_RECIPIENT];

for( var  i = 0 ; i < ActionConditionMax ; i++)
{
	ActionSettingList[i] = ["action" + i + "_type" , "action" + i + "_index" ];
}

function checkList(target) {
	var obj;
	obj = $("#" + target);
	if( obj.length == 0){
		obj = $("[name=" + target  +"]");
		if( obj.length == 0){
			//console.log("Can't find the " +  target);
			return null;
		}
	}
	return obj;
}
function getValue(obj) {
	var ret = null;
	if( obj.prop("type") == "radio") {
		ret = $("[name="+obj[0].name+"]:checked").val();
	} else if( obj.prop("type") == "checkbox") {
		if( obj.prop("checked") == true) {
			ret = 1;
		} else {
			ret  = 0;					
		}
	} else { 
		ret  = obj.val();				
	}
	return ret;	
}
function ChangeUI(view){
	if( view == "add" || view == "modify") {
		$("#actions_list").css("display", "none");
		$("#action_add_modify").css("display", "block");	
	} else {
		MODE = "LIST";
		$("#actions_list").css("display", "block");
		$("#action_add_modify").css("display", "none");	
	}
}
function initSettingsValue(index){
	try{
		if( typeof(index) == "undefined" )
		{
			$("#name").val("NewAction");
			$("#duration").val(0);
			$("[name=types]").val(0).trigger("change");
		}
		else
		{
			$("#name").val(data[index].name);
			$("#duration").val(data[index].duration);
			for(var i = 0 ; i < data[index].action_job.length ; i++)
			{
				$("#action" + i + "_type").val(data[index].action_job[i].type).trigger("change");
				obj = $("#action" + i + "_type option");
				if( obj && obj.length > 1 ){
					$("#action" + i + "_index").val(data[index].action_job[i].index);
				}
				//if( data[index].action_job[i].type == 1 ) {
				//	$("#action" + i + "_index").val(data[index].action_job[i].index);
				//} else if( data[index].action_job[i].type == 4){
				//	$("#action" + i + "_index").val(data[index].action_job[i].index);
				//}
			}
		}
	} catch(e)	{
		ERROR("EROR: initSettingsValue [" + e + "]");
	}
}

function initUI() {
	var i=0;
	for( i=0 ; i < ActionTypeList.length; i++) {
		if( (ActionTypeList[i] == Reccording) && 
				(capInfo.have_sdcard == 0 || (systemOption & DW_EDGE_FIRMWARE) )) {
			continue;
		}
		if( ActionTypeList[i] == RELAY_OUT && capInfo.relay_count == 0 ){
			continue;
		}
		if( (ActionTypeList[i] == PRESET || ActionTypeList[i] == PRESET_TOUR ) && (capInfo.camera_module != "ov_isp" || capInfo["oem"] != 24 ) ) {
			continue;
		}
		if( (ActionTypeList[i] == WHITE_LED ) && (capInfo.camera_module != "ov_isp" || capInfo["oem"] != 24 || capInfo.have_cds == 0) ) {
			continue;
		}
		if( (ActionTypeList[i] == HTTP_ACTION_RECIPIENT && capInfo["oem"] != 2 ) ) {
			continue;
		}
		if( (ActionTypeList[i] == FTP_CLIP_RECIPIENT && capInfo["oem"] != 19 ) ) {
			continue;
		}
		$("[name=types]").append("<option value=" + i + ">" + ActionTypeList[i] + "</option>");
	}
	if( data.length == MaxNumTrigger ) $("#add").attr("disabled", true);
	if( capInfo["oem"] == 2) $("#operation_layer").remove();
	
	if( capInfo["oem"] == 6 || capInfo.camera_module == "ov_isp")
		$("#action_rule1, #action_rule2, #action_rule3, #action_rule4").remove()
}
function setEventForListItem(){
	$("tr[name=list_items]").on("click", function(e) {
		$("tr[name=list_items]").removeClass("sel_list_item");
		$("#" + e.delegateTarget.id).addClass("sel_list_item");
        select_item = Number($(".sel_list_item").attr("val"));
        if(capInfo["oem"]==19 && select_item == 0 && data[select_item]["name"]=="iNode Action")
        {
            $("#modify").attr("disabled", true);
        }
        else
            $("#modify").attr("disabled", false);

	});
}
function disabledButton(cmd)
{
	if( cmd !== true && cmd != false ) return -1;
	$("button").attr("disabled", cmd);
	if( data.length == MaxNumTrigger ) $("#add").attr("disabled", true);
}
function check_name(val){
	for(i=0; i < data.length; i++){
		if(data[i]["name"] == val){
			//console.log("name:" + data[i]["name"]);
			return false ;
        }
    }
    if(capInfo["oem"]==19 && "iNode Action" == val){//iNode
        //console.log("name:" + data[i]["name"]);
        return false ;
    }
	return true ;
}
function getpreset(){
  $.ajax({
    type : 'get',
    url  : '/cgi-bin/ptz.cgi',
    async: false,
    data : 'getpreset=1' ,
    dataType: 'json',
    success : function(ret){
      if( ret.presetInfo == undefined ) return 0;
      presetInfo = ret.presetInfo ;
    }
  }).done(function(){ console.log("요청 성공시 호출") })
    .fail(function(){ console.log("fail") })
    .always(function(){ console.log("always") });
}
function getpresetTour(){
	$.ajax({
		type : 'get',
		url  : '/cgi-bin/ptz.cgi',
		async: false,
		dataType: 'json',
		data : 'getpresetTour=1',
		success : function(ret){
			presetTourInfo = ret.presetTourInfo ;
		}
	});
}

function initEvent() {
	menu = getLanguage("setup_action_rule_config");
	setEventForListItem();
	$("#add").click(function(e){
		MODE = "add";
		ChangeUI(e.currentTarget.id);
		initSettingsValue();
	});
	$("#modify").click(function(e){
		if( select_item < 0 ) {
			settingFail(menu, getLanguage("msg_select_item"));
			return ;
        }
		MODE = "modify";
		ChangeUI(e.currentTarget.id);
		initSettingsValue(select_item);
	});
	$("#delete").click(function(e){
		var datas;
		if( select_item < 0 ) {
			settingFail(menu, getLanguage("msg_select_item") );
			return ;
		}
		disabledButton(true);
		datas = "msubmenu=action&action=remove&id="+ data[select_item].id;
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/trigger.cgi",
			async : false,
			data: datas,
			success: function(msg){
				var OK = /OK/;
				var tmp= msg.trim().split('\n');
				var response = tmp[0];
				var error_code = tmp[1];
				if(OK.test(response)){
					settingSuccess(menu, null);
					refreshMenuContent();
				} else {
					settingFail(menu, getLanguage("msg_fail_retry"));
				}
			},
			error: function() {
				settingFail(menu, getLanguage("msg_fail_retry"));
				refreshMenuContent();
			}
		});
		disabledButton(false);
	});	
	$("#save").click(function(e){
		disabledButton(true);
		var datas = null;
		var newValue;
		var orgValue;
		var obj;
		var type = /action\d_type/;
		var index= /action\d_index/; 
		var changed = 0 ;

		try {
			for( var i = 0 ; i < SettingList.length ; i++) {
				obj = checkList( SettingList[i] );
				if( obj === null ) continue;
				//console.log(changed);
				newValue = getValue(obj);
				if( newValue === null) {
					//console.log(SettingList[i] + " can't find this value");
					continue;
				}
				if( MODE == "modify" ) {
					orgValue = data[select_item][SettingList[i]];
//					if( orgValue == newValue ) continue;
				}
				if( SettingList[i] == "name" ){
					if( !isValidText(newValue) ) {
						settingFail(menu, getLanguage("msg_invalid_text"));
						disabledButton(false);
						return;
					}
					if( newValue.length < 3 || newValue.length > 15 ){
						settingFail(menu, getLanguage("msg_invalid_text_length") + "(3~15)");
						disabledButton(false);
						return;
					}
					if( check_name(newValue) == false && MODE == "add"){
						settingFail(menu, getLanguage("msg_check_action_name"));
						disabledButton(false);
						return;
					}	
				}
				if( SettingList[i] == "duration"){
					var number = /^[0-9]*$/;	
					if( number.test(newValue, /g/) == false ){
						settingFail(menu, getLanguage("msg_onlynumber"));
						return;
					}
				}
				if( datas == null) { 
					datas = SettingList[i] + "=" + newValue;
				} else {
					datas += "&" + SettingList[i] + "=" + newValue;
				}
				if( newValue != orgValue ) changed = 1 ;
			}
			for( var i = 0 ; i < ActionSettingList.length ; i++ ) // 5 times
			{
				for( var j = 0 ; j < ActionSettingList[i].length ; j++) // 2 times
				{
					obj = checkList( ActionSettingList[i][j] );
					if( obj === null ) continue;

					newValue = getValue(obj);
					if( newValue === null) {
						continue;
					}
					if( datas == null) { 
						datas = "&" + ActionSettingList[i][j] + "=" + newValue;
					} else {
						datas += "&" + ActionSettingList[i][j] + "=" + newValue;
					}

					if( MODE == "modify" ) {	
						if( i < data[select_item].action_job.length ){
							if(j == 0 ) orgValue = data[select_item].action_job[i]["type"]	;	
							else orgValue = data[select_item].action_job[i]["index"]	;							
						}
						else orgValue = 0; 
					}	
					if( newValue != orgValue ) changed = 1 ;					
				}
			}
			if(!changed){
				settingFail(menu, getLanguage("msg_nothing_changed"));
				disabledButton(false);
				return ;
			}
			if( MODE == "modify"){
				datas = datas + "&id=" + data[select_item].id;
			}			
			if(datas != null) {
				datas = "msubmenu=action&action=" + MODE + "&"+ datas;
			} 			
			$.ajax({
				type:"get",
				url: "/cgi-bin/admin/trigger.cgi",
				async: false,
				data: datas,
				success: function(msg){
					var tmp= msg.trim().split('\n');
					var response = tmp[0];
					var error_code = tmp[1];
					if(response == "OK") {
						settingSuccess(menu, null);
						refreshMenuContent();
					} else {
						settingFail(menu, getLanguage("msg_fail_retry"));
					}
				},
				error: function() {
					settingFail(menu, getLanguage("msg_fail_retry"));
					refreshMenuContent();
				}
			});
		} catch (e){
			ERROR("Save error! [ " + e + "]");
		}
		disabledButton(false);
	});
	$("#cancel").click(function(e){ ChangeUI(e.target.id); });

	$("[name=types]").change( function(e){ 
		var items = e.target.value;
		var content, i, relay_id;
		var id;
		var index = e.target.id.replace(/[a-z]|_/g, '');

		$(".content").find("[name=details]").hide();
		$("#detail" + index).find("*").remove();
		if( items == 1) {
			id = "action" + e.target.id.replace(/[^0-9]/g,'') + "_index";
			content = "<label class='subtitle'> -"+getLanguage("Recording")+"</label>";
			content += "<div class='select'>";
			content += "<select id='" + id + "'>";
			for(i = 0; i < MaxNumRecord ; i++) {
				content += "<option value='" + i + "'>"+ getLanguage("record") + i  + "</option>";
			}
			content += "</select></div>";
		} else if( items == 4 ){
			id = "action" + e.target.id.replace(/[^0-9]/g,'') + "_index";
			content = "<label class='subtitle'>"+ getLanguage('setup_relay_out') +"</label>";
			content += "<div class='select'>";
			content += "<select id='" + id + "'>";
			for(i = 0; i < capInfo.relay_count ; i++) {
			  relay_id = i + 1;
				content += "<option value='" + i + "'>" + getLanguage('setup_relay_out') + 0 + relay_id + "</option>";
			}
			content += "</select></div>";
		}
		else if( (items == 2 || items == 3 ) && capInfo.is_proxy_camera ) {
			id = "action" + e.target.id.replace(/[^0-9]/g,'') + "_index";
			content = "<label class='subtitle'> - "+ getLanguage("setup_video") +"</label>";
			content += "<div class='select'>";
			content += "<select id='" + id + "'>";
			for(i = 0; i < capInfo.video_in ; i++) {
				content += "<option value='" + i + "'>" + getLanguage("setup_video");
				content += " " + Number(i+1)  + "</option>";
			}
			content += "</select></div>";
		} else if(items == 6){  // preset
			id = "action" + e.target.id.replace(/[^0-9]/g,'') + "_index";
			content = "<label class='subtitle'>"+ getLanguage('preset1') +"</label>";
			content += "<div class='select'>";
			content += "<select id='" + id + "'>";
			content += "<option value='-1' >Select Preset</option>";
			for( var i = 0 ; i < 256 ; i++ ){
				if( presetInfo[i] !=undefined )
					content += "<option value="+ i +">["+ (i+1) +"]"+ presetInfo[i]['name'] + "</option>";
			}
			content  += "</select></div>";
		} else if(items == 7){ //preset Tour
			id = "action" + e.target.id.replace(/[^0-9]/g,'') + "_index";
			content = "<label class='subtitle'>"+ getLanguage('preset_tour1') +"</label>";
			content += "<div class='select'>";
			content += "<select id='" + id + "'>";
			content += "<option value='-1' >Select Preset Tour</option>";
			for( var i = 0 ; i < 10 ; i++ ){
				if( presetTourInfo[i] !=undefined )
					content += "<option value="+ i +">["+ (i+1) +"]presettour"+ (i+1) + "</option>";
			}
			content  += "</select></div>";
		} else if(items == 8){ //White LED
			id = "action" + e.target.id.replace(/[^0-9]/g,'') + "_index";
			content = "<label class='subtitle'>"+ getLanguage('timeout') +"</label>";
			content += "<input id='" + id + "'";
			content += "class='short' type='number' value='5'>";
			content += "<label tkey='setup_transfer_sec'>Second(s)[5~60]</label>";
		}
		$("#detail" + index).show().append(content);
	});
	$("div[id^=action_title]").click( function(e){
		if( e.target.nodeName != "DIV") return;
		var index = e.target.id.replace(/[a-z]|_/g, '');
		$(".content").find("[name=details]").hide();
		$("#detail"+index).toggle();
	});
}

function initValue() {
	var content, action, num, cnt;
	$("tr[name=list_items]").remove();
	$record = $("#result_table");
	$record.empty();
	content = "";
	for(var i = 0 ; i < data.length ; i++) {
        action = '';
        for( var j=0 ; j < data[i].action_job.length ; j++)
        {
            if(data[i].action_job[j].type == 0)	 continue;
            else if(data[i].action_job[j].type == 1)	 action+= ","+ getLanguage("record");
            else if(data[i].action_job[j].type == 2)	 action+= ",FTP";
            else if(data[i].action_job[j].type == 3)	 action+= ",SMTP";
            else if(data[i].action_job[j].type == 4)	 action+= ","+ getLanguage('setup_relay_out');
            else if(data[i].action_job[j].type == 5)     action+= ","+ getLanguage('setup_http_config');
            else if(data[i].action_job[j].type == 6)	 action+= ",PRESET";
            else if(data[i].action_job[j].type == 7)	 action+= ",PRESET_TOUR";
            else if(data[i].action_job[j].type == 8)	 action+= ",WHITE_LED";
            else if(data[i].action_job[j].type == 9)	 action+= ",FTP_CLIP";
        }
	    action = action.replace(/^,/, '');


		if( data[i].id != 0 ) {
			content += "<tr class='list_items' name='list_items' id='list_item"+ i;
			content += "' val='" + i + "'>" 
			content += "<td class='athird'>" + data[i]['name'] + "</td>";
			cnt = 0 ; 
			data[i].action_job.forEach(function(z){
				if( z.type != 0 ){
					cnt++;
				}
			});
			content += "<td class='athird'>" + cnt + " / " + ActionConditionMax + "</td>";
			content += "<td class='athird'>" + action + "</td>";	
			content += "</tr>";
		}
	}
	if( content.length == 0 ) { 
		content += "<tr></tr>";
	}
	$record.append(content);
}
function onLoadPage() {
	getpreset();
	getpresetTour();
	initUI();
	initValue();
	initEvent();
}
$(document).ready( function() {
	data = getInformation( $(".select_minor").attr("id") );
	onLoadPage();
});

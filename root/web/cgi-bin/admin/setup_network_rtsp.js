var menu = "RTSP"+" "+ getLanguage("settings");
var settingList = ["rtsp_timeout", "dscp","Enabled", "IPv4Address", "Port", "TTL" ];
var source = MJ.id;
var audio_source =0;
var PAGE = 1;
var MAX_ITEMS_ON_PAGE = 4;
if( capInfo["oem"] == 2) {
	MAX_ITEMS_ON_PAGE = 2;
}
var MAX_PAGE = Math.ceil(RtspSessionInfo.length / MAX_ITEMS_ON_PAGE);

function onLoadPage()
{
	initUI(); 
    initValue();
    initEvent();
    dependncyUI();  
}
function Session_page(){
	var i, 
		items = 0,
		str = '';

	$("tr[name=sessions").remove();

	for( i = (PAGE-1)*MAX_ITEMS_ON_PAGE 
			; items++ < MAX_ITEMS_ON_PAGE && i < RtspSessionInfo.length 
			; i++){
		str += "<tr name='sessions' id='session"+(i+1)+"'>";
		str += "<td>"+(i+1)+"</td>";
		str += "<td>"+RtspSessionInfo[i]['addr']+"</td>";
		str += "<td>"+RtspSessionInfo[i]['port']+"</td>";
		str += "<td>"+RtspSessionInfo[i]['type']+"</td>";
		str += "</tr>";
	}
	if(str.length > 0 ) {
		$("#profile").append(str);
	}
    if( MAX_PAGE <= 1 ){
		$("#next_page, #prev_page").attr("disabled", true); 
	}
	else {
		if( PAGE <= 1 ){
			$("#prev_page").attr("disabled", true);
			$("#next_page").removeAttr("disabled");
		}
		else if(PAGE >= MAX_PAGE ) {
			$("#prev_page").removeAttr("disabled");
			$("#next_page").attr("disabled", true);
		}
        else {
			$("#prev_page").removeAttr("disabled");
			$("#next_page").removeAttr("disabled");
        }
	}
}
function initUI() {
	commonCreateSourceSelectBox("#vin_source");
	$(".select").css("margin-top","-4px");
	var i, obj='', index = 0;
	var name = ["setup_main_stream", "setup_sub_stream", "setup_third_stream" ];
	VinStreamInfo[source].forEach(function(ch){
		if( ch >= 0 ) 
		{
			obj += "<option value="+index+">"+getLanguage(name[index++])+"</option>";
		}
	});
    if(capInfo["oem"] == 12){
        if(capInfo.audio_in == 1){
            obj += "<option value="+index+">"+getLanguage("setup_audio_stream")+"</option>";
        }
    }
	$("#target_stream").find("option").remove();
	$("#target_stream").append(obj);
	Session_page();
}
function initValue(){
	var active_channel = $("#target_stream").val(); 
	var value = new Value() ; 
    if( active_channel == 3){
        value.setValue(settingList, RtpAudioInfo[audio_source]);
    }else {
        value.setValue(settingList, RtspTimeoutInfo[source][active_channel]);
    }
}
function dependncyUI()
{		
		var rtsp_value = $("#rtsp_timeout").val() ;
		if( rtsp_value > 0 ){
			$("#rtsp_timeout").prop("disabled", false);
			$("#ch0").prop("checked", true);
		}
		else{
			$("#rtsp_timeout").prop("disabled", true);
			$("#ch0").prop("checked", false);
		}		
		
		//if( $("[name=Enabled]:checked").val() == 0 ){
		//	$("#IPv4Address, #Port, #TTL").prop("disabled", true);
		//}else{				
		//	$("#IPv4Address, #Port, #TTL").prop("disabled", false);
		//}	
		$("#IPv4Address, #Port, #TTL").prop("disabled", false);	
}
function isvalid(val){
	var Valid = new Validation();	
	if( val == "rtsp_timeout"  )
	{
		var x = $('#rtsp_timeout').val();
		if (!x.match(/^[0-9]+$/)) 
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			return false;	
		}
		if( x == 0 ){
			return true;	
		}		
		else if(!(Valid.check_range(30 ,120, val))){
			return false;	
		}
	}	
	if( val == "dscp"  )
	{
		if(!(Valid.check_range(0 ,255, val))){
			return false;	
		}
	}
	if( val == "IPv4Address"  )
	{
		if(!(Valid.isValidMcasIP(val))){
			return false;	
		}
	}
	if( val == "Port"  )
	{
		if(!(Valid.isValiPort(val,1024,60000))){
			return false;	
		}
	}
	if( val == "TTL"  )
	{
		if(!(Valid.isValiPort(val,0,255))){
			return false;	
		}
	}
	return true;	
	
}
function initEvent()
{
	$("#vin_source").change(function(e){
		$("#target_stream option")[0].selected = true;
		source = getVinSourceIndex("#" + e.currentTarget.id);
		MJ.id = source;
    initValue();
		dependncyUI();
	});
	$("[name=Enabled]").change(function(e){
		dependncyUI();
	});		
	$("#target_stream").change(function(e){
			channel =  $("#target_stream").val(); 		   
			initValue();
			dependncyUI();
	});	
	$("#prev_page").click(function(){
		if( PAGE <= MAX_PAGE ) {
			PAGE--;
		}
		Session_page();
	});
	$("#next_page").click(function(){
		if( PAGE < MAX_PAGE ) {
			PAGE++;
		}
		Session_page();
	});
	$("#ch0").click(function(event){
		var active_channel = $("#target_stream").val(); 
		$("#rtsp_timeout").prop("disabled", !event.currentTarget.checked);		
		var value = 0;
		
		if(( $("#ch0" ).prop("checked") ) == true ) {
            if(active_channel == 3){
                if(	RtpAudioInfo[audio_source]["rtsp_timeout"] == 0 ) {
                    value = 30;				
                } else {
                    value =RtpAudioInfo[audio_source]["rtsp_timeout"];
                }
            }else{
                if(	RtspTimeoutInfo[source][active_channel]["rtsp_timeout"] == 0 ) {
                    value = 30;				
                } else {
                    value =RtspTimeoutInfo[source][active_channel]["rtsp_timeout"];
                }
            }
		} else {
			value = 0;
		}
		$("#rtsp_timeout").val(value); 
	});
	
	$("#btOK").click(function () {
		var active_channel = $("#target_stream").val(); 
		var cgiData = {};
		var newVal;
		var oldVal;
		var changed = 0;
		var valid_flag = 0 ;
		var value = new Value() ; 
        if(active_channel == 3){
		var items = RtpAudioInfo[audio_source];
        var cgiurl = "/cgi-bin/admin/basic.cgi?msubmenu=audio&action=apply";
        }else{
		var items = RtspTimeoutInfo[source][active_channel];
        var cgiurl = "/cgi-bin/admin/basic.cgi?msubmenu=video&action=apply";
		cgiData["channel_no"] = VinStreamInfo[source][active_channel];
        }
		settingList.some(function(e){
			newVal = value.getValue(e);              // get new value
			oldVal = items[e];                       // get old value
			if( newVal != oldVal ){                  // To compare the new value with the previous value. 
				if(!isvalid(e)) valid_flag = -1 ;    // validation
				cgiData[e] = newVal;
												
				changed++;
			}
		});	
		if( valid_flag == -1 )	return 0 ;
		if( changed == 0 ){
			settingFail(menu, getLanguage("msg_nothing_changed"));
		} else {
	//		console.log(cgiData);
			_ajax(cgiurl,cgiData);
		}
	 });
}
function _ajax(url,data)
{
	$.ajax({
		type:"get",
		url: url,
		data: data,
		success: function(ret){
			var reg=/OK/g;
			if( reg.test(ret) ){
				settingSuccess(menu, getLanguage("msg_success"));
				refreshMenuContent();
			} else {
				settingFail(menu, getLanguage("msg_fail_retry"));
			}
		},
		error: function(ret){
			settingSuccess(menu, getLanguage("msg_fail_retry"));
		}
	});
}

$(document).ready( function() {
	onLoadPage();	
	$("#target_stream").val(channel).change();	
});

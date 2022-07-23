var menu = "Smart LBR  Setting";
var settingList = ["lbr_streamid", "lbr_style", "lbr_bitrate", "lbr_motion_level", "lbr_noise_level", "lbr_autorun","lbr_onoff","lbr_profile_0","lbr_profile_1","lbr_profile_2","lbr_profile_3","lbr_profile_4"];

var g_lbr_mode = 0;

function setLBRAutoOn_status()
{
        $('[name=lbr_style]').prop("disabled",true);
        $('[name=lbr_motion_level]').prop("disabled",true);
        $('[name=lbr_noise_level]').prop("disabled",true);

		$("[name=lbr_streamid]").prop("disabled",true);
		$("[name=lbr_bitrate]").prop("disabled",true);

		$("[name=lbr_profile_0]").prop("disabled",true);
		$("[name=lbr_profile_1]").prop("disabled",true);
		$("[name=lbr_profile_2]").prop("disabled",true);
		$("[name=lbr_profile_3]").prop("disabled",true);
		$("[name=lbr_profile_4]").prop("disabled",true);
}

function setLBRManual_status()
{
        $('[name=lbr_style]').prop("disabled",false);
        $('[name=lbr_motion_level]').prop("disabled",false);
        $('[name=lbr_noise_level]').prop("disabled",false);

		$("[name=lbr_streamid]").prop("disabled",false);
		$("[name=lbr_bitrate]").prop("disabled",false);

		$("[name=lbr_profile_0]").prop("disabled",false);
		$("[name=lbr_profile_1]").prop("disabled",false);
		$("[name=lbr_profile_2]").prop("disabled",false);
		$("[name=lbr_profile_3]").prop("disabled",false);
		$("[name=lbr_profile_4]").prop("disabled",false);
}

function checkLBRStatus(){
	
	if(g_lbr_mode == 0){
		setLBRAutoOn_status();
	}
	else if(g_lbr_mode == 1){
		 setLBRAutoOn_status();
	}
	else{
		 setLBRManual_status();
	}
}

function initUI()
{ 
	console.log(SmartLBRInfo['lbr_onoff']);
	console.log(SmartLBRInfo['lbr_autorun']);

	if(SmartLBRInfo['lbr_onoff'] == '0'){
		g_lbr_mode = 0;
	}
	else if( SmartLBRInfo['lbr_autorun'] == '1'){
		g_lbr_mode = 1;
	}
	else{
		g_lbr_mode = 2;
	}
	console.log("MODE="+g_lbr_mode);
	checkLBRStatus();
}
function initValue()
{
	
	for( var i = 0 ; i < settingList.length ; i++)	
	{	
		var obj = $("[name=" + settingList[i] + "]");
		var tag = obj.prop("tagName");
		var type = obj.attr("type");
		if( tag == "SELECT" ) 
		{
			obj.val( SmartLBRInfo[settingList[i]]);
		}
		else if(tag == "DIV")
		{
			obj.parent().find("label").text( SmartLBRInfo[ settingList[i] ]);
			obj.slider("value", SmartLBRInfo[ settingList[i] ]);
		}
		else if( tag == "INPUT")
		{
			if(type == 'radio'){
				var obj_msg = "[name=" + settingList[i] + "][value="+ SmartLBRInfo[ settingList[i] ] + "]";
				$(obj_msg).prop("checked", true);
			}
			else{
				obj.val( SmartLBRInfo[settingList[i]]);
			}
		}
	}
	
	var obj_msg = "[name=lbr_onoff][value="+ g_lbr_mode + "]";
	$(obj_msg).prop("checked", true);
}
function initEvent()
{
	menu = getLanguage("setup_av_lbr_config");
	var  pop_msg ="";

	$("[name=lbr_onoff]").click(function ( obj ) {
		g_lbr_mode = $("[name=lbr_onoff]:checked").val();	
		checkLBRStatus();
	});
	$("#LBR_btOK").click(function(event) {

		var tmp_onoff = 0;
		var tmp_auto = 0;
		
		if(g_lbr_mode == 0){
			tmp_onoff = 0;
			tmp_auto = 0;
		}
		else if(g_lbr_mode == 1){
			tmp_onoff = 1;
			tmp_auto = 1;
		}
		else{
			tmp_onoff = 1;
			tmp_auto = 0;
		}

		var newValue;
		var orgValue;
		var data;
		data = null;
		data = "lbr_streamid=0";
		
		data += "&lbr_style=" + $('[name=lbr_style]:checked').val();
		data += "&lbr_motion_level=1";//  + $('[name=lbr_motion_level]:checked').val();
		data += "&lbr_noise_level=1";//   + $('[name=lbr_noise_level]:checked').val();
		data += "&lbr_autorun="    + tmp_auto;
	    data += "&lbr_bitrate="	   + $("[name=lbr_bitrate]").val();
		data += "&lbr_onoff="	   + tmp_onoff;
		data += "&lbr_profile_0=1";//     + $("[name=lbr_profile_0]").val();
		data += "&lbr_profile_1=1";//     + $("[name=lbr_profile_1]").val();
		data += "&lbr_profile_2=1";//     + $("[name=lbr_profile_2]").val();
		data += "&lbr_profile_3=1";//     + $("[name=lbr_profile_3]").val();
		data += "&lbr_profile_4=1";//     + $("[name=lbr_profile_4]").val();

		if( SmartLBRInfo["lbr_style"] == $('[name=lbr_style]:checked').val() && SmartLBRInfo["lbr_autorun"] == tmp_auto &&
		    SmartLBRInfo["lbr_bitrate"] == $("[name=lbr_bitrate]").val() &&  SmartLBRInfo["lbr_onoff"] == tmp_onoff )
		{
			pop_msg = getLanguage("msg_nothing_changed");
			settingFail(menu, pop_msg);
			return ;
		}
		else
			data = "msubmenu=SmartLBR&action=apply&"+data ;

		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/basic.cgi",
			data: data,	
			cache   : false,
			success: function(args){
				var pattern = /OK/g;
				if( pattern.test(args) == true){
					pop_msg = getLanguage("msg_lbr_success");
					settingSuccess(menu, pop_msg);
					refreshMenuContent();
				}else{
					settingFail(menu);
				}
			},
			error: function(args) {
				pop_msg = getLanguage("msg_fail_retry");
				settingFail(menu, pop_msg);
			}	
		});		
	});
	$("#lbr_bitrate").blur( function(obj){
		function check_range(min, max, name){ 
			console.log(name);
			var val = $("#"+ name ).val();
			if( val < min || val > max ) {
				var orgval = SmartLBRInfo[name] ;
				$("#"+name).val(orgval);  
				settingFail(menu, getLanguage("msg_outofrange"));
				return false ;
			}
			return true;
		}
		var name = obj.target.id ;
		var x = $("#"+ name ).val();
	    if (!x.match(/^[0-9]+$/))        // only nubmber
		{
	    	var orgval = SmartLBRInfo[name] ;
	    	$("#"+name).val(orgval);         // restore
	    	settingFail(menu, getLanguage("msg_onlynumber"));			
			return false; 
		}	
		if( name == "lbr_bitrate" ) check_range(64 ,20000,  name);    // check range
	});
}
function onLoadPage() 
{
	initUI();
	initValue();
	initEvent();
}
$(document).ready( function() {
    onLoadPage();
});

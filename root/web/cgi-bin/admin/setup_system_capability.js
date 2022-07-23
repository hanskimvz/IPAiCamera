var menu = getLanguage("setup_system_info");
var settingList = ["device_name", "location"];



$(document).ready( function() {
    onLoadPage();
});
function initUI(){
	if(capInfo["oem"] != 12)
        $("#serial_num").css("display","none");
    if(capInfo["oem"] != 19 && capInfo["oem"] != 20 && capInfo["oem"] != 21 && capInfo["oem"] != 10 && capInfo["oem"] != 11 && capInfo["oem"] != 13 && capInfo["oem"] != 25)
        $("#serial_number").css("display","none");
	  //	$("#location_div").css("display","none");
}
function initEvent()
{
		$("#btOK").click(function(event) { 

		function onSuccessApply(msg)
		{
			var tmp= msg.trim().split('\n');
			if(tmp == "OK")
			{		
				settingSuccess(menu, null);
			}
			else 
			{
				settingFail(menu, tmp[0]);
			}
			refreshMenuContent();
		}
		function onFailApply()
		{
			settingFail(menu, "apply fail. retry again.");
			refreshMenuContent();
		}				

		var data = null;
		{
			var newValue;
			var orgValue;

			for( var i = 0 ; i < settingList.length ; i++)	
			{	
				var obj = $("#" + settingList[i]);

					if(($("[name = "+settingList[i]+"]").prop("type")) == "radio")  // radio 
					{
						newValue = $("[name="+settingList[i]+"]:checked").val();
					}
					else if(($("#" + settingList[i]).prop("type")) == "checkbox")  // checkbox
					{
						if(($("#" + settingList[i]).prop("checked")) == true)
							newValue = 1;
						else				
							newValue = 0;					
					}
					else // select , input 
					{
						newValue = obj.val();				
					}

					orgValue = SysInfo[settingList[i]];
					if( orgValue != newValue )
					{
						if( settingList[i] == "device_name"  || settingList[i] == "location"){
							if( !isValidText(newValue) ) {
								settingFail(menu, getLanguage("msg_invalid_text"));
								return;
							}
							if( newValue.length < 1 || newValue.length > 30 ){
								settingFail(menu, getLanguage("msg_invalid_text_length") + "(1~30)");
								return;
							}	
						}
					
						if( data == null)
							data = settingList[i] + "=" + newValue;
						else
							data += "&" + settingList[i] + "=" + newValue;
					}
				}
			}
				 
			if(data != null)
			{
				data = "msubmenu=device_info&action=apply&"+ data;
			} else {
				settingFail(menu, getLanguage("msg_nothing_changed"));
				return ;
			}
			$.ajax({
				type:"get",
				url: "/cgi-bin/admin/system.cgi",
				data: data,
				success: onSuccessApply, 
				error: onFailApply	
			});
		});
}


function onLoadPage()
{
    initValue();
	initUI();
	initLanguage();
    initEvent();
}
function initValue()
{
  var have_AI = capInfo.board_chipset === 'amba_cv22s88' ? 1 : 0;
	for( var i = 0 ; i < settingList.length ; i++)	
	{	
		var obj = $("#" + settingList[i]);
		var tag = obj.prop("tagName");
		if( tag == "SELECT" || tag == "INPUT")
		{
			obj.val( SysInfo[settingList[i]]);
		}
	}	
    $("#model_name").text(SysInfo["model_name"]);
    $("#serialnum").text(SysInfo["serialnum"]);//mac address
    if(SysInfo["serialnumber"] != ""){
        $("#serialnumber").text(SysInfo["serialnumber"]);//serial number
    }
    else{
        $("#serial_number").css("display","none");
    }
    $("#manufacturer").text(SysInfo["manufacturer"]);
    $("#maxresol").text(printRsolution(capInfo.max_resolution_width, capInfo.max_resolution_height));
    $("#max_fps").text(capInfo.max_fps + " fps");
    $("#alarm_in").append(printSuport(capInfo.relay_count));
    $("#relay_out").append(printSuport(capInfo.sensor_count));
    if( capInfo.audio_in == 1 || capInfo.audio_out == 1)
        $("#audio_in_out").append(printSuport(1));
    else
        $("#audio_in_out").append(printSuport(0));
    
    if( capInfo.ptz_module == "af_licom_2812")
    	$("#have_zoom").append(printZoom_1(capInfo.have_zoom));
    else
    	$("#have_zoom").append(printZoom(capInfo.have_zoom));
    $("#have_digitalzoom").append(printZoom_1(capInfo.have_digitalzoom));
    $("#have_ptz").append(printSuport(capInfo.have_pantilt));
    $("#have_AI").append(printSuport(have_AI));
	$("#have_cds").append(printSuport(capInfo.have_cds));
    if( capInfo.is_proxy_camera ){
        $("#slave1").append(SlaveVersionInfo.slave1);
		if(capInfo.camera_type != "PROXY_DUAL_CLIENT"){
			$("#slave2").append(SlaveVersionInfo.slave2);
			$("#slave3").append(SlaveVersionInfo.slave3);
		}
		else{
			$(".slave2").css("display","none");
			$(".slave3").css("display","none");
		}
    }
    else
        $("#slave_version").css("display","none");
}
function printRsolution(width, height)
{
    if( width == 1920 && height == 1080)
        return "1080p";
    else if( width == 1280 && height == 720)
        return "720p";
    else if( width == 3008 && height == 3000)
        if (capInfo["oem"] == 10 ||capInfo["oem"] == 11 || capInfo["oem"] == 13 || capInfo["oem"] == 25 ){
            return "4000x3000";
        }
        else
            return "3008x3000";
    else if( width == 2592 && height == 1944 ){
        if(capInfo["camera_type"] == "4M"){
            return "2560x1440";
        }
        else{
            return "2592x1944";
        }
    }
	else {
		return width + " x " + height;
	}
}
function printSuport(val)
{ 
    if(val === 1) return "<span tkey='setup_capability_support'></span>";
    else            return "<span tkey='setup_capability_not_supported'></span>";
}
function printZoom(val)
{
    if( val == 0) return "<span tkey='setup_capability_not_supported'></span>";
    else return "<span>" + "X"+ val + "</span>";
}
function printZoom_1(val)
{
    if(val === 0) return "<span tkey='setup_capability_not_supported'></span>";   
    else return  "<span tkey='setup_capability_support'></span>";
}

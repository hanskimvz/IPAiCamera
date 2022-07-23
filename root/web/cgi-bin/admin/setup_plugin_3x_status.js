//var onvif_discovery_mode=0;
//var onvif_auth_mode=2;

var menu = "TEMPERATURE"+" "+ getLanguage("settings");;
var settingList = ["mode", "threshold" ];

function initUI()
{
	function temperature_result(val){
		var temp = " °C";
		if( $("#mode").val() == 1 ){
			val = val * 1.8 + 32 ;
			temp = " °F";
		}
		
		$("#temperatureval").text(Math.round(val) + temp);	
		$("#temperatureval_3x").text(Math.round(val) + temp);	
	}
	function systemtime_result(val){
                $("#timeval_3x").text(val);
        }
        function cds_result(val){
                $("#cds_3x").text(val  );
        }
        function cpuload_result(val){
                $("#cpuval_3x").text(val + " %");
        }
        function meminfo_result(val){
                $("#meminfoval_3x").text(val + " %");
        }
        function bandwidth_result(val){
                $("#bandwidth_3x").text(val);
        }

	function check()
	{
		
		try{
			$.ajax({
			url  : '/cgi-bin/result',
			data : "msubmenu=event&action=view",
			cache   : false,
			async: true,
			success : function(ret){
				var tmp = ret.trim().split('\n');
                                for( var i=0 ; i < tmp.length ; i++){
                                   if( tmp[i].split('=')[0].trim() == "temperature" ){
                                        var tmp5 = tmp[i].split('=')[1];
                                        try {
                                                if(tmp5.length > 0)
                                                        temperature_result(tmp5);
                                        } catch (e){ console.log(e); }
                                   }
                                   if( tmp[i].split('=')[0].trim() == "system_time" ){
                                        var tmp8 = tmp[i].split('=')[1];
                                        try {
                                                if(tmp8.length > 0)
                                                        systemtime_result(tmp8);
                                        } catch (e){ console.log(e); }
                                   }
                                   if( tmp[i].split('=')[0].trim() == "CDS" ){
                                        var tmp9 = tmp[i].split('=')[1];
                                        try {
                                                if(tmp9.length > 0)
                                                        cds_result(tmp9);
                                        } catch (e){ console.log(e); }
                                   }
                                   if( tmp[i].split('=')[0].trim() == "CpuLoad" ){
                                        var tmp10 = tmp[i].split('=')[1];
                                        try {
                                                if(tmp10.length > 0)
                                                        cpuload_result(tmp10);
                                        } catch (e){ console.log(e); }
                                   }
                                   if( tmp[i].split('=')[0].trim() == "MemUsage" ){
                                        var tmp11 = tmp[i].split('=')[1];
                                        try {
                                                if(tmp11.length > 0)
                                                        meminfo_result(tmp11);
                                        } catch (e){ console.log(e); }
                                   }
                                   if( tmp[i].split('=')[0].trim() == "Bandwidth" ){
                                        var tmp12 = tmp[i].split('=')[1];
                                        try {
                                                if(tmp12.length > 0)
                                                        bandwidth_result(tmp12);
                                        } catch (e){ console.log(e); }
                                   }
                                }
				clearTimeout(timeout);
				timeout = setTimeout(check, 2000);
				},
			}); 
		}
		catch(exception)
		{
			console.log(exception);
		}	
	}
	check();	
}
function initvalue()
{
	for( var i = 0 ; i < settingList.length ; i++)	
	{	
		var obj = $("#" + settingList[i]);
		var type = obj.prop("type");
		if( type == "checkbox" ){
			if( temperatureInfo[settingList[i]] == "0")    obj.prop("checked", false)
			else   obj.prop("checked", true)
		}
		else if( type == "text" || type == "select-one" || type == "number")
		{
			obj.val( temperatureInfo[settingList[i]]);
		}	
	}
	$("#model_name").text(SysInfo["model_name"]);
	$("#serialnum").text(SysInfo["serialnum"]);
        $("#manufacturer").text(SysInfo["manufacturer"]);
	$("#fwInfo").text(fwInfo);
}
function dependencyUI(){
	if( $("#mode").val()  == 0 ){
		$("#threshold_label").text( "[ 50 ~ 100 ]" );
		$("#threshold").val(temperatureInfo["threshold"]);
		if( $("#threshold").val() < 50 || $("#threshold").val() > 100 )  $("#threshold").val(65);		
	}
	else{
		$("#threshold_label").text( "[ 122 ~ 212 ]" )
		$("#threshold").val(temperatureInfo["threshold"]);
		if( $("#threshold").val() < 122 || $("#threshold").val() > 212 )  $("#threshold").val(150);
	}
}
function initEvent()
{
	$("#mode").click(function(){
		
		dependencyUI();
	});
	$("#btOK").click(function(event) { 
		
	    var x = $('#threshold').val();
	    if (!x.match(/^[0-9]+$/)) 
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			return 0;
		}	
	    var min, max ;
	    if( $("#mode").val() == 1){
	    	min = 122; 
	    	max = 212;	    	
	    }else{
	    	min = 50 ;
	    	max = 100;
		}
		if( x < min || x > max ) {
			settingFail(menu, getLanguage("msg_outofrange"));
			return 0 ;
		}
		
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
			var changed = 0 ;
			
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
					
					orgValue = temperatureInfo[settingList[i]];
					if(  orgValue != newValue )
					{
						changed = 1 ;						
					}
					if( ( orgValue != newValue ) || settingList[i] == "mode" ||  settingList[i] == "thre")
					{
						if( data == null)
							data = settingList[i] + "=" + newValue;
						else
							data += "&" + settingList[i] + "=" + newValue;
					}
					
				}
			}
			if( changed == 0 ){
				settingFail(menu, getLanguage("msg_nothing_changed"));
				return ;				
			}
			if(data != null)
			{
				data = "msubmenu=temperature&action=apply&"+ data;
			} 
			$.ajax({
				type:"get",
				url: "/cgi-bin/admin/io.cgi",
				data: data,
				success: onSuccessApply, 
				error: onFailApply
			});
		});
}
function onLoadPage()
{   
	initEvent();
	initvalue();
	initUI();
	dependencyUI()
}

$(document).ready( function() {
	onLoadPage();
});

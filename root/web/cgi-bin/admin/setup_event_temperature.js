//var onvif_discovery_mode=0;
//var onvif_auth_mode=2;

var menu = "TEMPERATURE"+" "+ getLanguage("settings");;
var settingList = ["mode", "threshold" ];

function initUI()
{
	function temperature(val){
		var temp = " °C";
		if( $("#mode").val() == 1 ){
			val = val * 1.8 + 32 ;
			temp = " °F";
		}
		
		$("#temperatureval").text(Math.round(val) + temp);	
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
				try {                                     // system_time
					for( var i=0 ; i<tmp.length ; i++)
					{
						if( tmp[i].split('=')[0].trim() == "temperature" )
						{
							var tmp5 = tmp[i].split('=')[1];
							temperature(tmp5);
						}
					}
				} catch (e){
					console.log(e);
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
	console.log("asd");
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
}
function dependencyUI(){
	if( $("#mode").val()  == 0 ){
		$("#threshold_label").text( "[ 50 ~ 100 ]" );
		$("#threshold").val(temperatureInfo["threshold"]);
		if( $("#threshold").val() < 50 || $("#threshold").val() > 100 ) {
			$("#threshold").val(Math.floor((temperatureInfo["threshold"] - 32) * 5 / 9));
		}
	}
	else{
		$("#threshold_label").text( "[ 122 ~ 212 ]" )
		$("#threshold").val(temperatureInfo["threshold"]);
		if( $("#threshold").val() < 122 || $("#threshold").val() > 212 )  {
			$("#threshold").val(Math.floor(((temperatureInfo["threshold"] * 9/5 ) + 32)));
		}
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

var menu = "schedule setting";
//var WeekList = [ "sun" , "mon", "tue", "wed", "thu", "fri", "sat" ];
//var time = ["shour", "smin", "ehour", "emin" ];
//var settingList = $.merge( ["enable", "activation", "interval", "always" ], WeekList);
//ar settingList = $.merge( settingList, time);
var settingList = ["enable", "interval" ];

function disabled(val ,cmd)
{
	$("#"+val).find("select, input").each(function(i, e){
		var type = $(this).prop("id") ;
		$("#"+ type).prop("disabled", cmd);		
	});
}
function getvalue(val)
{
	switch(val)
	{

		case "WeekList" :
			for( var i = 0 ; i < WeekList.length ; i++)	
			{	
				var obj = $("#" + WeekList[i]);

				if(scheduleInfo[WeekList[i]] == 1)
					obj.prop("checked", true);
				else
					obj.prop("checked", false);

			}			
			break ;		
		case "settingList" :
			for( var i = 0 ; i < settingList.length ; i++)	
			{	
				var obj = $("#" + settingList[i]);
				var tag = obj.prop("tagName");
				if( tag == "SELECT" || tag == "INPUT")
				{
					obj.val( scheduleInfo[settingList[i]]);
				}	
			}
			break ;

	}
}

function initUI()
{
	for(i=0;i<24;i++)
	{
		if(i<10){
			$("#shour,#ehour").append("<option value=" + i + ">0" + i + "</option>" );
		}
		else{
			$("#shour,#ehour").append("<option value=" + i + ">" + i + "</option>" );
		}	
	}
	for(i=0;i<60;i++)
	{
		if(i<10){
			$("#smin,#emin").append("<option value=" + i + ">0" + i + "</option>" );
		}
		else{
			$("#smin,#emin").append("<option value=" + i + ">" + i + "</option>" );
		}
	}
}
function initvalue()
{
	//getvalue("WeekList" );
	getvalue("settingList");

	function getradio(val)
	{
		if(scheduleInfo[val]== 0) 	$("[name="+val+"][value=0]").trigger("click");
		else 	$("[name="+val+"][value=1]").trigger("click"); 	
	}	

	getradio("enable");
	getradio("activation");
	checkDependency("enable");		

}

function checkDependency(index)
{
	if( index == "enable")
	{
		if(($("[name=enable]:checked").val()) == 1)
		{	
			//disabled("Activation_Time", false );
			//disabled("Transfer_Interval", false );
			$("#interval").attr("disabled", false);
			checkDependency("activation");	

		}
		else if(($("[name=enable]:checked").val()) == 0)
		{		
			//disabled("Activation_Time", true );
			//disabled("Transfer_Interval", true );
			$("#interval").attr("disabled", true);
		}
	}
	/*	if( index == "activation")
		{
		if(($("[name=activation]:checked").val()) == 1)
		{
		for( var i = 0 ; i < WeekList.length ; i++)	
		{	
		$("#" + WeekList[i]).prop("checked", true);	
		}
		var seltime = [ 0, 0, 23, 59];	

		for( var i = 0 ; i < seltime.length ; i++)	
		{	
		$("#" + time[i]).val(seltime[i]);			
		}
		disabled("Activation_Time", true );		
		$("[name=activation]").prop( "disabled" , false );
		}
		else if(($("[name=activation]:checked").val()) == 0)
		{	
		disabled("Activation_Time", false );
		getvalue("WeekList");	
		getvalue("settingList");
		}
		}
		*/}
function initEvent() {
	if( capInfo["oem"] == 11 || capInfo["oem"] == 25 ){
		$("#schedule_config").append('<span tkey="setup_recurrences_config"></span>');
		menu = getLanguage("setup_recurrences_config");
	}else{
		$("#schedule_config").append('<span tkey="setup_schedule_config"></span>');
		menu = getLanguage("setup_schedule_config");
	}

	$("[name=enable]").click(function ( obj ) {				
		checkDependency("enable");	
	});
	/*	$("[name=activation]").click(function ( obj ) {		

		checkDependency("activation");	
		});
		*/
	$("#btOK").click(function(event) {
		function onSuccessApply(msg) {
			var pattern = /OK/;
			if(pattern.test(msg) == true) {
				settingSuccess(menu, null);
			} else {
				settingFail(menu, getLanguage("msg_fail_retry"));
			}
			refreshMenuContent();
		}
		function onFailApply() {
			settingFail(menu, getLanguage("msg_fail_retry"));
			refreshMenuContent();
		}	

		var data = null;
		var newValue;
		var orgValue;

		for( var i = 0 ; i < settingList.length ; i++)	{	
			var obj = $("#" + settingList[i]);

			if(($("[name = "+settingList[i]+"]").prop("type")) == "radio") {
				newValue = $("[name="+settingList[i]+"]:checked").val();
			} else if(($("#" + settingList[i]).prop("type")) == "checkbox") {
				if(($("#" + settingList[i]).prop("checked")) == true)
					newValue = 1;
				else				
					newValue = 0;					
			} else {
				newValue = obj.val();				
			}
			orgValue = scheduleInfo[settingList[i]];
			if( orgValue != newValue ) {
				if( data == null)
					data = settingList[i] + "=" + newValue;
				else
					data += "&" + settingList[i] + "=" + newValue;
			}
		}

		if(data != null) {
			data = "msubmenu=schedule&action=apply&"+ data;
		} else {
			pop_msg = getLanguage("msg_nothing_changed");
			settingFail(menu, pop_msg);
			return ;
		}
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/event.cgi",
			data: data,
			success: onSuccessApply, 
			error: onFailApply
		});
	});
}
function onLoadPage() {
	initUI();	
	initEvent();
	initvalue();
}

$(document).ready( function() {
	onLoadPage();
});

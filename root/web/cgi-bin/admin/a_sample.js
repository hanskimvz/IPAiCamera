var menu = "rs485" + " " + getLanguage("settings");;
var settingList = ["protocol", "address", "baudrate", "databit", "stopbit", "parity" ];
var target = "rs485" ;

function initUI() {

}
function checkDependency()
{

}	
function initValue(){
	var value = new Value() ; 
	value.setValue(settingList, rs485);
	checkDependency();
}
function initEvent()
{
	$("[name=dst_enable]").click(function ( obj ) {
		checkDependency();		
	});
	
	$("#btOK").click(function(event) { 
		function onSuccessApply(msg)
		{
			var tmp= msg.trim().split('\n');
			console.log(tmp);
			if(tmp[0] == "OK")
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
			settingFail(menu, getLanguage("msg_fail_retry"));
			refreshMenuContent();
		}
		var data = null;
		{
			var items = rs485;
			var cgiData= new Object();
			var newVal;
			var oldVal;
			var changed = 0;
			var value = new Value() ; 

			settingList.some(function(e){
				console.log(e);
				newVal = value.getValue(e);              // get new value
				oldVal = items[e];                       // get old value
				if( newVal != oldVal ){                  // To compare the new value with the previous value. 
					cgiData[e] = newVal;
													
					changed++;
				}
			});	

			if( changed == 0 ){
				settingFail(menu, getLanguage("msg_nothing_changed"));
			} else {
				$.ajax({ 
					type:"get",
					url: "/cgi-bin/admin/io..cgi?msubmenu=rs485&action=apply",
					data: cgiData,
					success: onSuccessApply, 
					error: onFailApply
				});
			}	
		}
	});
}
$(document).ready( function() {
	initUI();
	initEvent();
	initValue();
});

var menu = "DST" + " " + getLanguage("settings");;
var settingList = ["dst_enable", "dst_start_mon", "dst_start_ordinal", "dst_start_week", "dst_start_hour", 
                   "dst_end_mon", "dst_end_ordinal", "dst_end_week", "dst_end_hour" /*, "dst_bias" */];
var target = "dstInfo" ;
var weekday = [ getLanguage("sunday"), getLanguage("monday"), getLanguage("tuesday"), getLanguage("wednesday"), getLanguage("thursday"),
             getLanguage("friday"), getLanguage("Saturday")] ;
var week = [ getLanguage("frist"), getLanguage("second"), getLanguage("third"), getLanguage("fourth"), getLanguage("last") ];
var month = [ getLanguage("jan"), getLanguage("feb"), getLanguage("mar"), getLanguage("apr"), getLanguage("may"), 
              getLanguage("jun"), getLanguage("jul"), getLanguage("aug"), getLanguage("sep"), getLanguage("oct"),
			  getLanguage("nov"), getLanguage("dec") ];
function initUI() {
	for(var i=0 ; i < 12 ; i++ ){
		$("#dst_start_mon").append("<option value=" + i + ">"+ month[i] +"</option>")
		$("#dst_end_mon").append("<option value=" + i + ">"+ month[i] +"</option>")
	}
	for(var i=0 ; i < 5 ; i++ ){
		$("#dst_start_ordinal").append("<option value=" + i + ">"+ week[i] +"</option>")
		$("#dst_end_ordinal").append("<option value=" + i + ">"+ week[i] +"</option>")
	}
	for(var i=0 ; i < 7 ; i++ ){
		$("#dst_start_week").append("<option value=" + i + ">"+ weekday[i] +"</option>")
		$("#dst_end_week").append("<option value=" + i + ">"+ weekday[i] +"</option>")
	}
	for(var i=0 ; i < 24 ; i++ ){
		$("#dst_start_hour").append("<option value=" + i + ">"+(i) +"</option>")
		$("#dst_end_hour").append("<option value=" + i + ">"+(i) +"</option>")
	}


}
function checkDependency()
{
	if( $("[name=dst_enable]:checked").val() == 0)     
    	$("#dst_timecontent").find("select").prop("disabled", true);
	else 
		$("#dst_timecontent").find("select").prop("disabled", false);
}	
function initValue(){
	var value = new Value() ; 
	value.setValue(settingList, dstInfo);
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
			var items = dstInfo;
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
					url: "/cgi-bin/admin/system.cgi?msubmenu=timezone&action=apply",
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

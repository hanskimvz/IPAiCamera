var menu = "PTZ Setting";
var settingList = ["parking_enabled", "powerup_enabled", "autoflip_enabled"];
// var check_run = 0;
//	Val = new Value();

function getpreset(){
	$.ajax({
		type : 'get',
		url  : '/cgi-bin/ptz.cgi',
		async: false,
		data : 'getpreset=1' ,
		dataType: 'json',
		success : function(ret){
			console.log(ret);
//			if( ret.presetInfo == undefined ) return 0;
			presetInfo = ret.presetInfo ;
			$("#preset_no").append("<option value='-1' >Select Preset</option>");
			$("#preset_no_power").append("<option value='-1' >Select Preset</option>");
			//Load Preset, Presettour
			if( typeof(presetInfo) != 'undefined' ) {
				for( var i = 0 ; i < 256 ; i++ ){
					if( presetInfo[i] != undefined ) {
						$("#preset_no").append("<option value="+ i +">["+pad(i+1,3)+"]"+ presetInfo[i]["name"] + "</option>");
						$("#preset_no_power").append("<option value="+ i +">["+pad(i+1,3)+"]"+ presetInfo[i]["name"] + "</option>");
					}
				}
			}
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
                console.log(ret);
                presetTourInfo = ret.presetTourInfo ;
				$("#presettour_no").append("<option value='-1' >Select Preset Tour</option>");
				$("#presettour_no_power").append("<option value='-1' >Select Preset Tour</option>");
				if( typeof(presetTourInfo) != 'undefined' ) {
					for( var i = 0 ; i < 10 ; i++ ){
						if( presetTourInfo[i] != undefined ) {
							$("#presettour_no").append("<option value="+ i +">Preset Tour"+ pad(i+1, 2) + "</option>");
							$("#presettour_no_power").append("<option value="+ i +">Preset Tour"+ pad(i+1, 2) + "</option>");
						}
					}
				}
			}
        });
}

function initUI() {
	if(capInfo.camera_module == "ytot_isp") {
		$("#AutoFlipDzoom").hide();
		$("#AutoFlip").show();
		$("#Dzoom").hide();
		$("#actiontype option:eq(2), #actiontype_power option:eq(2), [name=tourdiv]").remove();
	}
	else {
		$("#AutoFlipDzoom").show();
		$("#AutoFlip").hide();
		$("#Dzoom").show();
	}
}
function initValue()
{
	//parking
	$("[name=parking_enabled][value=" + parkingInfo.Enable + "]").trigger('click');
	$("#wait_time").val(parkingInfo.WaitTime);
	$("#actiontype").val(parkingInfo.Action);
	if( parkingInfo.Action == 1) { //preset
		$("#preset_no").val(parkingInfo.Number);
		$("#preset_no").prop("disabled", false);
		if( $("#preset_no").val() == null ) {
			$("#preset_no").val(-1);
		}
	}
	else if( parkingInfo.Action == 2) { //tour
		$("#presettour_no").val(parkingInfo.Number);
		$("#presettour_no").prop("disabled", false);
		if( $("#presettour_no").val() == null ) {
			$("#presettour_no").val(-1);
		}
	}
	checkDependency("parking_enabled");

	//powerupaction
	$("[name=powerup_enabled][value=" + powerupInfo.Enable + "]").trigger('click');
	$("#actiontype_power").val(powerupInfo.Action);

	if( powerupInfo.Action == 1) { // preset
		$("#preset_no_power").val(powerupInfo.Number);
		$("#preset_no_power").prop("disabled", false);
		if( $("#preset_no_power").val() == null ) {
			$("#preset_no_power").val(-1);
		}
	}
	else if( powerupInfo.Action == 2) { //tour
       $("#presettour_no_power").val(powerupInfo.Number);
       $("#presettour_no_power").prop("disabled", false);
       if( $("#presettour_no_power").val() == null ) {
           $("#presettour_no_power").val(-1);
       }
   }
	checkDependency("powerup_enabled");

	//autoflip
	$("[name=autoflip_enabled][value=" + autoflipInfo.Enable + "]").trigger('click');

	//overview
	if(capInfo.camera_module == "ov_isp") {
		$("[name=autoflip_enabled]").prop("disabled", true);
	}

	//Dzoom
	$("[name=Dzoom_enabled][value=" + dzoomInfo.Enable + "]").trigger('click');
}
function initEvent()
{
	$("[name=parking_enabled]").click(function ( obj ) {
		checkDependency("parking_enabled");
	});

	$("#actiontype").change(function(obj){
		checkDependency("actiontype");
	});

	$("[name=powerup_enabled]").click(function ( obj ) {
		checkDependency("powerup_enabled");
	});

	$("#actiontype_power").change(function(obj){
		checkDependency("actiontype_power");
	});

	//parking
	$("#btOK").on("click" , function(){
		//nothing changed
		if( parkingInfo.Enable == $("[name=parking_enabled]:checked").val() && parkingInfo.WaitTime == $("#wait_time").val() && parkingInfo.Action == $("#actiontype").val() )
		{
			if( parkingInfo.Action == 1 ) { // preset
				if( parkingInfo.Number == $("#preset_no").val() ) {
					settingFail(menu, getLanguage("msg_nothing_changed"));
					return ;
				}
			}
			else if( parkingInfo.Action == 2 ) { // tour
				if( parkingInfo.Number == $("#presettour_no").val() ) {
					settingFail(menu, getLanguage("msg_nothing_changed"));
					return ;
				}
			}
			else {
				settingFail(menu, getLanguage("msg_nothing_changed"));
				return;
			}
		}
		if( $("[name=parking_enabled]:checked").val() == 1 ) { // enable
			if( $("#actiontype").val() == 1 ) { // preset
				if( $("#preset_no").val() == -1 ) {
					settingFail(menu, getLanguage("msg_select_index"));
					return ;
				}
			} else if( $("#actiontype").val() == 2 ) { //tour
				if( $("#presettour_no").val() == -1 ) {
					settingFail(menu, getLanguage("msg_select_index"));
					return ;
				}
			}
		}

		if( !($("#wait_time").val()).match(/^[0-9]+$/)) {
			settingFail(menu, getLanguage("msg_onlynumber"));
			return ;
		}
		if( $("#wait_time").val() < 5 || $("#wait_time").val() > 14400) {
			settingFail(menu, getLanguage("msg_check_waittime"));
			return ;
		}

		var data = "msubmenu=parkingaction&action=apply";
		data += "&enabled="+$("[name=parking_enabled]:checked").val();
		data += "&waittime="+$("#wait_time").val();
		data += "&actiontype="+$("#actiontype").val();
			if( $("#actiontype").val() == 1 ) {    // actiontype = preset
				data += "&index="+$("#preset_no").val();
			}
			else if( $("#actiontype").val() == 2 ) {   // actiontype = presettour
				data += "&index="+$("#presettour_no").val();
			}
		console.log("data");
		console.log(data);
		$.ajax({
            type:"get",
            url: "/cgi-bin/ptz.cgi",
            data: data,
            success: function(){
				settingSuccess(menu, null);
				refreshMenuContent();
			},
            error: function(){
				pop_msg = getLanguage("msg_fail_retry");
				settingFail(menu, pop_msg);
				refreshMenuContent();
			}
        });
	});

	//powerupaction
	$("#btOK_power").on("click" , function(){
        //nothing changed
        if( powerupInfo.Enable == $("[name=powerup_enabled]:checked").val() && powerupInfo.Action == $("#actiontype_power").val() )
        {
            if( powerupInfo.Action == 1 ) { // preset
                if( powerupInfo.Number == $("#preset_no_power").val() ) {
                    settingFail(menu, getLanguage("msg_nothing_changed"));
                    return ;
                }
            }
            else if( powerupInfo.Action == 2 ) { // tour
                if( powerupInfo.Number == $("#presettour_no_power").val() ) {
                    settingFail(menu, getLanguage("msg_nothing_changed"));
                    return ;
                }
            }
            else {
                settingFail(menu, getLanguage("msg_nothing_changed"));
                return;
            }
        }
        if( $("[name=powerup_enabled]:checked").val() == 1 ) { // enable
            if( $("#actiontype_power").val() == 1 ) { // preset
                if( $("#preset_no_power").val() == -1 ) {
                    settingFail(menu, getLanguage("msg_select_index"));
                    return ;
                }
            } else if( $("#actiontype_power").val() == 2 ) { //tour
                if( $("#presettour_no_power").val() == -1 ) {
                    settingFail(menu, getLanguage("msg_select_index"));
                    return ;
                }
            }
        }

        var data = "msubmenu=powerupaction&action=apply";
        data += "&enabled="+$("[name=powerup_enabled]:checked").val();
        data += "&actiontype="+$("#actiontype_power").val();
            if( $("#actiontype_power").val() == 1 ) {    // actiontype = preset
                data += "&index="+$("#preset_no_power").val();
            }
			else if( $("#actiontype_power").val() == 2 ) {   // actiontype = presettour
                data += "&index="+$("#presettour_no_power").val();
            }
        console.log("data");
        console.log(data);
        $.ajax({
            type:"get",
            url: "/cgi-bin/ptz.cgi",
            data: data,
            success: function(){
                settingSuccess(menu, null);
                refreshMenuContent();
            },
            error: function(){
                pop_msg = getLanguage("msg_fail_retry");
                settingFail(menu, pop_msg);
                refreshMenuContent();
            }
        });
    });
	
	//autoflip Dzoom
	$("#btOK_autoflip_dzoom").on("click" , function(){
		var param = {
			msubmenu : '',
			action : 'apply',
			enabled : '',
		}, change = 0;

		if( autoflipInfo.Enable == $("[name=autoflip_enabled]:checked").val() && dzoomInfo.Enable == $("[name=Dzoom_enabled]:checked").val() ) {
			settingFail(menu, getLanguage("msg_nothing_changed"));
			return ;
		}
		if( autoflipInfo.Enable != $("[name=autoflip_enabled]:checked").val() ) {
			param['msubmenu'] = 'autoflip';
			param['enabled'] = $("[name=autoflip_enabled]:checked").val();
			change = 1;
			console.log(param);
			run_ajax();
		}
		if( dzoomInfo.Enable != $("[name=Dzoom_enabled]:checked").val() ) {
			param['msubmenu'] = 'dzoom';
			param['enabled'] = $("[name=Dzoom_enabled]:checked").val();
			change = 1;
			console.log(param);
			run_ajax();
		}
		if (change == 1) {
            settingSuccess(menu, null);
            refreshMenuContent();
        } else if (change == 0) {
            pop_msg = getLanguage("msg_fail_retry");
            settingFail(menu, pop_msg);
            refreshMenuContent();
        }
			
		function run_ajax() {
			$.ajax({
				type:"get",
				url: "/cgi-bin/ptz.cgi",
				data: param,
				success: function(){
				},
				error: function(){	
				}
			});
        }
	});
}
function pad(n, width) {
      n = n + '';
      return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
}

function checkDependency(index) {
	//parking
	if( index == "parking_enabled")
	{
		if(($("[name=parking_enabled]:checked").val()) == 1)
		{
			$("#wait_time").attr("disabled", false);
			$("#actiontype").attr("disabled", false);
			checkDependency("actiontype");
		}
		else if(($("[name=parking_enabled]:checked").val()) == 0)
		{
			$("#wait_time").attr("disabled", true);
			$("#actiontype").attr("disabled", true);
			$("#preset_no").prop("disabled", true);
			$("#presettour_no").prop("disabled", true);
		}
	}
	if( index == "actiontype")
	{
		if( $("#actiontype").val() == 0 ) {
             $("#preset_no").attr("disabled", "true");
             $("#presettour_no").attr("disabled", "true");
         }
         else if( $("#actiontype").val() == 1) {
             $("#preset_no").removeAttr("disabled");
             $("#presettour_no").attr("disabled", "true");
         }
         else {
             $("#preset_no").attr("disabled", "true");
             $("#presettour_no").removeAttr("disabled");
         }
	}
	//powerupaction
	if( index == "powerup_enabled")
	{
		if(($("[name=powerup_enabled]:checked").val()) == 1)
         {
             $("#actiontype_power").attr("disabled", false);
             checkDependency("actiontype_power");
         }
         else if(($("[name=powerup_enabled]:checked").val()) == 0)
         {
             $("#actiontype_power").attr("disabled", true);
             $("#preset_no_power").prop("disabled", true);
             $("#presettour_no_power").prop("disabled", true);
         }
     }
	if( index == "actiontype_power")
     {
         if( $("#actiontype_power").val() == 0 ) {
              $("#preset_no_power").attr("disabled", "true");
              $("#presettour_no_power").attr("disabled", "true");
          }
          else if( $("#actiontype_power").val() == 1) {
              $("#preset_no_power").removeAttr("disabled");
              $("#presettour_no_power").attr("disabled", "true");
          }
          else {
              $("#preset_no_power").attr("disabled", "true");
              $("#presettour_no_power").removeAttr("disabled");
          }
     }
}

function onLoadPage() 
{
	getpreset();
	initUI();
	initValue();
	initEvent();
}
$(document).ready( function() {
	getpresetTour();
    onLoadPage();
});

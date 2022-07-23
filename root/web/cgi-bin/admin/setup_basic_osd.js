var menu = "OSD Setting";
var settingList = ["time_x", "time_y", "text_x", "text_y", "text", "ptz_x", "ptz_y", "temperature_x", "temperature_y"];
var src = MJ.id;
	Val = new Value();

function initUI() {   
	commonCreateSourceSelectBox("#vin_source");
	if((capInfo.have_pantilt && capInfo.have_zoom > 1)&&(capInfo.ptz_module != "rs485"))
	{
	  $("#div_ptz").show();
  }
  else
  {
    $("#div_ptz").hide();
  }
	if( capInfo.camera_type != "thermal" )
		$('#temperature_div').hide();
	else
		$('#temperature_div').show();

	if(corridor_mode != 0)
		$('#text').prop("maxlength", 16);
	else
		$('#text').prop("maxlength", 30);

    //if( capInfo["oem"] != 2) //only DW //imsi DW OSD
    if(1)
        $('#osd_stream').hide();
    else
        $('#osd_stream').show();        
}
function initValue()
{
	var obj,
		tag,
		i;
	Val.setValue(settingList, OsdInfo[src]);
	$("[name=time_enabled][value=" + OsdInfo[src]['time_enabled'] + "]").trigger('click');
	$("[name=ptz_enabled][value=" + OsdInfo[src]['ptz_enabled'] + "]").trigger('click');
	$("[name=temperature_enabled][value=" + OsdInfo[src]['temperature_enabled'] + "]").trigger('click');
    $("[name=text_enabled][value=" + OsdInfo[src]['text_enabled'] + "]").trigger('click');
    

    switch(OsdInfo[src]['osd_stream'])
    {
        case 1:
            $("#main_stream").prop("checked", true);
            break;
        case 2:
            $("#sub_stream").prop("checked", true);
            break;
        case 3:
            $("#main_stream").prop("checked", true);
            $("#sub_stream").prop("checked", true);
            break;
        case 4:
            $("#third_stream").prop("checked", true);
            break;
        case 5:
            $("#main_stream").prop("checked", true);
            $("#third_stream").prop("checked", true);
            break;
        case 6:
            $("#sub_stream").prop("checked", true);
            $("#third_stream").prop("checked", true);
            break;
        case 7:
            $("#main_stream").prop("checked", true);
            $("#sub_stream").prop("checked", true);
            $("#third_stream").prop("checked", true);
            break;
        default :
            break;
    }
}
function checkblank(val , msg){
	pop_msg = getLanguage(msg);
	if($("#" + val).val() == "" ){
		settingFail(menu, pop_msg);
		initValue();
		return false ; 
	}		
	return true;
}
function check_text_excced( max, name){
	var text_length = $("#"+ name ).val().length;
	if( text_length > max ) {
		var orgval = OsdInfo[src][name] ;
		$("#"+name).val(orgval);  
		settingFail(menu, getLanguage("msg_invalid_text_length") + "("+max+")");
		return false ;
	}
	return true;
}
function initEvent()
{
	menu = getLanguage("osd_configuration");
	var pop_msg ="";	
	$("#vin_source").off("change").change(function(e){
		src = getVinSourceIndex("#" + e.currentTarget.id);
		MJ.id = src;
    initValue();
	});
	$("[name=time_enabled]").change(function ( obj ) {
		var disabled = obj.currentTarget.value == 0 ? true : false;
		$('#time_x').prop("disabled", disabled);
		$('#time_y').prop("disabled", disabled);
	});
	$("[name=ptz_enabled]").change(function ( obj ) {
		var disabled = obj.currentTarget.value == 0 ? true : false;
		$('#ptz_x').prop("disabled", disabled);
		$('#ptz_y').prop("disabled", disabled);
	});
	$("[name=temperature_enabled]").change(function ( obj ) {
		var disabled = obj.currentTarget.value == 0 ? true : false;
		$('#temperature_x').prop("disabled", disabled);
		$('#temperature_y').prop("disabled", disabled);
	});
	$("[name=text_enabled]").change(function ( obj ) {
		var disabled = obj.currentTarget.value == 0 ? true : false;
        $('#text_x').prop("disabled", disabled);
        $('#text_y').prop("disabled", disabled);
        $('#text').prop("disabled", disabled);
	});
	$("#text").blur( function(obj){
		var name = obj.target.id ;
		var max = 30;
		if(corridor_mode != 0)
			max = 16;
		if( name == "text" ) check_text_excced(max , name);	
	});
	
	$("#btOK").click(function(event) {
		if($("[name=time_enabled]:checked").val() == 1){
			if(!checkblank("time_x", "msg_check_x_pos")) return ;			
			if(!checkblank("time_y", "msg_check_y_pos")) return ;
		}
		if($("[name=ptz_enabled]:checked").val() == 1){
			if(!checkblank("ptz_x", "msg_check_x_pos")) return ;			
			if(!checkblank("ptz_y", "msg_check_y_pos")) return ;
		}		
		if($("[name=temperature_enabled]:checked").val() == 1){
			if(!checkblank("temperature_x", "msg_check_x_pos")) return ;			
			if(!checkblank("temperature_y", "msg_check_y_pos")) return ;
		}
		if($("[name=text_enabled]:checked").val() == 1){
			if(!checkblank("text_x", "msg_check_x_pos")) return ;			
			if(!checkblank("text_y", "msg_check_y_pos")) return ;
			if(!checkblank("text", "msg_check_osdtext")) return ;		
		}
		
	    function checkLang() {
			var i;
			var n;
			var ob = $('#text').val();

			for (i=0; i<ob.length; i++)
			{
				n = ob.charCodeAt(i);

				// English font
				if (0x20 <= n && n < 0x20+95) continue;
				// Chinese font
				// if (0x4E00  <= n && n < 0x4E00+20912) continue;

				return false;
			}
			return true;
		}   
		
		if (!checkLang()) {
			pop_msg = getLanguage("msg_language_nosupport");
			settingFail(menu, pop_msg);
			return;
		}
	    
	    if (!checkCharacters("osd",$('#text').val()))
	    {
			pop_msg = getLanguage("msg_onlyalphabet");
			if( gLanguage == 0 ){
				pop_msg = getLanguage("msg_onlyalphabet")+"( except #, &, +, ', " + '", \\\ ).' ;
			}
			else if( gLanguage == 1 ){
				pop_msg = getLanguage("msg_onlyalphabet")+ " #, &, +, '," + ' ", \\\ ' + getLanguage("msg_onlyalphabet2");
			}
	        settingFail(menu, pop_msg);
	        return 0;
	    }
	    
	    var x = $('#time_x').val();
	    var y = $('#time_y').val();
	    if (!x.match(/^[0-9]+$/)) 
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			return 0;
		}	
		if (!y.match(/^[0-9]+$/)) 
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			return 0;
		}	
		if (x < 0 || x > 100 || y < 0 || y > 100 )
		{
			pop_msg = getLanguage("msg_osd_checkpoision_time");
			settingFail(menu, pop_msg);
			return 0;
		}
	    
	    x = $('#text_x').val();
	    y = $('#text_y').val();
	    if (!x.match(/^[0-9]+$/)) 
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			return 0;
		}	
		if (!y.match(/^[0-9]+$/)) 
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			return 0;
		}
		if (x < 0 || x > 100 || y < 0 || y > 100)
		{
			pop_msg = getLanguage("msg_osd_checkpoision_txt");
			settingFail(menu, pop_msg);
			return 0;
		}
	    x = $('#ptz_x').val();
	    y = $('#ptz_y').val();
	    if (!x.match(/^[0-9]+$/)) 
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			return 0;
		}	
		if (!y.match(/^[0-9]+$/)) 
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			return 0;
		}
		if (x < 0 || x > 100 || y < 0 || y > 100)
		{
			pop_msg = getLanguage("msg_osd_checkposition_ptz");
			settingFail(menu, pop_msg);
			return 0;
		}		    
		
	    x = $('#temperature_x').val();
	    y = $('#temperature_y').val();
	    if (!x.match(/^[0-9]+$/)) 
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			return 0;
		}	
		if (!y.match(/^[0-9]+$/)) 
		{
			settingFail(menu, getLanguage("msg_onlynumber"));
			return 0;
		}
		if (x < 0 || x > 100 || y < 0 || y > 100)
		{
			pop_msg = getLanguage("msg_osd_checkposition_thermal");
			settingFail(menu, pop_msg);
			return 0;
		}  
		

		var data = null;	
	    var time_enabled	= 0;
	 	var temperature_enabled = 0;
		var text_enabled    = 0;
        var ptz_enabled    = 0;
        var osd_stream = 7;
		
		if( $('[name=time_enabled]:checked').val() == 1)
			time_enabled = 1;

		if(time_enabled != OsdInfo[src]['time_enabled']) {
			if( data == null) {
				data = "time_enabled=" + time_enabled;
			} else {
				data += "time_enabled=" + time_enabled;
			}
		}
		if( $('[name=text_enabled]:checked').val() == 1) 
			text_enabled= 1;

		if(text_enabled != OsdInfo[src]['text_enabled']){
			if( data == null) {
				data = "text_enabled=" + text_enabled;
			} else {
				data += "&text_enabled=" + text_enabled;
			}
		}
		if( $('[name=ptz_enabled]:checked').val() == 1)
			ptz_enabled = 1;

		if(ptz_enabled != OsdInfo[src]['ptz_enabled']) {
			if( data == null) {
				data = "ptz_enabled=" + ptz_enabled;
			} else {
				data += "&ptz_enabled=" + ptz_enabled;
			}
		}		
	
		if( $('[name=temperature_enabled]:checked').val() == 1) 
			temperature_enabled= 1;

		if(temperature_enabled != OsdInfo[src]['temperature_enabled']){
			if( data == null) {
				data = "temperature_enabled=" + temperature_enabled;
			} else {
				data += "&temperature_enabled=" + temperature_enabled;
			}
		}

        //if( capInfo["oem"] == 2){
        if( 0 ){
            if(temperature_enabled == 1 || ptz_enabled == 1 || text_enabled == 1 || time_enabled == 1)
            {
                if($('input:checkbox[id="main_stream"]').is(":checked") == true)
                    osd_stream = 1;
                if($('input:checkbox[id="sub_stream"]').is(":checked") == true)
                    osd_stream = osd_stream + 2;            
                if($('input:checkbox[id="third_stream"]').is(":checked") == true)
                    osd_stream = osd_stream + 4;      
            }
        }


        if(data == null)
        {
            data = "osd_stream=" + osd_stream;
        }
        else{
            data += "&osd_stream=" + osd_stream;
        }

		var newValue;
		var orgValue;

		for( var i = 0 ; i < settingList.length ; i++)	
		{	
			var obj = $("#" + settingList[i]);
			newValue = obj.val();
			orgValue = OsdInfo[src][settingList[i]];
						
			if( orgValue != newValue )
			{
					if( data == null)
					data = settingList[i] + "=" + newValue;
				else
					data += "&" + settingList[i] + "=" + newValue;
			}
		}
			
		if(data != null)
		{
			data = "msubmenu=osd&action=apply&"+data + "&source=" + (src+1);
		} else {
			pop_msg = getLanguage("msg_nothing_changed");
			settingFail(menu, pop_msg);
			return ;
		}
		$.ajax({
			type:"get",
			url: "/cgi-bin/admin/basic.cgi",
			data: data,	
			success: function(msg){
				var response = msg.trim();
				if(response == "OK")
				{
					settingSuccess(menu, null);
				}
				else 
				{
					settingFail(menu);
				}
				refreshMenuContent();
			},
			error: function() {
				pop_msg = getLanguage("msg_fail_retry");
				settingFail(menu, pop_msg);
				refreshMenuContent();
			}	
		});
		
	});



}

function onLoadPage() 
{
	initUI();
	initEvent();
	initValue();
}
$(document).ready( function() {
    onLoadPage();
});

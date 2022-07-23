var enc_settings = [ "input_volume", "input_samplerate", "input_format", "input_encode" ];
var menu = getLanguage("audio_configuration")
function onClickApply() {
	$.ajax({
		url : '/cgi-bin/admin/basic.cgi', 
		type: 'get',
		data : {
			submenu: 'audio',
			action: 'apply',
			input_gain: selInputGain.value,
			output_gain: selOutputGain.value,
		},
		onSuccess: function(req){
			alert('Apply');
			refreshMenuContent();
		},
		onFailure: function(req){
			refreshMenuContent();
		}
	});
}

function initUI() {
	$input = $("#input_volume");
	$output = $("#output_volume");
	var cmd;
	for( var i=10; i >= 0 ; --i){
		cmd = "<option value=" + i + ">" + i + "</option>";
		$input.append(cmd);
		$output.append(cmd);
	}
	switch(audioEnc.input_encode)
	{
		case 10:
			cmd = "<option value=8000> 8,000 Hz</option>";
			break;
		case 12: 
			cmd = "<option value=8000> 8,000 Hz</option>";
			cmd += "<option value=16000> 16,000 Hz</option>";
			cmd += "<option value=48000> 48,000 Hz</option>";
			break;
	}
	$("#input_samplerate").empty().append(cmd);
	if( capInfo["oem"] == 12) {
		$("#input_samplerate, #input_encode").prop("disabled",false);

		$("#audio_on_off").css('display','block');
		if(audioEnc.audio_enabled == 0){
			$('[name=audio_enabled][value=0]').attr("checked", true);
			$("#input_encode, #input_volume, #input_samplerate, #audio_amp_on_off").prop("disabled",true);
		}else{
			$('[name=audio_enabled][value=1]').attr("checked", true);
			$("#input_encode, #input_volume, #input_samplerate, #audio_amp_on_off").prop("disabled",false);
		}
  	if( audioEnc.aac_supported) {
  		$("#input_encode").append("<option value=12>AAC</option>");	  
  	}
	}else{
		$("#input_samplerate, #input_encode").prop("disabled",true);
		$("#audio_on_off").css('display','none');
		if( audioEnc.aac_supported) {
			$("#input_samplerate, #input_encode").prop("disabled",false);
			$("#input_encode").append("<option value=12>AAC</option>");	  
		}		
	}   
	if( capInfo["oem"] == 19|| capInfo["oem"] == 20 || capInfo["oem"] == 21) {
		$("#audio_amp_on_off").css('display','block');
		if(audioEnc.input_AmpEnabled == 0){
			$('[name=input_AmpEnabled][value=0]').attr("checked", true);
		}else{
			$('[name=input_AmpEnabled][value=1]').attr("checked", true);
		}
	}
	else{
		$("#audio_amp_on_off").css('display','none');
	}

}
function initValue() {
	enc_settings.forEach(function(id){
		if( typeof(audioEnc[id]) != 'undefined')
			$("#" + id).val(audioEnc[id]);
	})
}
function initEvent() {
	if( capInfo["oem"] == 12) 
	{
		$("[name=audio_enabled]").click(function ( obj ) {     
			if($("[name=audio_enabled]:checked").val()==0){
				$("#input_encode, #input_volume, #input_samplerate, #audio_amp_on_off").prop("disabled",true);
				//$("#input_volume").val(0);
			}else if($("[name=audio_enabled]:checked").val()==1){
				$("#input_encode, #input_volume, #input_samplerate, #audio_amp_on_off").prop("disabled",false);
				//if(audioEnc.input_volume != 0)
				//	$("#input_volume").val(audioEnc.input_volume);
				//else
				//	$("#input_volume").val(5);
			}
		});
	}
	$("#input_encode").off("change").on("change", function(e){
		var cmd;
		if($("#input_encode").val()==10){
				cmd = "<option value=8000> 8,000 Hz</option>";
		}else if($("#input_encode").val()==12){
			cmd = "<option value=8000> 8,000 Hz</option>";
			cmd += "<option value=16000> 16,000 Hz</option>";
			cmd += "<option value=48000> 48,000 Hz</option>";
		}
		$("#input_samplerate").empty().append(cmd);
	});

	$("#btOK").click(function () {
		var data='';
		var audio_enabled	= 0;
		if( $('[name=audio_enabled]:checked').val() == 1)
			audio_enabled = 1;
					
		enc_settings.forEach( function(id){
			var value = $("#" + id ).val();
			if( value != audioEnc[id] )
				data += id + "=" + value + "&";
		});
		if(audio_enabled != audioEnc['audio_enabled']) {
			if( data == "") {
				data = "audio_enabled=" + audio_enabled;
			} else {
				data += "&audio_enabled=" + audio_enabled;
			}
		}		
		if( capInfo["oem"] == 19|| capInfo["oem"] == 20 || capInfo["oem"] == 21 ) {
			if( audioEnc['input_AmpEnabled'] != $('[name=input_AmpEnabled]:checked').val()){
				if( data == "") {
					data = "input_AmpEnabled=" + $('[name=input_AmpEnabled]:checked').val();
				} else {
					data += "&input_AmpEnabled=" + $('[name=input_AmpEnabled]:checked').val();
				}
			}
		}
		if(data == ""){
			settingFail(menu, getLanguage("msg_nothing_changed"));
			return ;
		}
		$.ajax({
			method: 'get',
			url:'./basic.cgi?msubmenu=audio&action=apply', 
			data: data,
			success: function(req){
				settingSuccess(menu, null);
				refreshMenuContent();
			},
			error: function(req){
				settingFail(menu);
				refreshMenuContent();
			}
		});
	})
}
function onLoadPage() {
	initUI();
	initValue();
	initEvent();
}
$(document).ready( function() {
    onLoadPage();
});

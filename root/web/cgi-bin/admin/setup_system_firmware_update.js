var timer1;
var MODE;
var pop_msg="";
var complete = false;
function Elapsed_time() {
	pop_msg = getLanguage("msg_update_progress_message");
	if( MODE == "WEB"){
		$("#FileInput").prop( "disabled" , true );
		$("#progress_text").text(pop_msg);
	} else {
		$("#ftp_progress_text").text(pop_msg);
	}
    timer1 = setTimeout( function(){onUploading(); } , 100); 
}
function onUploading() {
	if( $("#upload").text() == "upload" && MODE == "FTP")
		return 0;

	var the_all = 0;
	$.ajax({
		url:'./system_up.cgi', 
		method: 'get',
		async : true,
		data: {
			submenu: 'upgrade',
		action: 'status',
		all: the_all,
		trycount: (new Date()).getTime()
		},success: function(req){
			var tmp = req.trim().split("\r\n");
			//var tmp = req.trim().split("\n");
			var status = tmp[0].split('=')[1];
			var percentComplete = (tmp[1].split('=')[1]);
			var prog_text;
			var prog_bar;
			var prog_box;
			var prog_status;

			if( MODE == "FTP"){
				prog_text = $("#ftp_progress_text");
				prog_bar = $("#ftp_progressbar");
				prog_box = $("#ftp_progressbox");
				prog_status = $("#ftp_statustxt");
			} else {
				prog_text = $("#progress_text");
				prog_bar = $("#progressbar");
				prog_status = $("#statustxt");
				$("#progressbox").show();
			}

            if(capInfo.camera_module == "s5l_internal_isp" && Number(percentComplete) < 0){
                switch( Number(percentComplete) )
                {
                    case -1 :
                        pop_msg = getLanguage("msg_upgrade_fail");
                        break;
                    case -2 :
                        pop_msg = getLanguage("msg_model_name_does_not_match");
                        break;
                    case -3 :
                        pop_msg = getLanguage("msg_does_not_support_version_downgrade");
                        break;
                }
				console.log(pop_msg);
				prog_text.text(pop_msg);
				//setTimeout( "", 500 );
				alert(pop_msg) ; 
				window.close();
            }

			if( status == 1){
				if( percentComplete == 1 ){
					pop_msg = getLanguage("msg_upgrade_boot_complete");
					prog_text.text(pop_msg);
				} else {
					pop_msg = getLanguage("msg_upgrade_boot_process");
					prog_text.text(pop_msg);
				}
			} else if(status == 2) {
				if( percentComplete >= 100 ){
					pop_msg = getLanguage("msg_upgrade_kernel_complete");
					prog_text.text(pop_msg);
				} else {
					pop_msg = getLanguage("msg_upgrade_kernel_process");
					prog_text.text(pop_msg);
				}
			} else if(status == 3){
				if( percentComplete >= 100 ){
					pop_msg = getLanguage("msg_upgrade_rootfs_complete");
					prog_text.text(pop_msg);
				} else {
					pop_msg = getLanguage("msg_upgrade_rootfs_process");
					prog_text.text(pop_msg);
				}
			} else if(status == 6){
				if( percentComplete >= 100 ){
					pop_msg = getLanguage("msg_upgrade_ptz_fw_complete");
					prog_text.text(pop_msg);
				} else {
					pop_msg = getLanguage("msg_upgrade_ptz_fw_progress");
					prog_text.text(pop_msg);
				}
			} else if(status == 7){
				if( percentComplete >= 100 ){
					pop_msg = getLanguage("msg_upgrade_slave_complete");
					prog_text.text(pop_msg);
				} else {
					pop_msg = getLanguage("msg_upgrade_slave_progress");
					prog_text.text(pop_msg);
				}
			} else if(status == 8){
				if( percentComplete >= 100 ){
					pop_msg = getLanguage("msg_upgrade_master_complete");
					prog_text.text(pop_msg);
				} else {
					pop_msg = getLanguage("msg_upgrade_master_progress");
					prog_text.text(pop_msg);
				}
			} else if( status < 0 ){
				clearInterval(timer1);	
				console.log(status);
				switch( Number(status) )
				{
					case -99 :
						pop_msg = getLanguage("msg_unsupported_upgrade_version");
						break;
					default : 
						pop_msg = getLanguage("msg_upgrade_fail");
						break;
				}
				console.log(pop_msg);
				prog_text.text(pop_msg);
				//setTimeout( "", 500 );
				alert(pop_msg) ; 
				refreshMenuContent();
			}
			prog_bar.width(percentComplete + '%') ;
			prog_status.html(percentComplete + '%');
			if( complete == false && status == 100 ){
				clearInterval(timer1);	
				pop_msg = getLanguage("msg_upgrade_success");
				prog_text.text(pop_msg);
				//setTimeout( "", 500 );
				alert(pop_msg) ; 			   		   
				complete = true;
				window.close();
			}
			if( status >= 0 && status != 100 )
				timer1 = setTimeout( function(){ onUploading("FTP"); } , 1000);
		} , error: function(){
			;
		}
	});
}

$(document).ready(function() { 
	onLoadPage();
}); 	


function onLoadPage()
{
	initUpload();
	initEvent();
	initValue();
}

function initValue()
{
	if(capInfo["oem"] == 11 || capInfo["oem"] == 13 || capInfo["oem"] == 10 || capInfo["oem"] == 25){
		$(".VCAFTP").css("display","block");
		$("#ftp_progressbox").css("display","none");
		$("#ftpinfomain").attr("tkey","msg_ftp_auto_up");
		$(".showonlyvca").css("display","block");
		$(".showonlyvcain").css("display","inline-block");
	}
	else {
		$(".showonlyvca").css("display","none");
		$(".showonlyvcain").css("display","none");
	}
    if(capInfo["oem"] == 12){
	    $("#fwInfo").text(ivfwInfo);

		$("#Hardware_Revision").css("display","block");
		if(capInfo["board_chipset"]== "amba_s3lm33")
			$("#hwInfo").append("1.0");
		else if(capInfo["board_chipset"]== "amba_s3l63")
			$("#hwInfo").append("2.1");
		else if(capInfo["board_chipset"]== "amba_s5l66")
			$("#hwInfo").append("3.0");
    }
    else if(capInfo["oem"] == 17){
    	$("#fwInfo").text(jcifwInfo);
    }
	else if(capInfo["oem"] == 19 || capInfo["oem"] == 20 || capInfo["oem"] == 21){
	    $("#fwInfo").text(fwInfo2);
	}
    else {      
	    $("#fwInfo").text(fwInfo);
	}
	if(capInfo["camera_module"] == "ytot_isp") // for 3x ptz version motion+isp
	{
		$("#motion_isp").css("display","block");
		$("#motionInfo").text((camInfo.substr(0,5)).toUpperCase());
		$("#ispInfo").text((camInfo.substr(6,5)).toUpperCase());
	}
	else
	{
		$("#camera_ver").css("display","block");
		$("#camInfo").text(camInfo.toUpperCase());
	}
	$("#address").val(ftpInfo.address);
	$("#port").val(ftpInfo.port);
	$("#id").val(ftpInfo.id);
	$("#password").val(ftpInfo.password);
	$("#location").val(ftpInfo.location);
	$("[name='autoupdate'][value=" + ftpInfo.autoupdate + "]").attr("checked", true);
	$("#interval").val(ftpInfo.interval);
}
function checkFTPUploading()
{
	$.ajax({
		type:'get',
		url: '/cgi-bin/getUploadStatus.cgi',
		//async: false,
		cache: false,
		timeout: 3000,
		data: { cmd: 'progress' },
		success: function(ret){
			tmp = ret.replace(/\r\n/g, '');
			tmp = tmp.split("/");
			var status = tmp[0];
			var progress = tmp[1];
			//console.log("status=" + status);
			//console.log("progress=" + progress+"%");
			if( status == 2 ){
				$("#ftp_progressbar").width(progress + "%");
				$("#ftp_statustxt").html(progress + "%");
				if( progress != 100){
					setTimeout(checkFTPUploading, 1000);
				} else if( progress == 100){
					afterSuccess();
				}
			} else {
				setTimeout(checkFTPUploading, 1000);
			}
		},
		error:checkFTPUploading
	});
}
function startFTPUpdate()
{
	if(confirm(getLanguage("msg_start_upgate_message")) == false) 
		return false;
	MODE = "FTP";
	$("#file").css("display", "none");
	$("#fileName").css("display", "none");

	$("#ftp_progressbox").show();
	$("#ftp_progressbar").show();
	$("#ftp_statustxt").show();

	$("#ftp_progressbar").css("width", "0%");
	$("#ftp_statustxt").html("0%");

	$("#ftp_progress_text").text(getLanguage("msg_update_progress_message"));

	$("#setup_menu").css("pointer-events", "");

	$("#save").prop('disabled', true);
	$("#cancle").prop('disabled', true);
	$("#upgrade").prop('disabled' , true);

	$("#submit-btn").css("display", "NONE");
	

	beforeSubmit();
	return true;
}
function initEvent() {
	var pop_menu = getLanguage("setup_ftp_config");
	$("#submit-btn").click(function(event){
		if(confirm(getLanguage("msg_start_upgate_message")) == false)
			return false;
	});
	$("#FileInput").change(function(event){
		function bytesToSize(bytes) {
			var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
			if (bytes == 0) return '0 Bytes';
			var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
			return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
		}
		var val = event.currentTarget.value;
		var filename = val.split("\\");

		var fsize = event.currentTarget.files[0].size; //get file size
		var ftype = event.currentTarget.files[0].type; // get file type
		var maxsize;
		if(capInfo["camera_module"] == "cv22_internal_isp")
			maxsize = MAX_CV22_FW_SIZE;
		else
			maxsize = MAX_FW_SIZE;
		if(fsize>maxsize) {
			var menu = getLanguage("msg_popmenu_firmwarecheck");
			var msg = getLanguage("msg_firmware_size_is_too_big");
			msg += " *" + getLanguage("setup_max_size")+" : "+maxsize/1024/1024 + "MB";
			settingFail(menu, msg);
			$("#FileInput").prop("disabled", false);
			return false;
		}
		filename = filename[filename.length-1];
		if(!(filename)) {
			$("#submit-btn").prop("disabled", true);
			$("#fw_status").text(getLanguage("msg_update_select_file"));
			return false;
		} else if (filename.substring(filename.length-3) == "bin" && capInfo["oem"] == 12 ){
			$("#submit-btn").prop("disabled", false);
			$("#fw_status").text(getLanguage("msg_update_ready_iv"));
			$("#fwfileInfo").css("display","block");
			$("#fwfileInfo").text("File name : " + filename);
			return true;
//		} else if (filename.substring(filename.length-3) != "img" || capInfo["oem"] == 12 ){
		} else if (filename.substring(filename.length-3) != "img"){ //MFZ펌웨어를 업데이트 하기 위해 원복
			$("#submit-btn").prop("disabled", true);
			$("#fw_status").text(getLanguage("msg_update_check_file"));
			return false;
		} else{
			$("#submit-btn").prop("disabled", false);
			if(capInfo["oem"] == 12)
			{
				$("#fw_status").text(getLanguage("msg_update_ready_iv"));
				$("#fwfileInfo").css("display","block");
				$("#fwfileInfo").text("File name : " + filename);
			}
			else
			{
			$("#fw_status").text(getLanguage("msg_update_ready_msg"));
			}
			return true;
		}
	});
	$("#save").click(function(){
		if($("#interval").val() > 720 || $("#interval").val() < 1) {
			pop_msg = getLanguage("msg_outofrange") + " (1-720)";
			alert(pop_msg);
			return;
		}
		function validateURL(textval) {   
			var urlregex = new RegExp("^(ftp.){1}([0-9A-Za-z]+\.)");
			return urlregex.test(textval);
		}   
		function validationAddress(textval) {   
			var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
			return ipformat.test(textval);
		}   

		var arg = {};
		var cmd ='';
		var obj = new Value;
		var validation = true;
		var submenu = getLanguage("setup_ftp_user_info");
		$.each(ftpInfo, function(key, value){
			var newVal = obj.getValue(key);
			if( !validation ) return false;
			if( key == "address"){
				if( !validateURL(newVal) && !validationAddress(newVal) ) {
					validation = false;
					return false;
				}
			};
			if( value != newVal ){
				if( cmd.length != 0 ) cmd += "&";
				cmd += key + "=" +  newVal;
			}
			arg[key] = newVal;
		});
		if( !validation ){
			settingFail(submenu, getLanguage("msg_ftp_wrong"));
		} else if ( cmd.length == 0 && validation ) {
			settingFail(submenu, getLanguage("msg_nothing_changed"));
		} else {
			$.ajax({
				type: 'get',
				url: '/cgi-bin/admin/upgrade.cgi?msubmenu=ftp&action=apply',
				data: arg,
				success: function(response){
					var OK = /OK/g;
					if( OK.test(response) ){
						settingSuccess(pop_menu, null);
						refreshMenuContent();
					} else {
						settingFail(pop_menu, null);
						initValue();						
					}
				},
				error: function(){
					settingFail(pop_menu, null);
				}
			});
		}
	});
	$("#cancle").click( function(obj){
		initValue();
	});
	$("#upgrade").click( function(obj){
        var status;
        status = $("#" + obj.target.id).val();
        text = null;
        if( status == "check")
        {
			disableFW("all", true);
			_ajax(status);
        }
        else if( status == "upgrade")
        {
            if( startFTPUpdate() )
            {
                disableFW("all", true);
                _ajax(status);
                checkFTPUploading();
            }
            else
            {
                refreshMenuContent();
            }
        } else {
            settingFail("Firmware check", "ERROR");
            refreshMenuContent();
        }
        function _ajax(cmd){
        	if( cmd == null || cmd == undefined ) return 0;
        	$.ajax({
        		type: 'get',
				async: false,
				url: '/cgi-bin/admin/upgrade.cgi?msubmenu=ftp&action=' + cmd,
				data: null,
				success: function(ret){
					var tmp;
					var response;
					var status;
					var cmd;
					var text;
					var statusObj;
					var progressObj;

					tmp = ret.replace(/\n/g, '').trim();
					response = tmp.split("/")[0];
					cmd = $("#upgrade").val();
					text=null;
					statusObj = $("#fw_status");
					progressObj = $("#ftpProgress");

					// console.log(response);
					// console.log(status);
					pop_menu = getLanguage("msg_popmenu_firmwarecheck");
					if( cmd == "check") {
						if ( response == 0){
	                    	_ajax(cmd);
	                    	return;
	                    } else if( response == 2){
							pop_msg = getLanguage("msg_upgrade_already");
	                    	text = pop_msg;
	                    	statusObj.text(text);
	                    	return;
	                    } else if( response == 3){
							text = getLanguage("msg_get_newfw");
	                        $("#upgrade").val("upgrade");
	                        $("#upgrade").text("upgrade");
							pop_msg = getLanguage("msg_findnew_please_start");
							settingSuccess(pop_menu, pop_msg);
							statusObj.text(text);
	                        $("#left_frame").find("*").prop("disabled", false);
	                        $("#upgrade").prop("disabled", false);
	                        return;
	                    } else if( response == 4 ){
							pop_msg = getLanguage("msg_nofind_newestfirmware");
							alert(pop_msg);
							disableFW("all", false);
							$("#submit-btn").attr('disabled', true);
							
	                    } else  if( response == 5){
							pop_msg = getLanguage("msg_check_ftp_server");
	                    	settingFail(pop_menu, pop_msg);
	                    	refreshMenuContent();
	                    } 
	                } else if( cmd == "upgrade") {
	                    progressObj.css("display", "block;");
					}
				}, error: function(){
					pop_menu = getLanguage("setup_ftp_config");
					settingFail(pop_menu, null);
				}
			});
		} // _ajax
	}); // $("#upgrade").click();
} // initEvent
function disableFW(cmd, opt){
 	if(cmd == 'all') {
 		$("#tabs").find("input").prop("disabled", opt);
 		$("#tabs").find("button").prop("disabled", opt);
 	} else if (cmd == "intput") {
 		$("#tabs").find("input").prop("disabled", opt);
 	} else if(cmd == "btn") {
 		$("#tabs").find("button").prop("disabled", opt);
 	}
}
function afterSuccess() {
	//$('#submit-btn').show(); //hide submit button
	//$('#loading-img').hide(); //hide submit button
	//$('#progressbox').delay( 1000 ).fadeOut(); //hide progress bar
	$('#progressbar').width("0%") ;
	$('#statustxt').html("0%");
	
	/*
	var fail = false;
	var the_all = 0;
	$.ajax({
		url:'./system_up.cgi', 
		method: 'get',
		async : false,
		data: {
			submenu: 'upgrade',
			action: 'check_end',
			all: the_all,
			trycount: (new Date()).getTime()
		}, success: function(req){
			if( req.trim() == "1" ){
				alert('Upgrade fail!!!');
				fail = true;
			}
		}, error: function(){
			return false;
		}
	});
	if ( fail ){
		return false;
		refreshMenuContent();
	}
	////
	$.ajax({
		url:'./system.cgi', 
		method: 'get',
		async : false,
		data: {
			submenu: 'upgrade',
			action: 'apply',
			all: the_all,
			trycount: (new Date()).getTime()
		},
		success: function(req){
			if( req.trim() == "NG" ){
				pop_msg = getLanguage("msg_upgrade_fail");
				alert(pop_msg);
				fail = true;
			}
		}, error: function(){
			return false;
		}
	});
	*/
	Elapsed_time();
}
function beforeSubmit()
{
	$("#fw_status").css("display", "none");
	$("#submit-btn").attr("disabled", true);
	if( MODE != "FTP"){
		MODE = "WEB";
		$("#save,#cancle,#upgrade").remove();
		$("#FileInput").prop("disabled", true);
	}
	if( (systemOption & SYSTEM_OPTION_DW_EDGE ) == SYSTEM_OPTION_DW_EDGE ) {
		$.ajax({
			url:"/cgi-bin/dwedge_control.cgi",
			method: "get",
			data: {
				action: "stop",
			}
		});
	}
	if( $("#upgrade").text() == "upgrade") return;
	var fail = false;
	var the_all = 0;
	$.ajax({
		url:'./system_up.cgi', 
		method: 'get',
		async : false,
		data: {
			submenu: 'upgrade',
			action: 'check',
			all: the_all,
			trycount: (new Date()).getTime()
		},
		success: function(req){
			if( req.trim() == "1" ){
				pop_menu = getLanguage("msg_popmenu_firmwareupgrade");
				pop_msg = getLanguage("msg_upgrade_already_runing");
				settingFail(pop_menu, pop_msg);
				refreshMenuContent();
				fail = true;
			}
		},
		error: function(){
			return false;
		}
	});
	if ( fail ) return false;
}
function afterError(response)
{
	switch ( response.status)
	{
		case 415:
		default:
			settingFail( getLanguage("msg_popmenu_firmwareupgrade"));
			break;
	}
}
function initUpload()
{
	$("#loading-img").css("display", "none");
	//function after succesful file upload (when server response)
	
	//progress bar function
	function OnProgress(event, position, total, uploadPercentComplete)
	{
		 //console.log(percentComplete);
		 //if( percentComplete == 1 ){
	     //   Elapsed_time();
		 //}
		pop_msg = getLanguage("msg_update_progress_message");
		$("#progress_text").text(pop_msg);
		$('#progressbox').show();
		$('#progressbar').width(uploadPercentComplete + '%') ;
		$('#statustxt').html(uploadPercentComplete + '%');
	    $('#statustxt').css('color','#000'); //change status text to white after 50%
	}

	//function to check file size before uploading.
	var options = 
	{ 
		//target:   	'#output',   // target element(s) to be updated with server response 
		beforeSubmit:  	beforeSubmit,  // pre-submit callback 
		success:       	afterSuccess,  // post-submit callback 
		uploadProgress: OnProgress, //upload progress callback 
		error: 			afterError,
		resetForm: 		true        // reset the form after successful submit 
	}; 

	$('#MyUploadForm').submit(function() { 
		$("#MyUploadForm").ajaxSubmit(options);
		return false; // always return false to prevent standard browser submit and page navigation
	}); 
}

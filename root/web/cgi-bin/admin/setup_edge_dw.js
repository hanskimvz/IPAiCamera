(function(){
	var menu = getLanguage('setup_spectrum_edge_js');
	function onloadPage(status){
		getStatus();
		initEvent();
	}
	function initEvent(){
		$("#FileInput").change(function(event){
			var filename = event.currentTarget.value.split("\\");
			filename = filename[filename.length-1];
			if(!(filename)) {
				$("button#install,button#update").prop("disabled", true);
				return false;
			}
			else {
				$("button#install,button#update").prop("disabled", false);
				return true;
			}
		});
		$("div[name=installed]").find("button").click(function(e){
			progressUI(true);
			var cmd = e.target.value;
			_ajax(cmd, function(req){
				$("#dwedge_status").text(req);
				progressUI(false);
			});
		});
		$("#install, button#update").click(function(e){
			if( confirm(getLanguage("setup_edge_install_and_update_msg")) == false ) {
				return;
			}
			var data = new FormData();
			data.append("uploadfile", $("input[name=FileInput]")[0].files[0]);
			$("#progressbox").css("display", "block");
			$.ajax({
				method : "POST",
				url : "../dwedge_update",
				data : data, 
				processData : false,
				contentType : false,
				xhr: function() {
					var xhr = $.ajaxSettings.xhr();
					xhr.upload.onprogress = function(e) {
						var progress = Math.floor(e.loaded / e.total *100);
						$("#progressbar").css('width', progress + '%');
						if( progress == 100 ){
							$("#statustxt").text(getLanguage('setup_spectrum_upload_success'));
							progressUI(true);
						} else {
							$("#statustxt").text(progress + '%');
						}

					};
					return xhr;
				},
				success : function(res){
					progressUI(false);
					var OK = /OK/g;
					if( OK.test(res) ){
						settingSuccess(menu, getLanguage("setup_spectrum_install_success")); 
						refreshMenuContent();
					} else {
						var msg = res.split('\n')[1];
                        try {
							if( msg.length == 0 || msg.length == 1 ){
								msg = getLanguage("setup_spectrum_install_fail");
							}
						} catch (e){
							;// use org message 
						}
						settingFail(menu, msg);
						progressUI(false);
					}
					$("#progressbox").css("display", "none");
				}, error : function(e){
					settingFail(menu, e.status + " - " + e.statusText);
					progressUI(false);
				}
			});
		});
	}

	/*
	   beforeSend: function(){ progressUI(true); },
	   progressUI(false);	
	   */
	function getStatus() {
		_ajax('status', function(req){
			$("#dwedge_status").text(req);
			var notInstall = /not installed/g;
			if( notInstall.test(req) ){
				$('[name=installed]').remove();
			} else {
				$('[name=notInstalled]').remove();
			}
		});
		_ajax('version', function(req){
			$("#dwedge_version").text(req);
		});
	}
	function _ajax(cmd, callback){
		$.ajax({
			url:"/cgi-bin/dwedge_control.cgi",
			method: "get",
			data: {
				action: cmd,
			},success: function(req){
				callback(req);
			}
		});
	}
	$(document).ready(function(){
		onloadPage();
	});
}());

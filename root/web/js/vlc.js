var Browser = { chk : navigator.userAgent.toLowerCase() };
Browser = {
	ie : Browser.chk.indexOf('msie') !== -1,
	ie6 : Browser.chk.indexOf('msie 6') !== -1,
	ie7 : Browser.chk.indexOf('msie 7') !== -1,
	ie8 : Browser.chk.indexOf('msie 8') !== -1,
	ie9 : Browser.chk.indexOf('msie 9') !== -1,
	ie10 : Browser.chk.indexOf('msie 10') !== -1,
	opera : !!window.opera,
	safari : Browser.chk.indexOf('safari') !== -1,
	safari3 : Browser.chk.indexOf('applewebkir/5') !== -1,
	mac : Browser.chk.indexOf('mac') !== -1,
	chrome : Browser.chk.indexOf('chrome') !== -1,
	firefox : Browser.chk.indexOf('firefox') !== -1
};
function isIE() {
	return ((navigator.appName == 'Microsoft Internet Explorer')
			|| ((navigator.appName == 'Netscape')
				&& (new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})").exec(navigator.userAgent) != null)));
}
var VLCManager = {
	'obj': null
		, 'preview_jpeg' : true
		, 'target' : null
		, "selectedChannel": 1
		, 'vlc_init_obj':  null
		, 'prevState' :  null
		, 'monitorTimerId' : null
		, 'URL' : null
		, 'Vid' : null
		//	option values
		, 'mute': true
		, 'volume': 10
		, 'buffering': 500
		, 'user' : new Object()
		, 'port' : null
		, 'showEncriptedImage' : function(id, width, height){
			var canvas = document.getElementById(id);
			var ctx = canvas.getContext('2d');
			var img = new Image(width, height);
			img.onload = function(){
				ctx.drawImage(img,0, 0,width,height); // Or at whatever offset you like
			};
			img.src="/images/encrypted.jpg";
		}
		, 'setPlayInfo' : function(user, port) {
			VLCManager.user = user;
			VLCManager.port = port;	
		} , 'error': function(msg) {
			var message;
			var height;
			var width;

			$("#vlc").remove();

			/*  =================== STICH ======================= */ 
			try {
				VLCManager.obj = null;
				height = $("#" + VLCManager.target).height();
				width = $("#" + VLCManager.target).width();
				MJ.fi = false ;
				MJ.dw = width;
				MJ.dh = height;
				$("#" + VLCManager.target).append("<canvas id='jpeg' width='" + width + "' height='"+ height + "'></canvas>");
				$("[class=warning]").css("display","none");
				$("#jpeg").css("display","block");
//				MJ.streaming() ;
			    if(capInfo["oem"]== 7)
    				$("#jpeg,.liveviewer").css("display","inline-table");
                else
    				$("#jpeg,.liveviewer").css("display","block");
				$("#" + VLCManager.target).find("*").remove();
				if ( msg == null || msg == undefined ) {
						msg = "vlc_not_supported_warning";
				}
				message = '<div class="warning">'
				message += getLanguage(msg);
				message += "</div>";
				VLCManager.obj = null;

				if( msg == "rtsp_warning") {
					$("#jpeg,.liveviewer").css("display","none");
				} else {
					$("#jpeg,.jpeg_1").css("display","none");
				}
				$("#" + VLCManager.target).append(message);				
			} catch(err) {
				console.log(err);
			}
			/*  =================== VIDEO_CROP ======================= */ 
			//var image_ch = 2;
			//if(VideoInfo[3].codec == '2')
			//	image_ch = 3;
			//
			//var input = {'width': VideoInfo[image_ch].resolution.split('x')[0],
			//	'height': VideoInfo[image_ch].resolution.split('x')[1]};
			//var height = 540;
			//var width = height  * input.width/ input.height;

			//	$("#jpeg").width(width).height(height);
			
//-------------------------------------------------------------			
			//	$("#jpeg,.liveviewer").css("display","block");
			//	$("#" + VLCManager.target).find("*").remove();
			//	if ( msg == null || msg == undefined ) {
			//			msg = "vlc_not_supported_warning";
			//	}
			//	message = '<div class="warning">'
			//	message += getLanguage(msg);
			//	message += "</div>";
			//	VLCManager.obj = null;

			//	if( msg == "rtsp_warning") {
			//		$("#jpeg,.liveviewer").css("display","none");
			//	} else {
			//		$("#jpeg,.jpeg_1").css("display","none");
			//	}

			//	$("#" + VLCManager.target).append(message);
//------------------------------------------------------------
//			//}
			

			return true;
		}
	, 'initPreview': function(target, windowless) {
		// it's called the Camera menu of Admin settting page.
		VLCManager.target = target;
		if( VLCManager.preview_jpeg ) {
			/*  =================== VIDEO_CROP ======================= */ 
			//var sensor = { 'width': VideoInfo[0].resolution.split('x')[0], 
			//	'height' : VideoInfo[0].resolution.split('x')[1] };
			//var image_ch = 2;
			//if(VideoInfo[3].codec == '2')
			//	image_ch = 3;
			//
			//var input = {'width': VideoInfo[image_ch].resolution.split('x')[0],
			//	'height': VideoInfo[image_ch].resolution.split('x')[1]};
			//var height = 288;
			//var width;
			//try {
			//	// video raito
			//	width  = height  * input.width/ input.height;
			//	//console.log("[PREVIEW]" + height + '/' + width);
			//	//console.log(input.width * height - input.height * width);
			//	MJ.fi = false ;
			//	MJ.dw = width;
			//	MJ.dh = height;
			//	$("#vlc_box").append("<canvas id='jpeg' width='" + width + "' height='"+ height + "'></canvas>");
			//	$("[class=warning]").css("display","none");
			//	$("#jpeg").css("display","block").css("margin", "auto");
			//	if( encodeVersion == 1 && VLCManager.user.auth != 1) {
			//		VLCManager.showEncriptedImage("jpeg", width, height);
			//	} else {
			//		MJ.streaming() ;					
			//	}
			//} catch(err) {
			//	VLCManager.target = null;
			//	return VLCManager.error();
			//}

			/*  =================== STICH ======================= */ 
			try {
				VLCManager.obj = null;
				var height = $("#" + VLCManager.target).height(),
					width = $("#" + VLCManager.target).width();
				MJ.fi = false ;
				MJ.dw = width;
				MJ.dh = height;
				$("#" + VLCManager.target).append("<canvas id='jpeg' width='" + width + "' height='"+ height + "'></canvas>");
				$("[class=warning]").css("display","none");
				$("#jpeg").css("display","block");
				MJ.streaming() ;					
			} catch(err) {
				VLCManager.target = null;
				return VLCManager.error();
			}
			
			
			return true;
		} else {
			var tmp = window.location.href.split('/');
			if( tmp.length > 3 ){ // index page is not include. it's only opreate the setup_main.html page.
				var count = 5;
				$("#vlc").remove();
				if( !isIE() && capInfo["oem"] != 19 && capInfo["oem"] != 20 && capInfo["oem"] != 21 ){
					$target = $("#" + target);
					var VLC;
					var width = $target.width();
					var height = $target.height();
					VLC = VLCManager.init(target, width, height, windowless);
					if( VLC ) {
						VLCManager.doGo();
						return true;
					} else {
						return VLCManager.error();
					}
					VLCManager.obj = document.getElementById("vlc");
				} else {
					$("#vlc").remove();
					$("#vlc_box").append("<iframe id='ie_vlc' name='ie_vlc' src='./preivew.cgi'></iframe>");
					$("#ie_vlc").on("load", function(){
						VLCManager.obj = document.frames['ie_vlc'].document.getElementById("vlc");
					});
				} 
				try{
					if( VLCManager.obj.VersionInfo == undefined || VLCManager.obj.VersionInfo == undefined) {
						return VLCManager.error();   
					}
					if(VLCManager.obj != null ) {
						VLCManager.doGo();	
					} else {
						return VLCManager.error();
					}
				} catch(err){
					return VLCManager.error();
				}
			}
			return true;
		}
	} , 'init': function(target, width, height, windowless){
		VLCManager.target = target;
		if(windowless == true){
			windowless = true;
		} else {
			windowless = false;
		}
		if( !isIE() && capInfo["oem"] != 19 && capInfo["oem"] != 20 && capInfo["oem"] != 21 ){
			$("#vlc").remove();
			VLCManager.vlc_init_obj = "<object";
			VLCManager.vlc_init_obj += " type='application/x-vlc-plugin'";
			VLCManager.vlc_init_obj += " pluginspage='http://www.videolan.org'";
			VLCManager.vlc_init_obj += " version='VideoLAN.VLCPlugin.2'";
			VLCManager.vlc_init_obj += " id='vlc' width='" + width + "px' height='" + height + "px'";
			VLCManager.vlc_init_obj += " align='center' vspace='0'";
			VLCManager.vlc_init_obj += " events='True' VIEWASTEXT>\
									<param name='MRL' value='' />\
									<param name='ShowDisplay' value='True' />\
									<param name='AutoLoop' value='False' />\
									<param name='AutoPlay' value='False' />\
									<param name='StartTime' value='0' />\
									<param name='branding' value='false' />\
									<param name='controls' value='false' />\
									<param name='mute' value='" + VLCManager.mute + "' />\
									<param name='windowless' value='"+ windowless+"' /></object>";
			$("#" + target).append(VLCManager.vlc_init_obj);
		} else {
			$("#vlc").remove();
			VLCManager.vlc_init_obj = "<object classid='clsid:9BE31822-FDAD-461B-AD51-BE1D1C159921' codebase='http://downloads.videolan.org/pub/videolan/vlc/last/win32/axvlc.cab#Version=0,8,6,0' ";
			VLCManager.vlc_init_obj += " id='vlc' events='True' >\
<param name='MRL' value='' />\
<param name='ShowDisplay' value='True' />\
<param name='AutoLoop' value='False' />\
<param name='AutoPlay' value='False' />\
<param name='toolbar' value='false' />\
<param name='Mute' value='false' /></object>";
			$("#" + target).append(VLCManager.vlc_init_obj);		
			$("#vlc").css("width","960px");
			$("#vlc").css("height","540px");
		}
		VLCManager.obj = document.getElementById('vlc');
		try{
			if( typeof(VLCManager.obj.VersionInfo) == 'undefined' || typeof(VLCManager.obj.VersionInfo) == 'undefined') {
				return VLCManager.error();   
			}
		} catch(err){
			return VLCManager.error();
		}
		return true;
	}
	, 'redirect' : function(){
		// 		example --------------> http://eyenix.dyndns.org:20000/login.htm
		//								http://192.168.0.191/login.htm
		var linkAd = location.href;
		var div = linkAd.split(":");
		var addChar= div[1].split("/");				// //192.168.0.191/login.htm e[2]=192.168.0.191	

		sslAdd = "rtsp://" + VLCManager.user['id'] + ":" + VLCManager.user['pass'] + "@" +addChar[2] + ":";
		if( capInfo["oem"] == 8){
			if( div[2] != undefined ){
				var port =  div[2].split("/");	            // for JSS OEM	// port[0] : browser		
				var Cport =  Number(port[0]) - 1000 ;		
				if( port[0] > 59000 && port[0] < 60000 && webPort == 80){	 // in case nadatel nvr
					sslAdd +=  Cport + "/channel" + VLCManager.selectedChannel;	
				}
				else{
					sslAdd +=  VLCManager.port + "/channel" + VLCManager.selectedChannel;			// rtsp://192.168.0.191	
				}		
			}else{
				sslAdd += VLCManager.port + "/channel" + VLCManager.selectedChannel;			// rtsp://192.168.0.191
			}
		}
		else{
			sslAdd += VLCManager.port + "/channel" + VLCManager.selectedChannel;			// rtsp://192.168.0.191
		}
		return sslAdd;
	}
	, 'vlcStateMonitor': function(chk) {
		var newState
		try {
			newState = VLCManager.obj.input.state;
		} catch(err) {
			clearInterval(VLCManager.monitorTimerId);
		}

		if( VLCManager.prevState != newState ) {
			switch(newState) {
				case 0: 
					break;
				case 1: 
					break;
				case 2: 
					break;
				case 3: 
					break;
				case 4: 
					break;
				case 5: 
				case 6:
				case 7:
					clearInterval(VLCManager.monitorTimerId);
					VLCManager.reConnect();
					break;
			}
			VLCManager.prevState = newState;
		} 
	}
	,'doGo' : function (){
		if( VLCManager.obj == null) return false;

		var version = VLCManager.obj.VersionInfo.split(" ")[0];
		if( (version == "2.2.3")  && (capInfo.audio_out == 1 )){
			return VLCManager.error("vlc_223_audio_error_msg");   
		}

		if ( VLCManager.checkRTSPConnectionNumber() < 0 )	return 0 ;
		var targetURL = VLCManager.redirect();
		if(targetURL !== undefined)
			VLCManager.URL = targetURL;
		VLCManager.obj.playlist.items.clear();
		VLCManager.Vid = VLCManager.obj.playlist.add(VLCManager.URL,"", ":rtsp-tcp :network-caching="+ VLCManager.buffering);
		VLCManager.obj.playlist.playItem(VLCManager.Vid);
		VLCManager.obj.playlist.play();
		VLCManager.monitorTimerId = setInterval("VLCManager.vlcStateMonitor()", 500);
		
		
	}
	,'reConnect' : function (){
		if( VLCManager.obj == null) return false;

		var State = VLCManager.obj.input.state;
		if(State > 5 || State == 0) {
			VLCManager.obj.playlist.items.clear();
			VLCManager.Vid = VLCManager.obj.playlist.add(VLCManager.URL,"", ":rtsp-tcp :network-caching="+ VLCManager.buffering);
			VLCManager.obj.playlist.playItem(VLCManager.Vid);
			VLCManager.obj.playlist.play();        
		} 
		if(VLCManager.obj.input.state == 3) {
			VLCManager.doGo();
		} else {
			setTimeout("VLCManager.reConnect()", 3000);  
		}
	}
	,'changeChannel': function(num) {
		if( VLCManager.obj == null) return false;

		VLCManager.selectedChannel = num;
		var tmp = VLCManager.URL.split("channel");
		VLCManager.obj.playlist.items.clear();
		VLCManager.doGo();
		return false;
	} , 'changeBuffer': function(num) {
		if( VLCManager.obj == null) return false;

		VLCManager.buffering = num;
		VLCManager.obj.playlist.stop();
		VLCManager.obj.video.marquee.text = "Changing latency";
		VLCManager.doGo();
		return true;
	} , "onClickFullScreen" : function (){

		if( VLCManager.obj == null) return false;
		VLCManager.obj.video.toggleFullscreen();
		return true;
	} , "toggleMute": function (deltaVol){
		if( VLCManager.obj == null) return false;
		VLCManager.obj.audio.toggleMute();
		return true;
	} , "updateVolume": function(volume){
		if( VLCManager.obj == null) return false;
		$("#volumeValue").html(Math.floor(volume));
		VLCManager.volume = Math.floor(volume) * 4;
		VLCManager.obj.audio.volume = VLCManager.volume ;
		return true;
	} , "checkRTSPConnectionNumber": function() {	
		   var flag = 0 ;
		   $.ajax({
		   type : 'get',
		   url  : '/cgi-bin/datetime.cgi?msubmenu=rtsp&action=session_info',
		   async : false,
		   success : function(response){
		// update new data
			   var tmp = response.split("\r\n");
			   var connection = tmp[tmp.length-3];
			   if ( connection > 9 ) 			{
					VLCManager.error("rtsp_warning");
					flag = -1 ;
			   }
		   }
		   });	
		   return flag ;
	}
}

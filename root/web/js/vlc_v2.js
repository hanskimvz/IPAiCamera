function VLC(id, capability, vin_conf, channel_list, windowless){
	// +-------------------------+
	// |     DEFINE VARIABLE     |
	// +-------------------------+
	this.target = 'vlc_play'; // object id for add vlc player
	this.preview_jpeg = true; // true : preview is jpeg image, false : preview is vlc 
	this.obj = [];
	this.selectedChannel = 1;
	this.prevState = [];
	this.monitorTimerId = [];
	this.URL = [];
	this.Vid = [];
	this.mute = true;
	this.volume = 10;
    if(capInfo.camera_type === "PREDATOR_CLIENT"){
	    this.buffering = 700;
	}
	else if(capInfo.camera_type === "seekware"){
		this.buffering = 1000;
	}
    else{
        this.buffering = 500;
    }
	this.user = new Object();
	this.port = null;
	this.lengthoffset = null;
	this.start = null;
	this.State_index = null;
	this.width = 0;
	this.height = 0;
	this.windowless = false;

	this.vin_source = 0;
	this.$channel_list = '';
	this.video_count = 1;  // capability 
	this.capability = null;
	this.vin_config = null;
	this.sub_stream = 1;// 0 : mainStream;
	this.multi_view = false;
	this.view_channel = 1; // 1,2,4(1 view, 4view, 16 view);

	// +-----------------------------+ 
	// |     INITIALIZE VARIABLE     |
	// +-----------------------------+ 
	if( typeof(id) == 'undefined'  ) {
		console.log("id is null");
		return null;
	}
	else {
		this.target = $("#" + id);
		if( typeof(this.target) == 'undefined' ){
			console.log("target is null");
			return null;
		}
		this.width = this.target.width();
		this.height = this.target.height();
	}

	if( typeof(capability) != 'undefined' ) {
		if( typeof(capability.video_in) != 'undefined' ){
			this.video_count = capability.video_in;
		}
		this.capability = capability;
	}
	else {
		return null;
	}

	if( typeof(vin_conf) != "undefined") {
		this.vin_config = vin_conf;
	}

	if( typeof(channel_list) != "undefined") {
		this.$channel_list = $("#" + channel_list);
	}

	if( typeof(windowless) != 'undefined' ){ this.windowless = windowless; }

	if( this.capability.video_in > 0 && this.capability.is_proxy_camera ){
		var tmp = "<p class='title'><span tkey='SELECT VIEWER'></span></p>";
		tmp += "<div class='align_center'>";
        if(capInfo.camera_type === "PREDATOR_CLIENT" || capInfo.camera_type === "PROXY_DUAL_CLIENT"){
		    tmp += "<input type='radio' id='multi-view' name='vins' value='";
            tmp += Number(this.video_count+1) + "' /><label for='multi-view' id='multi_vin'></label>";
        }
		for(var i=1; i <= this.video_count ; i++) {
			tmp += "<input type='radio' id='vin" + i + "' name='vins' value='" + i +"' />";
			tmp += "<label for='vin" + i + "'>" + i + "</label>";
		}
        if(capInfo.camera_type === "PROXY_CLIENT" ){
		    tmp += "<input type='radio' id='multi-view' name='vins' checked='checked' value='";
            tmp += Number(this.video_count+1) + "' /><label for='multi-view' id='multi_vin'></label>";
        }
		tmp += "</div>";

		$(".vlc_menu").before(tmp);
		this.multi_view = true;
		this.view_channel = capInfo.video_in;
        if(capInfo.camera_type === "PROXY_CLIENT"){
            $('#multi_vin').css("background-image","url(..//images/MultiView.png)");
        }else
			$('#multi_vin').css("background-image","url(..//images/DualView.png)");

		$("input[name=vins]").change({obj : this}, function(e){
			var vlc = e.data.obj;
			if( vlc.changeViewMode(e.target.value) ) {
				vlc.whetherActiveFullScreen("fullScreen");
				vlc.updateChannelSelect();
			}
			if( MJ.fi == false ){
				MJ.id = e.target.value-1; //0~3
			}
			vlc.selectedChannel = e.currentTarget.value;
		});
	}

	// +-------------------------+
	// |     DEFINE FUNCTION     |
	// +-------------------------+
	this.isIE = function() {
        var browserState = 'unknown';
		var agent = navigator.userAgent.toLowerCase();
		if(agent.indexOf("chrome")!=-1) browserState="chrome";
		else if(agent.indexOf("safari")!=-1) browserState="safari";
		else if(agent.indexOf("firefox")!=-1) browserState="firefox";
        else if(agent.indexOf("msie")!=-1 || agent.indexOf('trident')!=-1) browserState="IE";
        if(browserState == "IE")
            return true;
        else
            return false;

        //return (browserState == "IE");
		//return ((navigator.appName == 'Microsoft Internet Explorer')
		//		|| ((navigator.appName == 'Netscape')
		//			&& (new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})").exec(navigator.userAgent) != null)));
	};
	this.showEncriptedImage = function(id, width, height){
		var canvas = document.getElementById(id);
		var ctx = canvas.getContext('2d');
		var img = new Image(width, height);
		img.onload = function(){
			ctx.drawImage(img,0, 0,width,height); // Or at whatever offset you like
		};
		img.src="/images/encrypted.jpg";
	}
	this.setPlayInfo = function(user, port) {
		if( typeof(user) != 'undefined' ) {
			this.user = user;
		}
		if( typeof(port) != 'undefined' ){
			this.port = port;	
		}
	}
	this.error = function(msg) {
		var message='';

		$("[name=vlcplayers]").remove();

		/*  =================== STICH ======================= */ 
		try {
			console.log("ERROR");
			this.obj = [];
			MJ.fi = false ;
			MJ.dw = this.width;
			MJ.dh = this.height;

			this.target.append("<canvas id='jpeg' width='" + this.width + "' height='"+ this.height + "'></canvas>");
			$("[class=warning]").css("display","none");
			$("#jpeg").css("display","block");
			//MJ.streaming() ;

			$("#jpeg, .jpeg_menu").css("display","block");
			$("#multi-view").prop("disabled", true);

			this.target.find("*").remove();
			if(userInfo.pwchange == 0){
				if(capInfo.oem == 12){
                	msg = "admin_password_set";
				}else{
                	msg = "admin_password_change";
				}
            }
            else if ( typeof(msg) == 'null' || typeof(msg) == 'undefined' ) {
				msg = "vlc_not_supported_warning";
			}
			message = '<div class="warning">' + getLanguage(msg) + "</div>";

			if( msg == "rtsp_warning") {              // this.error("rtsp_warning");
				$("#jpeg, .jpeg_menu, .vlc_menu ").css("display","none");
			} else {
				$("#jpeg, .vlc_menu").css("display","none");
			}

			this.target.append(message);				
		}
		catch(err) {
			console.log('ERROR:' +err);
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
		//	$("#jpeg,.jpeg_menu").css("display","block");
		//	$("#" + this.target).find("*").remove();
		//	if ( msg == null || msg == undefined ) {
		//			msg = "vlc_not_supported_warning";
		//	}
		//	message = '<div class="warning">'
		//	message += getLanguage(msg);
		//	message += "</div>";
		//	this.obj = null;

		//	if( msg == "rtsp_warning") {
		//		$("#jpeg,.jpeg_menu").css("display","none");
		//	} else {
		//		$("#jpeg,.vlc_menu").css("display","none");
		//	}

		//	$("#" + this.target).append(message);
		//------------------------------------------------------------
		return false;
	}
	this.initPreview = function(target, windowless) {
		// it's called the Camera menu of Admin settting page.
		if( typeof(target) == 'undefined' ){
			return false;
		}
		else {
			this.target = target;
		}
		if( typeof(windowless) == 'undefined' ){
			windowless = false;
		}
		if( this.preview_jpeg ) {
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
			//	if( encodeVersion == 1 && this.user.auth != 1) {
			//		this.showEncriptedImage("jpeg", width, height);
			//	} else {
			//		MJ.streaming() ;					
			//	}
			//} catch(err) {
			//	this.target = null;
			//	return this.error();
			//}
			/*  =================== STICH ======================= */ 

			try {
				this.obj = [];
                var veiw_count=1;
                var height = $("#" + this.target).height(),
					width = $("#" + this.target).width();
                if( this.target == "image_box"){
                    width = $("#" + this.target).width()/capInfo.video_in;
                    veiw_count= capInfo.video_in;
                }
				MJ.fi = false ;
				MJ.dw = width;
				MJ.dh = height;
                if( this.target == "image_box"){
                    for(var i=1; i<=veiw_count;i++){
                        MJ.id=i-1;
        				$("#" + this.target).append("<canvas id='jpeg"+MJ.id+"' width='" + width + "' height='"+ height + "'></canvas>");
                    }
                    MJ.id=0;
                }
                else {
    				$("#" + this.target).append("<canvas id='jpeg' width='" + width + "' height='"+ height + "'></canvas>");
                }
                
                $("[class=warning]").css("display","none");
			$("#jpeg").css("display","block");
    		   	MJ.streaming() ;					
			} 
			catch(err) {
				this.target = null;
				return this.error();
			}
			return true;
		}
		else {
			try{
				$("[name=vlcplayers]").remove();
				var tmp = window.location.href.split('/');
                if( tmp.lengthoffset > 3 ){ // index page is not include. it's only opreate the setup_main.html page.
                    if(this.isIE() && capInfo["oem"] == 2)
                    {
                        $target = $("#" + target);
						var VLC;
						var width = $target.width();
						var height = $target.height();
						VLC = this.init();
						if( VLC ) {
							this.doGo();
							return true;
						}
						else {
							return this.error();
						}
						this.obj[0] = document.getElementById("vlc");
                    }
					else if( !this.isIE() && ( capInfo["oem"] != 19 && capInfo["oem"] != 20 && capInfo["oem"] != 21 && capInfo["oem"] != 2)){
						$target = $("#" + target);
						var VLC;
						var width = $target.width();
						var height = $target.height();
						VLC = this.init();
						if( VLC ) {
							this.doGo();
							return true;
						}
						else {
							return this.error();
						}
						this.obj[0] = document.getElementById("vlc");
					}
					else {
						$("#vlc_box").append("<iframe id='ie_vlc' name='ie_vlc' src='./preivew.cgi'></iframe>");
						$("#ie_vlc").on("load", function(){
							this.obj[0] = document.frames['ie_vlc'].document.getElementById("vlc");
							if( typeof(this.obj[0].VersionInfo) == 'undefined' && typeof(this.obj[0].VersionInfo) == 'undefined') {
								console.log("can't find version Infomation");
								return this.error();   
							}
							if(this.obj[0] != null ) {
								this.doGo();	
							}
							else {
								console.log("obj[0] is null!\n");
								return this.error();
							}
						});
					} 
				}
				return true;
			} catch(err){
				console.log("init_preview :" +err);
				return this.error();
			}
		}
	}
	this.init = function() {
		try{
			this.obj = [];
			$("[name=vlcplayers]").remove();
			if( this.multi_view && this.video_count > 1 ) {
				var width, height;
				var t = Math.sqrt(this.video_count);
				if( capInfo.camera_type === "PREDATOR_CLIENT"  || capInfo.camera_type === "PROXY_DUAL_CLIENT") {
					width = this.width / this.view_channel;
					height = this.height;
				}
				else {
					width = this.width /t;
					height = this.height /t;
				}
				for(var i=0; i < this.video_count ; ++i ) {
					this.obj[i] = this.addVLCPlayer(width, height);
				}
			}
			else {
				this.obj[0] = this.addVLCPlayer(this.width, this.height);
			}

            if(userInfo.pwchange == 0){
                throw "Admin Password not changed!!!";
            }
			if( typeof(this.obj[0].VersionInfo) == 'undefined' || typeof(this.obj[0].VersionInfo) == 'undefined' || capInfo["oem"] == 19 || capInfo["oem"] == 20 || capInfo["oem"] == 21 || (capInfo["oem"] == 2 && !this.isIE())) {
				throw "VLC is not added!";
			}
			this.whetherActiveFullScreen("fullScreen");
			this.updateChannelSelect();
			return true;	
		}
		catch(err){
			console.log("init :" + err);
			return this.error();
		}
	}
	this.addVLCPlayer = function(width, height) {
		var tmp = '';
        var id = "vlc" + this.obj.length;
        if( this.isIE() && capInfo["oem"] == 2){
			tmp= "<object classid='clsid:9BE31822-FDAD-461B-AD51-BE1D1C159921' ";
			tmp += "codebase='http://downloads.videolan.org/pub/videolan/vlc/last/win32/axvlc.cab#Version=0,8,6,0' ";
			tmp += " id='" + id + "' events='True' name='vlcplayers'>";
            if(this.multi_view){
    			tmp += "<param name='allowfullscreen' value='false' />";
            }else{
    			tmp += "<param name='allowfullscreen' value='true' />";
            }
			tmp += "<param name='MRL' value='' />";
			tmp += "<param name='ShowDisplay' value='True' />";
			tmp += "<param name='AutoLoop' value='False' />";
			tmp += "<param name='AutoPlay' value='False' />";
			tmp += "<param name='toolbar' value='false' />";
			tmp += "<param name='Mute' value='false' /></object>";
			this.target.append(tmp);
			$("#"+ id ).css("width", width + "px").css("height",height + "px");
		}
	    else if( !this.isIE() && (capInfo["oem"] != 19 && capInfo["oem"] != 20 && capInfo["oem"] != 21 && capInfo["oem"] != 2) ){
			tmp = "<object";
			tmp += " type='application/x-vlc-plugin'";
			tmp += " pluginspage='http://www.videolan.org'";
			tmp += " version='VideoLAN.VLCPlugin.2'";
			tmp += " id='" + id+ "' width='" + width + "px' height='" + height + "px'";
			tmp += " align='center' vspace='0'";
			tmp += " events='True' name='vlcplayers' VIEWASTEXT>";
            if(this.multi_view){
                tmp += "<param name='allowfullscreen' value='false' />";
            }else{
                tmp += "<param name='allowfullscreen' value='true' />";
            }
			tmp += "<param name='MRL' value='' />";
			tmp += "<param name='ShowDisplay' value='True' />";
			tmp += "<param name='AutoLoop' value='False' />";
			tmp += "<param name='AutoPlay' value='False' />";
			tmp += "<param name='StartTime' value='0' />";
			tmp += "<param name='branding' value='false' />";
			tmp += "<param name='controls' value='false' />";
			tmp += "<param name='mute' value='" + this.mute + "' />";
			tmp += "<param name='windowless' value='"+ this.windowless + "' /></object>";
			this.target.append(tmp);
		}
		else {
			tmp= "<object classid='clsid:9BE31822-FDAD-461B-AD51-BE1D1C159921' ";
			tmp += "codebase='http://downloads.videolan.org/pub/videolan/vlc/last/win32/axvlc.cab#Version=0,8,6,0' ";
			tmp += " id='" + id + "' events='True' name='vlcplayers'>";
            if(this.multi_view){
    			tmp += "<param name='allowfullscreen' value='false' />";
            }else{
    			tmp += "<param name='allowfullscreen' value='true' />";
            }
			tmp += "<param name='MRL' value='' />";
			tmp += "<param name='ShowDisplay' value='True' />";
			tmp += "<param name='AutoLoop' value='False' />";
			tmp += "<param name='AutoPlay' value='False' />";
			tmp += "<param name='toolbar' value='false' />";
			tmp += "<param name='Mute' value='false' /></object>";
			this.target.append(tmp);
			$("#"+ id ).css("width", width + "px").css("height",height + "px");
		}
		return document.getElementById(id);
	}

	this.redirect =  function(){
		try {
			var linkAd = location.href;
			var div = linkAd.split(":");
			var addChar= div[1].split("/");

			this.URL = [];
			if( this.view_channel > 1 )
			{
				if( this.view_channel > this.video_count ) {
					console.log("view channel exceed capability.");
					this.view_channel = this.video_count;
				}

				for( var i=0 ; i < this.view_channel; i++) {
					var ch = Number(vin_conf[i].stream[this.sub_stream])+1;
					this.URL[i] = "rtsp://" + this.user['id'] + ":" + this.user['pass'] + "@";
					this.URL[i] += addChar[2] + ":" + this.port + "/channel" + ch;
				}
			}
			else {
				this.URL[0] = "rtsp://" + this.user['id'] + ":" + this.user['pass'] + "@";
				this.URL[0] += addChar[2] + ":" + this.port + "/channel" + this.selectedChannel;
			}
			return true;
		}
		catch (e) {
			console.log("ERROR: " + e );
			return false;
		}
	}
	this.vlcStateMonitor = function() {
		try {
			for( var i=0; i< this.obj.length ; i++ ) {
				var newState = this.obj[i].input.state;
				if( this.prevState[i] != newState ) {
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
							this.reConnect(i);
							break;
					}
				}
				this.prevState[i] = newState;
			}
		} catch(err) {
			console.log("vlcStateMonitor : " + err);
			clearInterval(this.monitorTimerId);
		}
	}
	this.doGo = function (){
		if( this.obj.length == 0 ){
			return false;
		}

		var version = this.obj[0].VersionInfo.split(" ")[0];
		if( (version == "2.2.3")  && (capInfo.audio_out == 1 )){
			return this.error("vlc_223_audio_error_msg");   
		}

		if ( this.checkRTSPConnectionNumber() < 0 )	return 0 ;

		if( !this.redirect() ) {
			console.log("fail to initialize URL.");
		}
		for( var i=0 ; i < this.obj.length ; ++i ){
			this.obj[i].playlist.items.clear();
			this.Vid[i] = this.obj[i].playlist.add(this.URL[i],"", ":rtsp-tcp :network-caching="+ this.buffering);
			this.obj[i].playlist.playItem(this.Vid[i]);
			this.obj[i].playlist.play();
			this.obj[i].audio.volume = (this.multi_view == true && i > 0) ? 0 : this.volume;
		}
		this.monitorTimerId = setInterval(
				(function(self) {
					return function() {
						self.vlcStateMonitor(); 
					}
				}
		)(this), 500);				
		return true;
	}
	this.reConnect = function(view){
		try {
			if( typeof(this.obj[view]) == "undefined") {
				throw i + "of object is undefined object.";
			}

			var State = this.obj[view].input.state;
			if(State >= 5 || State == 0) {
				this.obj[view].playlist.items.clear();
				this.Vid[view] = this.obj[view].playlist.add(this.URL[view],"", ":rtsp-tcp :network-caching="+ this.buffering);
				this.obj[view].playlist.playItem(this.Vid[view]);
				this.obj[view].playlist.play();        
			} 
			if(this.obj[view].input.state == 3) {
				this.doGo();
			}
		} 
		catch(e) {
			console.log("reconnect : " + e);
		}
	}
	this.changeViewMode = function(num){
		if( this.obj.length == 0 ) return false;
		if( this.video_count <= 1 ) return false;
		this.vin_source = num-1;

		var multi_view = num > this.video_count ?  true : false;
		if( this.vin_source < this.video_count ) {
			this.selectedChannel = vin_conf[this.vin_source].stream[0]+1;
		}
		if( multi_view != this.multi_view  )	{
			this.view_channel = multi_view ? capInfo.video_in : 1;
			this.multi_view = multi_view;
		}
			this.init();
		this.doGo();
		return true;
	}
	this.changeChannel = function(num) {
		if( this.obj.length == 0 ) return false;

		this.selectedChannel = num;
		this.obj[0].playlist.stop();
		this.obj[0].playlist.items.clear();
		this.doGo();
		return false;
	}
	this.changeBuffer = function(num) {
		if( this.obj.length == 0 ) return false;
		this.buffering = num;
		this.obj.forEach(function(e){
			e.playlist.stop();
			e.video.marquee.text = "Changing latency";
		});
		this.doGo();
		return true;
	}
	this.onClickFullScreen = function (){
		if( this.obj.length == 0 ) return false;
		this.obj[0].video.toggleFullscreen();
		return true;
	}
	this.toggleMute = function (){
		if( this.obj.length == 0 ) return false;
		this.obj[0].audio.toggleMute();
		return true;
	}
	this.updateVolume = function(volume){
		if( this.obj.length == 0 ) return false;

		this.volume = Math.floor(volume) * 4;

		// fixme
		for(var i=0; i < this.obj.length ; ++i ) {
			if( this.obj[i] == null) return false;
			this.obj[i].audio.volume = (this.multi_view == true && i > 0) ? 0 : this.volume;
		}
		return true;
	}
	this.checkRTSPConnectionNumber = function() {
		var flag = 0 ;
		var connection = 0;
		$.ajax({
			type : 'get',
			url  : '/cgi-bin/datetime.cgi?msubmenu=rtsp&action=session_info',
			async : false,
			success : function(response){
				// update new data
				var tmp = response.split("\r\n");
				connection = tmp[tmp.length-3];
				console.log("connection:"+connection);
			}
		});	
		var max_session_count = 9;
		if (this.capability.video_in > 1) // multi sensor
		{
		  max_session_count = 15;
		}
		if ( connection > max_session_count ) {          // 9
			this.error("rtsp_warning");
			flag = -1 ;
		}
		return flag ;
	}
	this.whetherActiveFullScreen = function(id) {
		$("#" + id ).prop("disabled", this.multi_view);
	}
	this.updateChannelSelect = function() {
		var dom = '',
			stream = [
				getLanguage("setup_main_stream"),
				getLanguage("setup_sub_stream"),
				getLanguage("setup_third_stream"),
				"undefined"],
			ch,
			i;
		this.$channel_list.find("option").remove();
		if( this.multi_view == false ) {
			// renew the list of channel in index page
			for( i=0; i < this.capability.channels ; i++) {
				ch = Number(this.vin_config[this.vin_source].stream[i])+1;
				dom += "<option value=" + ch + ">" + stream[i] + "</option>";
			}
			this.$channel_list.append(dom);
		}
		this.$channel_list.prop("disabled", this.multi_view);
	}
	this.exit = function() {
		this.obj.forEach(function(object){
			object.playlist.stop();
		});
	}
}

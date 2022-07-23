function VLC(id, capability, vin_conf, enc_conf, channel_list, windowless){
	// +-------------------------+
	// |     DEFINE VARIABLE     |
	// +-------------------------+
	this.id = id;
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
		if(capInfo['oem'] === 19 || capInfo['oem'] === 20 || capInfo['oem'] === 21){     
			this.buffering = 1000;
		}else{
			this.buffering = 500;
		}
	}
	this.user = new Object();
	this.port = null;
	this.webport = null;
	this.httpmode = 0;
	this.lengthoffset = null;
	this.start = null;
	this.State_index = null;
	this.width = 0;
	this.height = 0;
	this.windowless = false;

	if(capInfo.video_in > 1){
		this.vin_source = capInfo.video_in;
	}
	else{
		this.vin_source = 0;
	}
	this.$channel_list = '';
	this.video_count = 1;  // capability 
	this.capability = null;
	this.vin_config = null;
	this.encode_config = null;
	this.sub_stream = 1;// 0 : mainStream;
	this.multi_view = false;
	this.view_channel = 1; // 1,2,4(1 view, 4view, 16 view);
	this.jpeg_mode_beta = [];
	this.isSpectrum = ( navigator.userAgent.toLowerCase().indexOf("qtwebengine") != -1 ) ? true : false;
	this.singleviewMode = this.isSpectrum; // true : remove multiview button
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
	if( typeof(enc_conf) != "undefined") {
		this.encode_config = enc_conf;
	}
	if( typeof(channel_list) != "undefined") {
		this.$channel_list = $("#" + channel_list);
	}

	if( typeof(windowless) != 'undefined' ){ this.windowless = windowless; }

	if( this.capability.video_in > 0 && this.capability.is_proxy_camera ){
		var tmp = "<p class='title'><span tkey='SELECT VIEWER'></span></p>";
		tmp += "<div class='align_center'>";
		if(capInfo.camera_type === "PREDATOR_CLIENT" || capInfo.camera_type === "PROXY_DUAL_CLIENT"){
			if(!this.singleviewMode) {
				tmp += "<input type='radio' id='multi-view' name='vins' checked='checked' value='";
				tmp += Number(this.video_count+1) + "' /><label for='multi-view' id='multi_vin'></label>";
			}
		}
		for(var i=1; i <= this.video_count ; i++) {
			tmp += "<input type='radio' id='vin" + i + "' name='vins' value='" + i +"' />";
			tmp += "<label for='vin" + i + "'>" + i + "</label>";
		}
		if(capInfo.camera_type === "PROXY_CLIENT"){
			if(!this.singleviewMode) {
				tmp += "<input type='radio' id='multi-view' name='vins' checked='checked' value='";
				tmp += Number(this.video_count+1) + "' /><label for='multi-view' id='multi_vin'></label>";
			}
		}
		tmp += "</div>";

		$(".vlc_menu").before(tmp);
		if (this.singleviewMode) {
			this.multi_view = false;
			this.view_channel = 1;
		} else {
			this.multi_view = true;
			this.view_channel = capInfo.video_in;
			if(capInfo.camera_type === "PROXY_CLIENT"){
				$('#multi_vin').css("background-image","url(..//images/MultiView.png)");
			}else
				$('#multi_vin').css("background-image","url(..//images/DualView.png)");
		}
		if(capInfo["oem"] == 20 || capInfo["oem"] == 21 || this.isSpectrum){
			for (var i = 0; i < this.view_channel ; i++){
				this.jpeg_mode_beta[i] = true;
			}
		}
		else if( this.target.selector != "#image_box"){
			for (var i = 0; i < this.view_channel ; i++){
				if(this.encode_config[1+(i*4)]['codec'] == 1)
				{
					this.jpeg_mode_beta[i] = false;
				} 
				else if(this.encode_config[2+(i*4)]['codec'] == 2)
				{
					this.jpeg_mode_beta[i] = true;
				}
			}
		}else{
			for (var i = 0; i < this.view_channel ; i++){
				this.jpeg_mode_beta[i] = false;
			}
		}
		$("input[name=vins]").change({obj : this}, function(e){
			var vlc = e.data.obj;
			var m_view = false;

			if(!vlc.isIE()){
				var m_volume = vlc.obj[0].volume;
				var m_muted = vlc.obj[0].muted;
			}
			if(e.target.value> capInfo.video_in){
				m_view=true;
			}
			else{
				m_view=false;

			}
			if(	m_view ){
				for(var i=0 ; i < vlc.vin_config.length ;i++){
					vlc.vin_source = e.target.value;
					vlc.checkEncodeConfig();					
				}
			}else{
				for(var i=0 ; i < vlc.vin_config.length ;i++){
					vlc.vin_source = i;
					vlc.checkEncodeConfig();					
				}
			}

			if( vlc.changeViewMode(e.target.value) ) {
				vlc.whetherActiveFullScreen("fullScreen");
				vlc.updateChannelSelect();
			}
			if(!vlc.isIE()){
				vlc.obj[0].muted = m_muted;
				vlc.obj[0].volume = m_volume;
			}
			if( MJ.fi == false ){
				if(e.target.value> capInfo.video_in){
					MJ.id = 0;
				}else{
					MJ.id = e.target.value-1; //0~3
				}
			}
		});
	}


	// +-------------------------+
	// |     DEFINE FUNCTION     |
	// +-------------------------+
	this.sel_channel = function(){
		if(!this.isIE())
		{
			if(this.vin_source < this.vin_config.length){
        var jpeg_view_mode = false;
  			for (var i = 0; i < this.capability.video_in ; i++){
  				if(this.jpeg_mode_beta[i])
  				{
  				  jpeg_view_mode = true;
  				}
  			}   

				if(capInfo["oem"] == 20 || capInfo["oem"] == 21 || this.isSpectrum || jpeg_view_mode){
					this.selectedChannel = 3+(this.vin_source*4);
					this.jpeg_mode_beta[this.vin_source] = true;
					if(this.capability.audio_in)
					{
						if(document.getElementById('sound_box'))
						{
							$("#sound_box").find("*").prop("disabled", true);
						}
					}
				}
				else if(this.encode_config[0+(this.vin_source*4)]['codec'] == 1)
				{
					this.selectedChannel = 1+(this.vin_source*4);
					this.jpeg_mode_beta[this.vin_source] = false;
				}
				else if(this.encode_config[1+(this.vin_source*4)]['codec'] == 1)
				{
					this.selectedChannel = 2+(this.vin_source*4);
					this.jpeg_mode_beta[this.vin_source] = false;
				} 
				else if(this.encode_config[2+(this.vin_source*4)]['codec'] == 2)
				{
					this.selectedChannel = 3+(this.vin_source*4);
					this.jpeg_mode_beta[this.vin_source] = true;
					if(this.capability.audio_in)
					{
						if(document.getElementById('sound_box'))
						{
							$("#sound_box").find("*").prop("disabled", true);
						}
					}
				}
			}
			else {			
				for (var i = 0; i < this.view_channel ; i++){
					if(this.encode_config[1+(i*4)]['codec'] == 1)
					{
						this.selectedChannel = 2+(i*4);
						this.jpeg_mode_beta[i] = false;
					} 
					else if(this.encode_config[2+(i*4)]['codec'] == 2)
					{
						this.selectedChannel = 3+(i*4);
						this.jpeg_mode_beta[i] = true;
						if(this.capability.audio_in)
						{
							if(document.getElementById('sound_box'))
							{
								$("#sound_box").find("*").prop("disabled", true);
							}
						}
					}
				}
			}

			if(document.getElementById('buffer_setup'))
			{
				$("#buffer_setup").find("*").prop("disabled", true);
			}
		}			
	}
	this.isIE = function() {
		return (((navigator.appName == 'Microsoft Internet Explorer') && (capInfo["oem"] != 19 && capInfo["oem"] != 20 && capInfo["oem"] != 21))
			|| ((navigator.appName == 'Netscape')
				&& (new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})").exec(navigator.userAgent) != null)));
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
	this.setPlayInfo = function(user, port, webport,httpmode) {
		if( typeof(user) != 'undefined' ) {
			this.user = user;
		}
		if( typeof(port) != 'undefined' ){
			this.port = port;	
		}
		if( typeof(webport) != 'undefined' ){
			this.webport = webport;	
		}		
		if( typeof(httpmode) != 'undefined' ){
			this.httpmode = httpmode;	
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

			document.getElementById("vlc_play").style.removeProperty("background-color")

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
						$("#video"+MJ.id).css("display","none");
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
					if( !this.isIE() ){
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
							if(this.isIE()){
								if( typeof(this.obj[0].VersionInfo) == 'undefined' && typeof(this.obj[0].VersionInfo) == 'undefined') {
									console.log("can't find version Infomation");
									return this.error();   
								}
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

				if( this.id == "image_box"){
					width = this.width / 4;
					height = this.height;
				}
				else if( capInfo.camera_type === "PREDATOR_CLIENT"  || capInfo.camera_type === "PROXY_DUAL_CLIENT") {
					width = this.width / this.view_channel;
					height = this.height;
				}
				else {
					width = this.width /t;
					height = this.height /t;
				}
				for(var i=0; i < this.video_count ; ++i ) {
					this.obj[i] = this.addVLCPlayer(width, height);
					if(document.querySelector('#jpeg') != null){
						$("#jpeg").remove();
					}
					if(capInfo.is_proxy_camera && $("input[name='vins']:checked").val() == (capInfo.video_in+1) && !this.isIE()){

						if( capInfo.camera_type === "PROXY_DUAL_CLIENT"){
							this.target.append("<canvas id='jpeg"+i+"' width='" + width + "px' height='"+ height/capInfo.video_in + "px' style='margin: auto'></canvas>");
						}else{
							this.target.append("<canvas id='jpeg"+i+"' width='" + width + "px' height='"+ height + "px' align='center' vspace='0'></canvas>");
						}
					}
				}
			}
			else {
				if(document.querySelector('#jpeg0') != null){
					this.target.append("<canvas id='jpeg' width='" + this.width + "px' height='"+ this.height + "px' style='display:none'></canvas>");
					for(var i=0; i < this.video_count ; ++i ) {
						$("#jpeg"+i).remove();
					}
				}
				this.obj[0] = this.addVLCPlayer(this.width, this.height);
			}

			if(userInfo.pwchange == 0){
				throw "Admin Password not changed!!!";
			}
			if(this.isIE()){    
				if( typeof(this.obj[0].VersionInfo) == 'undefined') {
					throw "VLC is not added!";
				}
			}

			if(( this.isSpectrum || capInfo["oem"] == 19 && this.isIE()) || capInfo["oem"] == 20 || capInfo["oem"] == 21)
			{
				this.selectedChannel = 3;
				this.jpeg_mode_beta[this.vin_source] = true;
				if(this.capability.audio_in)
				{
					if(document.getElementById('sound_box'))
					{
						$("#sound_box").find("*").prop("disabled", true);
					}
				}
				if(document.getElementById('buffer_setup'))
				{
					$("#buffer_setup").find("*").prop("disabled", true);
				}

				this.whetherActiveFullScreen("fullScreen");
				this.updateChannelSelect();
				return true;	
			}
			this.sel_channel();

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
		var id = "video" + this.obj.length;
		if(!this.isIE()){	
			tmp = "<video";	
			tmp += " id='" + id+ "' width='" + width + "px' height='" + height + "px'";		
			tmp += " align='center' vspace='0'";
			tmp += " autoplay muted name='vlcplayers'>";			  
			tmp += "</video>";

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
			tmp += "<param name='Mute' value='True' /></object>";

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
				if(!this.isIE()){	
					// check leo  
					if(!this.multi_view){
						var newState = this.Vid[i].isPlaying();
						if( this.prevState[i] != newState ) {
							if(this.prevState[i] != -1 && !newState)
							{
								this.reConnect(i);
							}
							this.prevState[i] = newState;
						}
					}
					else{
						for(var j = 0; j<this.vin_source;j++){
							var newState = this.Vid[j].isPlaying();
							if( this.prevState[j] != newState ) {
								if(this.prevState[j] != -1 && !newState)
								{
									this.selectedChannel = this.checkEncodeConfig();
									for( var z=0 ; z<this.vin_source;z++){
										if(this.jpeg_mode_beta[z]){
											this.doGo();
											break;
										}
									}
								}
								this.prevState[j] = newState;
							}

						}

					}
				}
				else
				{
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
			}
		} catch(err) {
			console.log("vlcStateMonitor : " + err);
			clearInterval(this.monitorTimerId);
		}
	}
	this.doGo = function (mode){
		if( this.obj.length == 0 ){
			return false;
		}

		var add_vin = 0;
		var multi_view_mode=0;
		if(this.isIE()){	 
			var version = this.obj[0].VersionInfo.split(" ")[0];
			if( (version == "2.2.3")  && (capInfo.audio_out == 1 )){
				return this.error("vlc_223_audio_error_msg");   
			}
		}

		if ( this.checkRTSPConnectionNumber(mode) < 0 )	return 0 ;

		if( !this.redirect() ) {
			console.log("fail to initialize URL.");
		}
		if ( this.obj.length == 1){
			add_vin= this.vin_source;
		}

		//ie가 아니고 multiview모드 일때 second channel이 하나라도 h.264가 아닐때를 구분
		if( this.multi_view && !this.isIE() ){
			for( var i=0 ; i < this.obj.length ; i++){
				if(this.jpeg_mode_beta[i])
				{
					multi_view_mode = 1;
					break;
				}
			}
		}
		// 위에서 하나라도 h.264가 아니면 Mjpeg stream으로 변경
		if(multi_view_mode == 1){
			this.checkSoundBox(0);
			for( var i=0 ; i < this.obj.length ; ++i ){
				var vid = "#video" + i;
				$(vid).css("display","none");	
				$("#jpeg"+i).css("display","inline");
			}
			MJ.fi = false ;
			MJ.dw = this.width / this.vin_config.length*2 ;
			MJ.dh = this.height / this.vin_config.length*2;          
			MJ.streaming();	  		    

		}
		else{
			for( var i=0 ; i < this.obj.length ; ++i ){
				if(!this.isIE()){	
					// check leo 
					if(this.Vid[i])
					{
						this.Vid[i].destroy();
					}
					if(!this.jpeg_mode_beta[i+add_vin])
					{
						this.checkSoundBox(1);
						var vid = "#video" + i;
						$(vid).css("display","inline");	
						$("#jpeg").css("display","none");

						MJ.fi = true ;			      
						this.prevState[i] = -1;
						this.obj[i].src = this.URL[i];
						this.obj[i].type="application/x-rtsp";
						this.obj[i].muted = true;

						if (window.Streamedian) {  		    
							var id = "video" + i;
							var linkAd = location.href;
							var div = linkAd.split(":");
							var addChar= div[1].split("/");  		
							if(this.httpmode == 0)
							{  
								this.Vid[i] = Streamedian.player(id, {socket: "ws://" + addChar[2] + ":" + this.webport + "/profile.ws"});  
							} 
							else
							{
								this.Vid[i] = Streamedian.player(id, {socket: "wss://" + addChar[2] + ":" + this.webport + "/profile.ws"});  
							}		  
						}
						$("#jpeg"+i).css("display","none");
					}
					else
					{
						this.checkSoundBox(0);
						var vid = "#video" + i;
						$(vid).css("display","none");	
						MJ.fi = false ;
						if(this.obj.length > 1){
							$("#jpeg"+i).css("display","inline");
							MJ.dw = this.width / this.vin_config.length*2 ;
							MJ.dh = this.height / this.vin_config.length*2;          
						}
						else{
							$("#jpeg").css("display","inline");
							if (corridor_mode) {
								var res_width = VideoInfo[2].resolution.split('x')[0];
								var res_height = VideoInfo[2].resolution.split('x')[1];
								//$("#jpeg").css("background-color", "#000000");
								MJ.dh = 540;
								MJ.dw = MJ.dh * res_height / res_width;
								MJ.dx = (960 / 2) - (MJ.dw / 2);
							}
							else {
								if (capInfo.camera_type === "seekware") {
									var res_width = VideoInfo[2].resolution.split('x')[0];
									var res_height = VideoInfo[2].resolution.split('x')[1];
									MJ.dh = 540;
									MJ.dw = MJ.dh / res_height * res_width;
									MJ.dx = (960-MJ.dw) / 2;
								}
								else{
									MJ.dw = this.width;
									MJ.dh = this.height;          
								}
							}       
						}
						MJ.streaming();	  		    
					}
				}
				else
				{
					this.prevState[i] = -1;
					this.obj[i].playlist.items.clear();
					this.Vid[i] = this.obj[i].playlist.add(this.URL[i],"", ":rtsp-tcp :network-caching="+ this.buffering);
					this.obj[i].playlist.playItem(this.Vid[i]);
					this.obj[i].playlist.play();
					this.obj[i].audio.volume = (this.multi_view == true && i > 0) ? 0 : this.volume;
				}
			}
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
				throw view + "of object is undefined object.";
			}
			if(!this.isIE()){
				// check leo
				if(this.Vid[view])
				{
					this.Vid[view].destroy();
				}

				var selchannel = this.checkEncodeConfig();
				if(this.selectedChannel != selchannel)
				{
					this.selectedChannel = selchannel;
					this.redirect();
					this.updateChannelSelect();
				}  			
				if(!this.jpeg_mode_beta[view])
				{
					this.checkSoundBox(1);
					var vid = "#video" + view;
					$(vid).css("display","inline");	
					$("#jpeg").css("display","none");  			  
					MJ.fi = true ;		
					this.obj[view].src = this.URL[view];
					this.obj[view].type="application/x-rtsp";
					// this.obj[view].muted = true;
					if (window.Streamedian) {
						var id = "video" + view;
						var linkAd = location.href;
						var div = linkAd.split(":");
						var addChar= div[1].split("/");  		 
						if(this.httpmode == 0)
						{
							this.Vid[view] = Streamedian.player(id, {socket: "ws://" + addChar[2] + ":" + this.webport + "/profile.ws"});
						}
						else
						{
							this.Vid[view] = Streamedian.player(id, {socket: "wss://" + addChar[2] + ":" + this.webport + "/profile.ws"});
						}
					}
				}
				else
				{
					this.checkSoundBox(0);
					var vid = "#video" + view;
					$(vid).css("display","none");	
					$("#jpeg").css("display","block");  		    

                    if (corridor_mode) {
                        var res_width = VideoInfo[2].resolution.split('x')[0];
                        var res_height = VideoInfo[2].resolution.split('x')[1];
                        //$("#jpeg").css("background-color", "#000000");
                        MJ.fi = false;
                        MJ.dh = 540;
                        MJ.dw = MJ.dh * res_height / res_width;
                        MJ.dx = (960 / 2) - (MJ.dw / 2);
                    }
                    else {
                        MJ.fi = false;
                        MJ.dw = this.width;
                        MJ.dh = this.height;
                    }

					MJ.streaming();	  	  		    
				}
			}
			else
			{
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
		} 
		catch(e) {
			console.log("reconnect : " + e);
		}
	}
	this.checkSoundBox = function(mode) {
		if(this.capability.audio_in)
		{
			if (mode)
			{
				if(document.getElementById('sound_box'))
				{
					$("#sound_box").find("*").prop("disabled",true );
					$(".slice2").find("*").prop("disabled",false );
				}
				if(document.getElementById('cb_speaker').checked)
				{
					$("#cb_speaker").prop("checked", true);
				}
				else {
					$("#cb_speaker").prop("checked", false);

				}
				if(document.getElementById('cb_mute')){
					$("#cb_mute").find("*").prop("disabled", false);
				}
			}
			else
			{

				if(this.capability.audio_in)
				{
					if(document.getElementById('sound_box'))
					{
						$("#sound_box").find("*").prop("disabled", true);
					}
					if(document.getElementById('cb_speaker'))
					{
						$("#cb_speaker").prop("checked", false);
					}
				}   		    
			}
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
		this.doGo(1);
		return true;
	}
	this.doStop = function (){
		if( this.obj.length == 0 ) return false;
		for( var i=0 ; i < this.obj.length ; ++i ){
			if(!this.isIE())
			{
				// check leo
				if(this.Vid[i])
				{
					this.Vid[i].destroy();
				}
			}
			else
			{
				this.obj[i].playlist.stop();
				this.obj[i].playlist.items.clear();
			}
		}
		return true;
	}	
	this.changeChannel = function(num) {
		if( this.obj.length == 0 ) return false;

		if(!this.isIE()){
			// check leo
			//this.Vid[0].stop();
			//this.Vid[0].destroy();	
			//this.Vid[0] = null;	  
		}
		else
		{
			this.selectedChannel = num;
			this.obj[0].playlist.stop();
			this.obj[0].playlist.items.clear();
			this.doGo();		  
		}
		return false;
	}
	this.changeBuffer = function(num) {
		if( this.obj.length == 0 ) return false;
		this.buffering = num;
		var vlc = this;
		this.obj.forEach(function(e){
			if(!vlc.isIE()){
				// check leo  
			}
			else
			{
				e.playlist.stop();
				e.video.marquee.text = "Changing latency";
			}
		});
		this.doGo();
		return true;
	}
	this.onClickFullScreen = function (){
		if( this.obj.length == 0 ) return false;
		if(!this.isIE()){		  
			var videoContainer = document.getElementById(this.id);    	
			if (videoContainer.requestFullscreen) {
				videoContainer.requestFullscreen();
			} else if (videoContainer.mozRequestFullScreen) {
				videoContainer.mozRequestFullScreen();
			} else if (videoContainer.webkitRequestFullscreen) {
				videoContainer.webkitRequestFullscreen();
			} else if(videoContainer.msRequestFullscreen){
				videoContainer.msRequestFullscreen();
			}

			//if (this.obj[0].mozRequestFullScreen) {
			//  this.obj[0].mozRequestFullScreen();
			//} else if (this.obj[0].webkitRequestFullScreen) {
			//  this.obj[0].webkitRequestFullScreen();
			//}  		
		}
		else
		{
			this.obj[0].video.toggleFullscreen();
		}
		return true;
	}
	this.toggleMute = function (){
		if( this.obj.length == 0 ) return false;
		if(!this.isIE()){
			if(this.obj[0].muted)
				this.obj[0].muted = false;
			else
				this.obj[0].muted = true;		

		}
		else
		{
			if(this.obj[0].audio.mute){
				this.obj[0].audio.mute = false;
			}
			else{
				this.obj[0].audio.mute = true;		
			}
		}
		return true;
	}
	this.updateVolume = function(volume){
		if( this.obj.length == 0 ) return false;
		if(!this.isIE()){
			this.volume = Math.floor(volume) /100.0;
		}
		else
		{
			this.volume = Math.floor(volume) * 4;
		}
		// fixme
        for(var i=0; i < this.obj.length ; ++i ) 
        {
			if( this.obj[i] == null) return false;
			if(!this.isIE()){ 
				this.obj[i].volume = (this.multi_view == true && i > 0) ? 0 : this.volume;
			}
			else
			{
				this.obj[i].audio.volume = (this.multi_view == true && i > 0) ? 0 : this.volume;
			}
		}
		return true;
	}
	this.checkEncodeConfig = function() {
		var selChannel = this.selectedChannel;
		var encode_config = this.encode_config;
		var vin_source = this.vin_source;
		var view_channel = this.view_channel;
		var jpeg_mode_beta = this.jpeg_mode_beta;
		$.ajax({
			type:"GET",
			url:'/cgi-bin/datetime.cgi?msubmenu=rtsp&action=codec_info',
			async : false,
			dataType:'json',
			complete: function (response) {
				encode_config = response.responseJSON;

				if(vin_source<capInfo.video_in){

					if(encode_config[0+(vin_source*4)]['codec'] == 1)
					{
						selChannel = 1+(vin_source*4);
						jpeg_mode_beta[vin_source] = false;
					}
					else if(encode_config[1+(vin_source*4)]['codec'] == 1)
					{
						selChannel = 2+(vin_source*4);
						jpeg_mode_beta[vin_source] = false;
					} 
					else if(encode_config[2+(vin_source*4)]['codec'] == 2)
					{
						selChannel = 3+(vin_source*4);
						jpeg_mode_beta[vin_source] = true;
					}
				}
				else {			
					for (var i = 0; i < this.video_count; i++){
						if(encode_config[1+(i*4)]['codec'] == 1)
						{
							selChannel = 2+(i*4);
							jpeg_mode_beta[i] = false;
						} 
						else if(encode_config[2+(i*4)]['codec'] == 2)
						{
							selChannel = 3+(i*4);
							jpeg_mode_beta[i] = true;
						}
					}
				}
			},
			error: function () {
			}
		});		
		this.encode_config = encode_config;
		this.jpeg_mode_beta = jpeg_mode_beta;
		return selChannel;
	}	
	this.checkRTSPConnectionNumber = function(add_num) {
		var flag = 0 ;
		var connection = 0;
		if( add_num ){
			add_num=1;
		}
		else{
			add_num=0;
		}
		$.ajax({
			type : 'get',
			url  : '/cgi-bin/datetime.cgi?msubmenu=rtsp&action=session_info',
			async : false,
			success : function(response){
				// update new data
				var tmp = response.split("\r\n");
				connection = tmp[tmp.length-2];
				console.log("connection:"+connection);
			}
		});	
		var max_session_count = 9;
		if (this.capability.video_in > 1) // multi sensor
		{
			max_session_count = 15+add_num;
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
		if(!this.isIE()){
			this.$channel_list.find("option").remove();
			ch = this.selectedChannel;
			if(!this.multi_view){
				if(capInfo.video_in > 1){
					dom += "<option value=" + ch + ">" + stream[(this.selectedChannel-1)%4] + "</option>";		
				}else{
					dom += "<option value=" + ch + ">" + stream[this.selectedChannel-1] + "</option>";		
				}
			}else{
				dom += "<option value=" + ch + ">Not Select</option>";		
			}
			this.$channel_list.append(dom);	  
			this.$channel_list.prop("disabled", true);
		}
		else
		{
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
	}
	this.exit = function() {
		this.obj.forEach(function(object){
			if(!this.isIE()){
				// check leo  
				for(var i=0; i < this.obj.length ; ++i ) {
					if( this.obj[i] == null) return false;
					if(this.Vid[i])
					{
						this.Vid[i].destroy();	  
					}
				}		    

			}
			else
			{
				object.playlist.stop();
			}
		});
	}
}


document.addEventListener("fullscreenchange", function(){
	var video = document.getElementById("video0");  
	var jpeg = document.getElementById("jpeg");
	var videoContainer = this.target;  
	if(!(document.fullScreen || document.fullscreenElement)){
		video.style.width = videoContainer.style.width;
		video.style.height = videoContainer.style.width;   
		jpeg.style.width = videoContainer.style.width;
		jpeg.style.height = videoContainer.style.width;           
	}
	else
	{
		video.style.width = "100%";
		video.style.height = "100%"; 
		jpeg.style.width = "100%";
		jpeg.style.height = "100%";              
	}
});
// Webkit
document.addEventListener("webkitfullscreenchange", function(){

	var video = document.getElementById("video0");  
	var jpeg = document.getElementById("jpeg");
	var videoContainer = this.target;    
	if(!document.webkitIsFullScreen){
		video.style.width = videoContainer.style.width;
		video.style.height = videoContainer.style.width;   
		jpeg.style.width = videoContainer.style.width;
		jpeg.style.height = videoContainer.style.width;         
	}
	else
	{
		video.style.width = "100%";
		video.style.height = "100%";  
		jpeg.style.width = "100%";
		jpeg.style.height = "100%";            
	}
});
// Firefox
document.addEventListener("mozfullscreenchange", function(){
	var video = document.getElementById("video0");  
	var jpeg = document.getElementById("jpeg");
	var videoContainer = this.target;  
	if(!document.mozIsFullScreen){
		video.style.width = videoContainer.style.width;
		video.style.height = videoContainer.style.width;   
		jpeg.style.width = videoContainer.style.width;
		jpeg.style.height = videoContainer.style.width;         
	}
	else
	{
		video.style.width = "100%";
		video.style.height = "100%";   
		jpeg.style.width = "100%";
		jpeg.style.height = "100%";            
	}
});
// Explorer
//document.addEventListener("MSFullscreenChange", function(){
//	  var video = document.getElementById("video0");  
//	  var videoContainer = this.target;//document.getElementById("vContainer0");    
//    if(!document.msFullscreenElement){
//        video.style.width = videoContainer.style.width;
//        video.style.height = videoContainer.style.width;   
//    }
//    else
//    {
//        video.style.width = "100%";
//        video.style.height = "100%";    
//   }
//});	
